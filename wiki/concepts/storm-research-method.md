---
title: STORM Multi-Perspective Research Method
type: concept
tags: [research, agents, skills]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# STORM Multi-Perspective Research Method

A research method (Stanford, peer-reviewed) that trades a single research pass for five parallel personas that are then forced to contradict and check each other before anything is trusted. Implemented in this repo as the `/storm-research` skill (`.claude/skills/storm-research/`).

## Why it matters here
A single Perplexity query or one-shot research prompt has blind spots — it only looks from one angle. This method's insight isn't the specific five personas, it's the structural idea: **agreement across independent angles is weak signal, disagreement is where the real information is.** Forcing contradiction, then adjudicating it with evidence, produces a more reliable answer than aggregating more of the same angle.

## The five default lenses
- **Practitioner** — on-the-ground, day-to-day reality
- **Academic** — what's rigorously established in the literature vs. anecdotal
- **Skeptic** — the counter-case, where hype outruns evidence
- **Economist** — costs, incentives, ROI, who profits from which narrative
- **Historian** — precedent, what happened last time this was tried

Lenses aren't fixed — add or swap one when the topic calls for it (e.g. a buyer/seller/agent lens for real estate topics, since the stock five all view a business from the owner's chair).

## Pipeline
1. Scope the topic (ask clarifying questions if vague — this is an expensive pipeline, don't run it on an underspecified question)
2. 5 lenses research in parallel (sub-agents, not agent teams — they report to the main session but don't talk to each other)
3. Contradiction mapping — where do they disagree, which side has stronger evidence
4. Synthesis into one report
5. Adversarial peer review — separate pass whose only job is to verify every citation and flag/correct/demote anything that doesn't hold up
6. Ship V2 (verified), never V1 (raw synthesis)
7. Explicit "missing lens" callout at the end — does the report have a structural blind spot even after 5 lenses?

## Sub-agents vs agent teams (reinforced by this source)
- **Sub-agents** (used here) — isolated, parallel, report only to the main thread, cannot talk to each other. Cheaper, predictable, right fit for "research this from N angles."
- **Agent teams** — can message/debate each other directly, better when you need agents to actually argue toward consensus rather than just report independently. More expensive. Right fit for decisions, not raw research gathering.

## Where to use it in this business
- Market/farm-area research before a listing pitch or prospect conversation
- Competitor deep-dives — extends [[Competitor Analysis Skill]] rather than replacing it (competitor-analysis is templated/repeatable monthly; storm-research is for a specific high-stakes question)
- Anywhere a single-angle research pass has previously produced a one-sided or later-corrected finding

## Related
- [[Stanford's Method Turns Claude Into a PHD Level Research Team]] — full source
- [[Claude Code Power Techniques]] — sub-agents vs agent teams distinction, cross-referenced here
- [[Competitor Analysis Skill]]
