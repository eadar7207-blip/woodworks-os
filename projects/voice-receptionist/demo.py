#!/usr/bin/env python3
"""
Text-based demo of AI voice receptionist
Runs 3 scenarios without requiring real Twilio or Anthropic API calls
"""

import json
import uuid
from datetime import datetime
from voice_receptionist.conversation import ConversationManager
from voice_receptionist.database import Database

# Mock Skill Bridge responses (simulates real API calls)
class MockSkillBridge:
    @staticmethod
    def create_calendar_event(payload):
        return {
            'success': True,
            'event_id': f"evt_{uuid.uuid4().hex[:8]}",
            'calendar_link': 'https://calendar.google.com/event/123',
            'confirmation_sent': True
        }

    @staticmethod
    def create_lead(payload):
        return {
            'success': True,
            'lead_id': f"lead_{uuid.uuid4().hex[:8]}",
            'crm_url': 'https://crm.app/leads/456'
        }

    @staticmethod
    def log_activity(payload):
        return {
            'success': True,
            'activity_id': f"act_{uuid.uuid4().hex[:8]}"
        }


class VoiceReceptionistDemo:
    def __init__(self):
        import tempfile
        # Create temporary database file for demo
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db = Database(db_path=self.temp_db.name)
        self.conversation_mgr = ConversationManager()
        self.skill_bridge = MockSkillBridge()

    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")

    def print_message(self, role, content):
        prefix = "👤 Caller: " if role == 'caller' else "🤖 Receptionist: "
        print(f"{prefix}{content}\n")

    def simulate_call(self, agent_id, scenario):
        """Simulate a complete call"""
        call_id = f"demo_call_{uuid.uuid4().hex[:8]}"

        # Initialize call state
        call_state = {
            'call_id': call_id,
            'agent_id': agent_id,
            'conversation_history': [],
            'state': 'greeting',
            'intent': None,
            'entities': {},
            'started_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat()
        }

        self.db.create_call(call_state)
        self.conversation_mgr.set_call_state(call_id, call_state)

        # Start with greeting
        greeting = "Hi! Thanks for calling. How can I help you today?"
        self.print_message('receptionist', greeting)

        # Run scenario
        if scenario == 'appointment':
            self.scenario_appointment(call_state, agent_id)
        elif scenario == 'qualification':
            self.scenario_lead_qualification(call_state, agent_id)
        elif scenario == 'message':
            self.scenario_message(call_state, agent_id)

        # End call
        call_state['completed_at'] = datetime.utcnow().isoformat()
        self.db.update_call(call_id, call_state)
        self.conversation_mgr.delete_call_state(call_id)

        print(f"\n✅ Call ended. Duration: {call_state.get('duration_seconds', 0)}s")
        print(f"Intent detected: {call_state.get('intent')}")

        return call_id

    def scenario_appointment(self, call_state, agent_id):
        """Scenario 1: Schedule an appointment"""
        print("\n--- Scenario: Appointment Scheduling ---\n")

        # Caller wants to schedule
        caller_msg = "Hi, I'd like to see the property on Oak Street. I've been interested in that neighborhood for a while."
        self.print_message('caller', caller_msg)

        # Claude detects: schedule_appointment
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg)
        call_state['intent'] = 'schedule_appointment'
        call_state['state'] = 'gathering_info'

        response1 = "Perfect! I'd love to help you schedule a showing for 123 Oak Street. That's a beautiful 3-bedroom property. What day would work best for you?"
        self.print_message('receptionist', response1)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response1)

        # Caller responds with time preference
        caller_msg2 = "Friday afternoon would be great."
        self.print_message('caller', caller_msg2)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg2)

        # Check availability
        response2 = "Great! I have a couple of slots available on Friday. How about 2:00 PM or 4:00 PM?"
        self.print_message('receptionist', response2)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response2)

        # Caller picks time
        caller_msg3 = "2 PM sounds perfect."
        self.print_message('caller', caller_msg3)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg3)

        # Create appointment
        calendar_result = self.skill_bridge.create_calendar_event({
            'title': 'Property Showing - 123 Oak St',
            'start_time': '2026-06-13T14:00:00Z',
            'end_time': '2026-06-13T14:30:00Z',
            'property_address': '123 Oak St, Chicago'
        })

        call_state['state'] = 'confirming'
        response3 = "Excellent! I've scheduled your showing for Friday, June 13th at 2:00 PM at 123 Oak Street. You'll receive a confirmation email shortly. Is there anything else you'd like to know about the property?"
        self.print_message('receptionist', response3)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response3)

        # Closing
        caller_msg4 = "No, that's all. Thanks!"
        self.print_message('caller', caller_msg4)

        response4 = "Great! See you Friday at 2 PM. Have a wonderful day!"
        self.print_message('receptionist', response4)

    def scenario_lead_qualification(self, call_state, agent_id):
        """Scenario 2: Qualify a lead"""
        print("\n--- Scenario: Lead Qualification ---\n")

        caller_msg = "Hi, I'm thinking about selling my condo in Lincoln Park. Do you think this is a good time to list?"
        self.print_message('caller', caller_msg)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg)

        call_state['intent'] = 'qualify_lead'
        call_state['state'] = 'gathering_info'

        response1 = "That's great! Lincoln Park is a fantastic area. Let me ask you a few quick questions to see if now is a good time to sell. How many bedrooms and bathrooms do you have?"
        self.print_message('receptionist', response1)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response1)

        caller_msg2 = "It's a 2 bed, 2 bath corner unit. I've owned it for 5 years."
        self.print_message('caller', caller_msg2)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg2)

        response2 = "Nice! Corner units are very desirable. And what's your timeline for selling? Are you in a hurry or flexible?"
        self.print_message('receptionist', response2)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response2)

        caller_msg3 = "I'd like to sell within 3 months. I'm relocating for work."
        self.print_message('caller', caller_msg3)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg3)

        response3 = "Understood. That's a reasonable timeline. Just one more question—what price range are you hoping to get?"
        self.print_message('receptionist', response3)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response3)

        caller_msg4 = "I'm thinking around $600K. The market seems strong right now."
        self.print_message('caller', caller_msg4)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg4)

        # Create lead in CRM
        lead_result = self.skill_bridge.create_lead({
            'name': 'Sarah Johnson',
            'phone': '312-555-0123',
            'email': 'sarah@example.com',
            'source': 'voice_receptionist',
            'lead_score': 'hot',  # Clear timeline + known property type
            'property_interest': '2BR condo, Lincoln Park',
            'timeline': '3 months',
            'budget': '$600K',
            'notes': 'Relocating for work. Motivated seller.'
        })

        call_state['state'] = 'confirming'
        call_state['entities']['lead_score'] = 'hot'

        response4 = "Perfect! Based on what you've told me, this sounds like a great time to sell. I'm logging your information and Sohail, one of our top agents, will give you a call within the hour to discuss a marketing strategy. Does that work?"
        self.print_message('receptionist', response4)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response4)

        caller_msg5 = "Great, I'll expect his call."
        self.print_message('caller', caller_msg5)

        response5 = "Wonderful! Thanks for calling. Talk soon!"
        self.print_message('receptionist', response5)

    def scenario_message(self, call_state, agent_id):
        """Scenario 3: Take a message"""
        print("\n--- Scenario: Message Taking ---\n")

        caller_msg = "Hi, I'd like to leave a message for Sohail about the listing on Oak Street."
        self.print_message('caller', caller_msg)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg)

        call_state['intent'] = 'take_message'
        call_state['state'] = 'gathering_info'

        response1 = "Of course! I'd be happy to help. Can I get your name first?"
        self.print_message('receptionist', response1)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'receptionist', response1)

        caller_msg2 = "It's Mike Thompson."
        self.print_message('caller', caller_msg2)

        response2 = "Thanks, Mike. And what's the best phone number to reach you?"
        self.print_message('receptionist', response2)

        caller_msg3 = "312-555-4567"
        self.print_message('caller', caller_msg3)

        response3 = "Got it. And what's your message for Sohail?"
        self.print_message('receptionist', response3)

        caller_msg4 = "I'm very interested in the 3 bedroom property at 123 Oak Street. We drove by it yesterday and loved the location. Please have him call me back with more information and pricing."
        self.print_message('caller', caller_msg4)
        self.conversation_mgr.append_to_history(call_state['call_id'], 'caller', caller_msg4)

        # Log activity in CRM
        activity_result = self.skill_bridge.log_activity({
            'lead_id': None,
            'activity_type': 'voicemail',
            'title': 'Interested in 123 Oak Street',
            'notes': 'Caller interested in 3BR property, drove by, wants pricing info',
            'priority': 'high'
        })

        call_state['state'] = 'closing'

        response4 = "Perfect! I've logged your message. Sohail will get back to you as soon as possible, usually within a few hours. Thanks for calling!"
        self.print_message('receptionist', response4)

    def print_statistics(self):
        """Print call statistics"""
        stats = self.db.get_stats()

        self.print_header("Call Statistics")
        print(f"Total calls: {stats['total_calls']}")
        print(f"Total leads captured: {stats['total_leads']}")
        print(f"Total appointments scheduled: {stats['total_appointments']}")
        if stats['avg_call_duration_seconds'] > 0:
            print(f"Average call duration: {stats['avg_call_duration_seconds']:.0f} seconds")


