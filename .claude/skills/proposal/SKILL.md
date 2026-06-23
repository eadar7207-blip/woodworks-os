---
name: proposal
description: Generate proposals, SOWs, and pricing for automation projects
---

# Proposal

Turn automation specs into professional proposals. Generate scopes, timelines, and pricing.

---

## Operations

### `/proposal [prospect name] [automation brief]` - Draft a proposal

When ready to create a proposal:

1. Pull prospect context from `wiki/entities/[prospect-slug].md`
2. Reference the automation spec from `/automate` (or create one if needed)
3. Build the proposal with:
   - Executive summary (their pain point → your solution)
   - Scope: what you're automating, what's in/out of scope
   - Deliverables: workflows built, integrations configured, testing, training
   - Timeline: estimate hours/days to build
   - Success metrics: time saved, errors reduced, revenue gained
   - Pricing: based on complexity and effort
   - Payment terms and next steps

4. Show draft for feedback before sending

Example: `/proposal ABC Real Estate Group lead follow-up automation`

### `/proposal pricing [complexity]` - Get pricing guidance

Complexity tiers for pricing:

- **Simple** (4-8 hours): Single-tool workflows, straightforward triggers/actions
  - Example: Zapier automation to email leads on form submission
  - Price range: $500–$1,500

- **Standard** (12-20 hours): Multi-step workflows, 2-3 tool integrations, some data mapping
  - Example: Lead capture → CRM → email sequence → calendar sync
  - Price range: $2,000–$5,000

- **Complex** (25-40 hours): Advanced logic, multiple system integrations, error handling, custom code
  - Example: Multi-step lead scoring, dynamic CRM sync, conditional routing
  - Price range: $5,000–$15,000

- **Enterprise** (40+ hours): Custom builds, multiple integrations, training, ongoing support
  - Example: Full real estate workflow, agent dashboard, reporting
  - Price range: $15,000–$50,000+

When you give the complexity, it returns:

- Estimated build hours
- Suggested price range
- What's included (design, build, testing, training, docs)
- Support and maintenance costs (if applicable)

Example: `/proposal pricing standard`

### `/proposal template [type]` - Load a proposal template

Supported templates:

- **standard** — general automation proposal
- **retainer** — ongoing automation maintenance/optimization
- **integration** — connecting specific systems
- **training** — teaching a team to use built automations

Example: `/proposal template retainer`

---

## Proposal Structure

Use this outline when drafting:

```
# Proposal: [Project Name] for [Company Name]

## Executive Summary
[1-2 sentences: their pain point + your solution]

## Current State
[What they're doing now, time/cost waste, bottlenecks]

## What We'll Build
[The automation, step by step in plain language]

## Scope
- IN SCOPE
  - [Deliverable 1]
  - [Deliverable 2]
- OUT OF SCOPE
  - [What you're NOT doing, set expectations]

## Deliverables
- [Workflow design and approval]
- [Build and integration in Make/Zapier/etc.]
- [Testing and QA]
- [Documentation and runbooks]
- [Training session for your team]
- [30 days of support included]

## Timeline
[X weeks, broken into: design → build → test → launch]

## Success Metrics
- Time saved per week: [X hours]
- Error reduction: [X%]
- Revenue impact: [if applicable]

## Investment
[Total project cost]

## Terms
- 50% deposit to start, 50% on completion
- Timeline: [Start date] – [End date]
- Support: [30 days included, then $X/month]

## Next Steps
1. You review and provide feedback
2. We refine scope if needed
3. Sign and schedule kickoff

Questions? Let's hop on a call. [Link to calendar]
```

---

## Pricing Rules

- **Build time is your core value.** Price for complexity and speed, not hourly labor.
- **Include 30 days of support.** Automations break; be there to fix them.
- **Retainers beat one-shots.** Offer ongoing optimization ($500-2k/month) after project launch.
- **Document everything.** Runbooks and training reduce support burden.
- **Real estate premium.** RE clients often have higher budgets and faster timelines; price accordingly.

---

## Proposal Tracking

After you send a proposal, log it in `wiki/entities/[prospect-slug].md`:

- Proposal sent: [date]
- Amount: $[X]
- Due date for response: [date]
- Status: sent | accepted | negotiating | rejected

Update prospect status with `/prospect update [name] proposal-sent`.

---

## Retainer Model

For ongoing clients, offer a retainer tier:

- **Optimization Retainer** ($500–$2k/month)
  - Monitor workflows, catch failures
  - Optimize automations quarterly
  - Add new integrations as needed
  - Consulting on new processes

Position retainers after the first project closes. It keeps clients engaged and provides recurring revenue.
