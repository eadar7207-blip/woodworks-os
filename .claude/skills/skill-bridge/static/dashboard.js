/**
 * Automation Dashboard - Main JavaScript
 * Handles dashboard functionality, API interactions, and UI updates
 */

class AutomationDashboard {
    constructor() {
        this.API_BASE = '/api';
        this.currentTab = 'workflows';
        this.workflows = [];
        this.executions = [];
        this.autoRefreshInterval = null;

        this.init();
    }

    /**
     * Initialize the dashboard
     */
    init() {
        this.setupEventListeners();
        this.setupTabNavigation();
        this.loadDashboardData();
        this.startAutoRefresh();
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Search functionality
        document.getElementById('searchInput')?.addEventListener('input', (e) => {
            this.filterWorkflows(e.target.value);
        });

        // Status filters
        document.getElementById('workflowStatus')?.addEventListener('change', () => {
            this.applyWorkflowFilters();
        });

        document.getElementById('executionStatus')?.addEventListener('change', () => {
            this.applyExecutionFilters();
        });

        document.getElementById('recoveryStatus')?.addEventListener('change', () => {
            this.applyRecoveryFilters();
        });

        // Date filter
        document.getElementById('executionDate')?.addEventListener('change', () => {
            this.applyExecutionFilters();
        });

        // Action buttons
        document.getElementById('createWorkflowBtn')?.addEventListener('click', () => {
            this.showCreateWorkflowModal();
        });

        // Modal close
        document.querySelector('.modal-close')?.addEventListener('click', () => {
            this.closeModal();
        });

        // Modal background click
        document.getElementById('executionModal')?.addEventListener('click', (e) => {
            if (e.target.id === 'executionModal') {
                this.closeModal();
            }
        });
    }

