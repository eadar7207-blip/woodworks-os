# AI Voice Receptionist Architecture

## Overview
A Claude-powered voice receptionist system for real estate agents. Handles inbound calls, schedules appointments, takes messages, qualifies leads, and answers property questions. Integrates with Eitan's automation framework.

## System Pipeline

```
Phone Call (Twilio)
  ↓
Transcription (Whisper)
  ↓
Claude Decision Engine
  ├─ Intent Detection
  ├─ Context Extraction
  └─ Action Selection
  ↓
Action Execution
  ├─ Calendar Skill (schedule appointment)
  ├─ CRM Skill (log lead, take message)
  ├─ Property Lookup (answer questions)
  └─ Lead Qualification (score prospect)
  ↓
Response Generation (Claude)
  ↓
Text-to-Speech (ElevenLabs)
  ↓
Play Back to Caller
```

## Core Components

### 1. Voice Processing Engine
- **Input:** Twilio webhook with recorded audio
- **Transcription:** OpenAI Whisper API
- **Language Model:** Claude 3.5 Sonnet
- **Output:** JSON with detected intent, entities, confidence

### 2. Conversation Manager
Maintains call state across turns:
```
{
  "call_id": "uuid",
  "agent_id": "real_estate_agent_id",
  "contact": {
    "name": "string",
    "phone": "string",
    "email": "string"
  },
  "conversation_history": [
    {"role": "receptionist", "content": "..."},
    {"role": "caller", "content": "..."}
  ],
  "intent": "schedule_appointment | take_message | answer_question | qualify_lead",
  "entities": {
    "property_address": "string",
    "appointment_type": "open_house | showing | consultation",
    "preferred_time": "string",
    "lead_score": "hot | warm | cold"
  },
  "state": "greeting | gathering_info | confirming | closing",
  "started_at": "ISO8601",
  "last_activity": "ISO8601"
}
```

### 3. Real Estate Decision Engine
Claude system prompt trained on:
- Common real estate inquiries (property info, availability, pricing)
- Lead qualification criteria (motivation, timeline, budget)
- Appointment scheduling preferences (types, availability)
- Message protocols (urgent vs. routine)

Flows:
- **Appointment Scheduling:** Gather time preference → check calendar (Calendar skill) → confirm → send email
- **Message Taking:** Get caller info → transcribe message → log to CRM → notify agent
- **Lead Qualification:** Ask 3-5 questions → score likelihood → log with high/medium/low priority
- **Property Questions:** Answer from property DB or offer showing → capture intent

### 4. Integration Layer
HTTP calls to existing automation framework:

**Calendar Skill (localhost:5000/skill/calendar)**
```json
{
  "action": "create_event",
  "title": "Property Showing - 123 Oak St",
  "start_time": "2026-06-10T14:00:00Z",
  "end_time": "2026-06-10T15:00:00Z",
  "attendee_email": "buyer@example.com",
  "location": "123 Oak St, Chicago IL"
}
```

**CRM Skill (localhost:5000/skill/crm)**
```json
{
  "action": "log_activity | create_lead",
  "lead_name": "John Doe",
  "phone": "555-0123",
  "email": "john@example.com",
  "activity_type": "call | message | voicemail",
  "notes": "Interested in 3BR homes on North Shore",
  "priority": "hot | warm | cold"
}
```

**Calendar Check (localhost:5000/skill/calendar)**
```json
{
  "action": "get_availability",
  "agent_id": "sohail_123",
  "date": "2026-06-10",
  "duration_minutes": 30
}
```

### 5. Call State Machine

```
START
  ↓
GREETING (play welcome message)
  ↓
[User responds]
  ↓
INTENT DETECTION (Claude analyzes input)
  ├─ SCHEDULE_APPOINTMENT → GATHER_TIME → CHECK_CALENDAR → CONFIRM → BOOK
  ├─ TAKE_MESSAGE → GATHER_INFO → TRANSCRIBE → LOG_CRM → CLOSE
  ├─ PROPERTY_QUESTION → ANSWER → OFFER_SHOWING → LOG_LEAD → CLOSE
  └─ LEAD_QUALIFICATION → ASK_3_QUESTIONS → SCORE → LOG_CRM → CLOSE
  ↓
CLOSING (confirm action, offer follow-up)
  ↓
END

TRANSITIONS:
- Caller interrupts: return to relevant step
- Confusion (low confidence): ask clarifying question
- Escalation needed: transfer to agent voicemail or queue
```

