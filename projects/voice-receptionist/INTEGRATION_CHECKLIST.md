# Integration Verification Checklist

Use this checklist before moving to production.

---

## Pre-Integration Setup

- [ ] Clone voice-receptionist repository
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Install dependencies: `pip3 install -r requirements.txt`
- [ ] Copy `.env.example` to `.env.local`
- [ ] Fill in all API keys in `.env.local`

---

## API Key Verification

- [ ] `ANTHROPIC_API_KEY` obtained from https://console.anthropic.com
- [ ] `OPENAI_API_KEY` obtained from https://platform.openai.com
- [ ] `ELEVENLABS_API_KEY` obtained from https://elevenlabs.io
- [ ] `TWILIO_ACCOUNT_SID` & `TWILIO_AUTH_TOKEN` obtained from Twilio
- [ ] `AUTOMATION_API_KEY` generated (use: `openssl rand -hex 32`)

---

## Skill Bridge Integration

### Endpoint: Calendar Skill

**Test command:**
```bash
curl -X POST http://localhost:9000/skills/calendar/create_event \
  -H "Authorization: Bearer $AUTOMATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Showing",
    "start_time": "2026-06-10T14:00:00Z",
    "end_time": "2026-06-10T14:30:00Z",
    "location": "123 Test St"
  }'
```

- [ ] Calendar skill responds with 200 OK
- [ ] Response includes `event_id`
- [ ] Confirmation email flag set

**Test availability check:**
```bash
curl -X GET "http://localhost:9000/skills/calendar/availability?agent_id=test_agent&date=2026-06-10" \
  -H "Authorization: Bearer $AUTOMATION_API_KEY"
```

- [ ] Returns available time slots for agent
- [ ] Slots formatted as `{"start": "14:00", "end": "14:30"}`

### Endpoint: CRM Skill

**Test command:**
```bash
curl -X POST http://localhost:9000/skills/crm/create_lead \
  -H "Authorization: Bearer $AUTOMATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Lead",
    "phone": "312-555-1234",
    "email": "test@example.com",
    "source": "voice_receptionist",
    "lead_score": "warm"
  }'
```

- [ ] CRM skill responds with 200 OK
- [ ] Response includes `lead_id`
- [ ] Lead appears in CRM

**Test activity logging:**
```bash
curl -X POST http://localhost:9000/skills/crm/log_activity \
  -H "Authorization: Bearer $AUTOMATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": "test_lead_id",
    "activity_type": "call",
    "title": "Test activity",
    "notes": "Testing integration"
  }'
```

- [ ] Activity logged with 200 OK
- [ ] Activity appears in lead record

### Endpoint: Send Skill

**Test command:**
```bash
curl -X POST http://localhost:9000/skills/send/email \
  -H "Authorization: Bearer $AUTOMATION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "template": "test",
    "data": {"test": "data"}
  }'
```

- [ ] Email skill responds with 200 OK
- [ ] Response includes `message_id`
- [ ] Email received (or logged in email service)

---

## Flask Application Tests

**Start the server:**
```bash
python3 app.py
```

### Health Check
```bash
curl http://localhost:5001/health
```

- [ ] Returns `{"status": "healthy"}`
- [ ] Status code: 200

### Start a Call
```bash
curl -X POST http://localhost:5001/call/start \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "sohail_123",
    "caller_phone": "+1-312-555-1234"
  }'
```

- [ ] Returns `call_id`
- [ ] Call logged in database
- [ ] Status code: 200

### Process Message
```bash
curl -X POST http://localhost:5001/call/{call_id}/message \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "I want to schedule a showing"
  }'
```

- [ ] Returns response message
- [ ] Intent detected
- [ ] Status code: 200

### End Call
```bash
curl -X POST http://localhost:5001/call/{call_id}/end
```

- [ ] Call marked as complete
- [ ] Duration calculated
- [ ] Status code: 200

### Get Call Statistics
```bash
curl http://localhost:5001/stats
```

- [ ] Returns call count, lead count, appointment count
- [ ] Timestamp included
- [ ] Status code: 200

---

## Database Verification

**Check database initialization:**
```bash
python3 -c "from voice_receptionist.database import Database; db = Database(); print('Tables created:', db.get_stats())"
```

- [ ] Database initializes without errors
- [ ] All tables created
- [ ] Stats endpoint returns valid data

**Check database CRUD operations:**
```bash
python3 -m pytest tests/test_database.py -v
```

- [ ] All database tests pass
- [ ] CRUD operations work
- [ ] Queries return expected results

---

## Integration Tests

**Run full integration test suite:**
```bash
python3 -m pytest tests/test_integration.py -v
```

- [ ] Conversation manager tests pass
- [ ] Message history tracking works
- [ ] State persistence works

**Run skill client tests:**
```bash
python3 -m pytest tests/test_skill_client.py -v
```

- [ ] Mock API calls work
- [ ] Error handling works
- [ ] Retry logic works

---

## Demo Mode

**Run demo scenario:**
```bash
python3 demo.py
```

- [ ] Demo starts without errors
- [ ] Scenario 1: Appointment scheduling completes
- [ ] Scenario 2: Lead qualification completes
- [ ] Scenario 3: Message taking completes
- [ ] Database stores all 3 calls
- [ ] Statistics updated

---

## Error Handling

**Test graceful degradation:**

1. Stop Skill Bridge, try to create event
   - [ ] Returns error gracefully (no crash)
   - [ ] Error message logged

2. Invalid API key
   - [ ] Returns 401 Unauthorized
   - [ ] Request rejected

3. Malformed request
   - [ ] Returns 400 Bad Request
   - [ ] Clear error message

---

## Performance Baseline

**Load test (light):**
```bash
# Run 10 calls concurrently
for i in {1..10}; do
  curl -X POST http://localhost:5001/call/start \
    -H "Content-Type: application/json" \
    -d '{"agent_id": "test", "caller_phone": "+1-555-0123"}' &
done
wait
```

- [ ] All 10 calls complete in < 5 seconds
- [ ] No errors
- [ ] Database handles concurrent writes

---

## Security Checklist

- [ ] API key is not logged
- [ ] API key stored in environment only (not in code)
- [ ] CORS configured (if needed)
- [ ] Rate limiting enabled (optional)
- [ ] Input validation on all endpoints
- [ ] No sensitive data in error messages

---

## Final Verification

- [ ] README.md reviewed and up-to-date
- [ ] ARCHITECTURE.md matches implementation
- [ ] DEPLOYMENT.md deployment steps tested
- [ ] All tests passing
- [ ] Demo scenario works
- [ ] No hardcoded secrets in code
- [ ] Documentation complete

---

## Sign-Off

**Ready for production?**

- Architect: _____ (date: _____)
- QA/Tester: _____ (date: _____)
- Operations: _____ (date: _____)

**Known limitations or blockers:**
- 
- 

**Go/No-go decision:** ☐ GO ☐ NO-GO

---

## Post-Deployment

- [ ] Monitor error logs for 24 hours
- [ ] Track call success rate
- [ ] Monitor API latency
- [ ] Alert on failed skill calls
- [ ] Backup database daily
