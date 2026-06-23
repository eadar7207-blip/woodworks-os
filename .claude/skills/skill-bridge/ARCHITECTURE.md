# Dashboard Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     WEB BROWSER (Client)                         │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              HTML/CSS/JavaScript UI                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐ │   │
│  │  │  Workflows   │  │ Executions   │  │ Details Modal  │ │   │
│  │  │  (Tab 1)     │  │ (Tab 2)      │  │ (Tab 3)        │ │   │
│  │  └──────────────┘  └──────────────┘  └────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓ API Calls                           │
│                     (JSON, HTTP/CORS)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK SERVER (Port 8080)                      │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API Routes                            │   │
│  │  /api/workflows          GET    List workflows          │   │
│  │  /api/workflow/{id}      GET    Workflow details        │   │
│  │  /api/executions         GET    List executions         │   │
│  │  /api/execution/{id}     GET    Execution details       │   │
│  │  /api/stats              GET    Statistics              │   │
│  │  /api/execute            POST   Execute workflow        │   │
│  │  /api/health             GET    Health check            │   │
│  │  /                       GET    Dashboard HTML          │   │
│  │  /static/*               GET    CSS/JS files            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓ Database Access                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          ExecutorDatabase Class                          │   │
│  │  • Safe parameterized queries                            │   │
│  │  • Connection pooling                                    │   │
│  │  • Row-as-dict conversion                               │   │
│  │  • Error handling and logging                            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   SQLite Database (executor.db)                  │
│                                                                   │
│  workflows ──────────┐                                            │
│  │ id                │                                            │
│  │ name              │         ┌──────────────────────┐          │
│  │ description       ├────────→│  executions          │          │
│  │ trigger_type      │         │  │ id               │          │
│  │ is_active         │         │  │ workflow_id───────┘          │
│  │ created_at        │         │  │ status                       │
│  │ updated_at        │         │  │ started_at                   │
│  │                   │         │  │ completed_at                 │
│  │                   │         │  │ error_message                │
│  │                   │         │                                  │
│  └───────────────────┘         └──────────────────────┐          │
│                                                        ↓          │
│                                  execution_steps      outputs    │
│                                  │ id                │ id        │
│                                  │ execution_id      │ exec_id   │
│                                  │ step_index        │ output_key│
│                                  │ step_name         │ value     │
│                                  │ action_type       │ type      │
│                                  │ status            │           │
│                                  │ input_data        │           │
│                                  │ output_data       │           │
│                                  │ error_message     │           │
│                                  │ duration_ms       │           │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Loads Dashboard

```
Browser
   ↓
GET / (HTML)
   ↓
Flask app
   ↓
render_template("dashboard.html")
   ↓
Return 200 + HTML
   ↓
Browser renders HTML, loads CSS/JS
```

### 2. Dashboard Auto-Refresh

```
JavaScript setInterval (5s)
   ↓
Call API.getStats()
Call API.getWorkflows()
Call API.getExecutions()
   ↓
Flask routes:
  /api/stats → db.query(stats_sql)
  /api/workflows → db.query(workflows_sql)
  /api/executions → db.query(executions_sql)
   ↓
Return JSON responses
   ↓
JavaScript updates DOM:
  - Update stat card values
  - Render workflow table
  - Render execution table
```

### 3. User Executes Workflow

```
User clicks "Run" button
   ↓
Dashboard shows confirmation
   ↓
POST /api/execute
  {
    "workflow_id": "wf-123",
    "trigger_data": {}
  }
   ↓
Flask endpoint:
  1. Validate workflow exists
  2. Create execution record in DB
  3. Return execution_id + 202 status
   ↓
JavaScript shows success notification
   ↓
Auto-refresh updates execution list
```

### 4. User Views Execution Details

```
User clicks "Details" on execution
   ↓
Dashboard shows execution ID in modal
   ↓
GET /api/execution/{id}
   ↓
Flask endpoint:
  1. Query execution record
  2. Query execution_steps
  3. Query outputs
  4. Combine and return JSON
   ↓
JavaScript renders modal:
  - Execution metadata
  - Step-by-step breakdown
  - Output values
  - Error messages
```

## Component Architecture

### Backend Layers

```
┌─────────────────────────────────────┐
│         Flask Application           │
│  • Route handlers                   │
│  • JSON serialization               │
│  • Error handling                   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      ExecutorDatabase Class         │
│  • SQL query execution              │
│  • Connection management            │
│  • Data transformation              │
│  • Error recovery                   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│    SQLite Database (File-based)     │
│  • Persistent storage               │
│  • ACID transactions                │
│  • Multi-table queries              │
└─────────────────────────────────────┘
```

### Frontend Layers

```
┌─────────────────────────────────────┐
│      HTML Template (structure)      │
│  • Dashboard layout                 │
│  • Tab navigation                   │
│  • Modal windows                    │
│  • Form elements                    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      CSS Stylesheet (presentation)  │
│  • Responsive grid                  │
│  • Color scheme                     │
│  • Animations                       │
│  • Mobile breakpoints               │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   API Client (api.js)               │
│  • HTTP requests                    │
│  • JSON parsing                     │
│  • Error handling                   │
│  • URL building                     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   Dashboard Logic (dashboard.js)    │
│  • State management                 │
│  • DOM updates                      │
│  • Event handling                   │
│  • Auto-refresh                     │
│  • Modal control                    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│    Browser DOM / User Display       │
└─────────────────────────────────────┘
```

## API Design Patterns

### Request/Response Structure

All endpoints follow this pattern:

```javascript
// Request
{
  method: "GET" or "POST",
  url: "/api/endpoint",
  headers: { "Content-Type": "application/json" },
  body: { /* optional */ }
}

