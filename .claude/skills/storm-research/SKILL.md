---
name: storm-research
description: Turns one research topic into a verified, multi-perspective HTML briefing using Stanford's STORM method. Simulates five expert lenses (practitioner, academic, skeptic, economist, historian), maps where they contradict each other, synthesizes into a single report, adversarially peer-reviews its own output, and verifies every citation before delivering. Use when a single-angle search or Perplexity query would leave blind spots — market research, competitor deep-dives, a farm-area/neighborhood study, or any topic where you need multiple angles to disagree with each other before you trust the answer. Not for quick lookups; this is a deliberate, slower research pass.
---

# Storm Research

Multi-perspective research pipeline adapted from Stanford's STORM method (peer-reviewed to produce ~25% more organized output than single-pass research). Source: [[Build & Sell with Claude Code (10hr Course) - Nate Herk]] video "Stanford's Method Turns Claude Into a PHD Level Research Team."

The core idea: a single research prompt has blind spots. Five personas with different priorities, run in parallel, each catch something the others miss — then they get forced to argue with each other before anything is trusted.

## When to use this vs a normal research skill
- Use `storm-research` when the topic matters enough to be worth 5-10x the tokens of a single search, and where getting it wrong (or one-sided) has real cost — e.g. before a pricing decision, before pitching a prospect on a market thesis, before publishing analysis externally.
- Don't use it for quick fact lookups, status checks, or anything `/prospect` or a single Perplexity/WebSearch call already handles well.

## Pipeline

### Phase 0 — Scope the topic
If the user's topic is vague, ask clarifying questions before starting: what's the topic, who's the reader (you, a prospect, external content), and what decision does this research inform. Don't run five expensive agents against an under-specified question.

### Phase 1 — Five expert lenses (parallel sub-agents)
Spin up five sub-agents in parallel, each researching the same topic from a distinct persona. Give each one the topic, the reader/decision context from Phase 0, and its specific lens:

- **Practitioner** — what does this look like in day-to-day, on-the-ground practice? What do people who actually do this say?
- **Academic** — what does the research/literature say? What's rigorously established vs. anecdotal?
- **Skeptic** — what's the counter-case? Where is the hype outrunning the evidence? What would a critic say?
- **Economist** — what are the costs, incentives, ROI, and market dynamics? Who profits from which narrative?
- **Historian** — what's the precedent? What happened last time something like this was tried, and how did it play out?

Each sub-agent should use web search / read tools to actually research (not just reason from priors) and return findings with sources.

### Phase 2 — Contradiction mapping
Once all five lenses report back, analyze where they disagree. For each point of disagreement: which side has stronger evidence, which is weaker, and why. This is the step that actually produces insight — agreement across all five lenses is low-value confirmation; disagreement is where the real signal is.

### Phase 3 — Synthesis
Merge the five perspectives plus the contradiction map into a single coherent report using `references/report_template.html` as the structure. Every claim should be traceable to which lens(es) supported it.

### Phase 4 — Adversarial peer review + citation verification
Run a second pass (2-3 more sub-agents) whose only job is to attack the draft: verify every citation against its primary source, and flag/correct/demote anything that doesn't hold up. Mark each source as **confirmed**, **corrected**, or **demoted**. This is what separates V1 (raw synthesis) from V2 (verified) — always ship V2, not V1.

### Output
A single self-contained HTML file matching `references/report_template.html`:
- 60-second summary at the top
- Key findings, each tagged with a reliability score (e.g. "High 9/10 — supported by academic + skeptic, challenged by practitioner + economist")
- Full body organized by theme, not by persona
- An explicit "missing lens" callout — after producing the report, ask whether all five lenses actually cover the question, or whether a sixth lens is needed (e.g. a customer/frontline-employee lens if all five looked at something from the owner's chair)
- Sources list at the bottom, tagged confirmed/corrected/demoted

## Tailoring
Before running, tell the skill your business context (Adar Realty Studio — AI automation agency, real estate niche, top priority is revenue) so findings translate into "what should we do differently" rather than a generic brain dump. If a topic calls for it, add a 6th lens (e.g. a **buyer/seller** or **real estate agent** perspective) — the five lenses above are a default, not a fixed set.

## Cost note
Sub-agents (this pipeline) are cheaper and more predictable than Claude Code's native deep-research feature, which can spin up 100+ agents and hit rate limits. This pipeline runs ~10-12 agents total (5 research + contradiction mapping + 2-3 verification) — model choice (Haiku/Sonnet/Opus) for the sub-agents is a cost/quality tradeoff to set based on how much the decision riding on this research matters.
