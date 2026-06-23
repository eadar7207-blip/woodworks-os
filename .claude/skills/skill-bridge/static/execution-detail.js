/**
 * Execution Details Page - JavaScript
 * Handles execution details viewing and real-time updates
 */

class ExecutionDetailView {
    constructor() {
        this.API_BASE = '/api';
        this.executionId = this.getExecutionIdFromUrl();
        this.autoRefreshInterval = null;
        this.execution = null;

        this.init();
    }

    /**
     * Initialize the execution detail view
     */
    init() {
        if (!this.executionId) {
            this.showError('Invalid execution ID');
            return;
        }

        this.setupEventListeners();
        this.loadExecutionDetails();
        this.startAutoRefresh();
    }

    /**
     * Get execution ID from URL
     */
    getExecutionIdFromUrl() {
        const match = window.location.pathname.match(/\/executions\/(.+)$/);
        return match ? match[1] : null;
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Action buttons
        document.getElementById('pauseBtn')?.addEventListener('click', () => {
            this.pauseExecution();
        });

        document.getElementById('resumeBtn')?.addEventListener('click', () => {
            this.resumeExecution();
        });

        document.getElementById('cancelBtn')?.addEventListener('click', () => {
            this.cancelExecution();
        });

        document.getElementById('retryBtn')?.addEventListener('click', () => {
            this.retryFailedSteps();
        });

        document.getElementById('refreshLogsBtn')?.addEventListener('click', () => {
            this.loadLogs();
        });

        document.getElementById('downloadLogsBtn')?.addEventListener('click', () => {
            this.downloadLogs();
        });
    }

