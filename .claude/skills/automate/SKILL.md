---
name: automate
description: Design and scope automation builds — map workflows, pick tools, plan implementation
---

# Automate

Think through an automation build from problem to implementation. Works for any business process.

---

## Operations

### `/automate [process description]` - Design an automation

When the user describes a business process or pain point:

1. Map the current workflow:
   - What triggers the process?
   - What are the manual steps?
   - What's the desired outcome?
   - How often does it happen?

2. Identify automation opportunities:
   - Which steps can be automated?
   - Where do you need human approval?
   - What data moves between systems?

3. Recommend tools:
   - Make, Zapier, n8n for low-code/no-code
   - Custom APIs if complex
   - Consider: cost, complexity, reliability, their existing stack

4. Draft the automation flow:
   - Trigger → action sequence
   - Error handling and fallbacks
   - Data mapping and transformations

5. Scope the work:
   - Estimated hours to build
   - Maintenance needs
   - Testing checklist

6. Present to user for feedback

Example: `/automate real estate agents spending 2 hours daily on lead follow-up`

### `/automate [tool] [brief]` - Build in a specific tool

When the user names a tool (Make, Zapier, n8n) and a scenario:

1. Check the wiki for past automation patterns and lessons learned
2. Outline the scenario module-by-module
3. Identify data sources (CRM, email, calendar, forms)
4. Show the full flow before building
5. Note any gotchas or edge cases

Example: `/automate Make automatically log cold emails to Airtable with sentiment scoring`

---

## Automation Best Practices

- **Start simple:** Get one flow working, then layer on complexity
- **Test first:** Always test with real (or realistic) data before going live
- **Document it:** Future you (or a team member) will need to understand it
- **Monitor:** Set up alerts for failed runs, then adjust
- **Version control:** Keep notes on what changed and why in the wiki log

---

## Common Real Estate Automations

Keep these patterns in your wiki for fast reference:

- Lead capture → CRM → follow-up sequence
- Listing notifications → client alert email
- Contract signing → document filing + calendar reminder
- Showing request → photographer + agent calendar sync
- Feedback form → listing update + agent notification

---

## File Automations

After you design an automation, save the spec in:

`projects/[project-name]/automations/[process]_[date].md`

Include: trigger, steps, tools, data sources, error handling.

Reference past automations in `/automate` calls to avoid rebuilding the wheel.