// Response (Success)
{
  "success": true,
  "data": { /* endpoint-specific */ },
  "total": 100,           // For list endpoints
  "limit": 50,           // For list endpoints
  "offset": 0            // For list endpoints
}

// Response (Error)
{
  "success": false,
  "error": "Description of error"
}
```

### Pagination Pattern

List endpoints use cursor-based pagination:

```
GET /api/endpoint?limit=50&offset=100

Returns:
{
  "success": true,
  "items": [...],      // limit results
  "total": 1000,       // total available
  "limit": 50,         // requested limit
  "offset": 100        // requested offset
}

Next page: offset=150
Previous page: offset=50
```

### Filtering Pattern

Executions endpoint supports filtering:

```
GET /api/executions?status=completed&workflow_id=wf-123

Parameters:
- status: Filter by execution status
- workflow_id: Filter by specific workflow

Multiple filters are AND'ed together
```

## Database Query Patterns

### Safe Query Execution

```python
# SAFE - Parameterized query
db.query("SELECT * FROM workflows WHERE id = ?", (id,))

# NOT SAFE - String interpolation
db.query(f"SELECT * FROM workflows WHERE id = '{id}'")  # SQL injection!
```

### Connection Handling

```python
def _get_connection(self):
    conn = sqlite3.connect(str(self.db_path))
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    return conn

# Each query gets fresh connection
# Automatically closed after query completes
# No persistent pool (single-threaded development)
```

### Data Transformation

```python
# Raw SQL returns Row objects
row = cursor.fetchone()

# Convert to dict for JSON
data = dict(row)

# Parse nested JSON fields
if data.get('config'):
    data['config'] = json.loads(data['config'])
```

## Error Handling Strategy

### Frontend Error Handling

```javascript
try {
  const response = await API.request('GET', endpoint);
  if (!response.success) {
    showError(response.error);  // User-friendly message
  } else {
    updateUI(response.data);
  }
} catch (error) {
  console.error('Request failed:', error);
  showError('Network error. Please try again.');
}
```

### Backend Error Handling

```python
try:
  # Query database
  data = db.query(sql, params)
  return jsonify({'success': True, 'data': data})
except sqlite3.Error as e:
  print(f"Database error: {e}")
  return jsonify({
    'success': False,
    'error': 'Failed to fetch data'
  }), 500
except Exception as e:
  print(f"Unexpected error: {e}")
  return jsonify({
    'success': False,
    'error': 'Internal server error'
  }), 500
```

## Performance Considerations

### Frontend Performance

1. **DOM Caching** - Cache frequently accessed elements
2. **Debouncing** - Delay rapid updates
3. **Pagination** - Load 50 items at a time
4. **Lazy Loading** - Create modals on-demand
5. **CSS Optimization** - Use CSS variables for theming

### Backend Performance

1. **Parameterized Queries** - Prevent full table scans
2. **Index Usage** - DB automatically indexes on id/fk
3. **Pagination** - LIMIT/OFFSET in all list queries
4. **Filtering** - WHERE clauses reduce result sets
5. **Connection Reuse** - Minimal connection overhead

### Database Performance

1. **File-based SQLite** - Fast for read-heavy workloads
2. **No locks** - Single-process Flask
3. **Indexed columns** - id, workflow_id, status
4. **Small result sets** - Pagination limits growth

## Deployment Considerations

### Development
- Single Flask process
- Auto-reload on changes
- Console output for debugging
- Database in file system

### Production (Gunicorn)
- Multiple worker processes
- No auto-reload
- Log files for persistence
- Same database file
- Add reverse proxy (Nginx)
- Use systemd service

### Cloud Deployment
- Container image (Docker)
- Environment variables for config
- Remote database connection
- Load balancer in front
- Health checks
- Auto-scaling

## Security Architecture

### Input Validation
- SQL: Parameterized queries prevent injection
- HTML: User data escaped in DOM
- JSON: Standard library parsing

### Output Escaping
- HTML templates: Auto-escaped by Flask
- JavaScript strings: JSON-serialized
- API responses: Valid JSON format

### CORS Policy
- Enabled for localhost
- Restrict in production
- OPTIONS pre-flight handling

### Data Access
- Read-only database access
- No direct file system access
- No command execution
- No network calls outside database

## Monitoring & Debugging

### Health Checks
```
GET /api/health → Verify DB connection, API status
```

### Logging
```python
# Errors logged to stdout/stderr
print(f"Query error: {e}")

# Check logs:
tail -f <output.log>
```

### Browser Console
```javascript
// Check network requests
F12 → Network tab

// Check console errors
F12 → Console tab

// API response inspection
console.log(response)
```

### Database Inspection
```bash
# Direct database queries
sqlite3 executor.db

# Count records
sqlite3 executor.db "SELECT COUNT(*) FROM executions"
```

## Extensibility

### Adding a New API Endpoint

1. Add route to `dashboard.py`
2. Implement query logic
3. Return JSON with `success` field
4. Test with curl or API client

### Adding a New UI Tab

1. Add tab button in `dashboard.html`
2. Add tab content div
3. Add tab handler in `dashboard.js`
4. Create load function for data
5. Update event listeners

### Modifying Database Access

1. Update SQL in relevant endpoint
2. Handle new field names in response
3. Update frontend to display new data
4. Test with curl

## Conclusion

The dashboard architecture is:
- **Simple** - Single Flask process, file-based DB
- **Scalable** - Easily convert to Gunicorn + Nginx
- **Maintainable** - Clear separation of concerns
- **Testable** - Each endpoint independently testable
- **Secure** - Parameterized queries, input escaping
- **Flexible** - Easy to add features and endpoints
