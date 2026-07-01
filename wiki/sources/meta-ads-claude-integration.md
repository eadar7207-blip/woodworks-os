---
title: Meta Officially Integrated Claude Into Facebook Ads (YouTube ingest)
type: source
tags: [meta-ads, mcp, automation-agency, real-estate-lead-gen]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# Meta Officially Integrated Claude Into Facebook Ads

**Video:** youtube.com/watch?v=DIe1uYwHBBo (dropshipping/e-com ads channel, ~$20M ad spend experience)

## Key Takeaways

- Meta released an **official MCP connector** for Claude → Meta Ads (replaces earlier unofficial connectors that got accounts banned in early 2026)
- Creator's pattern: a Claude Project = a named specialist persona ("Jordan," the media buyer) with saved instructions, called via a trigger phrase, connected live to the ad account via MCP
- **Diagnostic workflow**: pulls live account data, root-causes problems (not just symptoms) — e.g. too many new campaign launches resetting Meta's learning phase, high CPMs signaling creative isn't landing, strong add-to-cart/lead-form starts but weak completion signaling a **landing-page trust problem, not an ad problem**
- **Campaign build workflow**: CBO (Campaign Budget Optimization) structure, purchase/lead conversion event (not engagement), head-to-head audience test (proven winner vs. broad), creative variations with different hooks, 48-hour KPI gate
- **7-day management cadence**: days 1-2 hands-off data collection, day 3 first decision checkpoint, days 4-5 optimize without launching new campaigns, days 6-7 scale-or-kill
- Heavy promotional content in the video (Dodo/DTO store domains, EcomBoss UGC tool) — not relevant, skipped

## What This Updated

- Built [[Meta Ads Media Buyer Skill]](../concepts/meta-ads-media-buyer-skill.md) — `.claude/skills/meta-ads/SKILL.md`, invoked via `/ads`
- Confirmed the official Meta Ads MCP connector (`mcp__claude_ai_Facebook_Ads__*`) is already linked to eadar7207@gmail.com — one ad account found (`1721146352562942`, ILS, `is_ads_mcp_enabled: false` — Meta still gradually rolling out write access per-account)

## Notes

- Case study was dropshipping, not real estate — the skill built from this adapts the audit/build/manage pattern to real estate lead-gen terms (cost-per-lead, lead-form completion, listing/open-house creative angles) rather than e-com terms (add-to-cart, checkout)
- This is a sellable service angle: free diagnostic audit as a lead magnet → paid campaign build/management retainer, same shape as the PRICE framework in [[AI Agency Client Acquisition and Pricing]]
