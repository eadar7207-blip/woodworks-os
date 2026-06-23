/**
 * Adar Realty Studio Dashboard - Main Application JS
 */

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format a date string to a readable format
 */
function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Format milliseconds to a readable duration
 */
function formatDuration(ms) {
    if (ms < 1000) return Math.round(ms) + 'ms';
    if (ms < 60000) return (ms / 1000).toFixed(1) + 's';
    const minutes = Math.floor(ms / 60000);
    const seconds = ((ms % 60000) / 1000).toFixed(0);
    return minutes + 'm ' + seconds + 's';
}

/**
 * Get Bootstrap badge class for status
 */
function getStatusBadgeClass(status) {
    const map = {
        'completed': 'bg-success',
        'failed': 'bg-danger',
        'running': 'bg-info',
        'pending': 'bg-warning',
        'skipped': 'bg-secondary'
    };
    return map[status] || 'bg-secondary';
}

/**
 * Get icon for status
 */
function getStatusIcon(status) {
    const icons = {
        'completed': 'fa-check-circle',
        'failed': 'fa-times-circle',
        'running': 'fa-spinner fa-spin',
        'pending': 'fa-circle',
        'skipped': 'fa-forward'
    };
    return icons[status] || 'fa-circle';
}

/**
 * Make API call with error handling
 */
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification('Error: ' + error.message, 'danger');
        throw error;
    }
}

/**
 * Show a toast notification
 */
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHtml;
    document.body.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = alertDiv.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// ============================================================================
// DASHBOARD FUNCTIONS
// ============================================================================

/**
 * Load and display execution statistics
 */
