# Skill Bridge Dashboard

Interactive, real-time dashboard for managing and executing skills via the Skill Bridge API.

## Features

### Core Features
- **Real-time Polling** - 2-second polling intervals for live updates
- **Skill Management** - Browse, view details, and execute skills
- **Execution History** - Complete audit trail of all executions
- **Live Progress Tracking** - Monitor long-running tasks
- **Advanced Statistics** - Charts and analytics on skill performance
- **Search & Filter** - Quick find with search box and status filters
- **Responsive Design** - Works on desktop, tablet, and mobile

### User Interface
- **Workflows Tab** - Browse available skills in a card grid
- **History Tab** - Tabular view of execution history with filters
- **Statistics Tab** - Performance metrics and distribution charts
- **Status Indicator** - Real-time connection status
- **Execute Modal** - Advanced skill execution with JSON parameters
- **Result Viewer** - Modal dialogs for viewing execution results

### Developer Features
- **Keyboard Shortcuts**
  - `Ctrl+K` / `Cmd+K` - Focus search
  - `Ctrl+R` / `Cmd+R` - Refresh all data
  - `Esc` - Close modals
- **Auto-retry** - Automatic retry logic with exponential backoff
- **Error Handling** - Graceful error states and notifications
- **Async Support** - Full support for asynchronous skill execution
- **CORS Support** - Cross-origin requests when flask-cors is installed

## File Structure

```
skill-bridge/
├── skill_bridge.py           # Flask app (modified to serve dashboard)
├── templates/
│   └── index.html           # Main dashboard HTML
├── static/
│   ├── app.js               # Core dashboard JavaScript (1161 lines)
│   └── styles.css           # Responsive CSS (1234 lines)
└── DASHBOARD.md             # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

flask-cors is optional but recommended for real-time updates.

### 2. Verify Files

```bash
ls -lh static/app.js
ls -lh templates/index.html
ls -lh static/styles.css
```

### 3. Configure Flask App

The skill_bridge.py has been updated to:
- Serve the dashboard HTML at `/`
- Serve static files (CSS, JS) at `/static/`
- Configure template and static folders
- Enable CORS (if flask-cors is installed)

### 4. Start the Server

```bash
# Development
python skill_bridge.py

# With environment variables
SKILL_BRIDGE_HOST=0.0.0.0 SKILL_BRIDGE_PORT=9000 python skill_bridge.py

# Production
gunicorn -w 4 -b 0.0.0.0:9000 skill_bridge:app
```

### 5. Access Dashboard

Open in browser: http://localhost:9000

## API Integration

The dashboard communicates with these Flask API endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve dashboard HTML |
| `/static/<file>` | GET | Serve CSS/JS |
| `/health` | GET | Health check |
| `/available-skills` | GET | List all skills |
| `/skills/<name>` | GET | Get skill details |
| `/invoke/<name>` | POST | Execute skill synchronously |
| `/invoke/<name>/async` | POST | Execute skill asynchronously |
| `/status/<id>` | GET | Get execution status |
| `/history` | GET | Get execution history |

## Real-Time Updates

### Polling Architecture

```
Dashboard
    ↓
[2s interval]
    ↓
GET /available-skills
GET /history
GET /status/<id>
    ↓
Update DOM
Show notifications
Update charts
```

### Configuration

Edit `app.js` CONFIG object:

```javascript
const CONFIG = {
  API_BASE: 'http://localhost:9000',      // API endpoint
  POLL_INTERVAL: 2000,                    // 2 seconds
  HISTORY_LIMIT: 50,                      // Max records
  MAX_RETRIES: 3,                         // Retry attempts
  RETRY_DELAY: 1000                       // Retry delay (ms)
};
```

## Features Explained

### 1. Real-Time Polling

```javascript
startPolling()     // Start automatic updates
stopPolling()      // Stop updates
```

- Auto-updates every 2 seconds when viewing history or stats
- Pauses when switching tabs for efficiency
- Retries with exponential backoff on network errors

### 2. Skill Execution

**Synchronous:**
```
User clicks "Execute" 
→ Shows modal with skill selection
→ User fills parameters (JSON)
→ POST to /invoke/{skill}
→ Waits for response
→ Shows result modal
```

**Asynchronous:**
```
User checks "Run asynchronously"
→ POST to /invoke/{skill}/async
→ Returns invocation_id immediately
→ Dashboard polls /status/{id}
→ Updates progress bar in real-time
→ Completes when execution finishes
```

### 3. Search & Filter

- **Search Box** - Full-text search across skill name, action, invocation ID
- **Status Filter** - All, Completed, Failed, Running, Queued
- Debounced (300ms) for performance

### 4. Charts & Statistics

- **Status Distribution** - Pie chart of execution statuses
- **Top Skills** - Bar chart of most-used skills
- **Success Rate** - Percentage of successful executions
- **Average Duration** - Mean execution time in milliseconds

### 5. Error Handling

```javascript
// Automatic retry with exponential backoff
loadSkills(retries = 0)
  if (error && retries < MAX_RETRIES)
    setTimeout(() => loadSkills(retries + 1), RETRY_DELAY)

// Graceful error states
showNotification('Error message', 'error')  // Toast notification
renderSkillsError(error)                    // Error card in UI
setStatus('offline', 'Connection failed')   // Status indicator
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+K (Windows/Linux) / Cmd+K (Mac) | Focus search box |
| Ctrl+R / Cmd+R | Refresh all data |
| Esc | Close any open modal |