def main():
    demo = VoiceReceptionistDemo()

    demo.print_header("AI Voice Receptionist Demo")
    print("This demo shows the receptionist in action with 3 different scenarios.")
    print("No real Twilio, API calls, or transcription needed.\n")

    agent_id = "sohail_123"

    # Run 3 scenarios
    print("\n" + "="*60)
    print("SCENARIO 1: Appointment Scheduling")
    print("="*60)
    call1 = demo.simulate_call(agent_id, 'appointment')

    print("\n" + "="*60)
    print("SCENARIO 2: Lead Qualification")
    print("="*60)
    call2 = demo.simulate_call(agent_id, 'qualification')

    print("\n" + "="*60)
    print("SCENARIO 3: Message Taking")
    print("="*60)
    call3 = demo.simulate_call(agent_id, 'message')

    # Show stats
    demo.print_statistics()

    print("\n" + "="*60)
    print("✅ Demo Complete")
    print("="*60)
    print(f"""
The receptionist handled:
  ✓ Appointment scheduling (checked availability, booked time)
  ✓ Lead qualification (asked questions, scored as 'hot')
  ✓ Message taking (captured info, logged to CRM)

In production:
  - Real Twilio phone integration
  - Real Claude API for NLU
  - Real Skill Bridge API calls to automation framework
  - ElevenLabs voice synthesis
  - Database persistence to PostgreSQL

See README.md for next steps.
    """)


if __name__ == '__main__':
    main()
