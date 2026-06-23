---
name: content
description: Generate marketing and sales content — landing pages, emails, social posts, case studies, ad copy
---

# Content

Generate high-converting content for your automation agency. Works with brief outlines or detailed specs.

---

## Operations

### `/content [type] [brief]` - Generate content from a brief

Supported types:
- **email** — outreach or nurture email
- **post** — LinkedIn, Twitter, or social post
- **landing** — sales page section or full page copy
- **case** — case study or client success story
- **sales** — pitch deck talking points or sales script
- **guide** — educational guide or whitepaper section

Example: `/content email cold outreach for real estate agents`

When the user gives a brief:

1. Ask clarifying questions if needed (audience, tone, length, any specific claims or stats)
2. Pull relevant context from `wiki/entities/` (your clients, their pain points) and `wiki/concepts/` (positioning, value props)
3. Draft the content in the specified format
4. Show it to the user for feedback before saving

### `/content [url or file]` - Analyze and improve existing content

When the user points to existing content:

1. Read the content fully
2. Identify: tone, structure, missing elements, weak claims
3. Suggest improvements (stronger hook, proof elements, call-to-action clarity)
4. Draft a revised version if the user asks

---

## Content Rules

- **Agency positioning:** You solve business problems with automation. Lead with outcomes (time saved, revenue gained), not features.
- **Audience:** Usually business owners, ops managers, or decision-makers. Speak to their constraints (budget, time, risk).
- **Real estate angle:** If positioning for RE, emphasize automating tedious agent workflows (lead follow-up, document prep, CRM syncing).
- **Proof:** Use specific numbers where possible. "Save 10 hours/week" beats "save time."
- **CTAs:** Always end with a clear next step (book a call, watch demo, reply with questions).

---

## Content Library

After you generate content, file it in `projects/` under the relevant project, with a note in the wiki log.

Format: `projects/[project-name]/content/[type]_[date].md`

Keep a running list in `wiki/synthesis/content-audit.md` if you want to track what's been generated.
