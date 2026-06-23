"""Test the Skill Bridge Dashboard features."""

import unittest
import json
import sys
from skill_bridge import app
from unittest.mock import patch, MagicMock

class TestDashboard(unittest.TestCase):
    """Test dashboard functionality."""

    def setUp(self):
        """Setup test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_dashboard_loads(self):
        """Test that dashboard HTML loads."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Skill Bridge Dashboard', response.data)

    def test_static_files_served(self):
        """Test that static files are served."""
        # Test CSS
        response = self.client.get('/static/styles.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'app-container', response.data)

        # Test JS
        response = self.client.get('/static/app.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'initApp', response.data)

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)

    def test_api_endpoints_exist(self):
        """Test that API endpoints exist."""
        endpoints = [
            ('/available-skills', 'GET'),
            ('/history', 'GET'),
            ('/health', 'GET'),
        ]

        for endpoint, method in endpoints:
            if method == 'GET':
                response = self.client.get(endpoint)
                # Should not be 404
                self.assertNotEqual(response.status_code, 404,
                    f"Endpoint {endpoint} not found")

    def test_404_for_missing_files(self):
        """Test 404 for missing static files."""
        response = self.client.get('/static/nonexistent.js')
        self.assertEqual(response.status_code, 404)

class TestJavaScriptFeatures(unittest.TestCase):
    """Test that JavaScript has required features."""

    def test_app_js_contains_core_functions(self):
        """Verify app.js has all core functions."""
        with open('static/app.js', 'r') as f:
            content = f.read()

        required_functions = [
            'initApp',
            'loadSkills',
            'loadHistory',
            'startPolling',
            'stopPolling',
            'executeSkillRequest',
            'pollExecutionStatus',
            'renderSkills',
            'renderExecutionHistory',
            'updateStats',
            'renderCharts',
            'switchTab',
            'setupEventListeners',
            'setupKeyboardShortcuts',
            'showExecuteModal',
            'showSkillDetails',
            'closeModal',
            'showNotification'
        ]

        for func in required_functions:
            self.assertIn(func, content,
                f"Function '{func}' not found in app.js")

    def test_app_js_contains_features(self):
        """Verify app.js has required features."""
        with open('static/app.js', 'r') as f:
            content = f.read()

        features = [
            'CONFIG.POLL_INTERVAL',
            'CONFIG.API_BASE',
            'Real-time polling',
            'fetch(',
            'async function',
            'appendChild',
            'addEventListener',
            'setInterval',
        ]

        for feature in features:
            self.assertIn(feature, content,
                f"Feature '{feature}' not found in app.js")

    def test_html_has_elements(self):
        """Verify HTML has required elements."""
        with open('templates/index.html', 'r') as f:
            content = f.read()

        required_elements = [
            'id="skills-list"',
            'id="execution-history"',
            'id="stats-container"',
            'id="search-input"',
            'id="filter-status"',
            'id="execute-btn"',
            'id="refresh-btn"',
            'id="status-indicator"',
            'data-tab="workflows"',
            'data-tab="history"',
            'data-tab="stats"',
        ]

        for element in required_elements:
            self.assertIn(element, content,
                f"Element '{element}' not found in HTML")

    def test_styles_have_classes(self):
        """Verify CSS has required classes."""
        with open('static/styles.css', 'r') as f:
            content = f.read()

        required_classes = [
            '.app-container',
            '.app-header',
            '.app-main',
            '.skill-card',
            '.table-row',
            '.stat-card',
            '.modal',
            '.btn-primary',
            '.status-badge',
        ]

        for cls in required_classes:
            self.assertIn(cls, content,
                f"Class '{cls}' not found in CSS")

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
