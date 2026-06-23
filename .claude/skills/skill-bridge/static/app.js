/**
 * Skill Bridge Dashboard - Interactive Real-Time Dashboard
 * Features: Real-time polling, workflow execution, progress tracking, statistics
 */

// Configuration
const CONFIG = {
  API_BASE: 'http://localhost:9000',
  POLL_INTERVAL: 2000, // 2 seconds
  HISTORY_LIMIT: 50,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000
};

// Application State
const AppState = {
  currentTab: 'workflows',
  skills: [],
  executions: new Map(),
  history: [],
  isPolling: false,
  pollIntervals: [],
  filters: {
    search: '',
    status: 'all',
    skill: 'all'
  },
  stats: {
    total: 0,
    completed: 0,
    failed: 0,
    running: 0,
    avgDuration: 0
  }
};

// DOM Cache
const DOM = {
  skillsList: null,
  executionHistory: null,
  statsContainer: null,
  statusIndicator: null,
  searchInput: null,
  filterStatus: null,
  executeBtn: null,
  refreshBtn: null,
  progressBars: new Map()
};

/**
 * Initialize application
 */
async function initApp() {
  console.log('Initializing Skill Bridge Dashboard...');

  // Cache DOM elements
  cacheDOMElements();

  // Setup event listeners
  setupEventListeners();

  // Initial load
  await loadSkills();
  await loadHistory();

  // Start polling
  startPolling();

  // Setup keyboard shortcuts
  setupKeyboardShortcuts();

  console.log('Dashboard initialized successfully');
}

/**
 * Cache frequently accessed DOM elements
 */
function cacheDOMElements() {
  DOM.skillsList = document.getElementById('skills-list');
  DOM.executionHistory = document.getElementById('execution-history');
  DOM.statsContainer = document.getElementById('stats-container');
  DOM.statusIndicator = document.getElementById('status-indicator');
  DOM.searchInput = document.getElementById('search-input');
  DOM.filterStatus = document.getElementById('filter-status');
  DOM.executeBtn = document.getElementById('execute-btn');
  DOM.refreshBtn = document.getElementById('refresh-btn');
  DOM.tabs = document.querySelectorAll('[data-tab]');
  DOM.tabContents = document.querySelectorAll('[data-tab-content]');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  // Tab switching
  document.querySelectorAll('[data-tab]').forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      switchTab(tab.dataset.tab);
    });
  });

  // Search and filter
  if (DOM.searchInput) {
    DOM.searchInput.addEventListener('input', debounce(() => {
      AppState.filters.search = DOM.searchInput.value;
      renderExecutionHistory();
    }, 300));
  }

  if (DOM.filterStatus) {
    DOM.filterStatus.addEventListener('change', (e) => {
      AppState.filters.status = e.target.value;
      renderExecutionHistory();
    });
  }

  // Execute button
  if (DOM.executeBtn) {
    DOM.executeBtn.addEventListener('click', showExecuteModal);
  }

  // Refresh button
  if (DOM.refreshBtn) {
    DOM.refreshBtn.addEventListener('click', () => {
      loadSkills();
      loadHistory();
      updateStats();
    });
  }

  // Modal close buttons
  document.querySelectorAll('.modal-close').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal');
      if (modal) closeModal(modal);
    });
  });

  // Click outside modal to close
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        closeModal(overlay.closest('.modal'));
      }
    });
  });
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      if (DOM.searchInput) DOM.searchInput.focus();
    }

    // Ctrl/Cmd + R: Refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
      e.preventDefault();
      loadSkills();
      loadHistory();
    }

    // Escape: Close modals
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal.active').forEach(modal => {
        closeModal(modal);
      });
    }
  });
}

/**
 * Switch between tabs
 */
function switchTab(tabName) {
  AppState.currentTab = tabName;

  // Update active tab styling
  document.querySelectorAll('[data-tab]').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.tab === tabName);
  });

  // Show/hide content
  document.querySelectorAll('[data-tab-content]').forEach(content => {
    content.classList.toggle('hidden', content.dataset.tabContent !== tabName);
  });

  // Trigger refresh if needed
  if (tabName === 'workflows') {
    loadSkills();
  } else if (tabName === 'history') {
    loadHistory();
  } else if (tabName === 'stats') {
    updateStats();
    renderCharts();
  }
}

