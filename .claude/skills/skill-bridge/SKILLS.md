# Skill Parameters Reference

Complete parameter reference for all Claude Code skills.

## Prospect Skill

Research and manage sales prospects.

### prospect/research

Research a prospect's company and background.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `name` | string | Prospect's full name | "John Smith" |
| `company` | string | Prospect's company name | "ABC Real Estate" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `industry` | string | Company industry | "Real Estate" |
| `location` | string | Company location/city | "Chicago, IL" |
| `title` | string | Prospect's job title | "Sales Director" |

**Response**

```json
{
    "company_info": {
        "name": "ABC Real Estate",
        "industry": "Real Estate",
        "location": "Chicago, IL",
        "website": "https://abc-realestate.com",
        "size": "50-200 employees"
    },
    "contacts": [
        {
            "name": "John Smith",
            "title": "Sales Director",
            "email": "john@abc.com",
            "phone": "(555) 123-4567"
        }
    ],
    "social_links": {
        "linkedin": "https://linkedin.com/in/john-smith",
        "twitter": "https://twitter.com/johnsmith"
    },
    "recent_activity": [
        {"date": "2024-01-10", "activity": "Posted about new listings"}
    ]
}
```

**Example Request**

```bash
curl -X POST http://localhost:9000/invoke/prospect \
  -H "Content-Type: application/json" \
  -d '{
    "action": "research",
    "params": {
      "name": "John Smith",
      "company": "ABC Real Estate",
      "location": "Chicago"
    }
  }'
```

---

### prospect/outreach

Create and send outreach message to a prospect.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `prospect_name` | string | Prospect's name | "John Smith" |
| `prospect_email` | string | Prospect's email | "john@abc.com" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `subject` | string | Email subject line | "Lead Automation for ABC" |
| `template` | string | Outreach template name | "real_estate_intro" |
| `context` | string | Additional context | "Met at conference" |

**Response**

```json
{
    "sent": true,
    "message_id": "msg_abc123",
    "confirmation": "Outreach email sent to john@abc.com"
}
```

---

### prospect/update

Update prospect status and notes.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `prospect_id` | string | Prospect ID | "prospect_123" |
| `status` | string | New status | "qualified" / "negotiating" / "won" / "lost" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `notes` | string | Notes to add | "Interested in automation" |
| `next_step` | string | Next action | "Send proposal" |

**Response**

```json
{
    "updated": true,
    "prospect_id": "prospect_123",
    "new_status": "qualified",
    "updated_fields": ["status", "notes"]
}
```

---

### prospect/pipeline

Get prospect pipeline overview.

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `stage` | string | Filter by stage | "qualified" |
| `limit` | integer | Max results | 50 |

**Response**

```json
{
    "total_prospects": 150,
    "by_stage": {
        "lead": 40,
        "qualified": 50,
        "proposal": 30,
        "negotiating": 20,
        "won": 10
    },
    "pipeline": [
        {"name": "John Smith", "company": "ABC Real Estate", "stage": "qualified"},
        {"name": "Jane Doe", "company": "XYZ Properties", "stage": "proposal"}
    ]
}
```

---

## Proposal Skill

Generate and manage business proposals.

### proposal/generate

Generate a proposal for a prospect.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `prospect_name` | string | Prospect's name | "John Smith" |
| `company` | string | Client company | "ABC Real Estate" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `scope` | string | Project scope | "Lead automation system" |
| `budget` | string | Budget estimate | "10000" |
| `timeline` | string | Project timeline | "30 days" |
| `template` | string | Proposal template | "real_estate" |

**Response**

```json
{
    "proposal_id": "prop_abc123",
    "proposal_content": "Executive Summary...",
    "estimated_price": "$5,000 - $10,000",
    "document_url": "https://example.com/proposals/prop_abc123.pdf"
}
```

---

### proposal/review

Review proposal quality and completeness.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `proposal_id` | string | Proposal to review | "prop_abc123" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `review_criteria` | array | Criteria to check | ["pricing", "timeline"] |

**Response**

```json
{
    "review_status": "approved",
    "quality_score": 8.5,
    "issues": [
        "Consider adding ROI projections",
        "Add client testimonials"
    ],
    "recommendations": [
        "Include case studies",
        "Adjust pricing for market competitiveness"
    ]
}
```

---

### proposal/send

Send proposal to prospect.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `proposal_id` | string | Proposal to send | "prop_abc123" |
| `recipient_email` | string | Recipient email | "john@abc.com" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `message` | string | Cover message | "Here is your proposal..." |

