#!/usr/bin/env python3
"""
AI Voice Receptionist for Real Estate Agents
Main Flask application server
"""

import os
import json
import uuid
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

try:
    from twilio.rest import Client as TwilioClient
    from twilio.twiml.voice_response import VoiceResponse
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

from voice_receptionist.conversation import ConversationManager
from voice_receptionist.claude_engine import ClaudeDecisionEngine
from voice_receptionist.skill_client import SkillBridgeClient
from voice_receptionist.database import Database
from voice_receptionist.tts import TextToSpeechEngine

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

db = Database()
conversation_mgr = ConversationManager()
try:
    claude_engine = ClaudeDecisionEngine()
except Exception as e:
    logger.error(f"Claude initialization failed: {e}")
    claude_engine = None
skill_client = SkillBridgeClient()
try:
    tts_engine = TextToSpeechEngine()
except Exception as e:
    logger.error(f"TTS initialization failed: {e}")
    tts_engine = None


@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path}")


@app.after_request
def log_response(response):
    logger.info(f"{request.path} -> {response.status_code}")
    return response


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})


@app.route('/call/incoming', methods=['POST'])
def incoming_call():
    """
    Twilio webhook for incoming calls.
    Twilio sends form data (not JSON).
    """
    from twilio.twiml.voice_response import VoiceResponse

    call_sid = request.form.get('CallSid')
    caller_phone = request.form.get('From')

    logger.info(f"Incoming call {call_sid} from {caller_phone}")

    # Create Twilio response
    resp = VoiceResponse()

    # Start recording
    resp.record(timeout=60, max_speech_time=30, transcribe=False, action=f'/call/recording?CallSid={call_sid}')

    # Greeting
    resp.say("Hi! Thanks for calling. How can I help you today?", voice='alice')

    return str(resp)


@app.route('/call/start', methods=['POST'])
def start_call():
    """
    Start a new call. Called when Twilio routes an incoming call to us.

    Expected payload:
    {
        "agent_id": "sohail_123",
        "caller_phone": "+1-312-555-1234",
        "call_sid": "CA1234567890abcdef"
    }
    """
    data = request.get_json()
    call_id = str(uuid.uuid4())
    caller_phone = data.get('caller_phone', 'unknown')
    call_sid = data.get('call_sid')
    agent_id = data.get('agent_id')

    logger.info(f"Starting call {call_id} from {caller_phone}")

    # Initialize call state
    call_state = {
        'call_id': call_id,
        'call_sid': call_sid,
        'agent_id': agent_id,
        'caller_phone': caller_phone,
        'conversation_history': [],
        'state': 'greeting',
        'intent': None,
        'entities': {},
        'started_at': datetime.utcnow().isoformat(),
        'last_activity': datetime.utcnow().isoformat()
    }

    # Save to database
    db.create_call(call_state)
    conversation_mgr.set_call_state(call_id, call_state)

    # Generate greeting
    greeting = "Hi! Thanks for calling. How can I help you today?"
    tts_response = tts_engine.synthesize(greeting)

    return jsonify({
        'success': True,
        'call_id': call_id,
        'greeting': greeting,
        'audio_url': tts_response.get('audio_url'),
        'audio_base64': tts_response.get('audio_base64')
    })


@app.route('/call/<call_id>/message', methods=['POST'])
def process_message(call_id):
    """
    Process a message from the caller.

    Expected payload:
    {
        "transcript": "I'd like to schedule a showing",
        "audio_url": "https://..."  (optional, if speech-to-text not done yet)
    }
    """
    data = request.get_json()
    transcript = data.get('transcript')
    audio_url = data.get('audio_url')

    logger.info(f"Processing message for call {call_id}: {transcript}")

    call_state = conversation_mgr.get_call_state(call_id)
    if not call_state:
        return jsonify({'error': 'Call not found'}), 404

    # Add caller message to history
    call_state['conversation_history'].append({
        'role': 'caller',
        'content': transcript,
        'timestamp': datetime.utcnow().isoformat()
    })

    # Get Claude decision
    decision = claude_engine.process(call_state, transcript)

    logger.info(f"Claude decision for {call_id}: intent={decision.get('intent')}, action={decision.get('action')}")

    # Update call state with decision
    call_state['intent'] = decision.get('intent')
    call_state['state'] = decision.get('state', 'gathering_info')
    call_state['entities'].update(decision.get('entities', {}))

    # Execute action if needed
    action_result = None
    if decision.get('action'):
        action_result = execute_action(call_id, call_state, decision['action'])

    # Generate response
    response_text = decision.get('response', "I didn't catch that. Can you say that again?")

    # If action succeeded, include confirmation in response
    if action_result and action_result.get('success'):
        response_text = decision.get('response_success', response_text)

    # Add receptionist response to history
    call_state['conversation_history'].append({
        'role': 'receptionist',
        'content': response_text,
        'timestamp': datetime.utcnow().isoformat()
    })

    call_state['last_activity'] = datetime.utcnow().isoformat()

    # Synthesize response to speech
    tts_response = tts_engine.synthesize(response_text)

    # Update database
    db.update_call(call_id, call_state)
    conversation_mgr.set_call_state(call_id, call_state)

    return jsonify({
        'success': True,
        'call_id': call_id,
        'response': response_text,
        'audio_url': tts_response.get('audio_url'),
        'audio_base64': tts_response.get('audio_base64'),
        'intent': decision.get('intent'),
        'state': call_state['state'],
        'action_result': action_result
    })


