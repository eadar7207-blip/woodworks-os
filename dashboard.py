"""
Web Dashboard for Adar Realty Studio Automation System.

Visualizes workflows, execution history, and real-time progress.
Runs on http://localhost:8080
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Database path - default to executor.db in the same directory or parent
EXECUTOR_PATH = os.getenv('EXECUTOR_PATH', './.claude/worktrees/agent-a30d54a8a75ba81d8/executor')
DB_PATH = os.path.join(EXECUTOR_PATH, 'executor.db')

if not os.path.exists(DB_PATH):
    # Try alternate location
    alt_db_paths = [
        './.claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db',
        '../.claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db',
        '/Users/main10servicesgmail.com/Desktop/Woodworks-OS/.claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db'
    ]
    for path in alt_db_paths:
        if os.path.exists(path):
            DB_PATH = path
            break


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def dict_from_row(row):
    """Convert sqlite3.Row to dict."""
    if row is None:
        return None
    return dict(row)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_workflows():
    """Get all workflows from database."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, trigger_type, is_active, created_at, updated_at
        FROM workflows
        ORDER BY created_at DESC
    """)
    workflows = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    return workflows


def get_workflow_by_id(workflow_id):
    """Get a specific workflow."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, trigger_type, is_active, created_at, updated_at, config
        FROM workflows
        WHERE id = ?
    """, (workflow_id,))
    workflow = dict_from_row(cursor.fetchone())
    conn.close()

    if workflow and workflow.get('config'):
        try:
            workflow['config'] = json.loads(workflow['config'])
        except:
            pass

    return workflow


def get_executions(limit=100, offset=0, status=None, workflow_id=None):
    """Get execution history with optional filtering."""
    conn = get_db()
    cursor = conn.cursor()

    where_clauses = []
    params = []

    if status:
        where_clauses.append("status = ?")
        params.append(status)

    if workflow_id:
        where_clauses.append("workflow_id = ?")
        params.append(workflow_id)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

    cursor.execute(f"""
        SELECT id, workflow_id, status, started_at, completed_at, error_message, created_at
        FROM executions
        {where_sql}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])

    executions = [dict_from_row(row) for row in cursor.fetchall()]

    # Calculate durations and step counts
    for execution in executions:
        if execution['started_at'] and execution['completed_at']:
            start = datetime.fromisoformat(execution['started_at'])
            end = datetime.fromisoformat(execution['completed_at'])
            execution['duration_ms'] = int((end - start).total_seconds() * 1000)
            execution['duration_seconds'] = round((end - start).total_seconds(), 2)
        else:
            execution['duration_ms'] = 0
            execution['duration_seconds'] = 0

        # Get step count
        cursor.execute("SELECT COUNT(*) as count FROM execution_steps WHERE execution_id = ?", (execution['id'],))
        execution['step_count'] = dict_from_row(cursor.fetchone())['count']

        # Get workflow name
        cursor.execute("SELECT name FROM workflows WHERE id = ?", (execution['workflow_id'],))
        wf_row = cursor.fetchone()
        execution['workflow_name'] = dict_from_row(wf_row)['name'] if wf_row else 'Unknown'

    conn.close()
    return executions


def get_execution_detail(execution_id):
    """Get detailed execution info including all steps."""
    conn = get_db()
    cursor = conn.cursor()

    # Get execution
    cursor.execute("""
        SELECT id, workflow_id, status, started_at, completed_at, error_message, created_at, trigger_type, trigger_data
        FROM executions
        WHERE id = ?
    """, (execution_id,))
    execution = dict_from_row(cursor.fetchone())

    if not execution:
        conn.close()
        return None

    # Get workflow name
    cursor.execute("SELECT name FROM workflows WHERE id = ?", (execution['workflow_id'],))
    wf_row = cursor.fetchone()
    execution['workflow_name'] = dict_from_row(wf_row)['name'] if wf_row else 'Unknown'

    # Get steps
    cursor.execute("""
        SELECT id, step_index, step_name, action_type, status, input_data, output_data,
               error_message, started_at, completed_at, duration_ms, retry_count
        FROM execution_steps
        WHERE execution_id = ?
        ORDER BY step_index
    """, (execution_id,))

    steps = []
    for row in cursor.fetchall():
        step = dict_from_row(row)
        try:
            step['input_data'] = json.loads(step['input_data'] or '{}')
        except:
            step['input_data'] = {}
        try:
            step['output_data'] = json.loads(step['output_data'] or '{}')
        except:
            step['output_data'] = {}
        steps.append(step)

    execution['steps'] = steps

    # Calculate overall duration
    if execution['started_at'] and execution['completed_at']:
        start = datetime.fromisoformat(execution['started_at'])
        end = datetime.fromisoformat(execution['completed_at'])
        execution['duration_ms'] = int((end - start).total_seconds() * 1000)
        execution['duration_seconds'] = round((end - start).total_seconds(), 2)
    else:
        execution['duration_ms'] = 0
        execution['duration_seconds'] = 0

    conn.close()
    return execution


