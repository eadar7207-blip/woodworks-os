"""
HTTP client for calling Eitan's automation framework skills
Integrates with Skill Bridge API (localhost:9000)
"""

import os
import time
import logging
import requests

logger = logging.getLogger(__name__)

SKILL_BRIDGE_URL = os.environ.get('SKILL_BRIDGE_URL', 'http://localhost:9000')
API_KEY = os.environ.get('AUTOMATION_API_KEY', 'dev-key')


class SkillBridgeClient:
    """Client for calling automation skills"""

    def __init__(self):
        self.base_url = SKILL_BRIDGE_URL
        self.api_key = API_KEY
        self.timeout = 10

    def _call_skill(self, method, endpoint, payload=None, retries=3):
        """
        Generic method for calling skills with retry logic.

        Args:
            method: 'GET' or 'POST'
            endpoint: '/skills/calendar/create_event'
            payload: Dict to send as JSON
            retries: Number of retry attempts

        Returns:
            Dict with response or error
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        url = f"{self.base_url}{endpoint}"

        for attempt in range(retries):
            try:
                if method == 'GET':
                    response = requests.get(url, headers=headers, timeout=self.timeout)
                elif method == 'POST':
                    response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                else:
                    return {'success': False, 'error': f'Unknown method: {method}'}

                if response.status_code == 200:
                    return response.json()
                elif response.status_code in [429, 503]:  # Retryable
                    wait_time = 2 ** attempt
                    logger.warning(f"Skill call failed with {response.status_code}, retrying in {wait_time}s")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        'success': False,
                        'error': f"HTTP {response.status_code}",
                        'details': response.text
                    }

            except requests.Timeout:
                if attempt == retries - 1:
                    return {'success': False, 'error': 'Request timeout'}
                time.sleep(2 ** attempt)
            except Exception as e:
                if attempt == retries - 1:
                    return {'success': False, 'error': str(e)}
                time.sleep(2 ** attempt)

        return {'success': False, 'error': f'Failed after {retries} attempts'}

    def create_calendar_event(self, payload):
        """Create a calendar event (appointment/showing)"""
        logger.info(f"Creating calendar event: {payload.get('title')}")
        return self._call_skill(
            'POST',
            '/skills/calendar/create_event',
            payload
        )

    def get_availability(self, agent_id, date, duration_minutes=30):
        """Check agent availability for a given date"""
        logger.info(f"Checking availability for {agent_id} on {date}")
        endpoint = f'/skills/calendar/availability?agent_id={agent_id}&date={date}&duration_minutes={duration_minutes}'
        return self._call_skill('GET', endpoint)

    def create_lead(self, payload):
        """Create a new lead in CRM"""
        logger.info(f"Creating lead: {payload.get('name')}")
        return self._call_skill(
            'POST',
            '/skills/crm/create_lead',
            payload
        )

    def log_activity(self, payload):
        """Log an activity (call, message, email) in CRM"""
        logger.info(f"Logging activity: {payload.get('activity_type')}")
        return self._call_skill(
            'POST',
            '/skills/crm/log_activity',
            payload
        )

    def send_email(self, payload):
        """Send an email via Send skill"""
        logger.info(f"Sending email to {payload.get('to')}")
        return self._call_skill(
            'POST',
            '/skills/send/email',
            payload
        )

    def health_check(self):
        """Check if Skill Bridge is alive"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
