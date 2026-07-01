---
title: Build & Sell with Claude Code (10hr Course) - Nate Herk
type: source
tags: [claude-code, automation, mcp, skills, agency, pricing]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# Build & Sell with Claude Code (10+ Hour Course)

**Creator:** Nate Herk | AI Automation (793K views, 27.7K likes)
**Published:** 2026-03-12
**URL:** https://www.youtube.com/watch?v=mpALXah_PBg
**Ingested:** 2026-07-01 (full transcript, all ~10 hours)

Full build-and-sell course: uses Claude Code to build automations/agents, deploys them to production (Modal, Trigger.dev), then teaches how to price and sell them as a service business. High overlap with what [[Adar Realty Studio]] is already doing — validates several architectural choices already made here and fills a few real gaps.

## What This Updated
- Installed **Context7 MCP** server (up-to-date library docs, avoids stale training-data APIs) — genuinely missing capability, free/no-auth
- Created [[Claude Code Power Techniques]]
- Created [[AI Agency Client Acquisition and Pricing]]
- Added `.claude/rules/deployment-security.md`

## Key Takeaways

**Architecture validation:** the course's core pattern — CLAUDE.md (system prompt) + `workflows/*.md` (SOPs) + `tools/*.py` (executable scripts), self-improving loop where the agent edits its own tools/workflows on failure — is exactly the [[WAT Framework]] already documented in this repo's root CLAUDE.md. No changes needed there; it's confirmation the existing approach matches what a course selling for money teaches.

**Deployment gap:** course deploys automations to **Modal** (Python, pay-per-execution, cron/webhook triggers) or **Trigger.dev** (TypeScript, built-in retries/queuing/orchestration, preferred by the end of the course for reliability). This repo currently uses Anthropic cloud triggers + systemd for the YouTube Intelligence Pipeline. Not migrating — current setup works — but if a future automation needs heavier retry/queue guarantees, Trigger.dev is the documented upgrade path. Not installed since it requires a new account/API key the user hasn't provisioned.

**Skills already covered by what's installed:** front-end design skill, canvas design skill, skill-creator — all already present as Anthropic official skills in `.claude/skills/`. No action needed.

**Skills/tools NOT installed (niche, low relevance, skipped deliberately):**
- n8n + n8n MCP — this repo doesn't use n8n, it uses Python tools directly (per WAT framework); skipping
- Pinecone + Gemini Embedding 2 (multimodal RAG demos) — no current use case
- Google Workspace CLI (`gws`) — redundant with existing Gmail/Drive MCP connectors already live in this environment
- Excalidraw skill, Blotato MCP, 21st.dev component library, Kie.ai/Nano Banana image gen — content-creation extras with no immediate business need
- Pixel Agents VS Code extension (visualizes agents as pixel characters) — cosmetic, Windows-only, skipped
- Agent Teams (`/team create`, experimental multi-agent messaging) — real feature, worth knowing about, not enabled by default (requires a `settings.json` experimental flag) — noted in [[Claude Code Power Techniques]] but not turned on

**Selling framework — highest-value section for this business:** hours 8-10 are almost entirely about pricing and client acquisition for exactly this kind of AI automation agency. Captured in full in [[AI Agency Client Acquisition and Pricing]] — covers the PRICE framework, value-based retainer pricing (10-15% of year-1 savings), the "Trojan horse" partner-referral method, and a 7-day cold-to-closed client acquisition framework. This is directly applicable to the "make money" top priority and worth revisiting before the next prospect conversation.

## Notable Data Points
- Value-based pricing worked example: $38,400/yr in diagnosed labor savings → priced at 15% = $5,500 one-time/retainer anchor
- Referral ask stat cited: only 11% of salespeople ask for referrals despite 91% of clients being willing to give one
- Partner/reseller ("Trojan horse") deals cited as closing 46% faster than cold outreach
- Retainer range cited: $1,500-$15,000/mo, target 50-70% margin, 50% floor
