"""Skill Bridge API - REST API for invoking Claude Code skills."""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from functools import wraps

from skill_invoker import SkillInvoker
from bridge_database import SkillBridgeDatabase

# Try to import CORS for real-time updates
try:
    from flask_cors import CORS
    HAS_CORS = True
except ImportError:
    HAS_CORS = False

# Configure logging
log_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'skill_bridge.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Enable CORS if available
if HAS_CORS:
    CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize components
db = SkillBridgeDatabase()
invoker = SkillInvoker(db=db)

# API key for security (optional, set via environment)
API_KEY = os.getenv("SKILL_BRIDGE_API_KEY", "")


def require_api_key(f):
    """Decorator to require API key for endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not API_KEY:
            return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid API key"}), 401

        token = auth_header[7:]
        if token != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)

    return decorated_function


# Dashboard routes
@app.route('/', methods=['GET'])
def dashboard():
    """Serve the dashboard HTML."""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        return jsonify({"error": "Dashboard not available"}), 500


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)."""
    try:
        return send_from_directory('static', filename)
    except Exception as e:
        logger.error(f"Error serving static file {filename}: {e}")
        return jsonify({"error": "File not found"}), 404


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


# Available skills endpoint
@app.route('/available-skills', methods=['GET'])
@require_api_key
def get_available_skills():
    """List all available skills and their parameters."""
    try:
        skills_info = invoker.list_available_skills()
        return jsonify(skills_info), 200
    except Exception as e:
        logger.error(f"Error listing skills: {e}")
        return jsonify({"error": str(e)}), 500


# Skill details endpoint
@app.route('/skills/<skill_name>', methods=['GET'])
@require_api_key
def get_skill_details(skill_name):
    """Get detailed information about a specific skill."""
    try:
        details = invoker.get_skill_details(skill_name)
        if "error" in details:
            return jsonify(details), 404
        return jsonify(details), 200
    except Exception as e:
        logger.error(f"Error getting skill details: {e}")
        return jsonify({"error": str(e)}), 500


# Invoke skill synchronously
@app.route('/invoke/<skill_name>', methods=['POST'])
@require_api_key
def invoke_skill(skill_name):
    """Invoke a skill synchronously.

    Request body:
    {
        "action": "action_name",
        "params": {
            "param1": "value1",
            "param2": "value2"
        }
    }

    Response:
    {
        "status": "completed|failed|error",
        "output": {...},
        "raw_output": "...",
        "confidence": 0.8,
        "invocation_id": "uuid",
        "duration_ms": 1500,
        "error": "..."
    }
    """
    try:
        data = request.get_json() or {}

        action = data.get("action", "default")
        params = data.get("params", {})

        logger.info(f"Invoking skill: {skill_name}/{action} with params: {params}")

        result = invoker.invoke_sync(skill_name, action, params)

        status_code = 200 if result["status"] in ["completed", "success"] else (
            400 if result["status"] == "error" else 400
        )

        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error invoking skill {skill_name}: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500


# Invoke skill asynchronously
@app.route('/invoke/<skill_name>/async', methods=['POST'])
@require_api_key
def invoke_skill_async(skill_name):
    """Invoke a skill asynchronously.

    Returns immediately with invocation ID for polling.

    Request body:
    {
        "action": "action_name",
        "params": {
            "param1": "value1"
        }
    }

    Response:
    {
        "status": "queued",
        "invocation_id": "uuid",
        "message": "..."
    }
    """
    try:
        data = request.get_json() or {}

        action = data.get("action", "default")
        params = data.get("params", {})

        logger.info(f"Queuing async skill invocation: {skill_name}/{action}")

        result = invoker.invoke_async(skill_name, action, params)

        return jsonify(result), 202 if result["status"] == "queued" else 400

    except Exception as e:
        logger.error(f"Error queueing async skill {skill_name}: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500


# Get async invocation status
@app.route('/status/<invocation_id>', methods=['GET'])
@require_api_key
def get_status(invocation_id):
    """Get status of an async invocation.

    Response:
    {
        "invocation_id": "uuid",
        "status": "queued|running|completed|failed",
        "skill_name": "...",
        "action": "...",
        "created_at": "...",
        "started_at": "...",
        "completed_at": "...",
        "output": {...},
        "error": "..."
    }
    """
    try:
        result = invoker.get_invocation_status(invocation_id)

        if result["status"] == "not_found":
            return jsonify(result), 404

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error getting status for {invocation_id}: {e}")
        return jsonify({"error": str(e)}), 500


# Get invocation history
@app.route('/history', methods=['GET'])
@require_api_key
def get_history():
    """Get invocation history with optional filters.

    Query parameters:
    - skill: filter by skill name
    - status: filter by status
    - limit: number of records (default 100)
    """
    try:
        skill_name = request.args.get("skill")
        status = request.args.get("status")
        limit = int(request.args.get("limit", 100))

        invocations = db.list_invocations(
            skill_name=skill_name,
            status=status,
            limit=limit
        )

        # Parse JSON fields
        for inv in invocations:
            if inv["params"]:
                inv["params"] = json.loads(inv["params"])
            if inv["result"]:
                inv["result"] = json.loads(inv["result"])

        return jsonify({
            "total": len(invocations),
            "invocations": invocations
        }), 200

    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


@app.before_request
def log_request():
    """Log incoming requests."""
    logger.info(f"{request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log outgoing responses."""
    logger.info(f"Response: {response.status_code}")
    return response


def run_server(host="0.0.0.0", port=9000, debug=False):
    """Start the Skill Bridge API server."""
    logger.info(f"Starting Skill Bridge API on {host}:{port}")
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == "__main__":
    # Run with environment variables for configuration
    host = os.getenv("SKILL_BRIDGE_HOST", "0.0.0.0")
    port = int(os.getenv("SKILL_BRIDGE_PORT", 9000))
    debug = os.getenv("SKILL_BRIDGE_DEBUG", "false").lower() == "true"

    run_server(host=host, port=port, debug=debug)
