#!/bin/bash
# Voice Receptionist Skill - Demo Mode (works without API keys)

CALLER_MESSAGE="$1"

if [ -z "$CALLER_MESSAGE" ]; then
    echo '{"error": "No caller message provided"}'
    exit 1
fi

# Pass message to Python and run demo
python3 -c "
import json
import uuid
from datetime import datetime

caller_message = '''$CALLER_MESSAGE'''

def detect_intent_and_respond(message):
    msg_lower = message.lower()
    call_id = f'skill_{uuid.uuid4().hex[:8]}'

    # Schedule appointment
    if any(word in msg_lower for word in ['schedule', 'showing', 'viewing', 'see the property', 'property', 'friday', 'afternoon', 'morning', 'oak street']):
        return {
            'call_id': call_id,
            'intent': 'schedule_appointment',
            'receptionist': 'Perfect! I\\'d love to help you schedule a showing for the Oak Street property. Friday afternoon works great. I have 2 PM or 4 PM available. Which time works better for you?',
            'entities': {
                'property_address': '123 Oak St',
                'preferred_time': 'Friday afternoon'
            },
            'action': {'type': 'schedule_appointment', 'status': 'pending_confirmation'},
            'confidence': 0.95
        }

    # Qualify lead
    elif any(word in msg_lower for word in ['selling', 'list', 'interested in selling', 'sell my', 'condo', 'house', 'property']):
        return {
            'call_id': call_id,
            'intent': 'qualify_lead',
            'receptionist': 'That\\'s fantastic! I\\'d like to ask you a few quick questions to see if now is a good time. How many bedrooms and bathrooms does your property have?',
            'entities': {
                'lead_type': 'seller',
                'lead_score': 'warm'
            },
            'action': {'type': 'create_lead', 'status': 'initiated'},
            'confidence': 0.92
        }

    # Take message
    elif any(word in msg_lower for word in ['message', 'leave a message', 'call me back', 'get back']):
        return {
            'call_id': call_id,
            'intent': 'take_message',
            'receptionist': 'Of course! I\\'d be happy to take a message for Sohail. Can I get your name and phone number please?',
            'entities': {
                'message_for': 'Sohail'
            },
            'action': {'type': 'log_activity', 'status': 'pending_info'},
            'confidence': 0.93
        }

    # Default greeting
    else:
        return {
            'call_id': call_id,
            'intent': 'greeting',
            'receptionist': 'Thank you for calling! Are you interested in scheduling a showing, learning about selling your property, or something else?',
            'entities': {},
            'action': {'type': 'none'},
            'confidence': 0.50
        }

# Get response
result = detect_intent_and_respond(caller_message)
result['mode'] = 'demo'
result['timestamp'] = datetime.utcnow().isoformat()
result['caller_input'] = caller_message

print(json.dumps(result, indent=2))
"
