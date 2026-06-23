# Integration with Eitan's Automation Framework

## Overview
The Voice Receptionist integrates with the existing automation framework via HTTP calls to the Skill Bridge API (localhost:9000) and Automation Executor (localhost:5000).

## Existing Framework Architecture

```
Voice Receptionist (Flask, :5001)
  ↓ (HTTP calls)
Skill Bridge API (localhost:9000)
  ↓ (invokes)
Claude Code Skills (prospect, crm, calendar, etc.)
  ↓
Automation Executor (localhost:5000)
  ↓
SQLite Database (.claude/automations/database.db)
```

## API Integration Points

### 1. Calendar Skill (Schedule Appointments)

**Create Event:**
```bash
curl -X POST http://localhost:9000/skills/calendar/create_event \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Property Showing - 123 Oak St",
    "start_time": "2026-06-10T14:00:00Z",
    "end_time": "2026-06-10T14:30:00Z",
    "location": "123 Oak St, Chicago, IL 60614",
    "attendee_email": "buyer@example.com",
    "attendee_name": "John Smith",
    "property_price": 450000,
    "property_beds": 3,
    "property_baths": 2
  }'
```

**Response:**
```json
{
  "success": true,
  "event_id": "evt_abc123",
  "calendar_link": "https://calendar.google.com/...",
  "confirmation_sent": true,
  "error": null
}
```

**Get Availability:**
```bash
curl -X GET "http://localhost:9000/skills/calendar/availability?agent_id=sohail_123&date=2026-06-10&duration_minutes=30" \
  -H "Authorization: Bearer $API_KEY"
```

**Response:**
```json
{
  "agent_id": "sohail_123",
  "date": "2026-06-10",
  "available_slots": [
    {"start": "14:00", "end": "14:30"},
    {"start": "15:00", "end": "15:30"},
    {"start": "16:00", "end": "16:30"}
  ]
}
```

### 2. CRM Skill (Log Leads & Activities)

**Create Lead:**
```bash
curl -X POST http://localhost:9000/skills/crm/create_lead \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "phone": "312-555-0123",
    "email": "john@example.com",
    "source": "voice_receptionist",
    "property_interest": "3 bed homes on North Shore",
    "timeline": "3 months",
    "budget": "400000-500000",
    "lead_score": "warm",
    "call_id": "call_xyz789",
    "notes": "Interested in Lake View area, prefers hardwood floors"
  }'
```

**Response:**
```json
{
  "success": true,
  "lead_id": "lead_abc456",
  "crm_url": "https://crm.app/leads/lead_abc456",
  "assigned_agent": "sohail_123"
}
```

**Log Activity (Message, Call, etc.):**
```bash
curl -X POST http://localhost:9000/skills/crm/log_activity \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "lead_abc456",
    "activity_type": "voicemail",
    "activity_date": "2026-06-09T15:30:00Z",
    "title": "Message left about 123 Oak St showing",
    "notes": "Caller interested in Friday afternoon availability",
    "priority": "high",
    "call_id": "call_xyz789"
  }'
```

**Response:**
```json
{
  "success": true,
  "activity_id": "act_def789",
  "logged_at": "2026-06-09T15:30:00Z"
}
```

### 3. Send Skill (Email Confirmations)

**Send Email:**
```bash
curl -X POST http://localhost:9000/skills/send/email \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "buyer@example.com",
    "subject": "Your Showing is Confirmed - 123 Oak St",
    "template": "appointment_confirmation",
    "data": {
      "property_address": "123 Oak St, Chicago, IL",
      "showing_time": "2026-06-10 2:00 PM",
      "agent_name": "Sohail",
      "agent_phone": "312-555-0100",
      "property_price": 450000,
      "property_image_url": "https://..."
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message_id": "msg_ghi012",
  "sent_at": "2026-06-09T15:35:00Z"
}
```

### 4. Prospect Skill (Research Leads)

**Look Up Lead:**
```bash
curl -X GET "http://localhost:9000/skills/prospect/research?phone=312-555-0123&source=voice_receptionist" \
  -H "Authorization: Bearer $API_KEY"
```

**Response:**
```json
{
  "found": true,
  "existing_lead": {
    "id": "lead_existing_123",
    "name": "John Smith",
    "history": "2 previous interactions",
    "score": "warm"
  }
}
```

## Workflow Integration Examples

### Complete Flow: Appointment Scheduling

```python
# Voice Receptionist Flow (in voice_receptionist.py)

1. Caller: "I'd like to schedule a showing for the Oak St property"
   ↓
2. Claude detects intent = "schedule_appointment"
   ↓
3. Receptionist: "What day works for you?"
   ↓
4. Caller: "Friday afternoon"
   ↓
5. Claude requests availability
   HTTP GET /skills/calendar/availability
   ← Returns: [2pm, 4pm available]
   ↓
6. Receptionist: "I have 2 PM or 4 PM. Which?"
   ↓
7. Caller: "2 PM"
   ↓
8. Claude calls create_event
   HTTP POST /skills/calendar/create_event
   ← Returns: event_id, confirmation_sent=true
   ↓
9. Claude calls send confirmation
   HTTP POST /skills/send/email (with template data)
   ← Returns: message_id
   ↓
10. Log in local DB: appointment_scheduled record
    - appointment_id, call_id, property, time, confirmed
    ↓
11. Receptionist: "Perfect! Confirmation email sent. See you Friday!"
```

