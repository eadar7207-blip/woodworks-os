---
title: Meta Ads Media Buyer Skill
type: concept
tags: [meta-ads, mcp, automation, real-estate-lead-gen]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# Meta Ads Media Buyer Skill

## What It Is

`/ads` — a Claude Code skill (`.claude/skills/meta-ads/SKILL.md`) that audits, builds, and manages Meta (Facebook/Instagram) ad campaigns using the official Meta Ads MCP connector (`mcp__claude_ai_Facebook_Ads__*`, already linked to eadar7207@gmail.com, no extra setup needed).

Three operations:
- **Audit** — read-only diagnostic. Root-causes account problems: learning-phase resets from too-frequent campaign launches, unhealthy CPM, funnel drop-off (flags landing-page/trust issues separately from ad issues), wrong conversion event.
- **Build** — proposes a campaign blueprint (CBO structure, lead/purchase conversion objective, proven-vs-broad audience test, creative hook variations, 48-hour KPI gate). Requires explicit user confirmation before creating anything live — real client money.
- **Manage** — runs a 7-day cadence (hands-off data collection → decision checkpoint → optimize → scale-or-kill), reporting in the same bottom-line-first structure as the audit.

## Why It Matters to Eitan

- Directly sellable to real estate clients who run (or should run) Meta ads for listings/lead gen — the free-audit-as-lead-magnet motion matches the PRICE / Trojan-horse pricing framework already in the wiki
- First skill wired directly into a live external MCP connector (not just internal scripts) — proof of pattern for future client-account integrations

## Guardrails Built In

- Never writes/creates a live campaign or budget change without explicit confirmation in the same turn (per general risk-of-real-money handling)
- Checks `is_ads_mcp_enabled` before any write — Meta is still gradually rolling out MCP write access per account
- If ever turned into a scheduled/cron automation (e.g. auto-scaling budgets), must go through the deployment-security review first — as built, it's interactive/on-demand only

## Related

- [[Meta Officially Integrated Claude Into Facebook Ads (YouTube ingest)]](../sources/meta-ads-claude-integration.md) — source video this was built from
- [[AI Agency Client Acquisition and Pricing]] — pricing/acquisition framework this service angle fits into
- [[WAT Framework]] — this skill is MCP-driven rather than python-tool-driven since Meta's connector already exposes the API surface directly
