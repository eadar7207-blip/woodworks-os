---
title: AI Agency Client Acquisition and Pricing
type: concept
tags: [sales, pricing, agency, strategy]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# AI Agency Client Acquisition and Pricing

Sales/pricing framework from [[Build & Sell with Claude Code (10hr Course) - Nate Herk]] (hours 8-10), directly applicable to the top priority: make money. This is a well-known playbook in the AI automation agency space — treat it as a starting framework to test against real conversations, not gospel.

## Core thesis
Sell **outcomes tied to a diagnosed pain**, not "AI agents" or "workflows." Agents/workflows are commoditized and race to the bottom on price. Businesses only care about three things: time, money, focus. Lead with those, not the tech stack.

## PRICE framework
- **P**repare — research the prospect before the call
- **R**esearch — diagnose the actual pain (not the pain they think they have)
- **I**dentify ROI — quantify the cost of the current pain in dollars/hours
- **C**ommunicate — present the diagnosis and solution in their language, not tech language
- **E**xpand — retainers, maintenance, and upsells after the first win

## Value-based pricing
- Price at **10-15% of first-year savings** — target the client seeing roughly 10x ROI in year one.
- Worked example from the course: $38,400/yr in diagnosed labor savings → priced at 15% = $5,500.
- Retainers, not hourly — milestone-based billing positions you as a consultant, not a freelancer.
- Retainer range: **$1,500-$15,000/mo**. Target 50-70% margin, 50% is the floor.
- Recurring add-ons after the initial project: flat maintenance fee ($200-1,500/mo), monitoring/optimization, expansion projects priced at 10-25% of the original project cost.

## Client acquisition — three channels
1. **Cold outreach** — needs proof/case studies first. ~100 messages/day across LinkedIn, email, Reddit, relevant FB groups. Use ChatGPT/Perplexity to find niche-specific prospect directories before defaulting to Apollo/Sales Navigator.
2. **Referrals** — ask 1-2 months post-launch, tied to a results review conversation. Cited stat: only 11% of salespeople ask for referrals despite 91% of clients being willing to give one. This is the cheapest channel and most agencies just don't ask.
3. **"Trojan horse" / partner method** — partner with agencies or consultants who already have client trust. Offer free AI audits to their existing clients in exchange for a revenue share (~20% cited). Partner-sourced deals reportedly close 46% faster than cold outreach.

## 7-day cold-to-closed framework (case study cited: first client closed day 5, $1,500 → $2,000)
1. Day 1 — pick a loose niche, map ~20 warm contacts
2. Days 2-3 — warm, low-pressure conversations (no pitch)
3. Days 4-5 — propose a free pilot
4. Days 5-6 — build a tiny MVP fast
5. Day 7 — propose maintenance/expansion, then ask for a testimonial/referral

## Delivery/legal structure (stated as provider-agnostic, was framed around n8n but applies generally)
- Client should own the hosting instance — their account, their API keys, their billing. You build inside their instance. Avoids becoming a "billing babysitter" and simplifies IP/liability.
- IP split: client owns the final work product; you retain rights to reusable generic components/templates you built along the way.
- Security basics to have in place before handing off: encrypted-at-rest credentials, webhook signature verification, data-minimization if any EU/GDPR-relevant data is involved, a data processing agreement if applicable.
- QA/handover pipeline before calling anything done: internal QA (test with dozens/hundreds of sample inputs, log to a sheet) → client-facing QA (simple chat/form UI) → move test env to prod with versioned backups → Loom walkthrough + written documentation handover.

## How this applies here
- [[Adar Realty Studio]]'s current model (shadowing → automation → agent → sales) lines up with "diagnose pain before pitching" — the Sohail shadowing phase is effectively unpaid PRICE-framework research.
- Worth pricing future automation proposals against the 10-15%-of-savings anchor instead of flat project fees, once a client's actual cost baseline is known.
- The referral-ask stat is a concrete, cheap action: any client with a completed engagement should get an explicit referral ask, not an implicit hope.

## Related
- [[Build & Sell with Claude Code (10hr Course) - Nate Herk]] — full source
- [[Adar Realty Studio]]
