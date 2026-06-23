"""
Claude-based decision engine for voice receptionist
Handles intent detection, entity extraction, and action generation
"""

import os
import json
import logging
from anthropic import Anthropic

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI receptionist for a real estate agency. Your job is to handle incoming calls professionally and efficiently.

Your capabilities:
1. Schedule property showings and appointments
2. Take messages for agents
3. Qualify leads by asking about their needs, timeline, and budget
4. Answer basic questions about properties
5. Forward appropriate information to agents

Your constraints:
- Be friendly but professional
- Keep responses concise (under 2 minutes of speech)
- Ask for caller name and phone number early
- Don't make promises about prices or terms
- Escalate complex questions to the agent

When you respond, format your answer as JSON with:
{
    "intent": "schedule_appointment|take_message|qualify_lead|answer_question|greeting|farewell",
    "state": "gathering_info|confirming|closing|error",
    "response": "What you should say to the caller",
    "action": {
        "type": "schedule_appointment|create_lead|log_activity|send_email|none",
        "payload": {...}
    },
    "entities": {
        "caller_name": "string or null",
        "caller_email": "string or null",
        "property_address": "string or null",
        "appointment_type": "open_house|showing|consultation|string",
        "preferred_time": "string or ISO datetime or null",
        "lead_score": "hot|warm|cold or null"
    },
    "confidence": 0.0-1.0
}

Real estate context:
- Common properties: 123 Oak St (3BR, $450k), 456 Lake Ave (2BR, $350k), 789 Park Place (4BR, $550k)
- Lead scoring: Hot = ready to act soon, Warm = interested but flexible timeline, Cold = early stage
- Showing types: Open house (group), Private showing (scheduled), Virtual tour, Consultation
- Business hours: Mon-Fri 9am-5pm, Sat 10am-2pm, closed Sun"""


class ClaudeDecisionEngine:
    """Claude-powered decision engine for receptionist"""

    def __init__(self):
        self.client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_context = {}

    def process(self, call_state, caller_input):
        """
        Process caller input and generate decision.

        Args:
            call_state: Dict with call context (id, history, entities, etc.)
            caller_input: String with caller's message

        Returns:
            Dict with intent, response, action, entities, etc.
        """
        call_id = call_state.get('call_id')
        conversation_history = call_state.get('conversation_history', [])

        # Build conversation for Claude
        messages = self._format_messages(conversation_history, caller_input)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=messages
            )

            response_text = response.content[0].text

            # Parse Claude's JSON response
            decision = self._parse_response(response_text)

            logger.info(f"Claude decision for {call_id}: {decision.get('intent')}")

            return decision

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            return {
                'intent': 'error',
                'response': "I'm having trouble understanding. Can you try again?",
                'action': {'type': 'none'},
                'entities': {},
                'confidence': 0.0
            }

    def _format_messages(self, history, new_input):
        """Format conversation history for Claude API"""
        messages = []

        # Add conversation history
        for msg in history:
            messages.append({
                'role': msg['role'] if msg['role'] == 'user' else 'assistant',
                'content': msg['content']
            })

        # Add current user input
        messages.append({
            'role': 'user',
            'content': new_input
        })

        return messages

    def _parse_response(self, response_text):
        """Parse Claude's JSON response"""
        try:
            # Try to extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                decision = json.loads(json_str)
                return decision
            else:
                # If no JSON found, return error
                return {
                    'intent': 'error',
                    'response': response_text,
                    'action': {'type': 'none'},
                    'entities': {},
                    'confidence': 0.0
                }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            return {
                'intent': 'error',
                'response': "I'm having trouble processing that.",
                'action': {'type': 'none'},
                'entities': {},
                'confidence': 0.0
            }

    def reset_context(self, call_id):
        """Reset conversation context for a call"""
        if call_id in self.conversation_context:
            del self.conversation_context[call_id]
