"""
Tests for database operations
"""

import pytest
from datetime import datetime


def test_create_call(test_db, sample_call_state):
    """Test creating a call record"""
    test_db.create_call(sample_call_state)

    call = test_db.get_call(sample_call_state['call_id'])
    assert call is not None
    assert call['call_id'] == sample_call_state['call_id']
    assert call['agent_id'] == 'sohail_123'


def test_update_call(test_db, sample_call_state):
    """Test updating a call record"""
    test_db.create_call(sample_call_state)

    sample_call_state['intent'] = 'schedule_appointment'
    sample_call_state['state'] = 'confirming'
    sample_call_state['completed_at'] = '2026-06-10T10:05:00Z'

    test_db.update_call(sample_call_state['call_id'], sample_call_state)

    call = test_db.get_call(sample_call_state['call_id'])
    assert call['intent'] == 'schedule_appointment'
    assert call['duration_seconds'] == 300  # 5 minutes


def test_get_calls(test_db, sample_call_state):
    """Test retrieving calls list"""
    # Create 3 calls
    for i in range(3):
        call = sample_call_state.copy()
        call['call_id'] = f'call_{i}'
        test_db.create_call(call)

    calls = test_db.get_calls(limit=10)
    assert len(calls) == 3


def test_get_calls_by_agent(test_db):
    """Test retrieving calls filtered by agent"""
    call1 = {
        'call_id': 'call_1',
        'agent_id': 'sohail_123',
        'caller_phone': '+1-312-555-1234',
        'conversation_history': []
    }
    call2 = {
        'call_id': 'call_2',
        'agent_id': 'other_agent',
        'caller_phone': '+1-312-555-5678',
        'conversation_history': []
    }

    test_db.create_call(call1)
    test_db.create_call(call2)

    sohail_calls = test_db.get_calls(agent_id='sohail_123')
    assert len(sohail_calls) == 1
    assert sohail_calls[0]['agent_id'] == 'sohail_123'


def test_create_lead(test_db, sample_lead):
    """Test creating a lead record"""
    test_db.create_lead(sample_lead)

    # Verify by checking stats
    stats = test_db.get_stats()
    assert stats['total_leads'] == 1


def test_create_appointment(test_db, sample_appointment):
    """Test creating an appointment record"""
    test_db.create_appointment(sample_appointment)

    # Verify by checking stats
    stats = test_db.get_stats()
    assert stats['total_appointments'] == 1


def test_get_stats(test_db, sample_call_state, sample_lead, sample_appointment):
    """Test statistics aggregation"""
    test_db.create_call(sample_call_state)
    test_db.create_lead(sample_lead)
    test_db.create_appointment(sample_appointment)

    stats = test_db.get_stats()

    assert stats['total_calls'] == 1
    assert stats['total_leads'] == 1
    assert stats['total_appointments'] == 1
    assert 'timestamp' in stats


def test_db_initialization(test_db):
    """Test that database initializes with correct schema"""
    # Try to create records to verify tables exist
    test_db.create_call({
        'call_id': 'test',
        'agent_id': 'test',
        'caller_phone': 'test',
        'conversation_history': []
    })

    stats = test_db.get_stats()
    assert stats['total_calls'] == 1
