# /crm — Prospect Management & Activity Logging

Manage your real estate prospect pipeline and activity history. Create prospects, log activities, track deal stages, and view pipeline overview — all within Claude Code.

## Use when

- You're managing sales prospects (real estate leads)
- You need to log interactions (calls, emails, proposals)
- You want to track prospect stage (lead, contacted, proposal sent, negotiating, closed)
- You need to view your pipeline

## Syntax

```
/crm create [name] [company] [email] [phone]
/crm log [prospect_name] [activity_type] [notes]
/crm view [prospect_name]
/crm update [prospect_name] [new_stage]
/crm pipeline
/crm activities [prospect_name]
```

## Examples

**Create a prospect:**
```
/crm create "Sarah Johnson" "Johnson Realty Group" "sarah@johnsonrealty.com" "555-0123"
```

**Log an activity:**
```
/crm log "Sarah Johnson" "proposal_sent" "Sent automation proposal, following up June 14"
```

**View prospect details:**
```
/crm view "Sarah Johnson"
```

**Update prospect stage:**
```
/crm update "Sarah Johnson" "proposal_sent"
```

**View full pipeline:**
```
/crm pipeline
```

**See all activities:**
```
/crm activities "Sarah Johnson"
```

## What it does

- Stores prospects in local SQLite database
- Tracks activities (calls, emails, proposals, meetings)
- Manages pipeline stages: lead → contacted → proposal_sent → negotiating → closed
- Provides pipeline visibility
- Integrates with automation workflows

## Output

Returns structured data:
- Prospect name, company, email, phone
- Current pipeline stage
- Activity history with timestamps
- Pipeline summary by stage

## Workflows

Automation can call this to:
- Create prospects after research
- Log proposal generation
- Track email sends
- Update stages after interactions
- Keep CRM in sync with automation
