# Skill Bridge API Reference

Complete reference for all Skill Bridge endpoints.

## Base URL

```
http://localhost:9000
```

## Authentication

Optional API key authentication:

```
Authorization: Bearer YOUR_API_KEY
```

Set `SKILL_BRIDGE_API_KEY` environment variable to enable.

## Response Format

All responses are JSON with the following structure:

### Success Response

```json
{
    "status": "completed|success|partial",
    "output": { ... },
    "invocation_id": "uuid",
    "duration_ms": 1500
}
```

### Error Response

```json
{
    "status": "error|failed",
    "error": "Error message",
    "invocation_id": "uuid"
}
```

### Async Response

```json
{
    "status": "queued|running|completed|failed",
    "invocation_id": "uuid",
    "message": "..."
}
```

## Endpoints

### 1. Health Check

Check if the Skill Bridge API is running.

**Request**

```
GET /health
```

**Response (200 OK)**

```json
{
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00.000000",
    "version": "1.0.0"
}
```

**Example**

```bash
curl http://localhost:9000/health
```

---

### 2. List Available Skills

Get a list of all available skills and their parameters.

**Request**

```
GET /available-skills
```

**Response (200 OK)**

```json
{
    "total": 10,
    "skills": [
        {
            "name": "prospect",
            "description": "Research and manage sales prospects",
            "actions": ["research", "outreach", "update", "pipeline"],
            "parameters": {
                "research": {
                    "required": ["name", "company"],
                    "optional": ["industry", "location", "title"],
                    "description": "Research a prospect's company and background"
                },
                "outreach": {
                    "required": ["prospect_name", "prospect_email"],
                    "optional": ["subject", "template"],
                    "description": "Create and send outreach message"
                }
            }
        },
        ...
    ]
}
```

**Example**

```bash
curl http://localhost:9000/available-skills
```

---

### 3. Get Skill Details

Get detailed information about a specific skill.

**Request**

```
GET /skills/{skill_name}
```

**Parameters**

- `skill_name` (path, required) - Name of the skill (e.g., "prospect", "proposal")

**Response (200 OK)**

```json
{
    "name": "prospect",
    "description": "Research and manage sales prospects",
    "actions": ["research", "outreach", "update", "pipeline"],
    "parameters": {
        "research": {
            "required": ["name", "company"],
            "optional": ["industry", "location"],
            "description": "Research a prospect's company",
            "response_format": {
                "company_info": { "type": "dict" },
                "contacts": { "type": "list" },
                "social_links": { "type": "dict" }
            }
        }
    }
}
```

**Response (404 Not Found)**

```json
{
    "error": "Skill 'unknown' not found"
}
```

**Example**

```bash
curl http://localhost:9000/skills/proposal
```

---

### 4. Invoke Skill Synchronously

Execute a skill and wait for the result.

**Request**

```
POST /invoke/{skill_name}
```

**Request Body**

```json
{
    "action": "action_name",
    "params": {
        "param1": "value1",
        "param2": "value2"
    }
}
```

**Parameters**

- `skill_name` (path, required) - Name of the skill
- `action` (body, required) - Name of the action to perform
- `params` (body, required) - Parameters for the action

**Response (200 OK)**

```json
{
    "status": "completed|success|partial",
    "output": {
        "company_info": { ... },
        "contacts": [ ... ],
        "social_links": { ... }
    },
    "raw_output": "Raw text output from skill",
    "confidence": 0.85,
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000",
    "duration_ms": 2500
}
```

**Response (400 Bad Request)**

```json
{
    "status": "error",
    "error": "Parameter validation failed: Missing required parameter: company",
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Example**

```bash
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {
      "name": "John Smith",
      "company": "ABC Real Estate"
    }
  }'
```

---

### 5. Invoke Skill Asynchronously

Queue a skill invocation for async execution.

**Request**

```
POST /invoke/{skill_name}/async
```

**Request Body**

```json
{
    "action": "action_name",
    "params": {
        "param1": "value1"
    }
}
```

**Response (202 Accepted)**

```json
{
    "status": "queued",
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Skill invocation 550e8400... queued for execution"
}
```

**Example**

```bash
curl -X POST http://localhost:9000/invoke/proposal/async \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "prospect_name": "John Smith",
      "company": "ABC Real Estate",
      "scope": "Lead automation"
    }
  }'