def get_execution_stats():
    """Get execution statistics."""
    conn = get_db()
    cursor = conn.cursor()

    # Total executions
    cursor.execute("SELECT COUNT(*) as count FROM executions")
    total = dict_from_row(cursor.fetchone())['count']

    # Success rate
    cursor.execute("SELECT COUNT(*) as count FROM executions WHERE status = 'completed'")
    completed = dict_from_row(cursor.fetchone())['count']

    cursor.execute("SELECT COUNT(*) as count FROM executions WHERE status = 'failed'")
    failed = dict_from_row(cursor.fetchone())['count']

    success_rate = (completed / total * 100) if total > 0 else 0

    # Executions by status
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM executions
        GROUP BY status
    """)
    by_status = {dict_from_row(row)['status']: dict_from_row(row)['count'] for row in cursor.fetchall()}

    # Today's executions
    today = datetime.utcnow().date()
    cursor.execute("""
        SELECT COUNT(*) as count FROM executions
        WHERE DATE(created_at) = ?
    """, (today,))
    today_count = dict_from_row(cursor.fetchone())['count']

    # This week
    week_ago = datetime.utcnow() - timedelta(days=7)
    cursor.execute("""
        SELECT COUNT(*) as count FROM executions
        WHERE created_at >= ?
    """, (week_ago,))
    week_count = dict_from_row(cursor.fetchone())['count']

    # Average execution time
    cursor.execute("""
        SELECT AVG((julianday(completed_at) - julianday(started_at)) * 86400 * 1000) as avg_duration
        FROM executions
        WHERE status IN ('completed', 'failed') AND completed_at IS NOT NULL
    """)
    result = dict_from_row(cursor.fetchone())
    avg_duration = result['avg_duration'] if result['avg_duration'] else 0

    # Most used workflows
    cursor.execute("""
        SELECT w.name, COUNT(e.id) as count
        FROM workflows w
        LEFT JOIN executions e ON w.id = e.workflow_id
        GROUP BY w.id
        ORDER BY count DESC
        LIMIT 5
    """)
    most_used = [dict_from_row(row) for row in cursor.fetchall()]

    conn.close()

    return {
        'total': total,
        'completed': completed,
        'failed': failed,
        'success_rate': round(success_rate, 1),
        'by_status': by_status,
        'today_count': today_count,
        'week_count': week_count,
        'avg_duration_ms': round(avg_duration, 0),
        'most_used_workflows': most_used,
        'running': by_status.get('running', 0),
        'pending': by_status.get('pending', 0),
    }


def get_failed_executions():
    """Get failed executions for error recovery."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.workflow_id, e.status, e.error_message, e.started_at, e.completed_at, w.name
        FROM executions e
        JOIN workflows w ON e.workflow_id = w.id
        WHERE e.status = 'failed'
        ORDER BY e.created_at DESC
        LIMIT 20
    """)

    executions = []
    for row in cursor.fetchall():
        exec_dict = dict_from_row(row)

        # Get failed step info
        cursor.execute("""
            SELECT step_name, error_message FROM execution_steps
            WHERE execution_id = ? AND status = 'failed'
            LIMIT 1
        """, (exec_dict['id'],))

        failed_step = dict_from_row(cursor.fetchone())
        if failed_step:
            exec_dict['failed_step'] = failed_step['step_name']
            exec_dict['error_detail'] = failed_step['error_message']

        executions.append(exec_dict)

    conn.close()
    return executions


# ============================================================================
# ROUTES - HTML PAGES
# ============================================================================

@app.route('/')
def index():
    """Main dashboard page."""
    workflows = get_workflows()
    stats = get_execution_stats()
    return render_template('index.html', workflows=workflows, stats=stats)


@app.route('/workflows')
def workflows_page():
    """Workflows list page."""
    workflows = get_workflows()
    return render_template('workflows.html', workflows=workflows)


@app.route('/executions')
def executions_page():
    """Execution history page."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', None)
    workflow_id = request.args.get('workflow_id', None)

    limit = 20
    offset = (page - 1) * limit

    executions = get_executions(limit=limit, offset=offset, status=status, workflow_id=workflow_id)

    # Total count for pagination
    conn = get_db()
    cursor = conn.cursor()
    where_clauses = []
    params = []
    if status:
        where_clauses.append("status = ?")
        params.append(status)
    if workflow_id:
        where_clauses.append("workflow_id = ?")
        params.append(workflow_id)

    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    cursor.execute(f"SELECT COUNT(*) as count FROM executions {where_sql}", params)
    total_count = dict_from_row(cursor.fetchone())['count']
    conn.close()

    total_pages = (total_count + limit - 1) // limit
    workflows = get_workflows()

    return render_template('executions.html',
                         executions=executions,
                         page=page,
                         total_pages=total_pages,
                         total_count=total_count,
                         current_status=status,
                         current_workflow_id=workflow_id,
                         workflows=workflows)


