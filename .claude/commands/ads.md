---
description: Audit, build, and manage Meta (Facebook/Instagram) ad campaigns for real estate clients using the official Meta Ads MCP connector
---

# /ads

Run Meta ad accounts — for yourself or clients — end to end: diagnostic audit, campaign blueprint, and a 7-day management cadence. Uses the official Meta-authorized MCP connector (already linked, no separate setup).

Read `.claude/skills/meta-ads/SKILL.md` for full operations and guidelines, then follow the instructions there based on what the user asks for.

Supported operations:
- `/ads accounts` — list connected ad accounts and their MCP-enabled status
- `/ads audit [account name or id]` — root-cause diagnostic on a live account (read-only)
- `/ads build [account name or id]` — propose a campaign blueprint from audit findings (requires confirmation before creating anything live)
- `/ads manage [account name or id]` — run the day-appropriate step of the 7-day management cadence
