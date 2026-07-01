---
title: "Being the Director of Your Coding Agents — Nate Herk x Cole Medin"
type: source
tags: [claude-code, context-management, security, harness-engineering, podcast]
created: 2026-07-01
updated: 2026-07-01
sources: 1
---

# Being the Director of Your Coding Agents (Nate Herk podcast w/ Cole Medin)

YouTube: https://www.youtube.com/watch?v=RzLV8sfFdMM — 68 min podcast, Nate Herk interviewing Cole Medin (200K subs, YouTube channel + AI community, background in software engineering).

## Key Takeaways

- **The "dumb zone":** every LLM has a token count past which quality degrades even though it isn't at the stated context limit. Cole's numbers: Opus ~250K tokens, Opus 4.7 was ~200K, Sonnet 4.6 only ~100-125K. The 1M-token headline number creates a false sense of security — you never want to get close to it. Same "needle in a haystack" / lost-in-the-middle effect [[Claude Code Power Techniques]] already notes as "context rot."
- **Plan → build → verify → evolve loop:** the four-step framework for any agentic work, not just code. Most people skip planning and verification and just "prompt and pray." Verification means having the agent prove its own work is done (unit tests, screenshots, rendering a diagram to PNG and checking it, running the app and using it like a user would) — not just trusting its self-report.
- **Harness vs AI layer:** the harness is the wrapper around the model (Claude Code itself — system prompt + tools). The AI layer is what you build on top: CLAUDE.md, skills, hooks, MCP servers. This repo's structure (root CLAUDE.md + `.claude/skills/` + `.claude/rules/`) is exactly this AI layer.
- **Harness engineering / Ralph loop:** for tasks too big for one session, chain multiple Claude Code sessions like an assembly line — one plans, hands a spec/report to the next which implements, hands an execution report to the next which validates. This is the same shape as this repo's [[WAT Framework]] and the reason chunking exists in `/chunked`.
- **Security — assume the agent will do the thing you told it not to:** "if you have the mindset that anything the agent can read or touch, it will — even if you never asked it to — that assumption is what saves you from having your database deleted." Concretely: telling it not to delete a database doesn't stop it; blocking `DELETE` SQL statements doesn't stop it either — it can write and run a script to remove a file/folder in two steps. Cole's actual practice: use Claude Code **hooks** (pre-tool-use checks) to hard-block dangerous commands, not prompt instructions.
- **Real incident (Nate's team):** an agent misread its own task list, decided to be "proactive," and emailed their entire list an unauthorized discount code. Response wasn't blame — it was a written case study distributed to the whole team and (implicitly) a permission/hook fix. Directly reinforces [.claude/rules/deployment-security.md](../../.claude/rules/deployment-security.md) — MCP/webhook permissions need real scoping, not prompt-level "please don't."
- **System evolution — "every bug becomes a permanent upgrade":** don't just fix the immediate issue; ask what CLAUDE.md rule, skill update, or planning-doc addition prevents this class of bug from recurring. Treat failures as the trigger for improving the AI layer, same principle behind updating `workflows/*.md` per the WAT framework rule "when a script fails: read the error, fix it, verify it, then update the workflow."
- **Skills > sub-agents > agent teams**, in terms of maturity/reliability: skills are the most load-bearing surface (Cole's #1 favorite feature). Sub-agents are good for research/lookups but hard to make communicate well on longer handoffs. Agent teams (Claude's newer multi-teammate feature) are powerful for one specific use case both hosts agreed on: spinning up a panel of personas (CEO, skeptic, beginner, etc.) to independently research and then **debate to consensus** on a decision — not for production builds, since it's token-heavy and communication between teammates is still unrefined. Nate reports 4-10% of his 5-hour limit per debate-panel run on the $200/mo plan.
- **Non-coding applications:** the plan/build/verify/evolve and harness/skill patterns apply to any "knowledge work," e.g. Cole's example of B2B quote/estimate generation (multi-agent: one researches inventory, one compares vendor prices, one drafts the PDF, one formats it) — directly analogous to how this repo's `/proposal`, `/prospect`, `/crm` skills could be composed for automation-build quoting.
- **CLI + skill pairing beats bare MCP servers for token efficiency:** Cole's take — give the agent a CLI for a platform (CRM, GitHub, etc.) plus a skill that tells it how/when to use that CLI, rather than loading a full MCP server's tool schemas into context up front.
- **Intent engineering:** explain *why* you want something built, not just *what* — the reasoning changes how the agent approaches the *how*. Matches Anthropic's own Opus 4.8 prompting guidance per Cole (confirmed independently by Anthropic docs, per Nate).

## Relevance to Adar Realty Studio
- Reinforces (doesn't change) the existing [[WAT Framework]] and [.claude/rules/deployment-security.md](../../.claude/rules/deployment-security.md) — this is validation, not new architecture.
- The debate-panel agent-team pattern is a concrete technique worth trying for pricing/strategy decisions (e.g. "is $X/mo the right retainer for this prospect") instead of asking a single Claude session for its opinion.
- The "every bug becomes a permanent upgrade" framing is worth adopting explicitly as a working habit whenever a skill or automation misfires.

## What This Updated
- [[Claude Code Power Techniques]] — added dumb-zone token specifics, hooks-for-security detail, harness engineering/Ralph loop, agent-team debate-panel use case.
