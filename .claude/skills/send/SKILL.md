---
name: send
description: Send emails to prospects — draft, review, send, and log
---

# Send

Send personalized outreach emails to prospects. Draft → review → send → log, all in one place.

---

## Operations

### `/send [prospect email] [subject] [body]` - Send an email

Quick send:
1. You provide email, subject, message body
2. I draft it
3. You approve
4. I send it
5. Auto-log in CRM

Example: `/send eadar7207@icloud.com "15-min call: Automating your lead follow-up" "Hi Eden, I came across Adar Systems..."`

### `/send draft [prospect name]` - Draft from prospect context

Smart draft using wiki context:
1. Pull prospect info from `wiki/entities/`
2. Reference their business + pain points
3. Generate personalized email
4. You approve and send

Example: `/send draft Eden at Adar Systems Tech`

Then you say "looks good, send" and it goes out.

### `/send log [prospect name]` - Log that you sent it

After sending, automatically:
1. Updates `wiki/entities/[prospect].md` with send date
2. Logs in `/crm log [prospect]`
3. Creates follow-up reminder in `/tasks`

Example: `/send log Eden at Adar Systems Tech`

---

## How It Works

**Backend:**
- Uses Gmail MCP (authenticated via OAuth) or Zapier integration
- Tracks sent emails in wiki/log.md
- Links to /crm for follow-up tracking

**Workflow:**
```
You: /send draft [prospect]
Me: [Draft personalized email]
You: Send it
Me: [Sends] ✓ Sent to [email]
Me: [Logs in /crm and /tasks]
```

---

## Integration with Other Skills

- **`/prospect research`** → `/send draft` (uses prospect context)
- **`/content email`** → `/send [email]` (custom message)
- **`/crm log`** → auto-called after send
- **`/tasks add`** → auto-creates follow-up task

Full loop: research → content → send → track

---

## Email Best Practices (Built In)

When drafting, I automatically:
- Keep subject lines short (under 50 chars)
- Open with prospect-specific hook
- Lead with their pain point
- Include clear CTA (call link, reply prompt)
- Sign with your name
- No salesy language

---

## Tracking

Each sent email auto-logs:
- Send date and time
- Recipient email and name
- Subject line
- Response status (awaiting reply, replied, etc.)
- Follow-up date (default 3 days)

View all sent emails and follow-ups with `/crm follow-up [days]`.