def execute_action(call_id, call_state, action):
    """
    Execute an action based on Claude's decision.
    Actions include: schedule_appointment, log_lead, take_message, etc.
    """
    action_type = action.get('type')
    payload = action.get('payload', {})

    logger.info(f"Executing action for {call_id}: {action_type}")

    try:
        if action_type == 'schedule_appointment':
            return execute_schedule_appointment(call_id, call_state, payload)
        elif action_type == 'create_lead':
            return execute_create_lead(call_id, call_state, payload)
        elif action_type == 'log_activity':
            return execute_log_activity(call_id, call_state, payload)
        elif action_type == 'send_email':
            return execute_send_email(call_id, call_state, payload)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return {'success': False, 'error': 'Unknown action'}
    except Exception as e:
        logger.error(f"Action execution failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def execute_schedule_appointment(call_id, call_state, payload):
    """Schedule appointment via Calendar skill"""
    agent_id = call_state.get('agent_id')

    # Prepare request
    calendar_payload = {
        'title': payload.get('title', 'Property Showing'),
        'start_time': payload.get('start_time'),
        'end_time': payload.get('end_time'),
        'location': payload.get('location'),
        'attendee_email': payload.get('attendee_email'),
        'attendee_name': payload.get('attendee_name'),
        'property_address': payload.get('property_address'),
    }

    result = skill_client.create_calendar_event(calendar_payload)

    if result.get('success'):
        # Also send confirmation email
        email_payload = {
            'to': payload.get('attendee_email'),
            'subject': f"Showing Confirmed - {payload.get('property_address', 'Property')}",
            'template': 'appointment_confirmation',
            'data': {
                'property_address': payload.get('property_address'),
                'showing_time': payload.get('start_time'),
                'agent_name': payload.get('agent_name', 'Our Team'),
                'attendee_name': payload.get('attendee_name'),
            }
        }
        email_result = skill_client.send_email(email_payload)
        result['email_sent'] = email_result.get('success', False)

    return result


def execute_create_lead(call_id, call_state, payload):
    """Create lead via CRM skill"""
    crm_payload = {
        'name': payload.get('name'),
        'phone': payload.get('phone', call_state.get('caller_phone')),
        'email': payload.get('email'),
        'source': 'voice_receptionist',
        'property_interest': payload.get('property_interest'),
        'timeline': payload.get('timeline'),
        'budget': payload.get('budget'),
        'lead_score': payload.get('lead_score', 'warm'),
        'call_id': call_id,
        'notes': payload.get('notes'),
    }

    result = skill_client.create_lead(crm_payload)
    return result


def execute_log_activity(call_id, call_state, payload):
    """Log activity via CRM skill"""
    crm_payload = {
        'lead_id': payload.get('lead_id'),
        'activity_type': payload.get('activity_type', 'call'),
        'activity_date': datetime.utcnow().isoformat(),
        'title': payload.get('title'),
        'notes': payload.get('notes'),
        'priority': payload.get('priority', 'normal'),
        'call_id': call_id,
    }

    result = skill_client.log_activity(crm_payload)
    return result


def execute_send_email(call_id, call_state, payload):
    """Send email via Send skill"""
    result = skill_client.send_email(payload)
    return result


@app.route('/call/<call_id>/end', methods=['POST'])
def end_call(call_id):
    """End a call and save final state"""
    call_state = conversation_mgr.get_call_state(call_id)

    if not call_state:
        return jsonify({'error': 'Call not found'}), 404

    call_state['completed_at'] = datetime.utcnow().isoformat()
    call_state['duration_seconds'] = calculate_duration(
        call_state['started_at'],
        call_state['completed_at']
    )

    db.update_call(call_id, call_state)
    conversation_mgr.delete_call_state(call_id)

    logger.info(f"Call {call_id} ended. Duration: {call_state['duration_seconds']}s")

    return jsonify({
        'success': True,
        'call_id': call_id,
        'duration_seconds': call_state['duration_seconds'],
        'intent': call_state.get('intent'),
    })


@app.route('/call/<call_id>', methods=['GET'])
def get_call_state(call_id):
    """Get current state of a call"""
    call_state = conversation_mgr.get_call_state(call_id)

    if not call_state:
        return jsonify({'error': 'Call not found'}), 404

    return jsonify(call_state)


@app.route('/calls', methods=['GET'])
def list_calls():
    """List all calls with optional filtering"""
    agent_id = request.args.get('agent_id')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    calls = db.get_calls(agent_id=agent_id, limit=limit, offset=offset)

    return jsonify({
        'calls': calls,
        'count': len(calls),
        'limit': limit,
        'offset': offset
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get aggregated stats"""
    stats = db.get_stats()
    return jsonify(stats)


def calculate_duration(start_iso, end_iso):
    """Calculate duration in seconds between two ISO timestamps"""
    try:
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
        return int((end - start).total_seconds())
    except:
        return 0


if __name__ == '__main__':
    logger.info("Starting Voice Receptionist Server")
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5001)),
        debug=os.environ.get('DEBUG', 'False').lower() == 'true'
    )
