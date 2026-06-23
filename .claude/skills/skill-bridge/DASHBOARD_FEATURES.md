# Dashboard Features - Complete Reference

## Real-Time Updates Architecture

### Polling System

The dashboard uses intelligent polling with retry logic:

```javascript
// Configuration
POLL_INTERVAL: 2000        // 2 seconds
MAX_RETRIES: 3             // Retry 3 times
RETRY_DELAY: 1000          // 1 second between retries
```

### What Gets Updated

Every 2 seconds (when polling is active):

1. **Skills List** - Refreshes available skills
2. **Execution History** - Fetches latest executions
3. **Statistics** - Recalculates performance metrics
4. **Running Executions** - Polls status for in-progress tasks

### Retry Logic

```
Request fails
    ↓ (wait 1s)
Retry 1 → success? Yes → Update
       ↓ No (wait 1s)
Retry 2 → success? Yes → Update
       ↓ No (wait 1s)
Retry 3 → success? Yes → Update
       ↓ No
Show error state
```

## Interactive Features

### 1. Workflow Execution

#### Execute Synchronously
1. Click "Execute" button
2. Select skill from dropdown
3. Select action
4. Enter parameters (JSON)
5. Click "Execute"
6. Wait for result
7. View in modal

Example:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "action": "create"
}
```

#### Execute Asynchronously
1. Same as above
2. Check "Run asynchronously"
3. Get invocation ID immediately
4. Dashboard auto-polls for status
5. Shows real-time progress bar
6. Displays result when complete

### 2. Search & Filtering

#### Search Box
- Real-time search across:
  - Skill names
  - Action names
  - Invocation IDs
- Debounced (300ms) for performance
- Shortcut: `Ctrl+K` / `Cmd+K`

#### Status Filter
- All Status
- Completed (successful)
- Failed (error)
- Running (in progress)
- Queued (waiting)

#### Combined Filtering
Search + Status filter work together:
```
Search: "import" + Status: "failed"
↓
Shows only failed imports
```

### 3. Real-Time Progress Tracking

For async executions:

```
Queued (25% progress) →  Running (50%) →  Completed (100%)
   ↓                        ↓                  ↓
Status badge            Progress bar      Green checkmark
"QUEUED"                  updating         "COMPLETED"
```

Progress updates:
- Every 2 seconds via polling
- Shows current status
- Displays duration
- Shows errors if failed

### 4. Statistics & Analytics

#### Key Metrics Displayed

| Metric | Calculation | Use Case |
|--------|-------------|----------|
| Total Executions | Count all | Overall activity |
| Completed | Count where status='completed' | Success count |
| Failed | Count where status='failed' | Error tracking |
| Running | Count where status='running' | Active tasks |
| Success Rate | (completed / total) * 100 | Performance KPI |
| Avg Duration | Sum(duration) / count | Performance baseline |

#### Charts

1. **Status Distribution**
   - Pie-chart style bars
   - Shows count and percentage
   - Color-coded by status

2. **Top Skills**
   - Horizontal bar chart
   - Shows top 5 most-used skills
   - Ordered by execution count

### 5. Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| Ctrl+K / Cmd+K | Focus search | Any page |
| Ctrl+R / Cmd+R | Refresh all | Any page |
| Esc | Close modal | When modal open |
| Tab | Navigate form | Execute modal |
| Enter | Submit form | Execute modal |

### 6. Error Handling

#### Automatic Error Recovery

```
API Call
    ↓
Error?
├─ Yes → Retry 1 → Retry 2 → Retry 3 → Show error state
└─ No  → Update UI
```

#### Error Display

1. **Toast Notification**
   - Top-right corner
   - Auto-dismisses in 5s
   - Shows error message

2. **Error States**
   - Empty skill list → "No skills available"
   - API down → "Failed to load skills"
   - Network error → "Connection failed"

3. **User Actions**
   - Manual retry button
   - Refresh button
   - Close modal and try again

### 7. Responsive Design

#### Desktop (1024px+)
- Full feature set
- All columns visible
- Side-by-side layouts
- Hover effects enabled

#### Tablet (768px - 1023px)
- Stacked navigation
- Fewer visible columns
- Optimized touch targets
- Modal takes 90% width

#### Mobile (< 768px)
- Single column layouts
- Vertical stacking
- 40px+ touch targets
- Full-width modals
- Hamburger menus
- Simplified charts

### 8. Modals & Dialogs

All modals include:
- Centered overlay
- Close button (X)
- Click outside to close
- Esc key to close
- Smooth animations

#### Modal Types

1. **Execute Modal**
   - Skill selector
   - Action selector
   - JSON parameters
   - Async checkbox
   - Submit button

2. **Result Modal**
   - Status badge
   - Output JSON
   - Copy to clipboard
   - Execution duration

3. **Details Modal**
   - Skill information
   - List of actions
   - Parameter definitions
   - Execute button

4. **Error Modal**
   - Error message
   - Invocation ID
   - Copy error
   - Retry button

## State Management

### AppState Object

```javascript
AppState = {
  // Current view
  currentTab: 'workflows' | 'history' | 'stats',
  
  // Data cache
  skills: [],                    // All available skills
  executions: Map(),             // Active executions
  history: [],                   // Execution history
  
  // Polling control
  isPolling: false,              // Polling status
  pollIntervals: [],             // Interval IDs
  
  // User filters
  filters: {
    search: '',                  // Search query
    status: 'all',              // Status filter
    skill: 'all'                // Skill filter
  },
  
  // Cached statistics
  stats: {
    total: 0,
    completed: 0,
    failed: 0,
    running: 0,
    avgDuration: 0
  }
}
```

### Data Flow

```
initApp()
├─ cacheDOMElements()      // Cache DOM refs
├─ setupEventListeners()   // Bind events
├─ setupKeyboardShortcuts()
├─ loadSkills()           // Initial fetch
├─ loadHistory()          // Initial fetch
└─ startPolling()         // Start updates
   └─ Every 2 seconds:
      ├─ loadSkills()
      ├─ loadHistory()
      ├─ updateStats()
      └─ renderUI()
