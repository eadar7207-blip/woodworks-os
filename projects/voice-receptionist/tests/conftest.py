"""
Pytest configuration and fixtures for voice receptionist tests
"""

import pytest
import os
import tempfile
from voice_receptionist.database import Database


@pytest.fixture
def test_db():
    """Create a temporary test database"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    db = Database(db_path=db_path)
    yield db

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def sample_call_state():
    """Sample call state for testing"""
    return {
        'call_id': 'test_call_123',
        'call_sid': 'CA1234567890',
        'agent_id': 'sohail_123',
        'caller_phone': '+1-312-555-1234',
        'conversation_history': [
            {'role': 'receptionist', 'content': 'Hi! How can I help you today?'}
        ],
        'state': 'gathering_info',
        'intent': None,
        'entities': {},
        'started_at': '2026-06-10T10:00:00Z',
        'last_activity': '2026-06-10T10:00:00Z'
    }


@pytest.fixture
def sample_lead():
    """Sample lead data for testing"""
    return {
        'id': 'lead_abc123',
        'call_id': 'test_call_123',
        'lead_name': 'John Smith',
        'phone': '312-555-0123',
        'email': 'john@example.com',
        'lead_score': 'warm',
        'property_interest': '3 bed homes on North Shore',
        'timeline': '3 months',
        'budget': '400000-500000',
        'notes': 'Interested in Lake View area'
    }


@pytest.fixture
def sample_appointment():
    """Sample appointment data for testing"""
    return {
        'id': 'apt_xyz789',
        'call_id': 'test_call_123',
        'property_address': '123 Oak St, Chicago, IL',
        'appointment_type': 'showing',
        'scheduled_time': '2026-06-10T14:00:00Z',
        'attendee_email': 'buyer@example.com',
        'attendee_name': 'John Smith',
        'confirmed': True
    }
