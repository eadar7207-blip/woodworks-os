"""
Tests for Skill Bridge HTTP client
Uses mocking to avoid real HTTP calls
"""

import pytest
from unittest.mock import patch, MagicMock
from voice_receptionist.skill_client import SkillBridgeClient


@pytest.fixture
def client():
    return SkillBridgeClient()


def test_client_initialization(client):
    """Test client initializes correctly"""
    assert client.base_url == 'http://localhost:9000'
    assert client.timeout == 10


def test_create_calendar_event_success(client):
    """Test successful calendar event creation"""
    mock_response = {
        'success': True,
        'event_id': 'evt_123',
        'calendar_link': 'https://calendar.google.com/event'
    }

    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = client.create_calendar_event({
            'title': 'Property Showing',
            'start_time': '2026-06-10T14:00:00Z',
            'end_time': '2026-06-10T14:30:00Z'
        })

        assert result['success'] is True
        assert result['event_id'] == 'evt_123'


def test_create_lead_success(client):
    """Test successful lead creation"""
    mock_response = {
        'success': True,
        'lead_id': 'lead_123',
        'crm_url': 'https://crm.app/leads/123'
    }

    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = client.create_lead({
            'name': 'John Smith',
            'phone': '312-555-0123',
            'email': 'john@example.com'
        })

        assert result['success'] is True
        assert result['lead_id'] == 'lead_123'


def test_log_activity_success(client):
    """Test successful activity logging"""
    mock_response = {
        'success': True,
        'activity_id': 'act_456'
    }

    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = client.log_activity({
            'lead_id': 'lead_123',
            'activity_type': 'call',
            'notes': 'Interested in 3BR homes'
        })

        assert result['success'] is True


def test_send_email_success(client):
    """Test successful email sending"""
    mock_response = {
        'success': True,
        'message_id': 'msg_789'
    }

    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = client.send_email({
            'to': 'test@example.com',
            'subject': 'Confirmation'
        })

        assert result['success'] is True


def test_get_availability_success(client):
    """Test checking agent availability"""
    mock_response = {
        'agent_id': 'sohail_123',
        'available_slots': [
            {'start': '14:00', 'end': '14:30'},
            {'start': '15:00', 'end': '15:30'}
        ]
    }

    with patch('voice_receptionist.skill_client.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = client.get_availability('sohail_123', '2026-06-10')

        assert 'available_slots' in result
        assert len(result['available_slots']) == 2


def test_skill_call_retry_on_503(client):
    """Test retry logic on 503 error"""
    mock_response_fail = MagicMock()
    mock_response_fail.status_code = 503

    mock_response_success = MagicMock()
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {'success': True}

    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        # First call fails, second succeeds
        mock_post.side_effect = [mock_response_fail, mock_response_success]

        with patch('voice_receptionist.skill_client.time.sleep'):
            result = client._call_skill('POST', '/test', {'data': 'test'}, retries=2)

        assert result['success'] is True


def test_skill_call_timeout_handling(client):
    """Test timeout handling"""
    with patch('voice_receptionist.skill_client.requests.post') as mock_post:
        mock_post.side_effect = TimeoutError('Connection timeout')

        result = client._call_skill('POST', '/test', {'data': 'test'}, retries=1)

        assert result['success'] is False
        assert 'error' in result


def test_health_check_success(client):
    """Test health check endpoint"""
    with patch('voice_receptionist.skill_client.requests.get') as mock_get:
        mock_get.return_value.status_code = 200

        is_healthy = client.health_check()

        assert is_healthy is True


def test_health_check_failure(client):
    """Test health check when service is down"""
    with patch('voice_receptionist.skill_client.requests.get') as mock_get:
        mock_get.side_effect = Exception('Connection refused')

        is_healthy = client.health_check()

        assert is_healthy is False