## Mobile Experience

- **Responsive Grid** - Skills grid adapts to screen size
- **Touch-Friendly** - Buttons sized for touch (40px minimum)
- **Stacked Layout** - Header elements stack on small screens
- **Modal Optimization** - Modals use 90% width on mobile
- **Table Adaptation** - History table becomes single-column on mobile

## Performance

- **Efficient Updates** - Only updates changed DOM elements
- **Debounced Search** - 300ms debounce prevents excessive re-renders
- **Smart Polling** - Stops polling when tab is not in focus
- **DOM Caching** - Frequently accessed elements cached in memory
- **Lazy Loading** - Modals created on-demand

## Troubleshooting

### Dashboard not loading

```bash
# Check Flask is running
curl http://localhost:9000/health

# Check static files exist
ls -lh static/app.js templates/index.html

# Check Flask logs
tail -f skill_bridge.log
```

### API calls failing

```javascript
// Enable debug logging
CONFIG.DEBUG = true

// Check browser console
F12 → Console tab
```

### Real-time updates not working

1. Check polling interval in CONFIG
2. Verify API is returning data: `curl http://localhost:9000/history`
3. Check browser network tab in DevTools
4. Ensure no API key blocking requests (if API_KEY set)

### Styling issues

1. Clear browser cache (Ctrl+Shift+R)
2. Check CSS file loads: `curl http://localhost:9000/static/styles.css`
3. Verify CSS classes in styles.css

## Development

### Adding a New Feature

1. **Add HTML element** in `templates/index.html`
2. **Cache DOM element** in `cacheDOMElements()`
3. **Create handler** function in `app.js`
4. **Bind event listener** in `setupEventListeners()`
5. **Update state** in `AppState` object
6. **Test** in browser

### Extending the API

1. Add new Flask route in `skill_bridge.py`
2. Call from `app.js` using `fetch()`
3. Update UI to show results
4. Add error handling

### Styling

- CSS variables: see `:root` in `styles.css`
- Dark mode: wrapped in `@media (prefers-color-scheme: dark)`
- Responsive breakpoints: 1024px, 768px, 480px

## Architecture

### State Management

```javascript
AppState = {
  currentTab: 'workflows',           // Current view
  skills: [],                        // Available skills
  executions: Map,                   // Active executions
  history: [],                       // Execution history
  isPolling: false,                  // Polling status
  filters: { search, status, skill }, // Search/filter state
  stats: { total, completed, ... }   // Statistics cache
}
```

### Polling Loop

```javascript
startPolling()
├─ setInterval(2000)
│  ├─ loadSkills()
│  ├─ loadHistory()
│  └─ updateStats()
└─ Updates DOM after each fetch
```

### Event Flow

```
User Action
    ↓
Event Listener
    ↓
Handler Function
    ↓
API Call (fetch)
    ↓
Update AppState
    ↓
Re-render UI
    ↓
Show Notification
```

## Testing

Run the test suite:

```bash
python test_dashboard.py
```

Tests cover:
- Dashboard HTML loads
- Static files served
- API endpoints exist
- JavaScript functions present
- HTML elements present
- CSS classes defined

## Deployment

### Production Checklist

- [ ] Update `CONFIG.API_BASE` for production URL
- [ ] Set `SKILL_BRIDGE_API_KEY` if using authentication
- [ ] Configure CORS origins if needed
- [ ] Use HTTPS in production
- [ ] Set appropriate `POLL_INTERVAL` for load
- [ ] Monitor `/health` endpoint
- [ ] Review logs: `skill_bridge.log`

### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 9000
CMD ["python", "skill_bridge.py"]
```

### Systemd Service

```ini
[Unit]
Description=Skill Bridge Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/skill-bridge
ExecStart=/usr/bin/python3 skill_bridge.py
Restart=on-failure
Environment="SKILL_BRIDGE_PORT=9000"

[Install]
WantedBy=multi-user.target
```

## Monitoring

### Key Metrics

- Request latency (avg, p95, p99)
- Error rate by endpoint
- Active connections
- Polling success rate
- Average execution duration

### Logging

Logs are written to `skill_bridge.log`:

```
YYYY-MM-DD HH:MM:SS - skill_bridge - INFO - GET /available-skills
YYYY-MM-DD HH:MM:SS - skill_bridge - INFO - Response: 200
```

## Customization

### Colors

Edit CSS variables in `styles.css`:

```css
:root {
  --primary: #3b82f6;      /* Change primary color */
  --success: #10b981;      /* Change success color */
  --danger: #ef4444;       /* Change danger color */
}
```

### Polling Interval

```javascript
CONFIG.POLL_INTERVAL = 5000  // Change to 5 seconds
```

### History Limit

```javascript
CONFIG.HISTORY_LIMIT = 100   // Show more history
```

## Future Enhancements

- [ ] WebSocket support for real-time updates
- [ ] Skill grouping and categories
- [ ] Scheduled executions
- [ ] Execution retry logic
- [ ] Email/Slack notifications
- [ ] Export execution history
- [ ] User authentication
- [ ] API key management UI
- [ ] Bulk skill execution
- [ ] Skill templates/presets

## Support

- Check `skill_bridge.log` for errors
- Test endpoints with `curl`
- Review browser DevTools Console
- Verify network requests in Network tab
