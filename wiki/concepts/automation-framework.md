---
title: Automation Framework
type: concept
tags: [systems, delivery, operations, real-estate]
created: 2026-06-05
updated: 2026-06-05
sources: 0
---

# Automation Framework

YAML-based workflow orchestration system that lets you design and execute automations without leaving Claude Code. Replaces N8N for your automation agency.

## Core Capability

Define automations as simple configs (YAML). Chains together:
- Your existing skills (/proposal, /crm, /prospect, /tasks, /content, /calendar, /invoicing)
- External APIs (via HTTP)
- Logic (conditionals, loops, data transforms)
- Triggers (webhooks, schedules, events, manual)

Save templates to library and reuse across clients.

## Trigger Types

- **Webhook:** External POST to unique endpoint
- **Schedule:** Cron-based recurring (9am daily, 1st of month, every 30 min, etc.)
- **Event:** Internal events (proposal_sent, invoice_created, task_completed, etc.)
- **Manual:** Direct execution via `/automate-execute workflow-name`

## Action Types

1. **Skill integration** — Call your existing skills with custom inputs
2. **HTTP requests** — POST/GET/PATCH to external APIs
3. **Data transforms** — Map/filter/reduce arrays and objects
4. **Include** — Reuse other workflow configs

## Advanced Features

- **Conditionals:** If/then/else, switch/case routing
- **Loops:** Process arrays with concurrent or sequential execution
- **Error handling:** Try/catch, validation, retry logic
- **Variables:** Environment secrets, step outputs, passed parameters
- **Logging:** Full execution history with timestamps, input/output, error traces

## Real Estate Use Cases

- Lead intake → research → proposal → email sequence
- Daily agent outreach (personalized emails at scale)
- Proposal acceptance → invoice → calendar scheduling
- Slack/email notifications on leads or events
- MLS/external API syncing

## Storage & Reuse

Automations stored in `.claude/automations/` — treat as version-controlled code.

Template pattern: Define once for a client, reuse with different variables (prospect list, timeline, messaging, etc.)

## Why Built This

- N8N requires context switching and visual workflows
- Claude Code is the command center already
- Your 15 existing skills are powerful building blocks
- Want to ship automation solutions fast (especially post-shadowing)

## Next Iteration

After shadowing [[Sohail Real Estate Group]], will discover which patterns repeat and codify as pre-built domain-specific actions (MLS sync, property posting, etc.).

Currently generic enough to handle any real estate automation pattern via HTTP + your skills.

## Related

- [[AI Automation Agency]] — business model and revenue structure
- [[Sohail Shadowing Plan]] — how to discover what agents actually need
