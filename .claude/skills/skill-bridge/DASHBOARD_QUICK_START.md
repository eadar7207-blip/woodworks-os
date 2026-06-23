# Dashboard Quick Start Guide

## Launch the Dashboard

```bash
cd /Users/main10servicesgmail.com/Desktop/Woodworks-OS/.claude/skills/skill-bridge
./start_dashboard.sh
```

Then open: **http://localhost:8080**

## What You Get

### Real-Time Dashboard
- Live statistics (workflows, executions, success rate)
- Workflow list with status
- Execution history with filtering
- Detailed execution logs

### API Endpoints
- `GET /api/workflows` - List workflows
- `GET /api/executions` - List executions
- `GET /api/execution/{id}` - Get execution details
- `GET /api/stats` - Get statistics
- `POST /api/execute` - Run a workflow
- `GET /api/health` - Health check

## Quick API Examples

### Get all workflows
```bash
curl http://localhost:8080/api/workflows?limit=10
```

### Get execution statistics
```bash
curl http://localhost:8080/api/stats
```

### Get execution details
```bash
curl http://localhost:8080/api/execution/exec-id-here
```

### Execute a workflow
```bash
curl -X POST http://localhost:8080/api/execute \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "workflow-id-here", "trigger_data": {}}'
```

## Files

| File | Purpose |
|------|---------|
| `dashboard.py` | Flask backend with API |
| `templates/dashboard.html` | Web UI |
| `static/css/style.css` | Styling |
| `static/js/api.js` | API client |
| `static/js/dashboard.js` | UI logic |
| `start_dashboard.sh` | Startup script |
| `DASHBOARD.md` | Full documentation |

## Features

✓ View all workflows and their status
✓ See execution history and details
✓ Filter executions by status
✓ View step-by-step execution logs
✓ Execute workflows manually
✓ Auto-refresh every 5 seconds
✓ Responsive design
✓ JSON REST API
✓ Error handling
✓ Health monitoring

## Database

Connected to: `.claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db`

Tables:
- `workflows` - Workflow definitions
- `executions` - Execution records
- `execution_steps` - Step details
- `outputs` - Execution outputs

## Troubleshooting

### Port 8080 already in use?
```bash
# Find and kill the process
lsof -i :8080 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Flask not installed?
```bash
python3 -m pip install flask flask-cors
```

### Database connection error?
```bash
# Verify database exists
ls -la /Users/main10servicesgmail.com/Desktop/Woodworks-OS/.claude/worktrees/agent-a30d54a8a75ba81d8/executor/executor.db
```

## Development

### Test without running server
```bash
python3 -c "from dashboard import app; print(app)"
```

### Test specific endpoint
```python
from dashboard import app
with app.test_client() as client:
    res = client.get('/api/health')
    print(res.get_json())
```

### Access database directly
```python
from dashboard import db
workflows = db.query("SELECT * FROM workflows")
```

## Deployment

For production, use a WSGI server:

```bash
pip install gunicorn
gunicorn dashboard:app --bind 0.0.0.0:8080 --workers 4
```

## Next Steps

1. Start the dashboard: `./start_dashboard.sh`
2. Visit http://localhost:8080
3. Click on workflows to view details
4. Click "Run" to execute a workflow
5. Check the Executions tab for history
6. Use the API for programmatic access

For detailed documentation, see `DASHBOARD.md`