```

## Advanced Features

### 1. Auto-Retry Mechanism

When an API call fails:

```javascript
async function loadSkills(retries = 0) {
  try {
    const response = await fetch(`${CONFIG.API_BASE}/available-skills`)
    // Process response
  } catch (error) {
    if (retries < CONFIG.MAX_RETRIES) {
      setTimeout(() => loadSkills(retries + 1), CONFIG.RETRY_DELAY)
    } else {
      setStatus('offline', 'Failed to load skills')
    }
  }
}
```

### 2. Debounced Search

```javascript
// Search updates run max once per 300ms
DOM.searchInput.addEventListener('input', debounce(() => {
  AppState.filters.search = DOM.searchInput.value
  renderExecutionHistory()
}, 300))
```

Prevents:
- Excessive API calls
- UI re-renders on every keystroke
- High CPU usage

### 3. Progress Bar Updates

For running executions:

```javascript
// Status → Progress %
queued   → 25%
running  → 50%
completed → 100%
failed   → 0%

// Updates every 2s via polling
setInterval(() => {
  fetch(`/status/${invocationId}`)
  → updateExecutionProgress()
  → redraw progress bar
}, CONFIG.POLL_INTERVAL)
```

### 4. Smart Status Caching

Tracks execution states in-memory:

```javascript
AppState.executions = new Map()
  .set('exec-123', {
    id: 'exec-123',
    skill: 'email-sender',
    status: 'running',
    startTime: 1717891234000,
    createdAt: '2024-06-08T01:00:00Z'
  })
```

Benefits:
- Instant UI updates
- Reduced API calls
- Better offline support

## Performance Optimizations

### 1. DOM Caching

```javascript
const DOM = {
  skillsList: document.getElementById('skills-list'),
  executionHistory: document.getElementById('execution-history'),
  // ... cached references
}

// Reuse instead of querySelector on every update
```

### 2. Efficient Re-rendering

```javascript
// Only re-render what changed
renderSkills()     // Only if skills array changed
renderHistory()    // Only if history changed
updateStats()      // Only if new data available
```

### 3. Event Delegation

```javascript
// Single listener for dynamic content
document.addEventListener('click', (e) => {
  if (e.target.matches('.skill-card button')) {
    // Handle click
  }
})
```

### 4. Throttled Polling

```javascript
// Polling stops automatically when:
- User switches tabs
- Browser window loses focus
- Polling takes longer than interval

// Resumes when:
- User returns to tab
- Browser regains focus
```

## Integration Points

### API Communication

```
Browser
   ↓ fetch()
   ├─ GET /available-skills
   ├─ POST /invoke/{skill}
   ├─ POST /invoke/{skill}/async
   ├─ GET /status/{id}
   ├─ GET /history
   └─ GET /health
   ↓ JSON response
UI Update
```

### Error Scenarios

1. **Network Error**
   - Auto-retry with backoff
   - Show "offline" status
   - Disable execute button

2. **API Error (4xx/5xx)**
   - Show error message
   - Log to console
   - Offer retry

3. **Invalid JSON Response**
   - Catch parse error
   - Fall back to string display
   - Log error

4. **Timeout**
   - After 30s wait
   - Assume API unresponsive
   - Show retry option

## User Experience Features

### 1. Visual Feedback

- **Loading States** - Spinner animations
- **Status Indicators** - Color-coded badges
- **Progress Bars** - Animated fill
- **Transitions** - Smooth animations (200ms)
- **Hover Effects** - Interactive elements highlight

### 2. Accessibility

- **Semantic HTML** - Proper heading hierarchy
- **Form Labels** - All inputs labeled
- **Color Contrast** - WCAG compliant
- **Keyboard Navigation** - All features keyboard-accessible
- **ARIA Labels** - Screen reader support

### 3. Mobile Optimization

- **Touch Targets** - 44px minimum (Apple Human Interface)
- **Viewport Meta** - Proper scaling
- **Responsive Grid** - Adapts to screen size
- **Simplified Tables** - Stack columns on mobile
- **Large Buttons** - Easy to tap

## Configuration Options

Edit at top of `app.js`:

```javascript
const CONFIG = {
  API_BASE: 'http://localhost:9000',  // API URL
  POLL_INTERVAL: 2000,                // 2 seconds
  HISTORY_LIMIT: 50,                  // Max history records
  MAX_RETRIES: 3,                     // Retry attempts
  RETRY_DELAY: 1000                   // Retry delay (ms)
}
```

## Troubleshooting Guide

### No Data Showing

1. Check API is running: `curl http://localhost:9000/health`
2. Check browser console for errors (F12)
3. Check network tab (F12) for failed requests
4. Verify API_BASE matches your server URL

### Search Not Working

1. Type slowly - debounce is 300ms
2. Check browser console for errors
3. Verify data in history tab
4. Try refreshing page (Ctrl+R)

### Progress Bar Stuck

1. Check API `/status/{id}` returns valid response
2. Verify polling is enabled (check startPolling logs)
3. Try clicking monitor button to force update
4. Check skill bridge logs for errors

### Styling Issues

1. Clear browser cache (Ctrl+Shift+R)
2. Check styles.css loads (Network tab)
3. Check no CSS errors (Console tab)
4. Try different browser

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

Requires:
- ES6 JavaScript
- Fetch API
- CSS Grid
- CSS Custom Properties
