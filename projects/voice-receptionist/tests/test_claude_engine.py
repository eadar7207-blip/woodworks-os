"""
Tests for Claude decision engine
"""

import pytest
from voice_receptionist.claude_engine import ClaudeDecisionEngine


@pytest.fixture
def engine():
    return ClaudeDecisionEngine()


@pytest.fixture
def sample_call_state():
    return {
        'call_id': 'test_call_123',
        'agent_id': 'sohail_123',
        'conversation_history': [
            {
                'role': 'receptionist',
                'content': 'Hi! How can I help you today?'
            }
        ]
    }


def test_engine_initialization(engine):
    """Test engine initializes correctly"""
    assert engine is not None
    assert engine.model == "claude-3-5-sonnet-20241022"


def test_parse_response_valid_json(engine):
    """Test parsing valid JSON response"""
    response_text = '{"intent": "schedule_appointment", "response": "test"}'
    result = engine._parse_response(response_text)

    assert result['intent'] == 'schedule_appointment'
    assert result['response'] == 'test'


def test_parse_response_invalid_json(engine):
    """Test handling of invalid JSON"""
    response_text = 'This is not JSON'
    result = engine._parse_response(response_text)

    assert result['intent'] == 'error'
    assert result['success'] is False or 'error' in result


def test_format_messages(engine, sample_call_state):
    """Test message formatting for Claude"""
    messages = engine._format_messages(
        sample_call_state['conversation_history'],
        'I want to schedule a showing'
    )

    assert len(messages) == 2
    assert messages[0]['role'] == 'assistant'
    assert messages[1]['role'] == 'user'
    assert 'schedule' in messages[1]['content']


def test_context_reset(engine):
    """Test conversation context reset"""
    engine.conversation_context['call_123'] = {'test': 'data'}
    engine.reset_context('call_123')

    assert 'call_123' not in engine.conversation_context