/**
 * Load skills from API
 */
async function loadSkills(retries = 0) {
  try {
    setStatus('loading', 'Loading skills...');

    const response = await fetch(`${CONFIG.API_BASE}/available-skills`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    AppState.skills = data.skills || [];

    renderSkills();
    setStatus('online', 'Connected');

  } catch (error) {
    console.error('Error loading skills:', error);

    if (retries < CONFIG.MAX_RETRIES) {
      console.log(`Retrying... (${retries + 1}/${CONFIG.MAX_RETRIES})`);
      setTimeout(() => loadSkills(retries + 1), CONFIG.RETRY_DELAY);
    } else {
      setStatus('offline', 'Failed to load skills');
      renderSkillsError(error);
    }
  }
}

/**
 * Render skills list
 */
function renderSkills() {
  if (!DOM.skillsList) return;

  if (AppState.skills.length === 0) {
    DOM.skillsList.innerHTML = '<div class="empty-state">No skills available</div>';
    return;
  }

  DOM.skillsList.innerHTML = AppState.skills.map(skill => `
    <div class="skill-card">
      <div class="skill-header">
        <h3>${escapeHtml(skill.name)}</h3>
        <span class="skill-type">${escapeHtml(skill.type || 'skill')}</span>
      </div>
      <p class="skill-description">${escapeHtml(skill.description || 'No description')}</p>
      <div class="skill-meta">
        <span class="meta-item">Actions: ${skill.actions?.length || 0}</span>
        <span class="meta-item">Status: <span class="status-badge success">Available</span></span>
      </div>
      <div class="skill-actions">
        <button class="btn btn-primary" onclick="showSkillDetails('${escapeHtml(skill.name)}')">
          View Details
        </button>
        <button class="btn btn-secondary" onclick="executeSkill('${escapeHtml(skill.name)}')">
          Execute
        </button>
      </div>
    </div>
  `).join('');
}

/**
 * Render skills error state
 */
function renderSkillsError(error) {
  if (!DOM.skillsList) return;

  DOM.skillsList.innerHTML = `
    <div class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Failed to Load Skills</h3>
      <p>${escapeHtml(error.message)}</p>
      <button class="btn btn-primary" onclick="loadSkills()">Retry</button>
    </div>
  `;
}

/**
 * Show skill details modal
 */
async function showSkillDetails(skillName) {
  try {
    const response = await fetch(`${CONFIG.API_BASE}/skills/${encodeURIComponent(skillName)}`);
    const data = await response.json();

    if (data.error) {
      showNotification('Error: ' + data.error, 'error');
      return;
    }

    const modal = createModal('skill-details-modal', 'Skill Details');
    modal.innerHTML = `
      <div class="skill-details">
        <h2>${escapeHtml(data.name)}</h2>
        <p>${escapeHtml(data.description || 'No description')}</p>

        <h3>Actions</h3>
        <div class="actions-list">
          ${(data.actions || []).map(action => `
            <div class="action-item">
              <strong>${escapeHtml(action.name)}</strong>
              <p>${escapeHtml(action.description || 'No description')}</p>
              ${action.parameters ? `
                <details>
                  <summary>Parameters</summary>
                  <pre>${JSON.stringify(action.parameters, null, 2)}</pre>
                </details>
              ` : ''}
            </div>
          `).join('')}
        </div>

        <div class="modal-footer">
          <button class="btn btn-primary" onclick="executeSkill('${escapeHtml(skillName)}')">
            Execute Skill
          </button>
          <button class="btn btn-secondary modal-close">Close</button>
        </div>
      </div>
    `;

  } catch (error) {
    showNotification('Error loading skill details: ' + error.message, 'error');
  }
}

/**
 * Show execution modal
 */
function showExecuteModal() {
  const modal = createModal('execute-modal', 'Execute Skill');

  const skillOptions = AppState.skills
    .map(s => `<option value="${escapeHtml(s.name)}">${escapeHtml(s.name)}</option>`)
    .join('');

  modal.innerHTML = `
    <form id="execute-form" class="form-group">
      <div class="form-field">
        <label for="skill-select">Skill</label>
        <select id="skill-select" required>
          <option value="">Select a skill...</option>
          ${skillOptions}
        </select>
      </div>

      <div class="form-field">
        <label for="action-select">Action</label>
        <select id="action-select" required>
          <option value="">Select an action...</option>
        </select>
      </div>

      <div class="form-field">
        <label for="params-input">Parameters (JSON)</label>
        <textarea id="params-input" rows="6" placeholder='{"key": "value"}'>{}</textarea>
      </div>

      <div class="form-field checkbox">
        <input type="checkbox" id="async-exec" />
        <label for="async-exec">Run asynchronously</label>
      </div>

      <div class="modal-footer">
        <button type="submit" class="btn btn-primary">Execute</button>
        <button type="button" class="btn btn-secondary modal-close">Cancel</button>
      </div>
    </form>
  `;

  const skillSelect = modal.querySelector('#skill-select');
  const actionSelect = modal.querySelector('#action-select');
  const form = modal.querySelector('#execute-form');

  // Load actions when skill is selected
  skillSelect.addEventListener('change', (e) => {
    const skill = AppState.skills.find(s => s.name === e.target.value);
    actionSelect.innerHTML = '<option value="">Select an action...</option>';
    if (skill && skill.actions) {
      actionSelect.innerHTML += skill.actions
        .map(a => `<option value="${escapeHtml(a.name)}">${escapeHtml(a.name)}</option>`)
        .join('');
    }
  });

  // Handle form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const skillName = skillSelect.value;
    const action = actionSelect.value;
    const isAsync = modal.querySelector('#async-exec').checked;

    let params = {};
    try {
      const paramsInput = modal.querySelector('#params-input').value;
      if (paramsInput.trim()) {
        params = JSON.parse(paramsInput);
      }
    } catch (error) {
      showNotification('Invalid JSON in parameters', 'error');
      return;
    }

    closeModal(modal);
    await executeSkillRequest(skillName, action, params, isAsync);
  });
}

