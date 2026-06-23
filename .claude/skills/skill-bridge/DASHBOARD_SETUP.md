# Dashboard Setup Guide

Quick integration guide for adding the HTML/CSS dashboard to your Flask application.

## Quick Start (5 minutes)

### 1. Install Flask (if not already installed)

```bash
pip install flask
```

### 2. Create Flask Application

```python
# app.py
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')

# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/executions/<execution_id>')
def execution_detail(execution_id):
    """Execution detail page"""
    return render_template('execution.html')

# ============================================================================
# API ENDPOINTS (Integrate with your backend)
# ============================================================================

@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """List all workflows"""
    # TODO: Implement workflow fetching from your database
    return jsonify({
        'workflows': []  # Return list of workflow objects
    })

@app.route('/api/executions', methods=['GET'])
def get_executions():
    """List execution history"""
    limit = request.args.get('limit', 50, type=int)
    # TODO: Implement execution history fetching
    return jsonify({
        'executions': []  # Return list of execution objects
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    # TODO: Calculate from your data
    return jsonify({
        'total_workflows': 0,
        'active_executions': 0,
        'success_rate': 96,
        'failed_executions': 0
    })

@app.route('/api/recovery/status', methods=['GET'])
def get_recovery_status():
    """Get error recovery status"""
    # TODO: Fetch from error recovery system
    return jsonify({
        'items': []  # Return list of recovery items
    })

@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute a workflow"""
    # TODO: Trigger workflow execution
    return jsonify({
        'execution_id': 'exec-123',
        'status': 'started'
    })

@app.route('/api/executions/<execution_id>', methods=['GET'])
def get_execution(execution_id):
    """Get execution details"""
    # TODO: Fetch execution details
    return jsonify({
        'id': execution_id,
        'workflow_name': '',
        'status': 'running',
        'progress': 50,
        'steps': []
    })

@app.route('/api/executions/<execution_id>/logs', methods=['GET'])
def get_execution_logs(execution_id):
    """Get execution logs"""
    # TODO: Fetch logs
    return jsonify({
        'logs': []
    })

@app.route('/api/executions/<execution_id>/pause', methods=['POST'])
def pause_execution(execution_id):
    """Pause execution"""
    # TODO: Implement pause
    return jsonify({'status': 'paused'})

@app.route('/api/executions/<execution_id>/resume', methods=['POST'])
def resume_execution(execution_id):
    """Resume execution"""
    # TODO: Implement resume
    return jsonify({'status': 'running'})

@app.route('/api/executions/<execution_id>/cancel', methods=['POST'])
def cancel_execution(execution_id):
    """Cancel execution"""
    # TODO: Implement cancel
    return jsonify({'status': 'cancelled'})

@app.route('/api/executions/<execution_id>/retry', methods=['POST'])
def retry_execution(execution_id):
    """Retry failed execution"""
    # TODO: Implement retry
    return jsonify({'status': 'retrying'})

# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    # Development
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    # Production (use gunicorn instead)
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Run the Application

```bash
python app.py
```

Visit: `http://localhost:5000`

## File Structure

```
skill-bridge/
├── app.py                    # Flask application (your code)
├── templates/
│   ├── index.html           # Main dashboard
│   └── execution.html       # Execution details
├── static/
│   ├── style.css            # All styling
│   ├── dashboard.js         # Dashboard logic
│   └── execution-detail.js  # Execution detail logic
└── DASHBOARD_README.md      # Documentation
```

## Data Models

### Workflow Object

```python
{
    'id': 'workflow-123',
    'name': 'Lead Follow-up Sequence',
    'description': 'Automated follow-up emails for leads',
    'status': 'active',  # active | scheduled | paused
    'execution_count': 42,
    'success_rate': 96,
    'last_executed_at': '2026-06-08T10:30:00Z',
    'avg_duration': 120,  # seconds
}
```

### Execution Object

