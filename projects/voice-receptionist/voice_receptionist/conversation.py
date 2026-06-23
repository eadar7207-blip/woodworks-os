"""
Conversation state management for voice calls
Maintains in-memory and persistent state
"""

import logging

logger = logging.getLogger(__name__)


class ConversationManager:
    """Manages conversation state for active calls"""

    def __init__(self):
        self.active_calls = {}

    def set_call_state(self, call_id, state):
        """Store call state in memory"""
        self.active_calls[call_id] = state
        logger.debug(f"Stored state for call {call_id}")

    def get_call_state(self, call_id):
        """Retrieve call state from memory"""
        return self.active_calls.get(call_id)

    def delete_call_state(self, call_id):
        """Remove call from memory (after call ends)"""
        if call_id in self.active_calls:
            del self.active_calls[call_id]
            logger.debug(f"Cleared state for call {call_id}")

    def get_active_calls(self):
        """Get all active calls"""
        return len(self.active_calls)

    def append_to_history(self, call_id, role, content):
        """Append message to call history"""
        call_state = self.get_call_state(call_id)
        if call_state:
            call_state['conversation_history'].append({
                'role': role,
                'content': content
            })