```

---

### 6. Get Async Invocation Status

Poll the status of an async invocation.

**Request**

```
GET /status/{invocation_id}
```

**Parameters**

- `invocation_id` (path, required) - ID returned from async invocation

**Response (200 OK)**

```json
{
    "invocation_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "queued|running|completed|failed",
    "skill_name": "proposal",
    "action": "generate",
    "created_at": "2024-01-15T10:30:00.000000",
    "started_at": "2024-01-15T10:30:01.000000",
    "completed_at": "2024-01-15T10:30:05.000000",
    "output": {
        "proposal_id": "prop_123",
        "proposal_content": "...",
        "estimated_price": "$5,000"
    },
    "error": null
}
```

**Response (404 Not Found)**

```json
{
    "status": "not_found",
    "error": "Invocation 550e8400... not found"
}
```

**Example**

```bash
curl http://localhost:9000/status/550e8400-e29b-41d4-a716-446655440000
```

---

### 7. Get Invocation History

Retrieve past invocations with optional filtering.

**Request**

```
GET /history
```

**Query Parameters**

- `skill` (optional) - Filter by skill name
- `status` (optional) - Filter by status (completed, failed, error)
- `limit` (optional) - Number of records to return (default: 100)

**Response (200 OK)**

```json
{
    "total": 3,
    "invocations": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "skill_name": "prospect",
            "action": "research",
            "params": {
                "name": "John Smith",
                "company": "ABC Real Estate"
            },
            "status": "completed",
            "result": {
                "company_info": { ... },
                "contacts": [ ... ]
            },
            "error": null,
            "created_at": "2024-01-15T10:30:00.000000",
            "completed_at": "2024-01-15T10:30:02.500000",
            "duration_ms": 2500
        },
        ...
    ]
}
```

**Example**

```bash
# Get all completed prospect invocations
curl "http://localhost:9000/history?skill=prospect&status=completed&limit=50"
```

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful sync invocation |
| 202 | Accepted | Async invocation queued |
| 400 | Bad Request | Invalid parameters or validation failure |
| 401 | Unauthorized | Missing or invalid API key |
| 404 | Not Found | Skill or invocation not found |
| 405 | Method Not Allowed | Wrong HTTP method |
| 500 | Server Error | Internal server error |

---

## Skill Reference

### Prospect

Research and manage sales prospects.

**Actions**

- `research` - Research a prospect's company
- `outreach` - Send outreach message
- `update` - Update prospect status
- `pipeline` - Get pipeline overview

**Example: Research**

```bash
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {
      "name": "John Smith",
      "company": "ABC Real Estate",
      "industry": "Real Estate",
      "location": "Chicago"
    }
  }'
```

---

### Proposal

Generate and manage business proposals.

**Actions**

- `generate` - Generate proposal
- `review` - Review proposal quality
- `send` - Send proposal to prospect
- `track` - Track proposal status

**Example: Generate**

```bash
curl -X POST http://localhost:9000/invoke/proposal \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "prospect_name": "John Smith",
      "company": "ABC Real Estate",
      "scope": "Lead automation system",
      "budget": "10000",
      "timeline": "30 days"
    }
  }'
```

---

### CRM

Manage customer relationship management data.

**Actions**

- `log_activity` - Log contact activity
- `update_contact` - Update contact information
- `query` - Query contacts
- `create_contact` - Create new contact

**Example: Log Activity**

```bash
curl -X POST http://localhost:9000/invoke/crm \
  -H "Content-Type: application/json" \
  -d '{
    "action": "log_activity",
    "params": {
      "contact_id": "contact_123",
      "activity_type": "proposal_sent",
      "description": "Sent proposal to John Smith"
    }
  }'
