"""
Flask Backend for Automation Dashboard

Serves the automation dashboard UI and provides JSON APIs for:
- Workflow management
- Execution history and monitoring
- Real-time statistics
- Workflow execution

Database: SQLite at .claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db
"""

import os
import sys
import json
import sqlite3
import threading
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

try:
    from flask import Flask, jsonify, request, render_template, send_from_directory
    from flask_cors import CORS
except ImportError:
    print("ERROR: Flask not installed. Installing...")
    os.system("pip install flask flask-cors")
    from flask import Flask, jsonify, request, render_template, send_from_directory
    from flask_cors import CORS

# Configuration
WOODWORKS_ROOT = Path(__file__).parent.parent.parent
DB_PATH = WOODWORKS_ROOT / "worktrees" / "agent-a30d54a8a75ba81d8" / "executor" / "executor.db"
SKILL_BRIDGE_ROOT = Path(__file__).parent

# Flask app initialization
app = Flask(
    __name__,
    template_folder=str(SKILL_BRIDGE_ROOT / "templates"),
    static_folder=str(SKILL_BRIDGE_ROOT / "static"),
)
CORS(app)

# Enable JSON pretty-printing
app.config['JSON_SORT_KEYS'] = False


class ExecutorDatabase:
    """Database interface for executor.db"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._verify_db_exists()

    def _verify_db_exists(self):
        """Verify database exists and is accessible"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def query(self, sql: str, params: Tuple = ()) -> List[Dict]:
        """Execute SELECT query and return results"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Query error: {e}\nSQL: {sql}")
            return []

    def execute(self, sql: str, params: Tuple = ()) -> bool:
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Execute error: {e}\nSQL: {sql}")
            return False

    def fetch_one(self, sql: str, params: Tuple = ()) -> Optional[Dict]:
        """Execute SELECT query and return first result"""
        results = self.query(sql, params)
        return results[0] if results else None

    def fetch_count(self, sql: str, params: Tuple = ()) -> int:
        """Execute COUNT query and return result"""
        result = self.fetch_one(sql, params)
        return result['count'] if result else 0


# Initialize database interface
db = ExecutorDatabase(DB_PATH)


# ============================================================================
# Helper Functions
# ============================================================================

def format_timestamp(ts: Optional[str]) -> Optional[str]:
    """Format timestamp to ISO format"""
    if not ts:
        return None
    try:
        # Try parsing ISO format
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.isoformat()
    except:
        return ts


def parse_json_field(value: Optional[str]) -> Any:
    """Safely parse JSON field"""
    if not value:
        return None
    try:
        return json.loads(value)
    except:
        return value


def calculate_duration(started_at: Optional[str], completed_at: Optional[str]) -> Optional[int]:
    """Calculate duration in milliseconds"""
    if not started_at or not completed_at:
        return None
    try:
        start = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
        end = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        return int((end - start).total_seconds() * 1000)
    except:
        return None


def get_execution_stats() -> Dict[str, Any]:
    """Calculate execution statistics"""
    stats = {
        'total_workflows': 0,
        'active_workflows': 0,
        'total_executions': 0,
        'successful_executions': 0,
        'failed_executions': 0,
        'pending_executions': 0,
        'average_duration_ms': 0,
        'success_rate': 0.0,
    }

    # Total and active workflows
    stats['total_workflows'] = db.fetch_count("SELECT COUNT(*) as count FROM workflows")
    stats['active_workflows'] = db.fetch_count("SELECT COUNT(*) as count FROM workflows WHERE is_active = 1")

    # Execution counts
    stats['total_executions'] = db.fetch_count("SELECT COUNT(*) as count FROM executions")
    stats['successful_executions'] = db.fetch_count("SELECT COUNT(*) as count FROM executions WHERE status = 'completed'")
    stats['failed_executions'] = db.fetch_count("SELECT COUNT(*) as count FROM executions WHERE status = 'failed'")
    stats['pending_executions'] = db.fetch_count("SELECT COUNT(*) as count FROM executions WHERE status = 'pending'")

    # Success rate
    total = stats['total_executions']
    if total > 0:
        stats['success_rate'] = (stats['successful_executions'] / total) * 100
        # Average duration
        result = db.fetch_one("""
            SELECT AVG(CAST((julianday(completed_at) - julianday(started_at)) * 86400000 AS INTEGER)) as avg_duration
            FROM executions
            WHERE status = 'completed' AND started_at IS NOT NULL AND completed_at IS NOT NULL
        """)
        if result and result.get('avg_duration'):
            stats['average_duration_ms'] = int(result['avg_duration'])

    return stats


# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/')
def index():
    """Serve dashboard HTML"""
    try:
        return render_template('dashboard.html')
    except FileNotFoundError:
        # Fallback if template not found
        return send_dashboard_fallback()


def send_dashboard_fallback():
    """Fallback dashboard HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Automation Dashboard</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #333; margin-top: 0; }
            .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #f9f9f9; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; }
            .stat-label { color: #666; font-size: 14px; }
            .stat-value { font-size: 32px; font-weight: bold; color: #333; }
            .section { margin-bottom: 30px; }
            .section h2 { border-bottom: 1px solid #eee; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f5f5f5; font-weight: 600; }
            .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; }
            .status-completed { background: #d4edda; color: #155724; }
            .status-pending { background: #fff3cd; color: #856404; }
            .status-failed { background: #f8d7da; color: #721c24; }
            .error-message { color: #721c24; background: #f8d7da; padding: 10px; border-radius: 4px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Automation Dashboard</h1>

            <div class="stats" id="stats"></div>

            <div class="section">
                <h2>Workflows</h2>
                <div id="workflows-error" style="display:none;" class="error-message"></div>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Name</th><th>Status</th><th>Created</th></tr>
                    </thead>
                    <tbody id="workflows-list"></tbody>
                </table>
            </div>

            <div class="section">
                <h2>Recent Executions</h2>
                <div id="executions-error" style="display:none;" class="error-message"></div>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Workflow</th><th>Status</th><th>Started</th><th>Duration</th></tr>
                    </thead>
                    <tbody id="executions-list"></tbody>
                </table>
            </div>
        </div>

        <script>
            const BASE_URL = window.location.origin;

            async function loadStats() {
                try {
                    const res = await fetch(BASE_URL + '/api/stats');
                    const data = await res.json();
                    document.getElementById('stats').innerHTML = `
                        <div class="stat-card">
                            <div class="stat-label">Total Workflows</div>
                            <div class="stat-value">${data.total_workflows}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Active Workflows</div>
                            <div class="stat-value">${data.active_workflows}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Total Executions</div>
                            <div class="stat-value">${data.total_executions}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Success Rate</div>
                            <div class="stat-value">${data.success_rate.toFixed(1)}%</div>
                        </div>
                    `;
                } catch (e) {
                    console.error('Stats error:', e);
                }
            }

            async function loadWorkflows() {
                try {
                    const res = await fetch(BASE_URL + '/api/workflows');
                    const data = await res.json();
                    const tbody = document.getElementById('workflows-list');
                    tbody.innerHTML = data.workflows.slice(0, 10).map(w => `
                        <tr>
                            <td><small>${w.id.substring(0, 8)}</small></td>
                            <td>${w.name}</td>
                            <td><span class="status-badge ${w.is_active ? 'status-completed' : 'status-pending'}">${w.is_active ? 'Active' : 'Inactive'}</span></td>
                            <td><small>${new Date(w.created_at).toLocaleDateString()}</small></td>
                        </tr>
                    `).join('');
                } catch (e) {
                    document.getElementById('workflows-error').textContent = 'Error loading workflows: ' + e.message;
                    document.getElementById('workflows-error').style.display = 'block';
                }
            }

            async function loadExecutions() {
                try {
                    const res = await fetch(BASE_URL + '/api/executions?limit=10');
                    const data = await res.json();
                    const tbody = document.getElementById('executions-list');
                    tbody.innerHTML = data.executions.map(e => `
                        <tr>
                            <td><small>${e.id.substring(0, 8)}</small></td>
                            <td><small>${e.workflow_id.substring(0, 8)}</small></td>
                            <td><span class="status-badge status-${e.status}">${e.status}</span></td>
                            <td><small>${e.started_at ? new Date(e.started_at).toLocaleString() : '-'}</small></td>
                            <td><small>${e.duration_ms ? e.duration_ms + 'ms' : '-'}</small></td>
                        </tr>
                    `).join('');
                } catch (e) {
                    document.getElementById('executions-error').textContent = 'Error loading executions: ' + e.message;
                    document.getElementById('executions-error').style.display = 'block';
                }
            }

            function refresh() {
                loadStats();
                loadWorkflows();
                loadExecutions();
            }

            refresh();
            setInterval(refresh, 5000);
        </script>
    </body>
    </html>
    """
    return html, 200, {'Content-Type': 'text/html'}


@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """GET /api/workflows - List all workflows"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)

        workflows = db.query("""
            SELECT id, name, description, trigger_type, created_at, updated_at, is_active
            FROM workflows
            ORDER BY updated_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))

        total = db.fetch_count("SELECT COUNT(*) as count FROM workflows")

        return jsonify({
            'success': True,
            'workflows': workflows,
            'total': total,
            'limit': limit,
            'offset': offset,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/executions', methods=['GET'])
def get_executions():
    """GET /api/executions - List execution history"""
    try:
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        status_filter = request.args.get('status', default='', type=str)
        workflow_id = request.args.get('workflow_id', default='', type=str)

        query = "SELECT * FROM executions WHERE 1=1"
        params = []

        if status_filter:
            query += " AND status = ?"
            params.append(status_filter)

        if workflow_id:
            query += " AND workflow_id = ?"
            params.append(workflow_id)

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        executions = db.query(query, tuple(params))

        # Enrich with duration
        for ex in executions:
            if ex.get('started_at') and ex.get('completed_at'):
                ex['duration_ms'] = calculate_duration(ex['started_at'], ex['completed_at'])

        total_query = "SELECT COUNT(*) as count FROM executions WHERE 1=1"
        total_params = []

        if status_filter:
            total_query += " AND status = ?"
            total_params.append(status_filter)

        if workflow_id:
            total_query += " AND workflow_id = ?"
            total_params.append(workflow_id)

        total = db.fetch_count(total_query, tuple(total_params))

        return jsonify({
            'success': True,
            'executions': executions,
            'total': total,
            'limit': limit,
            'offset': offset,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/execution/<execution_id>', methods=['GET'])
def get_execution(execution_id: str):
    """GET /api/execution/{id} - Get execution details"""
    try:
        execution = db.fetch_one(
            "SELECT * FROM executions WHERE id = ?",
            (execution_id,)
        )

        if not execution:
            return jsonify({'success': False, 'error': 'Execution not found'}), 404

        # Add duration
        if execution.get('started_at') and execution.get('completed_at'):
            execution['duration_ms'] = calculate_duration(execution['started_at'], execution['completed_at'])

        # Get steps
        steps = db.query(
            "SELECT * FROM execution_steps WHERE execution_id = ? ORDER BY step_index",
            (execution_id,)
        )

        for step in steps:
            # Parse JSON fields
            if step.get('input_data'):
                step['input_data'] = parse_json_field(step['input_data'])
            if step.get('output_data'):
                step['output_data'] = parse_json_field(step['output_data'])

        # Get outputs
        outputs = db.query(
            "SELECT * FROM outputs WHERE execution_id = ?",
            (execution_id,)
        )

        return jsonify({
            'success': True,
            'execution': execution,
            'steps': steps,
            'outputs': outputs,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """GET /api/stats - Get dashboard statistics"""
    try:
        stats = get_execution_stats()
        return jsonify({
            'success': True,
            'stats': stats,
            **stats  # Also return at top level for convenience
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/execute', methods=['POST'])
def execute_workflow():
    """POST /api/execute - Execute a workflow"""
    try:
        data = request.get_json()
        workflow_id = data.get('workflow_id')
        trigger_data = data.get('trigger_data', {})

        if not workflow_id:
            return jsonify({'success': False, 'error': 'workflow_id is required'}), 400

        # Check workflow exists
        workflow = db.fetch_one(
            "SELECT * FROM workflows WHERE id = ?",
            (workflow_id,)
        )

        if not workflow:
            return jsonify({'success': False, 'error': 'Workflow not found'}), 404

        # Create execution record
        execution_id = str(uuid.uuid4())
        trigger_type = workflow.get('trigger_type', 'manual')

        success = db.execute("""
            INSERT INTO executions (id, workflow_id, trigger_type, trigger_data, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            execution_id,
            workflow_id,
            trigger_type,
            json.dumps(trigger_data) if trigger_data else None,
            'pending',
            datetime.utcnow().isoformat() + 'Z',
        ))

        if not success:
            return jsonify({'success': False, 'error': 'Failed to create execution'}), 500

        return jsonify({
            'success': True,
            'execution_id': execution_id,
            'message': 'Workflow execution started'
        }), 202
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """GET /api/health - Health check endpoint"""
    try:
        # Test database connection
        db.fetch_count("SELECT COUNT(*) as count FROM workflows")
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
        }), 503


@app.route('/api/workflow/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id: str):
    """GET /api/workflow/{id} - Get workflow details"""
    try:
        workflow = db.fetch_one(
            "SELECT * FROM workflows WHERE id = ?",
            (workflow_id,)
        )

        if not workflow:
            return jsonify({'success': False, 'error': 'Workflow not found'}), 404

        # Parse config
        if workflow.get('config'):
            workflow['config'] = parse_json_field(workflow['config'])

        # Get execution history
        executions = db.query("""
            SELECT id, status, created_at, started_at, completed_at
            FROM executions
            WHERE workflow_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        """, (workflow_id,))

        return jsonify({
            'success': True,
            'workflow': workflow,
            'recent_executions': executions,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/workflow/<workflow_id>/executions', methods=['GET'])
def get_workflow_executions(workflow_id: str):
    """GET /api/workflow/{id}/executions - Get workflow execution history"""
    try:
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)

        executions = db.query("""
            SELECT * FROM executions
            WHERE workflow_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (workflow_id, limit, offset))

        for ex in executions:
            if ex.get('started_at') and ex.get('completed_at'):
                ex['duration_ms'] = calculate_duration(ex['started_at'], ex['completed_at'])

        total = db.fetch_count(
            "SELECT COUNT(*) as count FROM executions WHERE workflow_id = ?",
            (workflow_id,)
        )

        return jsonify({
            'success': True,
            'executions': executions,
            'total': total,
            'limit': limit,
            'offset': offset,
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# Server Startup
# ============================================================================

if __name__ == '__main__':
    print(f"Starting Automation Dashboard")
    print(f"Database: {DB_PATH}")
    print(f"Database exists: {DB_PATH.exists()}")

    if not DB_PATH.exists():
        print(f"WARNING: Database file not found at {DB_PATH}")
        sys.exit(1)

    print(f"Starting Flask server on http://localhost:8080")
    print(f"Dashboard: http://localhost:8080/")
    print(f"API docs: http://localhost:8080/api/health")

    try:
        app.run(
            host='0.0.0.0',
            port=8080,
            debug=False,
            use_reloader=False,
            threaded=True,
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Server startup error: {e}")
        sys.exit(1)