    /**
     * Setup tab navigation
     */
    setupTabNavigation() {
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                this.switchTab(button.dataset.tab);
            });
        });
    }

    /**
     * Switch between tabs
     */
    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });

        this.currentTab = tabName;

        // Load data for the tab if needed
        if (tabName === 'executions') {
            this.loadExecutions();
        } else if (tabName === 'recovery') {
            this.loadRecoveryStatus();
        }
    }

    /**
     * Load all dashboard data
     */
    async loadDashboardData() {
        try {
            await Promise.all([
                this.loadWorkflows(),
                this.loadStats()
            ]);
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        }
    }

    /**
     * Load workflows
     */
    async loadWorkflows() {
        try {
            const response = await fetch(`${this.API_BASE}/workflows`);
            if (!response.ok) throw new Error('Failed to load workflows');

            this.workflows = await response.json();
            this.renderWorkflows();
            this.updateWorkflowCount();
        } catch (error) {
            console.error('Error loading workflows:', error);
        }
    }

    /**
     * Load execution history
     */
    async loadExecutions() {
        try {
            const response = await fetch(`${this.API_BASE}/executions?limit=50`);
            if (!response.ok) throw new Error('Failed to load executions');

            this.executions = await response.json();
            this.renderExecutions();
            this.updateExecutionCount();
        } catch (error) {
            console.error('Error loading executions:', error);
        }
    }

    /**
     * Load recovery status
     */
    async loadRecoveryStatus() {
        try {
            const response = await fetch(`${this.API_BASE}/recovery/status`);
            if (!response.ok) throw new Error('Failed to load recovery status');

            const data = await response.json();
            this.renderRecoveryStatus(data);
        } catch (error) {
            console.error('Error loading recovery status:', error);
        }
    }

    /**
     * Load dashboard statistics
     */
    async loadStats() {
        try {
            const response = await fetch(`${this.API_BASE}/stats`);
            if (!response.ok) throw new Error('Failed to load stats');

            const stats = await response.json();
            this.updateStats(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    /**
     * Render workflows grid
     */
    renderWorkflows() {
        const grid = document.getElementById('workflowsGrid');
        const emptyState = document.getElementById('workflowsEmpty');

        if (!this.workflows || this.workflows.length === 0) {
            grid.innerHTML = '';
            emptyState.style.display = 'flex';
            return;
        }

        emptyState.style.display = 'none';
        grid.innerHTML = this.workflows.map(workflow => `
            <div class="workflow-card" data-workflow-id="${workflow.id}">
                <div class="workflow-header">
                    <h3 class="workflow-title">${this.escapeHtml(workflow.name)}</h3>
                    <span class="workflow-status ${workflow.status}">
                        <span class="status-dot"></span>
                        ${this.capitalizeStatus(workflow.status)}
                    </span>
                </div>

                <p class="workflow-description">${this.escapeHtml(workflow.description || 'No description')}</p>

                <div class="workflow-meta">
                    <div class="meta-item">
                        <div class="meta-label">Executions</div>
                        <div class="meta-value">${workflow.execution_count || 0}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Success Rate</div>
                        <div class="meta-value">${workflow.success_rate || '0'}%</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Last Run</div>
                        <div class="meta-value">${this.formatDate(workflow.last_executed_at || 'Never')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Avg Duration</div>
                        <div class="meta-value">${this.formatDuration(workflow.avg_duration || 0)}</div>
                    </div>
                </div>

                <div class="workflow-footer">
                    <button class="btn btn-secondary" onclick="dashboard.executeWorkflow('${workflow.id}')">
                        Execute
                    </button>
                    <button class="btn btn-secondary" onclick="dashboard.viewWorkflowDetails('${workflow.id}')">
                        View
                    </button>
                </div>
            </div>
        `).join('');
    }

    /**
     * Render executions table
     */
    renderExecutions() {
        const tbody = document.getElementById('executionsTableBody');
        const emptyState = document.getElementById('executionsEmpty');

        if (!this.executions || this.executions.length === 0) {
            tbody.innerHTML = '';
            emptyState.style.display = 'flex';
            return;
        }

        emptyState.style.display = 'none';
        tbody.innerHTML = this.executions.map(execution => `
            <tr onclick="dashboard.viewExecution('${execution.id}')">
                <td class="table-workflow-name">${this.escapeHtml(execution.workflow_name)}</td>
                <td>
                    <span class="table-status ${execution.status}">
                        <span class="status-dot"></span>
                        ${this.capitalizeStatus(execution.status)}
                    </span>
                </td>
                <td>${this.formatDateTime(execution.started_at)}</td>
                <td>${this.formatDuration(execution.duration)}</td>
                <td>
                    <div class="progress-bar-small">
                        <div class="progress-bar-small-fill" style="width: ${execution.progress || 0}%"></div>
                    </div>
                </td>
                <td class="table-actions">
                    <button class="btn btn-secondary action-btn" onclick="event.stopPropagation(); dashboard.viewExecution('${execution.id}')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    /**
     * Render recovery status
     */
    renderRecoveryStatus(data) {
        const recoveryList = document.getElementById('recoveryList');
        const emptyState = document.getElementById('recoveryEmpty');

        if (!data.items || data.items.length === 0) {
            recoveryList.innerHTML = '';
            emptyState.style.display = 'flex';
            document.getElementById('recoveryBadge').textContent = '0';
            return;
        }

        emptyState.style.display = 'none';
        document.getElementById('recoveryBadge').textContent = data.items.length;

        recoveryList.innerHTML = data.items.map(item => `
            <div class="recovery-item">
                <div class="recovery-item-header">
                    <h4 class="recovery-item-title">${this.escapeHtml(item.workflow_name)}</h4>
                    <span class="recovery-item-meta">Execution: ${item.execution_id}</span>
                </div>
                <p style="color: var(--color-text-secondary); margin: var(--spacing-md) 0;">
                    Error: ${this.escapeHtml(item.error_message)}
                </p>
                <ul class="recovery-strategy-list">
                    ${item.strategies.map(strategy => `
                        <li class="recovery-strategy-item">
                            <strong>${strategy.name}:</strong> ${strategy.status}
                            ${strategy.result ? ` - ${strategy.result}` : ''}
                        </li>
                    `).join('')}
                </ul>
            </div>
        `).join('');
    }

    /**
     * Update dashboard statistics
     */
    updateStats(stats) {
        document.getElementById('totalWorkflows').textContent = stats.total_workflows || 0;
        document.getElementById('activeExecutions').textContent = stats.active_executions || 0;
        document.getElementById('successRate').textContent = `${stats.success_rate || 0}%`;
        document.getElementById('failedExecutions').textContent = stats.failed_executions || 0;
    }

    /**
     * Update workflow count badge
     */
    updateWorkflowCount() {
        document.getElementById('workflowCount').textContent = this.workflows.length;
    }

    /**
     * Update execution count badge
     */
    updateExecutionCount() {
        document.getElementById('executionCount').textContent = this.executions.length;
    }

    /**
     * Filter workflows by search term
     */
    filterWorkflows(searchTerm) {
        const filtered = this.workflows.filter(w =>
            w.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (w.description && w.description.toLowerCase().includes(searchTerm.toLowerCase()))
        );

        this.renderFilteredWorkflows(filtered);
    }

    /**
     * Render filtered workflows
     */
    renderFilteredWorkflows(workflows) {
        const grid = document.getElementById('workflowsGrid');

        if (workflows.length === 0) {
            grid.innerHTML = '<div class="empty-state"><p>No workflows match your search</p></div>';
            return;
        }

        // Reuse renderWorkflows logic but with filtered list
        const backup = this.workflows;
        this.workflows = workflows;
        this.renderWorkflows();
        this.workflows = backup;
    }

    /**
     * Apply workflow filters
     */
    applyWorkflowFilters() {
        const statusFilter = document.getElementById('workflowStatus')?.value || '';

        const filtered = this.workflows.filter(w =>
            !statusFilter || w.status === statusFilter
        );

        this.renderFilteredWorkflows(filtered);
    }

    /**
     * Apply execution filters
     */
    applyExecutionFilters() {
        const statusFilter = document.getElementById('executionStatus')?.value || '';
        const dateFilter = document.getElementById('executionDate')?.value || '';

        const filtered = this.executions.filter(e => {
            const statusMatch = !statusFilter || e.status === statusFilter;
            const dateMatch = !dateFilter || this.formatDate(e.started_at).includes(dateFilter);
            return statusMatch && dateMatch;
        });

        // Re-render with filtered results
        const tbody = document.getElementById('executionsTableBody');
        this.executions = filtered;
        this.renderExecutions();
    }

    /**
     * Apply recovery filters
     */
    applyRecoveryFilters() {
        this.loadRecoveryStatus();
    }

    /**
     * Execute a workflow
     */
    async executeWorkflow(workflowId) {
        if (!confirm('Are you sure you want to execute this workflow?')) return;

        try {
            const response = await fetch(`${this.API_BASE}/workflows/${workflowId}/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) throw new Error('Failed to execute workflow');

            const result = await response.json();
            this.showSuccess(`Workflow execution started: ${result.execution_id}`);

            // Switch to executions tab and reload
            this.switchTab('executions');
            setTimeout(() => this.loadExecutions(), 500);
        } catch (error) {
            console.error('Error executing workflow:', error);
            this.showError('Failed to execute workflow');
        }
    }

    /**
     * View workflow details
     */
    viewWorkflowDetails(workflowId) {
        window.location.href = `/workflows/${workflowId}`;
    }

    /**
     * View execution details
     */
    viewExecution(executionId) {
        window.location.href = `/executions/${executionId}`;
    }

    /**
     * Show create workflow modal
     */
    showCreateWorkflowModal() {
        // Placeholder - implement based on your needs
        alert('Create workflow functionality coming soon');
    }

    /**
     * Close modal
     */
    closeModal() {
        document.getElementById('executionModal').style.display = 'none';
    }

    /**
     * Show success message
     */
    showSuccess(message) {
        console.log('Success:', message);
        // Implement toast/notification as needed
    }

    /**
     * Show error message
     */
    showError(message) {
        console.error('Error:', message);
        // Implement toast/notification as needed
    }

    /**
     * Utility: Format date
     */
    formatDate(dateStr) {
        if (!dateStr || dateStr === 'Never') return dateStr;
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        } catch {
            return '--';
        }
    }

    /**
     * Utility: Format date and time
     */
    formatDateTime(dateStr) {
        if (!dateStr) return '--';
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
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

        if (hours > 0) return `${hours}h ${minutes}m`;
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
            if (this.currentTab === 'workflows') {
                this.loadWorkflows();
                this.loadStats();
            } else if (this.currentTab === 'executions') {
                this.loadExecutions();
            } else if (this.currentTab === 'recovery') {
                this.loadRecoveryStatus();
            }
        }, 5000); // Refresh every 5 seconds
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

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AutomationDashboard();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.stopAutoRefresh();
    }
});