```python
{
    'id': 'exec-456',
    'workflow_id': 'workflow-123',
    'workflow_name': 'Lead Follow-up Sequence',
    'status': 'running',  # running | success | failed | cancelled | paused
    'progress': 50,  # percentage (0-100)
    'started_at': '2026-06-08T10:30:00Z',
    'completed_at': None,
    'duration': 120,  # seconds
    'success_rate': 0.96,  # decimal (0-1)
    'steps_completed': 3,
    'total_steps': 5,
    'recovery_active': False,
    'steps': [
        {
            'name': 'Check Lead Status',
            'status': 'success',
            'started_at': '2026-06-08T10:30:00Z',
            'duration': 5,
            'output': 'Lead status: qualified',
            'error': None
        }
    ]
}
```

### Recovery Item Object

```python
{
    'workflow_name': 'Lead Follow-up',
    'execution_id': 'exec-456',
    'error_message': 'Email service timeout',
    'status': 'recovering',  # recovering | recovered | unrecoverable
    'strategies': [
        {
            'name': 'Exponential Backoff',
            'status': 'in_progress',
            'result': 'Retrying after 8 seconds'
        }
    ]
}
```

### Stats Object

```python
{
    'total_workflows': 12,
    'active_executions': 3,
    'success_rate': 96,  # percentage
    'failed_executions': 2
}
```

## Integration Checklist

- [ ] Flask app created
- [ ] Templates folder configured
- [ ] Static folder configured
- [ ] API endpoints stubbed
- [ ] Database queries implemented
- [ ] Data models matching dashboard expectations
- [ ] CORS enabled (if needed for cross-origin requests)
- [ ] Authentication/authorization added (if needed)
- [ ] Error handling implemented
- [ ] Tested all dashboard tabs
- [ ] Verified responsive on mobile
- [ ] Set up auto-refresh intervals
- [ ] Configured logging

## Common Issues

### "Templates not found" Error

Ensure Flask is initialized with correct paths:

```python
app = Flask(__name__, 
    template_folder='templates',  # Or your path
    static_folder='static')        # Or your path
```

### CSS/JS not loading

Check Network tab in browser DevTools. Ensure files are in the `static/` folder and paths in HTML are correct:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<script src="{{ url_for('static', filename='dashboard.js') }}"></script>
```

### API returns empty data

Implement the API endpoints to return data matching the expected models above.

### Auto-refresh too slow/fast

Edit the intervals in JavaScript:

```javascript
// dashboard.js
startAutoRefresh() {
    this.autoRefreshInterval = setInterval(() => {
        // ...
    }, 5000);  // Change from 5000ms to desired interval
}
```

## Production Deployment

### Using Gunicorn

```bash
# Install
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run with systemd service (see DEPLOYMENT.md)
```

### Environment Variables

```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export DATABASE_URL=postgresql://...
```

### Static Files

For production, serve CSS/JS with a CDN or reverse proxy:

```nginx
location /static/ {
    alias /path/to/skill-bridge/static/;
    expires 30d;
}
```

## Advanced Customization

### Custom Theming

Edit CSS variables in `style.css`:

```css
:root {
    --color-primary: #3b82f6;  /* Change to your brand color */
    --color-bg-primary: #0f172a;
    /* ... edit others as needed */
}
```

### Adding Columns to Execution Table

Edit `templates/index.html`:

```html
<th>New Column Header</th>
<!-- In tbody -->
<td>{{ execution.new_field }}</td>
```

Then update `dashboard.js` to populate the field.

### WebSocket Real-Time Updates

Replace polling with WebSocket:

```javascript
const socket = new WebSocket('ws://localhost:5000/api/stream');
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    this.execution = data;
    this.renderExecutionDetails();
};
```

## Testing

### Load Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/
```

### Browser Testing

- Open DevTools (F12)
- Check Console for errors
- Check Network tab for failed requests
- Use Mobile view (Ctrl+Shift+M)

## Support

- Check `DASHBOARD_README.md` for full documentation
- Review API integration examples above
- Check browser console for errors
- Verify all data models match expected format

## Next Steps

1. Implement API endpoints with real data
2. Test with sample workflows and executions
3. Customize styling to match your brand
4. Add authentication/authorization
5. Deploy to production
6. Monitor dashboard performance
7. Gather user feedback and iterate

Enjoy your automation dashboard!
