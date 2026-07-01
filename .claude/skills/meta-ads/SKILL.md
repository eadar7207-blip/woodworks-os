# /ads — Meta Ads Media Buyer

Run Meta (Facebook/Instagram) ad accounts for yourself or clients using the official Meta Ads MCP connector. Modeled on the "Jordan" media-buyer persona pattern from the Nate Herk-style video ingest (2026-07-01): diagnose the account, build a campaign blueprint, then run a 7-day management cadence. Adapted here for real estate lead gen (listings, open houses, buyer/seller leads) instead of dropshipping.

Source: [[wiki/sources/meta-ads-claude-integration.md]]

## Connection status

This skill uses the `mcp__claude_ai_Facebook_Ads__*` tools (official Meta-authorized connector, already linked to eadar7207@gmail.com — no separate OAuth setup needed).

Before running anything, call `ads_get_ad_accounts` to confirm which account you're working on. Check `is_ads_mcp_enabled` on the result:
- If `false`, the account can't be written to yet (Meta is gradually rolling out MCP access per-account) — surface `is_ads_mcp_disabled_reason` to the user and stop.
- If a client's account, you need to be added to their Business Manager first, then re-run `ads_get_ad_accounts` to confirm it shows up with `is_ads_mcp_enabled: true`.

**Never proceed to campaign creation or budget changes without explicit user confirmation** — this moves real money and is visible to the client. Diagnostics/read-only calls don't need confirmation; anything that creates or edits a campaign, ad set, ad, or budget does.

## Use when

- User wants a Meta ad account audited (theirs or a client's)
- User wants a new campaign built from scratch or from audit findings
- User wants ongoing campaign management following the 7-day cadence
- User is pitching a real estate client on ads management as a service

## Syntax

```
/ads audit [account name or id]
/ads build [account name or id]
/ads manage [account name or id]        — run the day-appropriate step of the 7-day cadence
/ads accounts                            — list connected ad accounts
```

## Operation 1: Audit (diagnostic)

Read-only. Pulls live account data and produces a root-cause report, not just symptoms.

1. `ads_get_ad_accounts` → confirm target account, `is_ads_mcp_enabled: true`
2. `ads_get_ad_entities` / insights tools → pull campaigns, ad sets, ads, and performance for the lookback window (default: since account start or last 30 days)
3. Check for these specific failure patterns (from the source video, adapted to real estate lead gen):
   - **Learning-phase resets**: count new campaign launches in the window. Every new campaign resets Meta's learning phase — if the account is launching new campaigns frequently instead of feeding winners, flag this as the #1 problem before looking at anything else.
   - **CPM health**: compare CPM against a benchmark (~$15–$45 is healthy for most local real estate targeting; above that signals creative isn't resonating with the audience — flag it).
   - **Funnel drop-off vs. landing page problem**: if lead-form starts (or link clicks) are healthy but form completions / appointment bookings are weak, call this out as a **landing page / trust problem, not an ad problem** — check for: no clear agent photo/credentials, no reviews/testimonials, no clear CTA above the fold, slow load, unclear next step after form submit. Do not recommend just running more ad spend to fix a landing page problem.
   - **Conversion event correctness**: verify the account is optimizing for the actual business outcome (lead form complete / appointment booked), not vanity events (engagement, video views, link clicks).
4. Output format — bottom line first, then root causes ranked by impact, then 2–3 concrete fixes ranked by priority, then a set of 48-hour KPI targets to gate the next decision (CPM ceiling, lead-form completion rate floor, cost-per-lead ceiling).

## Operation 2: Build (campaign blueprint)

Only after an audit, or if the user explicitly wants a fresh campaign. Requires explicit confirmation before actually creating anything live.

Structure to propose:
- **Objective**: Leads (lead form) or Sales, with the conversion event set to the real business outcome — not engagement/traffic
- **Budget structure**: single CBO (Campaign Budget Optimization) campaign rather than per-ad-set fixed budgets, so Meta's algorithm allocates spend to the best-performing ad set. Minimum viable daily budget: enough that Meta has real signal to optimize on — ballpark $30–50/day starting point for local real estate, confirm with user based on their actual budget.
- **Ad set test structure**: head-to-head — one ad set using the proven/winning audience (from audit findings or past performance), one broad ad set with minimal targeting (age + location only) to let Meta's algorithm find buyers/sellers on its own.
- **Creative**: keep the proven creative format as a base, add 2–4 variations with different opening hooks (different pain points: "just listed," "price drop," "open house this weekend," agent-credibility angle). Real estate creative should lead with the property/neighborhood, not generic branding.
- **KPI gate**: define the same 48-hour thresholds as the audit (CPM ceiling, lead-form completion rate, cost-per-lead ceiling) — these decide whether the campaign lives or dies at the next checkpoint.

Before calling any create/write tool, present the full blueprint to the user and get a go-ahead — this is spending real money on their behalf.

## Operation 3: Manage (7-day cadence)

Track which day of the cycle the campaign is on (store in wiki or ask the user) and run the matching step:

| Day | Action |
|---|---|
| 1–2 | Hands off. Don't touch the campaign. Monitor CPM only — Meta needs uninterrupted signal to leave the learning phase. |
| 3 | First decision checkpoint. Pull lead-form completion rate and cost-per-lead, compare against the KPI gate set at launch. Report pass/fail — don't change anything yet unless it's a clear failure. |
| 4–5 | Optimization window. Kill underperforming ads within the campaign, shift budget toward winners. **Do not launch new campaigns** — that resets the learning phase and wastes the signal already built up. |
| 6–7 | Scale-or-kill decision. If KPIs are met, scale budget up (recommend %, don't just double blindly). If not met after the optimization window, recommend killing the campaign and report exactly what failed and why (ad-level, audience-level, or landing-page-level). |

Always report findings in the same "bottom line → root cause → fix" structure as the audit, so results stay consistent whether you're auditing or managing.

## Guardrails

- This is real client money — never create/edit a live campaign, ad set, or budget without explicit confirmation in the current turn.
- If `is_ads_mcp_enabled` is `false` for an account, do not attempt writes against it — surface the reason and stop.
- If this ever gets wired into a scheduled/automated trigger (e.g. auto-scaling budgets on a cron), that requires the security review in `.claude/rules/deployment-security.md` first — this skill as built is interactive/on-demand only, not scheduled.
- Don't recommend ad-spend increases as a fix for a landing-page/trust problem — diagnose which layer (ad, audience, landing page) is actually broken before prescribing spend.