### Complete Flow: Lead Qualification

```python
# Lead Qualification Flow

1. Caller: "I'm interested in selling"
   ↓
2. Claude detects intent = "lead_qualification"
   ↓
3. Receptionist: "Great! How many bedrooms? What's your timeline?"
   ↓
4. Caller: "3 bedrooms, want to sell in 3 months"
   ↓
5. Receptionist: "What's your target price range?"
   ↓
6. Caller: "Around 500K"
   ↓
7. Claude scores: lead_score = "warm" (clear timeline, known property type)
   ↓
8. Claude calls create_lead
   HTTP POST /skills/crm/create_lead
   ← Returns: lead_id, assigned_agent
   ↓
9. Claude calls log_activity
   HTTP POST /skills/crm/log_activity
   ← Returns: activity_id
   ↓
10. Log in local DB: lead_captured record
   ↓
11. Receptionist: "We'll have Sohail reach out soon. What's your email?"
```

### Complete Flow: Message Taking

```python
# Message Taking Flow

1. Caller: "I'd like to leave a message for Sohail"
   ↓
2. Claude detects intent = "take_message"
   ↓
3. Receptionist: "Of course! What's your message?"
   ↓
4. Caller: [long message transcribed by Whisper]
   ↓
5. Claude calls log_activity (high priority = "voicemail")
   HTTP POST /skills/crm/log_activity
   ← Returns: activity_id
   ↓
6. Log in local DB: call record with transcript
   ↓
7. Receptionist: "Got it! Sohail will call you back shortly."
```

## Error Handling & Retries

If skill calls fail:

```python
# In voice_receptionist/utils/skill_client.py

def call_skill(method, endpoint, payload, retries=3):
    for attempt in range(retries):
        try:
            response = requests.request(
                method,
                f"{SKILL_BRIDGE_URL}{endpoint}",
                json=payload,
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code in [429, 503]:  # Retryable
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    
    raise SkillCallError(f"Failed after {retries} attempts: {endpoint}")
```

**Fallback Behavior:**
- Calendar full: Offer voicemail instead of showing
- CRM unavailable: Log to local DB, sync when available
- Email send fails: Skip, still confirm verbally

## Authentication

All skill calls require Bearer token:

```python
# In .env
AUTOMATION_API_KEY=your_secret_key_here_generate_with_openssl

# In code
headers = {
    "Authorization": f"Bearer {os.environ['AUTOMATION_API_KEY']}",
    "Content-Type": "application/json"
}
```

To generate a key:
```bash
openssl rand -hex 32
# 9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f
```

## Database Schema Changes

Add these tables to sync with skill calls:

```sql
-- Track which leads were created via voice
CREATE TABLE voice_leads (
  id TEXT PRIMARY KEY,
  call_id TEXT,
  crm_lead_id TEXT,  -- ID returned from CRM skill
  source TEXT = 'voice_receptionist',
  synced_to_crm BOOLEAN DEFAULT FALSE,
  synced_at TIMESTAMP,
  FOREIGN KEY(call_id) REFERENCES calls(call_id)
);

-- Track which appointments were scheduled
CREATE TABLE voice_appointments (
  id TEXT PRIMARY KEY,
  call_id TEXT,
  calendar_event_id TEXT,  -- ID returned from Calendar skill
  confirmation_email_sent BOOLEAN,
  synced_to_calendar BOOLEAN DEFAULT FALSE,
  FOREIGN KEY(call_id) REFERENCES calls(call_id)
);

-- Track skill invocations for debugging
CREATE TABLE skill_calls (
  id TEXT PRIMARY KEY,
  call_id TEXT,
  skill_name TEXT,  -- 'calendar', 'crm', 'send', 'prospect'
  endpoint TEXT,
  payload TEXT,
  response TEXT,
  status_code INTEGER,
  succeeded BOOLEAN,
  error TEXT,
  duration_ms INTEGER,
  created_at TIMESTAMP,
  FOREIGN KEY(call_id) REFERENCES calls(call_id)
);
```

## Testing Integration

```bash
# Test skill bridge connectivity
curl http://localhost:9000/health

# Test calendar skill
curl -X GET "http://localhost:9000/skills/calendar/availability?agent_id=test&date=2026-06-10&duration_minutes=30" \
  -H "Authorization: Bearer test-key"

# Test CRM skill
curl -X POST http://localhost:9000/skills/crm/create_lead \
  -H "Authorization: Bearer test-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Lead", "phone": "555-1234", "source": "test"}'
```

## Production Deployment

Once all tests pass:

1. Get `API_KEY` from Eitan
2. Set env vars on production server
3. Test each skill endpoint with real data
4. Deploy voice receptionist Flask server
5. Configure Twilio webhooks to point to voice receptionist URL
6. Monitor skill calls for 24 hours (watch for failures)
7. Alert Eitan if skill calls drop below 90% success rate
