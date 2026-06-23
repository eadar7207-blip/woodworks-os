/**
 * API Client for Dashboard
 * Handles all HTTP requests to the backend
 */

const API = {
    BASE_URL: window.location.origin,

    async request(method, endpoint, data = null) {
        try {
            const options = {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
            };

            if (data) {
                options.body = JSON.stringify(data);
            }

            const url = `${this.BASE_URL}${endpoint}`;
            const response = await fetch(url, options);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error [${method} ${endpoint}]:`, error);
            throw error;
        }
    },

    // Workflows
    async getWorkflows(limit = 100, offset = 0) {
        return this.request('GET', `/api/workflows?limit=${limit}&offset=${offset}`);
    },

    async getWorkflow(id) {
        return this.request('GET', `/api/workflow/${id}`);
    },

    async getWorkflowExecutions(id, limit = 50, offset = 0) {
        return this.request('GET', `/api/workflow/${id}/executions?limit=${limit}&offset=${offset}`);
    },

    // Executions
    async getExecutions(limit = 50, offset = 0, status = '', workflowId = '') {
        let url = `/api/executions?limit=${limit}&offset=${offset}`;
        if (status) url += `&status=${status}`;
        if (workflowId) url += `&workflow_id=${workflowId}`;
        return this.request('GET', url);
    },

    async getExecution(id) {
        return this.request('GET', `/api/execution/${id}`);
    },

    async executeWorkflow(workflowId, triggerData = {}) {
        return this.request('POST', '/api/execute', {
            workflow_id: workflowId,
            trigger_data: triggerData,
        });
    },

    // Statistics
    async getStats() {
        return this.request('GET', '/api/stats');
    },

    // Health
    async healthCheck() {
        return this.request('GET', '/api/health');
    },
};

/**
 * Utility functions for data formatting
 */
const Formatters = {
    formatDate(dateString) {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
            });
        } catch {
            return dateString;
        }
    },

    formatDateTime(dateString) {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            });
        } catch {
            return dateString;
        }
    },

    formatDuration(ms) {
        if (!ms || ms === 0) return '-';
        if (ms < 1000) return `${ms}ms`;
        if (ms < 60000) return `${(ms / 1000).toFixed(2)}s`;
        return `${(ms / 60000).toFixed(2)}m`;
    },

    formatJson(obj) {
        try {
            return JSON.stringify(obj, null, 2);
        } catch {
            return String(obj);
        }
    },

    truncateId(id, length = 8) {
        return id ? id.substring(0, length) : '-';
    },
};