**Response**

```json
{
    "sent": true,
    "sent_at": "2024-01-15T10:30:00Z",
    "tracking_id": "track_abc123"
}
```

---

### proposal/track

Track proposal status and engagement.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `proposal_id` | string | Proposal to track | "prop_abc123" |

**Response**

```json
{
    "status": "viewed",
    "views": 3,
    "opened_at": [
        "2024-01-15T10:35:00Z",
        "2024-01-16T14:20:00Z"
    ],
    "feedback": [
        "Interested in timeline adjustment",
        "Budget seems high"
    ]
}
```

---

## CRM Skill

Manage customer relationship management data.

### crm/log_activity

Log an activity for a contact.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `contact_id` | string | Contact ID | "contact_123" |
| `activity_type` | string | Type of activity | "email_sent" / "call" / "meeting" |
| `description` | string | Activity description | "Sent proposal to John" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `date` | string | Activity date (ISO 8601) | "2024-01-15T10:30:00Z" |
| `outcome` | string | Activity outcome | "interested" / "not_interested" |

**Response**

```json
{
    "activity_id": "activity_abc123",
    "logged_at": "2024-01-15T10:30:00Z",
    "confirmation": "Activity logged for John Smith"
}
```

---

### crm/update_contact

Update contact information.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `contact_id` | string | Contact ID | "contact_123" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `name` | string | Contact name | "John Smith" |
| `email` | string | Contact email | "john@abc.com" |
| `phone` | string | Contact phone | "(555) 123-4567" |
| `company` | string | Company | "ABC Real Estate" |
| `status` | string | Contact status | "lead" / "customer" / "inactive" |
| `notes` | string | Contact notes | "Prefers email communication" |

**Response**

```json
{
    "updated": true,
    "contact_id": "contact_123",
    "updated_fields": ["email", "status", "notes"]
}
```

---

### crm/query

Query contacts by criteria.

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Filter by status | "lead" |
| `company` | string | Filter by company | "ABC Real Estate" |
| `tags` | array | Filter by tags | ["hot_prospect", "real_estate"] |
| `limit` | integer | Max results | 100 |

**Response**

```json
{
    "total_found": 45,
    "contacts": [
        {
            "contact_id": "contact_123",
            "name": "John Smith",
            "email": "john@abc.com",
            "company": "ABC Real Estate",
            "status": "lead"
        }
    ]
}
```

---

### crm/create_contact

Create a new contact.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `name` | string | Contact name | "John Smith" |
| `email` | string | Contact email | "john@abc.com" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `phone` | string | Contact phone | "(555) 123-4567" |
| `company` | string | Company | "ABC Real Estate" |
| `title` | string | Job title | "Sales Director" |
| `tags` | array | Tags | ["hot_prospect", "real_estate"] |

**Response**

```json
{
    "contact_id": "contact_abc123",
    "created_at": "2024-01-15T10:30:00Z",
    "confirmation": "Contact created successfully"
}
```

---

## Send Skill

Send emails and messages.

### send/email

Send an email.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `to` | string | Recipient email | "john@abc.com" |
| `subject` | string | Email subject | "Your Proposal" |
| `body` | string | Email body (text) | "Here is your proposal..." |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `cc` | array | CC recipients | ["manager@abc.com"] |
| `bcc` | array | BCC recipients | ["log@example.com"] |
| `html` | string | HTML email body | "<p>Here is...</p>" |
| `attachments` | array | Files to attach | ["proposal.pdf"] |
| `template` | string | Email template | "proposal_followup" |

**Response**

```json
{
    "sent": true,
    "message_id": "msg_abc123",
    "sent_at": "2024-01-15T10:30:00Z",
    "confirmation": "Email sent to john@abc.com"
}
```

---

### send/sms

Send an SMS message.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `phone` | string | Phone number | "+1-555-123-4567" |
| `message` | string | SMS body | "Your proposal is ready" |

**Response**

```json
{
    "sent": true,
    "message_id": "sms_abc123",
    "status": "delivered"
}
```

---

### send/slack

Send a Slack message.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `channel` | string | Channel or user | "#sales" or "@john" |
| `message` | string | Message text | "New lead: ABC Real Estate" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `thread_ts` | string | Thread timestamp | "1234567890.123456" |
| `attachments` | array | Message attachments | [...] |

**Response**

```json
{
    "sent": true,
    "ts": "1234567890.123456",
    "confirmation": "Message sent to #sales"
}
```

---

## Tasks Skill

Create and manage tasks.

### tasks/create