async function loadStats() {
    try {
        const stats = await apiCall('/api/stats');

        // Update stat cards
        document.getElementById('total-executions').textContent = stats.total;
        document.getElementById('success-rate').textContent = stats.success_rate + '%';
        document.getElementById('running-count').textContent = stats.running;
        document.getElementById('failed-count').textContent = stats.failed;

        // Update charts if they exist
        if (document.getElementById('status-chart')) {
            updateStatusChart(stats.by_status);
        }

        return stats;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

/**
 * Load recent executions
 */
async function loadRecentExecutions() {
    try {
        const executions = await apiCall('/api/executions?limit=10');

        const container = document.getElementById('recent-executions');
        if (!container) return;

        if (!executions || executions.length === 0) {
            container.innerHTML = `
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>ID</th>
                            <th>Workflow</th>
                            <th>Status</th>
                            <th>Date</th>
                            <th>Duration</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td colspan="5" class="text-center text-muted py-4">
                                No executions yet
                            </td>
                        </tr>
                    </tbody>
                </table>
            `;
            return;
        }

        const rows = executions.map(e => `
            <tr>
                <td>
                    <a href="/execution/${e.id}" class="text-decoration-none">
                        <code>${e.id.substring(0, 8)}...</code>
                    </a>
                </td>
                <td>${e.workflow_name}</td>
                <td>
                    <span class="badge ${getStatusBadgeClass(e.status)}">
                        ${e.status}
                    </span>
                </td>
                <td>
                    <small>${formatDate(e.created_at)}</small>
                </td>
                <td>
                    <small>${formatDuration(e.duration_ms)}</small>
                </td>
            </tr>
        `).join('');

        container.innerHTML = `
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Workflow</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Duration</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error('Failed to load executions:', error);
    }
}

/**
 * Load popular workflows
 */
async function loadPopularWorkflows() {
    try {
        const stats = await apiCall('/api/stats');
        const container = document.getElementById('popular-workflows');

        if (!container) return;

        const workflows = stats.most_used_workflows || [];

        if (workflows.length === 0) {
            container.innerHTML = '<p class="text-muted">No workflows executed yet</p>';
            return;
        }

        const maxCount = Math.max(...workflows.map(w => w.count)) || 1;
        const items = workflows.map(w => `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                    <div><strong>${w.name}</strong></div>
                    <small class="text-muted">${w.count} executions</small>
                </div>
                <div class="progress" style="width: 100px; height: 6px;">
                    <div class="progress-bar" style="width: ${(w.count / maxCount * 100)}%"></div>
                </div>
            </div>
        `).join('');

        container.innerHTML = items;
    } catch (error) {
        console.error('Failed to load workflows:', error);
    }
}

/**
 * Update status chart
 */
let statusChart = null;

function updateStatusChart(byStatus) {
    const ctx = document.getElementById('status-chart');
    if (!ctx) return;

    const context = ctx.getContext('2d');

    if (statusChart) {
        statusChart.destroy();
    }

    const labels = Object.keys(byStatus);
    const data = Object.values(byStatus);
    const colors = {
        'completed': '#84fab0',
        'failed': '#fa709a',
        'running': '#ffd89b',
        'pending': '#a8edea'
    };

    const backgroundColor = labels.map(label => colors[label] || '#cccccc');

    statusChart = new Chart(context, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColor,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            return label + ': ' + value;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Refresh the entire dashboard
 */
async function refreshDashboard() {
    try {
        await Promise.all([
            loadStats(),
            loadRecentExecutions(),
            loadPopularWorkflows()
        ]);
    } catch (error) {
        console.error('Failed to refresh dashboard:', error);
    }
}

// ============================================================================
// EXECUTION MONITORING
// ============================================================================

class ExecutionMonitor {
    constructor(executionId, options = {}) {
        this.executionId = executionId;
        this.options = {
            refreshInterval: options.refreshInterval || 1000,
            container: options.container || '#execution-status',
            autoStart: options.autoStart !== false,
            onComplete: options.onComplete || null,
            onError: options.onError || null
        };
        this.isRunning = false;
        this.intervalId = null;
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.update();
        this.intervalId = setInterval(() => this.update(), this.options.refreshInterval);
    }

    stop() {
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    async update() {
        try {
            const execution = await apiCall(`/api/executions/${this.executionId}`);

            this.render(execution);

            // Stop monitoring if execution is complete
            if (execution.status === 'completed' || execution.status === 'failed') {
                this.stop();
                if (this.options.onComplete) {
                    this.options.onComplete(execution);
                }
            }
        } catch (error) {
            console.error('Monitor error:', error);
            if (this.options.onError) {
                this.options.onError(error);
            }
        }
    }

    render(execution) {
        const container = document.querySelector(this.options.container);
        if (!container) return;

        const totalSteps = execution.steps ? execution.steps.length : 0;
        const completedSteps = execution.steps
            ? execution.steps.filter(s => ['completed', 'failed', 'skipped'].includes(s.status)).length
            : 0;
        const progress = totalSteps > 0 ? (completedSteps / totalSteps * 100) : 0;

        const statusBadge = `<span class="badge ${getStatusBadgeClass(execution.status)}">${execution.status}</span>`;

        const stepsHtml = execution.steps && execution.steps.length > 0
            ? execution.steps.map(step => `
                <div class="step-status ${step.status}">
                    <span class="me-2">
                        <i class="fas ${getStatusIcon(step.status)}"></i>
                    </span>
                    <span class="flex-grow-1">
                        <strong>${step.step_name}</strong>
                        <small class="text-muted d-block">${step.action_type}</small>
                    </span>
                    ${step.duration_ms ? `<span class="text-muted"><small>${formatDuration(step.duration_ms)}</small></span>` : ''}
                </div>
            `).join('')
            : '<p class="text-muted">No steps recorded</p>';

        container.innerHTML = `
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <strong>Status:</strong>
                    ${statusBadge}
                </div>
                <small class="text-muted">
                    ${completedSteps} / ${totalSteps} steps complete (${progress.toFixed(1)}%)
                </small>
                <div class="progress mt-2" style="height: 24px;">
                    <div class="progress-bar" style="width: ${progress}%; transition: width 0.3s ease;"></div>
                </div>
            </div>

            <div class="mt-3">
                <strong class="d-block mb-2">Steps:</strong>
                ${stepsHtml}
            </div>

            <div class="mt-3 text-center">
                <a href="/execution/${this.executionId}" class="btn btn-sm btn-primary">
                    <i class="fas fa-external-link-alt"></i> View Full Details
                </a>
            </div>
        `;
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize dashboard refresh
    const dashboardContainer = document.querySelector('main');

    if (dashboardContainer) {
        // Auto-refresh dashboard every 5 seconds if on dashboard page
        const isDashboard = !window.location.pathname.startsWith('/execution') &&
                            !window.location.pathname.startsWith('/workflow');

        if (isDashboard && document.getElementById('recent-executions')) {
            refreshDashboard();
            setInterval(refreshDashboard, 5000);
        }
    }

    // Initialize tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});

// ============================================================================
// EXPORTS
// ============================================================================

window.ExecutionMonitor = ExecutionMonitor;
window.apiCall = apiCall;
window.formatDate = formatDate;
window.formatDuration = formatDuration;
window.getStatusBadgeClass = getStatusBadgeClass;
window.getStatusIcon = getStatusIcon;
window.showNotification = showNotification;
window.refreshDashboard = refreshDashboard;
window.loadStats = loadStats;
window.loadRecentExecutions = loadRecentExecutions;
window.loadPopularWorkflows = loadPopularWorkflows;
