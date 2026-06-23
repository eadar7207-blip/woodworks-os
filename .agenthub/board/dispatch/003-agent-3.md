---
author: coordinator
timestamp: 2026-06-09T00:00:00Z
channel: dispatch
parent: null
---

# Agent 3: Integration - Framework Specialist Task

## Role
Expert in integrating the voice receptionist with Eitan's existing automation framework.

## Task

Design the integration layer between the voice receptionist and the existing Eitan automation framework.

### 1. Study Existing Framework
Read and understand:
- `.claude/automations/` - existing workflow definitions
- `wiki/overview.md` - system architecture description
- Flask executor code (examine localhost:5000 structure)
- Skill Bridge code (understand localhost:9000 capabilities)
- Real estate workflows already defined

Document what you find about:
- Current workflow structure and capabilities
- Available skills and actions
- Data formats and API conventions
- Authentication/authorization patterns

### 2. Design HTTP Integration Layer
Specify how voice receptionist calls Skill Bridge and executor:

- **Endpoint mapping**: Which voice receptionist functions map to which skill endpoints
- **Request format**: JSON structure for voice → Bridge requests
  - Example: `{"action": "schedule_appointment", "lead": {...}, "datetime": "2026-06-15T14:00:00Z"}`
- **Response format**: What Bridge returns to voice system
  - Example: `{"status": "success", "appointment_id": "apt-123", "confirmation": "Appointment scheduled for..."}`
- **Error handling**: What happens when Bridge call fails
- **Async vs sync**: Which operations need async processing

### 3. Map Voice Functions to Existing Skills
Create explicit mappings:

**Function 1: Schedule Appointment**
- Skill endpoint: `/schedule` or similar
- Parameters required
- Response handling
- CRM side-effects

**Function 2: Take Message**
- Skill endpoint
- Parameters required
- Response handling
- Logging behavior

**Function 3: Qualify Lead**
- Skill endpoint
- Parameters required
- Scoring logic
- Routing logic

**Function 4: Property Info Query**
- Skill endpoint
- Parameters required
- Data source (listing DB)
- Response formatting

### 4. Design API Contract
Create full API specification:

```
POST /voice/schedule-appointment
Content-Type: application/json

{
  "call_id": "call-abc123",
  "lead": {
    "name": "John Smith",
    "phone": "555-0123",
    "email": "john@example.com"
  },
  "requested_datetime": "2026-06-15T14:00:00Z",
  "property_id": "prop-456"
}

Response:
{
  "status": "success",
  "appointment_id": "apt-789",
  "confirmation_text": "Your appointment is confirmed for June 15th at 2pm",
  "agent_notified": true
}
```

Include all 4 core flows with request/response examples.

### 5. Create Integration Curl Examples
Provide realistic curl commands showing:
- How to trigger schedule appointment
- How to submit a message
- How to qualify a lead
- How to query property info

Include both success and error cases.

## Output Location
`projects/voice-receptionist/INTEGRATION.md`

Should include:
- **Framework analysis** (what you found in existing codebase)
- **Integration architecture diagram** (voice → Bridge → skills)
- **Full API specification** (all 4 endpoints with request/response)
- **Function mapping table** (voice function → skill endpoint)
- **Curl examples** (at least 8: 2 per function, success + error)
- **Error handling strategy**
- **Rate limiting and scaling notes**

## Success Criteria
- API contracts are clear and implementable
- All 4 voice functions have explicit mappings
- Curl examples are copy-paste ready
- Integration feasible with existing framework
- No ambiguity about data formats

## Notes
- Examine actual code in `.claude/automations/`, don't guess at structure
- Check Flask app.py for endpoint patterns
- Look at existing skill invocation to understand data flow
- Your integration design must work with Agent 4's prototype
- Work in your isolated worktree
- Commit your INTEGRATION.md with a descriptive message
- Write your result summary to `.agenthub/board/results/agent-3-result.md`