/**
 * Show execute skill modal for a specific skill
 */
function executeSkill(skillName) {
  showExecuteModal();
  const modal = document.querySelector('.modal.active');
  if (modal) {
    modal.querySelector('#skill-select').value = skillName;
    modal.querySelector('#skill-select').dispatchEvent(new Event('change'));
  }
}

/**
 * Execute skill request
 */
async function executeSkillRequest(skillName, action, params, isAsync = false) {
  try {
    setStatus('loading', 'Executing skill...');

    const endpoint = isAsync
      ? `/invoke/${encodeURIComponent(skillName)}/async`
      : `/invoke/${encodeURIComponent(skillName)}`;

    const response = await fetch(`${CONFIG.API_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        action: action,
        params: params
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }

    const invocationId = data.invocation_id;

    if (isAsync) {
      showNotification(`Skill queued: ${invocationId}`, 'success');
      AppState.executions.set(invocationId, {
        id: invocationId,
        skill: skillName,
        action: action,
        status: 'queued',
        startTime: Date.now(),
        createdAt: new Date().toISOString()
      });

      // Poll for updates
      pollExecutionStatus(invocationId);
    } else {
      showNotification('Skill executed successfully', 'success');

      // Show result
      if (data.output) {
        showResultModal(data, skillName, action);
      }
    }

    setStatus('online', 'Connected');

    // Refresh history
    await loadHistory();

  } catch (error) {
    console.error('Error executing skill:', error);
    showNotification('Error: ' + error.message, 'error');
    setStatus('offline', 'Error executing skill');
  }
}

/**
 * Show result modal
 */
function showResultModal(data, skillName, action) {
  const modal = createModal('result-modal', 'Execution Result');

  const resultHtml = typeof data.output === 'string'
    ? `<p>${escapeHtml(data.output)}</p>`
    : `<pre>${JSON.stringify(data.output, null, 2)}</pre>`;

  modal.innerHTML = `
    <div class="result-container">
      <div class="result-header">
        <h2>${escapeHtml(skillName)} / ${escapeHtml(action)}</h2>
        <span class="status-badge ${data.status}">${escapeHtml(data.status)}</span>
      </div>

      ${data.duration_ms ? `<p class="meta">Duration: ${data.duration_ms}ms</p>` : ''}

      <h3>Output</h3>
      <div class="result-output">
        ${resultHtml}
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="copyToClipboard(this)">Copy to Clipboard</button>
        <button class="btn btn-primary modal-close">Close</button>
      </div>
    </div>
  `;
}

/**
 * Poll execution status
 */
function pollExecutionStatus(invocationId, retries = 0) {
  const checkStatus = async () => {
    try {
      const response = await fetch(`${CONFIG.API_BASE}/status/${encodeURIComponent(invocationId)}`);
      const data = await response.json();

      if (response.ok && data.status !== 'not_found') {
        // Update execution state
        AppState.executions.set(invocationId, {
          ...AppState.executions.get(invocationId),
          ...data
        });

        // Update progress in UI
        updateExecutionProgress(invocationId, data);

        // Continue polling if still running
        if (data.status === 'queued' || data.status === 'running') {
          setTimeout(checkStatus, CONFIG.POLL_INTERVAL);
        } else {
          // Execution complete
          await loadHistory();
        }
      } else if (retries < CONFIG.MAX_RETRIES) {
        retries++;
        setTimeout(checkStatus, CONFIG.POLL_INTERVAL);
      }
    } catch (error) {
      console.error('Error polling status:', error);
      if (retries < CONFIG.MAX_RETRIES) {
        setTimeout(checkStatus, CONFIG.POLL_INTERVAL);
      }
    }
  };

  checkStatus();
}

/**
 * Update execution progress in UI
 */
function updateExecutionProgress(invocationId, data) {
  const progressBar = DOM.progressBars.get(invocationId);
  if (!progressBar) return;

  const progressPercent = data.status === 'completed' ? 100
    : data.status === 'running' ? 50
    : data.status === 'queued' ? 25
    : 0;

  const progressElement = progressBar.querySelector('.progress-fill');
  if (progressElement) {
    progressElement.style.width = progressPercent + '%';
  }

  const statusElement = progressBar.querySelector('.progress-status');
  if (statusElement) {
    statusElement.textContent = data.status.toUpperCase();
    statusElement.className = `progress-status status-badge ${data.status}`;
  }
}

/**
 * Load execution history
 */
async function loadHistory(retries = 0) {
  try {
    const response = await fetch(`${CONFIG.API_BASE}/history?limit=${CONFIG.HISTORY_LIMIT}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    AppState.history = data.invocations || [];

    renderExecutionHistory();
    updateStats();

  } catch (error) {
    console.error('Error loading history:', error);

    if (retries < CONFIG.MAX_RETRIES) {
      console.log(`Retrying history... (${retries + 1}/${CONFIG.MAX_RETRIES})`);
      setTimeout(() => loadHistory(retries + 1), CONFIG.RETRY_DELAY);
    }
  }
}

/**
 * Render execution history
 */
function renderExecutionHistory() {
  if (!DOM.executionHistory) return;

  // Filter history
  let filtered = AppState.history;

  if (AppState.filters.search) {
    const search = AppState.filters.search.toLowerCase();
    filtered = filtered.filter(item =>
      (item.skill_name || '').toLowerCase().includes(search) ||
      (item.action || '').toLowerCase().includes(search) ||
      (item.id || '').toLowerCase().includes(search)
    );
  }

  if (AppState.filters.status !== 'all') {
    filtered = filtered.filter(item => item.status === AppState.filters.status);
  }

  if (filtered.length === 0) {
    DOM.executionHistory.innerHTML = '<div class="empty-state">No executions found</div>';
    return;
  }

  DOM.executionHistory.innerHTML = `
    <div class="history-table">
      <div class="table-header">
        <div class="col-time">Time</div>
        <div class="col-skill">Skill</div>
        <div class="col-action">Action</div>
        <div class="col-status">Status</div>
        <div class="col-duration">Duration</div>
        <div class="col-actions">Actions</div>
      </div>
      <div class="table-body">
        ${filtered.map((item, idx) => `
          <div class="table-row" data-invocation-id="${escapeHtml(item.id)}">
            <div class="col-time" title="${escapeHtml(item.created_at || '')}">${formatTime(item.created_at)}</div>
            <div class="col-skill">${escapeHtml(item.skill_name || 'Unknown')}</div>
            <div class="col-action">${escapeHtml(item.action || 'N/A')}</div>
            <div class="col-status"><span class="status-badge ${item.status}">${item.status.toUpperCase()}</span></div>
            <div class="col-duration">${item.duration_ms ? item.duration_ms + 'ms' : '—'}</div>
            <div class="col-actions">
              ${item.status === 'running' ? `<button class="btn-small" onclick="showExecutionDetails('${escapeHtml(item.id)}')">Monitor</button>` : ''}
              ${item.result ? `<button class="btn-small" onclick="showExecutionResult('${escapeHtml(item.id)}')">View</button>` : ''}
              ${item.error ? `<button class="btn-small" onclick="showExecutionError('${escapeHtml(item.id)}')">Error</button>` : ''}
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  `;

  // Cache progress bars
  document.querySelectorAll('[data-invocation-id]').forEach(row => {
    const id = row.dataset.invocationId;
    DOM.progressBars.set(id, row);
  });
}

/**
 * Show execution details
 */
function showExecutionDetails(invocationId) {
  const execution = AppState.executions.get(invocationId) ||
    AppState.history.find(h => h.id === invocationId);

  if (!execution) {
    showNotification('Execution not found', 'error');
    return;
  }

  const modal = createModal('execution-details-modal', 'Execution Details');

  const startTime = execution.started_at ? new Date(execution.started_at) : null;
  const endTime = execution.completed_at ? new Date(execution.completed_at) : null;
  const duration = startTime && endTime
    ? ((endTime - startTime) / 1000).toFixed(2) + 's'
    : execution.duration_ms ? (execution.duration_ms / 1000).toFixed(2) + 's' : 'Running...';

  modal.innerHTML = `
    <div class="execution-details">
      <h2>${escapeHtml(execution.skill_name)} / ${escapeHtml(execution.action || 'N/A')}</h2>

      <div class="detail-grid">
        <div class="detail-item">
          <strong>ID:</strong>
          <code>${escapeHtml(execution.id)}</code>
        </div>
        <div class="detail-item">
          <strong>Status:</strong>
          <span class="status-badge ${execution.status}">${execution.status.toUpperCase()}</span>
        </div>
        <div class="detail-item">
          <strong>Created:</strong>
          ${formatDateTime(execution.created_at)}
        </div>
        <div class="detail-item">
          <strong>Duration:</strong>
          ${duration}
        </div>
      </div>

      ${execution.params ? `
        <h3>Parameters</h3>
        <pre>${JSON.stringify(typeof execution.params === 'string' ? JSON.parse(execution.params) : execution.params, null, 2)}</pre>
      ` : ''}

      ${execution.status === 'running' ? `
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" style="width: 50%"></div>
          </div>
          <p class="progress-text">Execution in progress...</p>
        </div>
      ` : ''}

      <div class="modal-footer">
        ${execution.status === 'running' ? `<button class="btn btn-secondary" onclick="location.reload()">Auto-refresh</button>` : ''}
        <button class="btn btn-primary modal-close">Close</button>
      </div>
    </div>
  `;
}

/**
 * Show execution result
 */
function showExecutionResult(invocationId) {
  const execution = AppState.history.find(h => h.id === invocationId);

  if (!execution || !execution.result) {
    showNotification('Result not found', 'error');
    return;
  }

  const modal = createModal('result-modal', 'Execution Result');

  let result;
  try {
    result = typeof execution.result === 'string' ? JSON.parse(execution.result) : execution.result;
  } catch (e) {
    result = execution.result;
  }

  const resultHtml = typeof result === 'string'
    ? `<p>${escapeHtml(result)}</p>`
    : `<pre>${JSON.stringify(result, null, 2)}</pre>`;

  modal.innerHTML = `
    <div class="result-container">
      <h2>Result - ${escapeHtml(execution.skill_name)}</h2>
      <div class="result-output">
        ${resultHtml}
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="copyToClipboard(this)">Copy</button>
        <button class="btn btn-primary modal-close">Close</button>
      </div>
    </div>
  `;
}

/**
 * Show execution error
 */
function showExecutionError(invocationId) {
  const execution = AppState.history.find(h => h.id === invocationId);

  if (!execution || !execution.error) {
    showNotification('Error not found', 'error');
    return;
  }

  const modal = createModal('error-modal', 'Execution Error');

  modal.innerHTML = `
    <div class="error-container">
      <h2>Error - ${escapeHtml(execution.skill_name)}</h2>
      <div class="error-output">
        <p>${escapeHtml(execution.error)}</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="copyToClipboard(this)">Copy</button>
        <button class="btn btn-primary modal-close">Close</button>
      </div>
    </div>
  `;
}

/**
 * Update statistics
 */
function updateStats() {
  if (AppState.history.length === 0) {
    AppState.stats = {
      total: 0,
      completed: 0,
      failed: 0,
      running: 0,
      avgDuration: 0
    };
  } else {
    const completed = AppState.history.filter(h => h.status === 'completed').length;
    const failed = AppState.history.filter(h => h.status === 'failed').length;
    const running = AppState.history.filter(h => h.status === 'running').length;

    const durations = AppState.history
      .filter(h => h.duration_ms)
      .map(h => h.duration_ms);

    const avgDuration = durations.length > 0
      ? durations.reduce((a, b) => a + b, 0) / durations.length
      : 0;

    AppState.stats = {
      total: AppState.history.length,
      completed: completed,
      failed: failed,
      running: running,
      avgDuration: Math.round(avgDuration)
    };
  }

  renderStats();
}

/**
 * Render statistics
 */
function renderStats() {
  if (!DOM.statsContainer) return;

  const stats = AppState.stats;
  const successRate = stats.total > 0
    ? Math.round((stats.completed / stats.total) * 100)
    : 0;

  DOM.statsContainer.innerHTML = `
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-number">${stats.total}</div>
        <div class="stat-label">Total Executions</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${stats.completed}</div>
        <div class="stat-label">Completed</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${stats.failed}</div>
        <div class="stat-label">Failed</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${stats.running}</div>
        <div class="stat-label">Running</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${successRate}%</div>
        <div class="stat-label">Success Rate</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">${stats.avgDuration}ms</div>
        <div class="stat-label">Avg Duration</div>
      </div>
    </div>
    <div id="chart-container"></div>
  `;

  // Render charts
  renderCharts();
}

/**
 * Render charts
 */
function renderCharts() {
  const container = document.getElementById('chart-container');
  if (!container || AppState.history.length === 0) return;

  // Status distribution chart
  const statuses = {};
  AppState.history.forEach(item => {
    statuses[item.status] = (statuses[item.status] || 0) + 1;
  });

  const statusChart = `
    <div class="chart-container">
      <h3>Status Distribution</h3>
      <div class="chart-bars">
        ${Object.entries(statuses).map(([status, count]) => {
          const percent = (count / AppState.history.length) * 100;
          return `
            <div class="chart-bar">
              <div class="bar-label">${status}</div>
              <div class="bar-container">
                <div class="bar-fill ${status}" style="width: ${percent}%"></div>
              </div>
              <div class="bar-value">${count}</div>
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;

  // Top skills chart
  const skillCounts = {};
  AppState.history.forEach(item => {
    skillCounts[item.skill_name] = (skillCounts[item.skill_name] || 0) + 1;
  });

  const topSkills = Object.entries(skillCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  const skillChart = `
    <div class="chart-container">
      <h3>Top Skills</h3>
      <div class="chart-bars">
        ${topSkills.map(([skill, count]) => {
          const maxCount = topSkills[0][1];
          const percent = (count / maxCount) * 100;
          return `
            <div class="chart-bar">
              <div class="bar-label">${escapeHtml(skill)}</div>
              <div class="bar-container">
                <div class="bar-fill" style="width: ${percent}%"></div>
              </div>
              <div class="bar-value">${count}</div>
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;

  container.innerHTML = statusChart + skillChart;
}

/**
 * Start polling for updates
 */
function startPolling() {
  if (AppState.isPolling) return;

  AppState.isPolling = true;
  console.log('Starting polling...');

  const pollInterval = setInterval(() => {
    if (AppState.currentTab === 'history' || AppState.currentTab === 'workflows') {
      loadHistory();
    }

    if (AppState.currentTab === 'stats') {
      updateStats();
    }
  }, CONFIG.POLL_INTERVAL);

  AppState.pollIntervals.push(pollInterval);
}

/**
 * Stop polling
 */
function stopPolling() {
  AppState.pollIntervals.forEach(interval => clearInterval(interval));
  AppState.pollIntervals = [];
  AppState.isPolling = false;
  console.log('Polling stopped');
}

/**
 * Set status indicator
 */
function setStatus(status, message) {
  if (!DOM.statusIndicator) return;

  DOM.statusIndicator.className = `status-indicator ${status}`;
  DOM.statusIndicator.title = message;

  const dot = DOM.statusIndicator.querySelector('.status-dot');
  if (dot) {
    dot.className = `status-dot ${status}`;
  }

  const text = DOM.statusIndicator.querySelector('.status-text');
  if (text) {
    text.textContent = message;
  }
}

/**
 * Create modal
 */
function createModal(id, title) {
  // Remove existing modal if present
  const existing = document.getElementById(id);
  if (existing) existing.remove();

  const modal = document.createElement('div');
  modal.id = id;
  modal.className = 'modal active';
  modal.innerHTML = `
    <div class="modal-overlay"></div>
    <div class="modal-content">
      <div class="modal-header">
        <h2>${escapeHtml(title)}</h2>
        <button class="modal-close">&times;</button>
      </div>
      <div class="modal-body"></div>
    </div>
  `;

  // Setup close handlers
  modal.querySelector('.modal-close').addEventListener('click', () => closeModal(modal));
  modal.querySelector('.modal-overlay').addEventListener('click', () => closeModal(modal));

  document.body.appendChild(modal);

  const body = modal.querySelector('.modal-body');
  return body;
}

/**
 * Close modal
 */
function closeModal(modal) {
  if (modal instanceof Element) {
    modal.remove();
  } else {
    const el = document.querySelector(modal);
    if (el) el.remove();
  }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <span>${escapeHtml(message)}</span>
    <button class="close-btn">&times;</button>
  `;

  document.body.appendChild(notification);

  notification.querySelector('.close-btn').addEventListener('click', () => {
    notification.remove();
  });

  setTimeout(() => {
    notification.classList.add('hidden');
    setTimeout(() => notification.remove(), 300);
  }, 5000);
}

/**
 * Copy to clipboard
 */
function copyToClipboard(btn) {
  const modal = btn.closest('.modal');
  const output = modal?.querySelector('.result-output, .error-output, pre');

  if (output) {
    const text = output.textContent;
    navigator.clipboard.writeText(text).then(() => {
      showNotification('Copied to clipboard', 'success');
    });
  }
}

/**
 * Format time
 */
function formatTime(dateString) {
  if (!dateString) return '—';

  const date = new Date(dateString);
  const now = new Date();
  const diff = now - date;

  if (diff < 60000) return 'just now';
  if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
  if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';

  return date.toLocaleDateString();
}

/**
 * Format datetime
 */
function formatDateTime(dateString) {
  if (!dateString) return '—';

  const date = new Date(dateString);
  return date.toLocaleString();
}

/**
 * Escape HTML
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return String(text).replace(/[&<>"']/g, m => map[m]);
}

/**
 * Debounce function
 */
function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', initApp);

/**
 * Cleanup on page unload
 */
window.addEventListener('beforeunload', () => {
  stopPolling();
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AppState, CONFIG, initApp };
}
