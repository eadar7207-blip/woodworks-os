/**
 * Dashboard JavaScript
 * Main application logic for the automation dashboard
 */

const Dashboard = {
    // State
    state: {
        currentTab: 'workflows',
        selectedExecution: null,
        autoRefresh: true,
        refreshInterval: 5000,
        refreshTimer: null,
    },

    // Initialize
    async init() {
        console.log('Dashboard: Initializing...');

        // Setup event listeners
        this.setupEventListeners();

        // Initial load
        await this.refresh();

        // Setup auto-refresh
        this.setupAutoRefresh();

        console.log('Dashboard: Initialized');
    },

    // Setup event listeners
    setupEventListeners() {
        // Tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.switchTab(tab);
            });
        });

        // Refresh button
        document.getElementById('refresh-btn').addEventListener('click', () => {
            this.refresh();
        });

        // Status filter
        document.getElementById('status-filter').addEventListener('change', () => {
            this.loadExecutions();
        });

        // Modal close
        document.querySelector('.modal-close').addEventListener('click', () => {
            this.closeModal();
        });

        document.getElementById('modal-close-btn').addEventListener('click', () => {
            this.closeModal();
        });

        document.getElementById('modal').addEventListener('click', (e) => {
            if (e.target.id === 'modal') {
                this.closeModal();
            }
        });
    },

    // Setup auto-refresh
    setupAutoRefresh() {
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
        }

        if (this.state.autoRefresh) {
            this.state.refreshTimer = setInterval(() => {
                this.refresh();
            }, this.state.refreshInterval);
        }
    },

    // Switch tab
    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabName}-tab`);
        });

        this.state.currentTab = tabName;

        // Load data for tab
        if (tabName === 'workflows') {
            this.loadWorkflows();
        } else if (tabName === 'executions') {
            this.loadExecutions();
        }
    },

    // Refresh all data
    async refresh() {
        try {
            console.log('Dashboard: Refreshing...');

            await Promise.all([
                this.loadStats(),
                this.loadWorkflows(),
                this.loadExecutions(),
            ]);

            this.updateLastUpdated();
            console.log('Dashboard: Refresh complete');
        } catch (error) {
            console.error('Dashboard: Refresh error', error);
            this.showError('Failed to refresh dashboard');
        }
    },

    // Load statistics
    async loadStats() {
        try {
            const response = await API.getStats();

            if (response.success) {
                const stats = response.stats;

                document.querySelector('#stat-workflows .stat-value').textContent = stats.total_workflows;
                document.querySelector('#stat-active .stat-value').textContent = stats.active_workflows;
                document.querySelector('#stat-executions .stat-value').textContent = stats.total_executions;
                document.querySelector('#stat-success .stat-value').textContent = `${stats.success_rate.toFixed(1)}%`;
            }
        } catch (error) {
            console.error('Load stats error:', error);
        }
    },

    // Load workflows
    async loadWorkflows() {
        const container = document.getElementById('workflows-loading');
        const table = document.getElementById('workflows-table');
        const tbody = document.getElementById('workflows-tbody');
        const errorDiv = document.getElementById('workflows-error');

        try {
            container.style.display = 'block';
            table.style.display = 'none';
            errorDiv.style.display = 'none';

            const response = await API.getWorkflows(50, 0);

            if (!response.success) {
                throw new Error(response.error || 'Failed to load workflows');
            }

            const workflows = response.workflows || [];

            if (workflows.length === 0) {
                container.innerHTML = '<p class="placeholder-text">No workflows found</p>';
                return;
            }

            tbody.innerHTML = workflows.map(w => `
                <tr data-workflow-id="${w.id}">
                    <td><strong>${this.escapeHtml(w.name)}</strong></td>
                    <td>${w.trigger_type || 'manual'}</td>
                    <td>
                        <span class="badge ${w.is_active ? 'badge-active' : 'badge-inactive'}">
                            ${w.is_active ? 'Active' : 'Inactive'}
                        </span>
                    </td>
                    <td><small>${Formatters.formatDate(w.created_at)}</small></td>
                    <td><small>${Formatters.formatDate(w.updated_at)}</small></td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="Dashboard.viewWorkflowDetails('${w.id}')">View</button>
                        <button class="btn btn-sm" onclick="Dashboard.executeWorkflow('${w.id}')">Run</button>
                    </td>
                </tr>
            `).join('');

            container.style.display = 'none';
            table.style.display = 'table';
        } catch (error) {
            console.error('Load workflows error:', error);
            container.style.display = 'none';
            errorDiv.textContent = `Error: ${error.message}`;
            errorDiv.style.display = 'block';
        }
    },

    // Load executions
    async loadExecutions() {
        const container = document.getElementById('executions-loading');
        const table = document.getElementById('executions-table');
        const tbody = document.getElementById('executions-tbody');
        const errorDiv = document.getElementById('executions-error');
        const statusFilter = document.getElementById('status-filter').value;

        try {
            container.style.display = 'block';
            table.style.display = 'none';
            errorDiv.style.display = 'none';

            const response = await API.getExecutions(50, 0, statusFilter, '');

            if (!response.success) {
                throw new Error(response.error || 'Failed to load executions');
            }

            const executions = response.executions || [];

            if (executions.length === 0) {
                container.innerHTML = '<p class="placeholder-text">No executions found</p>';
                return;
            }

            tbody.innerHTML = executions.map(e => {
                const duration = e.duration_ms ? Formatters.formatDuration(e.duration_ms) : '-';
                return `
                    <tr data-execution-id="${e.id}">
                        <td><small>${Formatters.truncateId(e.id)}</small></td>
                        <td><small>${Formatters.truncateId(e.workflow_id)}</small></td>
                        <td>
                            <span class="badge badge-${e.status}">
                                ${e.status}
                            </span>
                        </td>
                        <td><small>${Formatters.formatDateTime(e.started_at)}</small></td>
                        <td><small>${duration}</small></td>
                        <td>
                            <button class="btn btn-sm btn-primary" onclick="Dashboard.viewExecutionDetails('${e.id}')">Details</button>
                        </td>
                    </tr>
                `;
            }).join('');

            container.style.display = 'none';
            table.style.display = 'table';
        } catch (error) {
            console.error('Load executions error:', error);
            container.style.display = 'none';
            errorDiv.textContent = `Error: ${error.message}`;
            errorDiv.style.display = 'block';
        }
    },

    // View workflow details
    async viewWorkflowDetails(workflowId) {
        this.switchTab('details');

        try {
            const response = await API.getWorkflow(workflowId);

            if (!response.success) {
                throw new Error(response.error || 'Failed to load workflow');
            }

            const workflow = response.workflow;
            const executions = response.recent_executions || [];

            const html = `
                <div class="details-section">
                    <h3>Workflow Information</h3>
                    <div class="details-grid">
                        <div class="detail-item">
                            <div class="detail-label">ID</div>
                            <div class="detail-value">${this.escapeHtml(workflow.id)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Name</div>
                            <div class="detail-value">${this.escapeHtml(workflow.name)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Type</div>
                            <div class="detail-value">${workflow.trigger_type || 'manual'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Status</div>
                            <div class="detail-value">
                                <span class="badge ${workflow.is_active ? 'badge-active' : 'badge-inactive'}">
                                    ${workflow.is_active ? 'Active' : 'Inactive'}
                                </span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Created</div>
                            <div class="detail-value">${Formatters.formatDateTime(workflow.created_at)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Updated</div>
                            <div class="detail-value">${Formatters.formatDateTime(workflow.updated_at)}</div>
                        </div>
                    </div>
                </div>

                ${workflow.description ? `
                    <div class="details-section">
                        <h3>Description</h3>
                        <p>${this.escapeHtml(workflow.description)}</p>
                    </div>
                ` : ''}

                <div class="details-section">
                    <h3>Configuration</h3>
                    <pre style="background: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto;">${this.escapeHtml(
                    typeof workflow.config === 'string' ? workflow.config : JSON.stringify(JSON.parse(workflow.config || '{}'), null, 2)
                )}</pre>
                </div>

                ${executions.length > 0 ? `
                    <div class="details-section">
                        <h3>Recent Executions</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Status</th>
                                    <th>Started</th>
                                    <th>Completed</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${executions.map(e => `
                                    <tr>
                                        <td><small>${Formatters.truncateId(e.id)}</small></td>
                                        <td><span class="badge badge-${e.status}">${e.status}</span></td>
                                        <td><small>${Formatters.formatDateTime(e.started_at)}</small></td>
                                        <td><small>${Formatters.formatDateTime(e.completed_at)}</small></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                ` : ''}
            `;

            document.getElementById('details-content').innerHTML = html;
        } catch (error) {
            console.error('View workflow details error:', error);
            document.getElementById('details-content').innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
        }
    },

    // View execution details
    async viewExecutionDetails(executionId) {
        this.showModal('Execution Details');

        try {
            const response = await API.getExecution(executionId);

            if (!response.success) {
                throw new Error(response.error || 'Failed to load execution');
            }

            const execution = response.execution;
            const steps = response.steps || [];
            const outputs = response.outputs || [];

            let html = `
                <div class="details-section">
                    <h3>Execution Information</h3>
                    <div class="details-grid">
                        <div class="detail-item">
                            <div class="detail-label">ID</div>
                            <div class="detail-value">${this.escapeHtml(execution.id)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Workflow ID</div>
                            <div class="detail-value">${this.escapeHtml(execution.workflow_id)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Status</div>
                            <div class="detail-value">
                                <span class="badge badge-${execution.status}">${execution.status}</span>
                            </div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Type</div>
                            <div class="detail-value">${execution.trigger_type || 'manual'}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Started</div>
                            <div class="detail-value">${Formatters.formatDateTime(execution.started_at)}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Completed</div>
                            <div class="detail-value">${Formatters.formatDateTime(execution.completed_at)}</div>
                        </div>
                    </div>
                </div>
            `;

            if (execution.error_message) {
                html += `
                    <div class="details-section">
                        <h3>Error</h3>
                        <div class="error-message">${this.escapeHtml(execution.error_message)}</div>
                    </div>
                `;
            }

            if (steps.length > 0) {
                html += `
                    <div class="details-section">
                        <h3>Execution Steps</h3>
                        <div class="steps-list">
                            ${steps.map((step, idx) => `
                                <div class="step-item">
                                    <div class="step-header">
                                        <div class="step-title">Step ${step.step_index + 1}: ${this.escapeHtml(step.step_name || 'Unknown')}</div>
                                        <span class="badge badge-${step.status}">${step.status}</span>
                                    </div>
                                    <div class="step-metadata">
                                        <div><strong>Type:</strong> ${step.action_type}</div>
                                        <div><strong>Duration:</strong> ${step.duration_ms ? Formatters.formatDuration(step.duration_ms) : '-'}</div>
                                        <div><strong>Retries:</strong> ${step.retry_count || 0}</div>
                                    </div>
                                    ${step.error_message ? `
                                        <div class="error-message" style="margin-top: 10px;">
                                            <strong>Error:</strong> ${this.escapeHtml(step.error_message)}
                                        </div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            if (outputs.length > 0) {
                html += `
                    <div class="details-section">
                        <h3>Outputs</h3>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Key</th>
                                    <th>Value</th>
                                    <th>Type</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${outputs.map(o => `
                                    <tr>
                                        <td>${this.escapeHtml(o.output_key)}</td>
                                        <td><small>${this.escapeHtml(o.output_value || '-')}</small></td>
                                        <td>${o.data_type || 'string'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }

            document.getElementById('modal-body').innerHTML = html;
        } catch (error) {
            console.error('View execution details error:', error);
            document.getElementById('modal-body').innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
        }
    },

    // Execute workflow
    async executeWorkflow(workflowId) {
        if (!confirm('Execute this workflow now?')) {
            return;
        }

        try {
            const response = await API.executeWorkflow(workflowId, {});

            if (!response.success) {
                throw new Error(response.error || 'Failed to execute workflow');
            }

            alert(`Workflow execution started: ${response.execution_id}`);
            this.loadExecutions();
        } catch (error) {
            console.error('Execute workflow error:', error);
            alert(`Error: ${error.message}`);
        }
    },

    // Modal functions
    showModal(title) {
        document.getElementById('modal-title').textContent = title;
        document.getElementById('modal').classList.add('show');
    },

    closeModal() {
        document.getElementById('modal').classList.remove('show');
    },

    // Utility functions
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    showError(message) {
        alert(`Error: ${message}`);
    },

    updateLastUpdated() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
        });
        document.getElementById('last-updated').textContent = `Last updated: ${timeStr}`;
    },
};

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Dashboard.init();
});