```

---

### Send

Send emails and messages.

**Actions**

- `email` - Send email
- `sms` - Send SMS
- `slack` - Send Slack message

**Example: Send Email**

```bash
curl -X POST http://localhost:9000/invoke/send \
  -H "Content-Type: application/json" \
  -d '{
    "action": "email",
    "params": {
      "to": "john@example.com",
      "subject": "Your Proposal",
      "body": "Here is your proposal...",
      "cc": ["manager@example.com"],
      "html": "<p>Here is your proposal...</p>"
    }
  }'
```

---

### Tasks

Create and manage tasks.

**Actions**

- `create` - Create new task
- `assign` - Assign task to someone
- `update_status` - Update task status
- `list` - List tasks

**Example: Create Task**

```bash
curl -X POST http://localhost:9000/invoke/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "params": {
      "title": "Follow up with John",
      "description": "Send follow-up email to John Smith",
      "due_date": "2024-01-20",
      "priority": "high"
    }
  }'
```

---

### Content

Generate and manage content.

**Actions**

- `generate` - Generate content
- `customize` - Customize content
- `review` - Review content
- `publish` - Publish content

**Example: Generate**

```bash
curl -X POST http://localhost:9000/invoke/content \
  -H "Content-Type: application/json" \
  -d '{
    "action": "generate",
    "params": {
      "type": "email",
      "topic": "Lead automation benefits",
      "length": "medium",
      "tone": "professional"
    }
  }'
```

---

### Calendar

Manage calendar events.

**Actions**

- `create_event` - Create event
- `send_invite` - Send invitation
- `update` - Update event
- `list` - List events

**Example: Create Event**

```bash
curl -X POST http://localhost:9000/invoke/calendar \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create_event",
    "params": {
      "title": "Sales meeting",
      "start_time": "2024-01-20T10:00:00",
      "end_time": "2024-01-20T11:00:00",
      "location": "Conference Room A",
      "attendees": ["john@example.com"]
    }
  }'
```

---

### Invoicing

Create and manage invoices.

**Actions**

- `create` - Create invoice
- `send` - Send invoice
- `track_payment` - Track payment status
- `list` - List invoices

**Example: Create**

```bash
curl -X POST http://localhost:9000/invoke/invoicing \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create",
    "params": {
      "client_name": "ABC Real Estate",
      "amount": "5000",
      "items": [
        {"description": "Lead automation setup", "amount": "3000"},
        {"description": "Training", "amount": "2000"}
      ],
      "due_date": "2024-02-15"
    }
  }'
```

---

## Confidence Scores

Response confidence indicates how confident the parser is in the extracted data:

- **1.0** - Valid JSON response (no parsing needed)
- **0.8-0.9** - High confidence text parsing
- **0.5-0.7** - Moderate confidence (partial data extracted)
- **0.3-0.4** - Low confidence (mostly raw output)
- **< 0.3** - Very low confidence (parsing failed)

Always check the `confidence` score when using parsed output.

---

## Error Codes

### Parameter Validation Errors

```json
{
    "status": "error",
    "error": "Parameter validation failed: Missing required parameter: company"
}
```

### Skill Not Found

```json
{
    "status": "error",
    "error": "Skill 'unknown_skill' not found"
}
```

### Execution Failed

```json
{
    "status": "failed",
    "error": "Skill execution failed: Command exited with code 1",
    "raw_output": "..."
}
```

### Timeout

```json
{
    "status": "error",
    "error": "Skill execution timed out after 120 seconds"
}
```

---

## Rate Limiting

No built-in rate limiting. Implement at reverse proxy level if needed.

---

## Monitoring

Monitor Skill Bridge health via:

1. **Health endpoint**: `GET /health`
2. **Log file**: `.claude/skills/skill-bridge/skill_bridge.log`
3. **Database**: `.claude/skills/skill-bridge/bridge.db`

---

## Performance

Typical response times:

- Sync invocation: 2-10 seconds
- Async queue: < 100ms
- Status poll: < 50ms
- Health check: < 10ms

---

## Pagination

History endpoint supports limit parameter (max 1000):

```bash
curl "http://localhost:9000/history?limit=200"
```

---

## CORS

CORS is not enabled by default. Add CORS headers via reverse proxy if needed.
