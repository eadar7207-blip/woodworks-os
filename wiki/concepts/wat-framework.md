---
title: WAT Framework
type: concept
tags: [claude-code, workflow, architecture]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# WAT Framework (Workflows / Agent / Tools)

Documented in this repo's root `CLAUDE.md` under "Automation Execution." Separates three concerns when building automations:

- **Workflows** (`workflows/`) — markdown SOPs for recurring tasks: objective, inputs, tools to use, edge cases. Updated when a better method is found or a constraint is discovered.
- **Tools** (`tools/`) — Python scripts for deterministic execution: API calls, data transforms, file ops. Credentials only ever go in `.env`.
- **Agent** (Claude) — reads the relevant workflow, calls the right tools in sequence, handles failures, asks when unsure.

**Rule:** don't create or overwrite workflows without being asked — they're instructions, not throwaway notes. When a script fails, fix it, verify it works, then update the workflow so it doesn't happen again.

## Validation

[[Build & Sell with Claude Code (10hr Course) - Nate Herk]] independently teaches the same three-layer split (CLAUDE.md as system prompt + `workflows/*.md` + `tools/*.py` or `src/trigger/*.ts`) as the core pattern across every automation built in that 10-hour course. Confirms this repo's architecture matches what's being taught/sold as best practice elsewhere — no changes made as a result, just a validation point.

## Related
- [[Automation Framework]] — the YAML-based orchestration layer built on top of this (replaces N8N for this agency)
- [[Claude Code Power Techniques]]