### 6. Data Storage (SQLite)

**Calls Table**
```sql
CREATE TABLE calls (
  call_id TEXT PRIMARY KEY,
  agent_id TEXT,
  caller_name TEXT,
  caller_phone TEXT,
  caller_email TEXT,
  intent TEXT,
  outcome TEXT,
  duration_seconds INTEGER,
  recorded_url TEXT,
  transcript TEXT,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE TABLE appointments_scheduled (
  id TEXT PRIMARY KEY,
  call_id TEXT,
  property_address TEXT,
  appointment_type TEXT,
  scheduled_time TIMESTAMP,
  attendee_email TEXT,
  confirmed BOOLEAN,
  FOREIGN KEY(call_id) REFERENCES calls(call_id)
);

CREATE TABLE leads_captured (
  id TEXT PRIMARY KEY,
  call_id TEXT,
  lead_name TEXT,
  phone TEXT,
  email TEXT,
  lead_score TEXT,
  property_interest TEXT,
  timeline TEXT,
  budget TEXT,
  notes TEXT,
  logged_to_crm BOOLEAN,
  created_at TIMESTAMP,
  FOREIGN KEY(call_id) REFERENCES calls(call_id)
);
```

## Real Estate Scenarios

### Scenario 1: Appointment Scheduling
```
Receptionist: "Hi! Thanks for calling. Are you looking to schedule a showing?"
Caller: "Yes, I'm interested in the property on Oak Street"
Receptionist: "Great! I have that listing available. What day works best for you?"
Caller: "Friday afternoon"
[Claude checks calendar via Calendar skill]
Receptionist: "I have openings at 2 PM or 4 PM. Which works better?"
Caller: "2 PM"
[Claude creates calendar event + sends confirmation email via Calendar skill]
Receptionist: "Perfect! I've scheduled your showing for Friday at 2 PM. You'll get a confirmation email. See you then!"
```

### Scenario 2: Lead Qualification
```
Receptionist: "Hi! What brings you in today?"
Caller: "I'm thinking about selling my condo"
[Claude enters qualification mode]
Receptionist: "That's great! A few quick questions... What's your timeline for selling?"
Caller: "Probably within 3 months"
Receptionist: "And have you lived in your current place long?"
Caller: "5 years, it's in Lincoln Park"
[Claude scores lead as WARM, logs to CRM]
Receptionist: "Perfect. We'd love to discuss your options. Can I have your email so we can send you some information?"
```

### Scenario 3: Message Taking
```
Receptionist: "Hi there! How can I help?"
Caller: "I'd like to leave a message for Sohail about the listing at 200 North Ave"
Receptionist: "Of course! Can I get your name and phone number?"
[Claude logs message + caller info to CRM with URGENT flag]
Receptionist: "Got it. I've logged your message and Sohail will get back to you shortly."
```

## Integration Points

| Function | Skill | Endpoint | Auth |
|----------|-------|----------|------|
| Schedule appointment | Calendar | POST /skill/calendar | API key |
| Check availability | Calendar | GET /skill/calendar/availability | API key |
| Log lead | CRM | POST /skill/crm/lead | API key |
| Log activity | CRM | POST /skill/crm/activity | API key |
| Send email | Send | POST /skill/send | API key |
| Get property info | (custom DB) | GET /properties | API key |

## Deployment Model

### Development/Demo
- Runs locally in Flask (localhost:5000)
- Simulated voice input (text → Claude → TTS)
- Connected to real Skill Bridge (localhost:9000)
- SQLite database for call logging

### Production
- Twilio webhooks receive real phone calls
- Whisper transcription (real-time or async)
- Same Claude logic
- Same skill integration
- Hosted on server (systemd service or cloud)

## Security & Privacy

- All API calls to skills authenticated with API keys
- Call recordings stored with caller consent
- Transcripts stored encrypted
- PII (names, emails, phone) marked as sensitive
- Audit log for all CRM/calendar actions

## Success Metrics

1. **Call Completion Rate:** % of calls that end with intended action (appointment booked, message taken, lead logged)
2. **Accuracy:** % of lead scoring that matches human agent assessment
3. **Speed:** Average call duration (target: 2-5 minutes)
4. **Integration Success:** % of skill invocations that succeed (target: >95%)
5. **Customer Satisfaction:** Agent feedback on lead quality and appointment booking accuracy
