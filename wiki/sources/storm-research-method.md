---
title: Stanford's Method Turns Claude Into a PHD Level Research Team
type: source
tags: [claude-code, research, skills, agents]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# Stanford's Method Turns Claude Into a PHD Level Research Team

**Creator:** Nate Herk | AI Automation (35.9K views, 1,363 likes)
**Published:** 2026-06-29
**URL:** https://www.youtube.com/watch?v=Tj3018n5MVg
**Duration:** 12 min
**Ingested:** 2026-07-01 (full transcript)

Same channel as [[Build & Sell with Claude Code (10hr Course) - Nate Herk]]. Short, high-density video: builds a Claude Code skill implementing Stanford's **STORM** research method (peer-reviewed, ~25% more organized output than single-pass research).

## What This Updated
- Built `.claude/skills/storm-research/` — `SKILL.md` + `references/report_template.html` — a new, real capability, not just notes
- Created [[STORM Multi-Perspective Research Method]] concept page
- Updated wiki index, log, and CLAUDE.md skills list

## Key Takeaways
- Core method: 5 persona sub-agents in parallel (practitioner, academic, skeptic, economist, historian) research the same topic → contradiction mapping (where they disagree, whose evidence is stronger) → synthesis into a single HTML report → adversarial peer review + citation verification → V2 (verified) output
- Beat Claude Code's native "deep research" (100+ agents) head-to-head on evidence quality, source diversity, and actionability, while running only ~10-12 agents total — cheaper, faster, no rate-limit issues
- Key distinction reinforced: **sub-agents** report only to the main session and can't talk to each other; **agent teams** can message/debate each other directly (more expensive, better for genuine disagreement resolution)
- Explicitly designed to be tailored: tell the skill your business context so findings translate into "what should we do differently," not a generic brain dump
- Suggests adding extra lenses beyond the default five when the topic calls for it (his example: a "beginner in AI" or "content creator" lens for his own use case)

## Applied Here
Built as a real skill (`/storm-research` invokable) rather than just documented, since this is directly usable for market/competitor research where a single Perplexity query would leave blind spots — the exact category of work already done in [[Competitor Landscape]] and [[Chicago Prospect Analysis]]. Added a 6th "buyer/seller/agent" lens as an option in the skill instructions, matching the video's own suggestion to customize the lens set per use case.
