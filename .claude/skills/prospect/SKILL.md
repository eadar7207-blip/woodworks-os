---
name: prospect
description: Research leads, pull together context, draft outreach, track deal status
---

# Prospect

Manage your sales pipeline. Research leads, understand their business, draft personalized outreach, and track where deals stand.

---

## Operations

### `/prospect research [name or company]` - Build a prospect brief

When researching a new lead:

1. Gather context:
   - Company size, industry, recent news
   - Decision-maker info (title, LinkedIn, email if available)
   - Current tools and stack (if knowable)
   - Pain points relevant to your automation services

2. Check the wiki:
   - Is this prospect already in `wiki/entities/`?
   - What similar companies have you worked with?
   - What patterns from past deals apply?

3. Create or update the prospect page in `wiki/entities/[prospect-slug].md` with:
   - Company overview
   - Key decision-makers
   - Their likely pain points (lead follow-up, data entry, scheduling, etc.)
   - Best contact approach
   - Deal status and next steps

4. Surface competitive or timing intel if relevant

Example: `/prospect research ABC Real Estate Group`

### `/prospect outreach [prospect name]` - Draft personalized outreach

When ready to reach out:

1. Pull the prospect's brief from the wiki
2. Check what you know about their business and pain points
3. Draft an email or message that:
   - References something specific about their business
   - Connects their pain point to what you do
   - Includes a clear, low-friction next step (15-min call, demo video link)
   - Shows you understand their industry (real estate angle helps here)

4. Show the draft for feedback before sending

Example: `/prospect outreach ABC Real Estate Group`

### `/prospect update [prospect name] [status]` - Move deal status

When deal status changes:

1. Pull the prospect from the wiki
2. Update deal stage: `prospect → contact made → demo scheduled → proposal sent → negotiating → won/lost`
3. Log key moments: call outcomes, objections, pricing discussions
4. Update `wiki/overview.md` if this is a big deal
5. Append to `wiki/log.md`

Supported statuses: `prospect | contact-made | demo-scheduled | proposal-sent | negotiating | closed-won | closed-lost`

Example: `/prospect update ABC Real Estate Group demo-scheduled`

### `/prospect pipeline` - View your current deals

Show summary of all prospects in the wiki with their stage, last update, and next action.

---

## Prospect Page Template

When you create a new prospect in the wiki, use this structure:

```yaml
---
title: [Company Name]
type: entity
tags: [prospect, real-estate, automation, etc.]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: 0
---

# [Company Name]

## Business

[What they do, size, industry, recent context]

## Decision-Makers

- [Name] (Title) — [Contact info, LinkedIn, notes]

## Their Pain Points

- [Problem 1: e.g., lead follow-up taking 10 hrs/week]
- [Problem 2]

## Our Fit

How your automation services solve their pain points.

## Deal Status

- Stage: prospect | contact-made | demo-scheduled | proposal-sent | negotiating | closed-won | closed-lost
- Last Update: YYYY-MM-DD
- Next Step: [What's the next action?]

## Notes

[Call outcomes, objections, pricing discussions, timeline info]
```

---

## Pipeline Stages

Track where each prospect is:

1. **Prospect** — Company identified, not yet contacted
2. **Contact Made** — Reached out, waiting on response or had initial chat
3. **Demo Scheduled** — They've agreed to see what you can do
4. **Proposal Sent** — You've sent a scope and pricing
5. **Negotiating** — Back-and-forth on terms, timeline, or scope
6. **Closed Won** — Deal signed, start date set
7. **Closed Lost** — They said no, or went another direction

---

## Real Estate Verticals to Target

Keep these in the wiki as concept pages — refine them as you learn:

- Independent real estate agents (10-50 agent teams)
- Real estate brokerages (50+ agents)
- Real estate tech platforms
- Property management companies
- Title/escrow companies

For each, document: typical pain points, buying process, deal size, decision-maker titles, timing.