@app.route('/execution/<execution_id>')
def execution_detail(execution_id):
    """Execution details page."""
    execution = get_execution_detail(execution_id)
    if not execution:
        return "Execution not found", 404

    return render_template('execution_detail.html', execution=execution)


@app.route('/workflow/<workflow_id>/execute')
def execute_workflow_page(workflow_id):
    """Workflow execution page."""
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        return "Workflow not found", 404

    return render_template('execute_workflow.html', workflow=workflow)


@app.route('/errors')
def errors_page():
    """Error recovery page."""
    failed = get_failed_executions()
    return render_template('errors.html', failed_executions=failed)


# ============================================================================
# ROUTES - API ENDPOINTS
# ============================================================================

@app.route('/api/workflows', methods=['GET'])
def api_workflows():
    """Get all workflows."""
    workflows = get_workflows()
    return jsonify(workflows)


@app.route('/api/workflows/<workflow_id>', methods=['GET'])
def api_workflow(workflow_id):
    """Get a specific workflow."""
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        return jsonify({'error': 'Workflow not found'}), 404
    return jsonify(workflow)


@app.route('/api/executions', methods=['GET'])
def api_executions():
    """Get executions with optional filtering."""
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    status = request.args.get('status')
    workflow_id = request.args.get('workflow_id')

    executions = get_executions(limit=limit, offset=offset, status=status, workflow_id=workflow_id)
    return jsonify(executions)


@app.route('/api/executions/<execution_id>', methods=['GET'])
def api_execution(execution_id):
    """Get execution details."""
    execution = get_execution_detail(execution_id)
    if not execution:
        return jsonify({'error': 'Execution not found'}), 404
    return jsonify(execution)


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get dashboard statistics."""
    stats = get_execution_stats()
    return jsonify(stats)


@app.route('/api/executions/<execution_id>/monitor', methods=['GET'])
def api_monitor_execution(execution_id):
    """Get current execution status for real-time monitoring."""
    execution = get_execution_detail(execution_id)
    if not execution:
        return jsonify({'error': 'Execution not found'}), 404

    # Calculate progress
    total_steps = len(execution['steps'])
    completed_steps = sum(1 for s in execution['steps'] if s['status'] in ['completed', 'failed', 'skipped'])

    progress_percent = (completed_steps / total_steps * 100) if total_steps > 0 else 0

    return jsonify({
        'execution_id': execution['id'],
        'status': execution['status'],
        'progress_percent': round(progress_percent, 1),
        'total_steps': total_steps,
        'completed_steps': completed_steps,
        'current_step': execution['steps'][-1] if execution['steps'] else None,
        'duration_ms': execution['duration_ms'],
        'steps': execution['steps'],
    })


@app.route('/api/executions/<execution_id>/retry', methods=['POST'])
def api_retry_execution(execution_id):
    """Retry a failed execution (placeholder)."""
    execution = get_execution_detail(execution_id)
    if not execution:
        return jsonify({'error': 'Execution not found'}), 404

    if execution['status'] != 'failed':
        return jsonify({'error': 'Can only retry failed executions'}), 400

    # This would call the executor to retry
    return jsonify({
        'message': 'Retry would be triggered here',
        'execution_id': execution_id,
        'workflow_id': execution['workflow_id'],
    })


@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
def api_execute_workflow(workflow_id):
    """Execute a workflow and return execution ID."""
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        return jsonify({'error': 'Workflow not found'}), 404

    try:
        data = request.get_json() or {}
        trigger_data = data.get('trigger_data', {})

        # Create a new execution record
        conn = get_db()
        cursor = conn.cursor()

        execution_id = f"exec-{datetime.utcnow().isoformat()}-{workflow_id[:8]}"

        cursor.execute("""
            INSERT INTO executions (id, workflow_id, status, created_at, trigger_type, trigger_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (execution_id, workflow_id, 'pending', datetime.utcnow().isoformat(), 'manual', json.dumps(trigger_data)))

        conn.commit()
        conn.close()

        return jsonify({
            'execution_id': execution_id,
            'workflow_id': workflow_id,
            'status': 'pending'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({'status': 'healthy', 'db': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'db': 'disconnected', 'error': str(e)}), 500


@app.route('/api/executions/<execution_id>/export', methods=['GET'])
def api_export_execution(execution_id):
    """Export execution as JSON."""
    execution = get_execution_detail(execution_id)
    if not execution:
        return jsonify({'error': 'Execution not found'}), 404

    response = jsonify(execution)
    response.headers["Content-Disposition"] = f"attachment; filename=execution_{execution_id}.json"
    return response


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"Warning: Database not found at {DB_PATH}")
        print(f"Please ensure executor is running or set EXECUTOR_PATH environment variable")

    print(f"Dashboard running on http://localhost:8080")
    print(f"Using database: {DB_PATH}")
    app.run(host='0.0.0.0', port=8080, debug=True)