    /**
     * Load execution details
     */
    async loadExecutionDetails() {
        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}`);
            if (!response.ok) throw new Error('Failed to load execution details');

            this.execution = await response.json();
            this.renderExecutionDetails();
            this.updateActionButtons();
        } catch (error) {
            console.error('Error loading execution details:', error);
            this.showError('Failed to load execution details');
        }
    }

    /**
     * Load execution logs
     */
    async loadLogs() {
        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}/logs`);
            if (!response.ok) throw new Error('Failed to load logs');

            const data = await response.json();
            this.renderLogs(data.logs);
        } catch (error) {
            console.error('Error loading logs:', error);
        }
    }

    /**
     * Render execution details
     */
    renderExecutionDetails() {
        if (!this.execution) return;

        // Header info
        document.getElementById('executionTitle').textContent = this.execution.workflow_name;
        document.getElementById('executionId').textContent = `ID: ${this.execution.id}`;

        // Status badge
        const badge = document.getElementById('executionStatusBadge');
        badge.className = `execution-status-badge ${this.execution.status}`;
        badge.innerHTML = `
            <span class="status-dot"></span>
            <span class="status-text">${this.capitalizeStatus(this.execution.status)}</span>
        `;

        // Stats
        document.getElementById('executionStarted').textContent = this.formatDateTime(this.execution.started_at);
        document.getElementById('executionDuration').textContent = this.formatDuration(this.execution.duration);
        document.getElementById('executionProgressPct').textContent = `${this.execution.progress || 0}%`;
        document.getElementById('executionSuccessRate').textContent = `${this.execution.success_rate || 0}%`;

        // Progress bar
        const progressFill = document.getElementById('progressBarFill');
        const progress = this.execution.progress || 0;
        progressFill.style.width = `${progress}%`;
        document.getElementById('progressPercentage').textContent = `${progress}%`;

        // Steps completed
        const stepsCompleted = this.execution.steps_completed || 0;
        const totalSteps = this.execution.total_steps || 0;
        document.getElementById('stepsCompleted').textContent = `${stepsCompleted} of ${totalSteps} steps completed`;

        // Timeline
        this.renderTimeline();

        // Recovery info
        if (this.execution.recovery_active) {
            document.getElementById('recoveryInfoSection').style.display = 'block';
            this.renderRecoveryStrategies();
        }

        // Logs
        this.loadLogs();
    }

    /**
     * Render execution timeline
     */
    renderTimeline() {
        const container = document.getElementById('timelineContainer');

        if (!this.execution.steps || this.execution.steps.length === 0) {
            container.innerHTML = '<p style="color: var(--color-text-muted);">No steps to display</p>';
            return;
        }

        container.innerHTML = this.execution.steps.map(step => `
            <div class="timeline-item ${step.status}">
                <div class="timeline-item-content">
                    <div class="timeline-item-title">${this.escapeHtml(step.name)}</div>
                    <div class="timeline-item-meta">
                        ${this.formatDateTime(step.started_at)} - ${this.formatDuration(step.duration)}
                    </div>
                    ${step.output ? `
                        <div class="timeline-item-output">${this.escapeHtml(step.output)}</div>
                    ` : ''}
                    ${step.error ? `
                        <div style="color: var(--color-danger); margin-top: var(--spacing-md);">
                            <strong>Error:</strong> ${this.escapeHtml(step.error)}
                        </div>
                    ` : ''}
                </div>
            </div>
        `).join('');
    }

    /**
     * Render recovery strategies
     */
    renderRecoveryStrategies() {
        const container = document.getElementById('recoveryStrategies');

        if (!this.execution.recovery_strategies || this.execution.recovery_strategies.length === 0) {
            container.innerHTML = '<p>No recovery strategies available</p>';
            return;
        }

        container.innerHTML = this.execution.recovery_strategies.map(strategy => `
            <div class="recovery-strategy">
                <div class="recovery-strategy-name">${this.escapeHtml(strategy.name)}</div>
                <div class="recovery-strategy-status">${this.capitalizeStatus(strategy.status)}</div>
                ${strategy.result ? `
                    <div style="margin-top: var(--spacing-sm); color: var(--color-text-secondary);">
                        ${this.escapeHtml(strategy.result)}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    /**
     * Render logs
     */
    renderLogs(logs) {
        const container = document.getElementById('logsContent');

        if (!logs || logs.length === 0) {
            container.textContent = 'No logs available';
            return;
        }

        const logText = logs.map(log => {
            const timestamp = this.formatDateTime(log.timestamp);
            const level = log.level || 'INFO';
            return `[${timestamp}] [${level}] ${log.message}`;
        }).join('\n');

        container.textContent = logText;
    }

    /**
     * Update action buttons based on execution status
     */
    updateActionButtons() {
        if (!this.execution) return;

        const isRunning = this.execution.status === 'running';
        const isFailed = this.execution.status === 'failed';
        const isPaused = this.execution.status === 'paused';

        document.getElementById('pauseBtn').style.display = isRunning ? 'inline-flex' : 'none';
        document.getElementById('resumeBtn').style.display = isPaused ? 'inline-flex' : 'none';
        document.getElementById('cancelBtn').style.display = (isRunning || isPaused) ? 'inline-flex' : 'none';
        document.getElementById('retryBtn').style.display = isFailed ? 'inline-flex' : 'none';
    }

    /**
     * Pause execution
     */
    async pauseExecution() {
        if (!confirm('Are you sure you want to pause this execution?')) return;

        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}/pause`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to pause execution');

            this.showSuccess('Execution paused');
            this.loadExecutionDetails();
        } catch (error) {
            console.error('Error pausing execution:', error);
            this.showError('Failed to pause execution');
        }
    }

    /**
     * Resume execution
     */
    async resumeExecution() {
        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}/resume`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to resume execution');

            this.showSuccess('Execution resumed');
            this.loadExecutionDetails();
        } catch (error) {
            console.error('Error resuming execution:', error);
            this.showError('Failed to resume execution');
        }
    }

    /**
     * Cancel execution
     */
    async cancelExecution() {
        if (!confirm('Are you sure you want to cancel this execution? This cannot be undone.')) return;

        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}/cancel`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to cancel execution');

            this.showSuccess('Execution cancelled');
            setTimeout(() => {
                this.loadExecutionDetails();
            }, 500);
        } catch (error) {
            console.error('Error cancelling execution:', error);
            this.showError('Failed to cancel execution');
        }
    }

    /**
     * Retry failed steps
     */
    async retryFailedSteps() {
        if (!confirm('Retry all failed steps in this execution?')) return;

        try {
            const response = await fetch(`${this.API_BASE}/executions/${this.executionId}/retry`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to retry execution');

            this.showSuccess('Execution retried');
            setTimeout(() => {
                this.loadExecutionDetails();
            }, 500);
        } catch (error) {
            console.error('Error retrying execution:', error);
            this.showError('Failed to retry execution');
        }
    }

    /**
     * Download logs
     */
    downloadLogs() {
        const logsText = document.getElementById('logsContent').textContent;
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(logsText));
        element.setAttribute('download', `execution-${this.executionId}-logs.txt`);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    /**
     * Show error message
     */
    showError(message) {
        console.error('Error:', message);
        alert(message); // Simple error display - can be improved with toast notifications
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        console.log('Success:', message);
        // Simple success display - can be improved with toast notifications
    }

    /**
     * Utility: Format date and time
     */
    formatDateTime(dateStr) {
        if (!dateStr) return '--';
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        } catch {
            return '--';
        }
    }

    /**
     * Utility: Format duration in seconds to readable format
     */
    formatDuration(seconds) {
        if (!seconds || seconds === 0) return '--';

        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);

        if (hours > 0) return `${hours}h ${minutes}m ${secs}s`;
        if (minutes > 0) return `${minutes}m ${secs}s`;
        return `${secs}s`;
    }

    /**
     * Utility: Capitalize status text
     */
    capitalizeStatus(status) {
        return status.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
    }

    /**
     * Utility: Escape HTML
     */
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Start auto-refresh
     */
    startAutoRefresh() {
        this.autoRefreshInterval = setInterval(() => {
            this.loadExecutionDetails();
        }, 3000); // Refresh every 3 seconds
    }

    /**
     * Stop auto-refresh
     */
    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
    }
}

// Initialize execution detail view when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.executionDetailView = new ExecutionDetailView();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.executionDetailView) {
        window.executionDetailView.stopAutoRefresh();
    }
});