Create a new task.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | string | Task title | "Follow up with John" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `description` | string | Task description | "Send follow-up email" |
| `due_date` | string | Due date (ISO 8601) | "2024-01-20T17:00:00Z" |
| `priority` | string | Priority level | "high" / "medium" / "low" |
| `assignee` | string | Assignee | "user@example.com" |

**Response**

```json
{
    "task_id": "task_abc123",
    "created_at": "2024-01-15T10:30:00Z",
    "confirmation": "Task created successfully"
}
```

---

### tasks/assign

Assign a task to someone.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `task_id` | string | Task ID | "task_abc123" |
| `assignee` | string | Assignee email | "user@example.com" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `message` | string | Notification message | "Please follow up" |

**Response**

```json
{
    "assigned": true,
    "task_id": "task_abc123",
    "assigned_to": "user@example.com"
}
```

---

### tasks/update_status

Update task status.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `task_id` | string | Task ID | "task_abc123" |
| `status` | string | New status | "completed" / "in_progress" / "pending" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `notes` | string | Status notes | "Completed early" |

**Response**

```json
{
    "updated": true,
    "task_id": "task_abc123",
    "new_status": "completed"
}
```

---

### tasks/list

List tasks.

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Filter by status | "pending" |
| `assignee` | string | Filter by assignee | "user@example.com" |
| `due_date` | string | Filter by due date | "2024-01-20" |
| `limit` | integer | Max results | 50 |

**Response**

```json
{
    "total": 15,
    "tasks": [
        {
            "task_id": "task_abc123",
            "title": "Follow up with John",
            "status": "pending",
            "due_date": "2024-01-20T17:00:00Z"
        }
    ]
}
```

---

## Content Skill

Generate and manage content.

### content/generate

Generate content.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `type` | string | Content type | "email" / "blog" / "social" |
| `topic` | string | Content topic | "Lead automation benefits" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `length` | string | Content length | "short" / "medium" / "long" |
| `tone` | string | Tone of voice | "professional" / "casual" / "urgent" |
| `style` | string | Writing style | "formal" / "conversational" |

**Response**

```json
{
    "content_id": "content_abc123",
    "content": "Generated content here...",
    "word_count": 250
}
```

---

## Calendar Skill

Manage calendar events.

### calendar/create_event

Create a calendar event.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | string | Event title | "Sales Meeting" |
| `start_time` | string | Start time (ISO 8601) | "2024-01-20T10:00:00Z" |
| `end_time` | string | End time (ISO 8601) | "2024-01-20T11:00:00Z" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `description` | string | Event description | "Quarterly review meeting" |
| `location` | string | Event location | "Conference Room A" |
| `attendees` | array | Attendee emails | ["john@abc.com"] |

**Response**

```json
{
    "event_id": "event_abc123",
    "created_at": "2024-01-15T10:30:00Z",
    "confirmation": "Event created successfully"
}
```

---

## Invoicing Skill

Create and manage invoices.

### invoicing/create

Create an invoice.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `client_name` | string | Client name | "ABC Real Estate" |
| `amount` | string | Invoice amount | "5000" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `items` | array | Line items | [{"description": "Setup", "amount": "3000"}] |
| `due_date` | string | Due date (ISO 8601) | "2024-02-15" |
| `terms` | string | Payment terms | "Net 30" |

**Response**

```json
{
    "invoice_id": "inv_abc123",
    "created_at": "2024-01-15T10:30:00Z",
    "amount": "$5,000"
}
```

---

### invoicing/send

Send invoice to client.

**Required Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `invoice_id` | string | Invoice ID | "inv_abc123" |
| `client_email` | string | Client email | "john@abc.com" |

**Optional Parameters**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `message` | string | Cover message | "Please find attached..." |

**Response**

```json
{
    "sent": true,
    "sent_at": "2024-01-15T10:30:00Z",
    "confirmation": "Invoice sent to john@abc.com"
}
```

---

## Parameter Types

- **string** - Text value
- **integer** - Whole number
- **array** - List of values
- **object** - Nested JSON object
- **boolean** - True/False

## Date Formats

- ISO 8601: `2024-01-15T10:30:00Z`
- Date only: `2024-01-15`

## Common Status Values

**Prospect Status**
- lead
- qualified
- proposal
- negotiating
- won
- lost

**Task Status**
- pending
- in_progress
- completed
- cancelled

**Contact Status**
- lead
- customer
- inactive
- archived

**Email Status**
- sent
- delivered
- failed
- bounced
- opened
- clicked
