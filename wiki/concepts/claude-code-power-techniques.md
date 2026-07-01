---
title: Claude Code Power Techniques
type: concept
tags: [claude-code, workflow, techniques]
created: 2026-07-01
updated: 2026-07-01
sources: 2
---

# Claude Code Power Techniques

Reference cheat sheet of Claude Code techniques and habits worth reusing, pulled from [[Build & Sell with Claude Code (10hr Course) - Nate Herk]] and [[Being the Director of Your Coding Agents — Nate Herk x Cole Medin]]. Most of these are prompting/workflow habits, not installable features — keep this page as the checklist to draw from when building or debugging automations.

## Context management
- `/context` — audit token usage before it becomes a problem
- `/compact` around ~60% context used; can target what to preserve ("compact but keep the website design decisions")
- `/clear` between unrelated tasks — don't carry stale context forward
- `/rewind` — quick undo to a prior checkpoint instead of re-explaining a correction
- Watch for "context rot" / "lost in the middle" — quality degrades as context fills, not just when it's full
- **The "dumb zone" (Cole Medin's term):** the token count past which quality degrades even though the model's stated limit is far higher. Cole's working numbers: Opus ~250K tokens, Opus 4.7 was ~200K, Sonnet 4.6 only ~100-125K — smaller models hit the dumb zone much sooner relative to their max context. The marketed "1M token context" creates false security; plan to `/compact` or hand off well before that ceiling, not near it.
- Delegate file-heavy or tool-heavy lookups (e.g. searching a big API, scraping) to a sub-agent so the main thread's context stays clean
- Cap parallel sessions at 3-4 — more than that becomes unmanageable to track

## CLAUDE.md discipline
- Keep CLAUDE.md under ~150-200 lines. This repo's root CLAUDE.md is at [CLAUDE.md](../../CLAUDE.md) — worth a periodic length check.
- Route to other files instead of inlining everything — this repo already does this via `.claude/rules/communication-style.md` and `wiki/CLAUDE.md`. Keep extending that pattern rather than growing the root file.
- Treat it as a living doc — update it same-day when a new gotcha or pattern is discovered, not in a batch later.
- `/init` auto-generates a CLAUDE.md from an existing codebase if one doesn't exist yet.

## Build habits
- Default to plan mode for anything that needs research or design decisions before code — let Claude ask clarifying questions rather than guessing.
- Tell it explicitly: "be 95% sure before proceeding, ask me anything unclear" — forces the AskUserQuestion pattern instead of silent assumptions.
- Screenshot self-check loop for frontend work: build → screenshot (Playwright/Chrome DevTools) → compare to reference/critique → fix → repeat. Disable this loop for animated/dynamic elements — it causes infinite fix loops on things that are supposed to move.
- Security review before any deploy: explicitly ask "check this code for exposed secrets, webhook vulnerabilities, and anything a security review should catch" before pushing something live. Codified as [.claude/rules/deployment-security.md](../../.claude/rules/deployment-security.md) in this repo.
- Fine-grained permissions (allow safe commands, explicitly deny destructive ones) over blanket `--dangerously-skip-permissions` — safer default for anything touching real accounts or money.
- **Assume the agent will do the thing you told it not to.** Cole Medin's framing: telling an agent "never delete the database" doesn't stop it; blocking `DELETE` SQL statements doesn't stop it either — it can write and run a script to remove a file/folder in two steps instead. The only real control is Claude Code **hooks** (pre-tool-use checks that hard-block a command before it runs), not prompt-level instructions. Nate Herk's team had an agent misinterpret a task-list item and email their entire list an unauthorized discount code — the fix was a written case study + presumably a permission/hook change, not just "don't do that again."
- **System evolution — "every bug becomes a permanent upgrade":** when something breaks, don't just patch it — add the CLAUDE.md rule, skill update, or planning-doc addition that prevents the whole class of bug from recurring. Same principle as this repo's WAT rule to update `workflows/*.md` whenever a script fails.
- **Harness engineering / Ralph loop:** for tasks too big for one session (i.e. that would hit the dumb zone mid-task), chain multiple Claude Code sessions like an assembly line — one plans and writes a spec, hands it to the next which implements and writes an execution report, hands that to the next which validates/code-reviews. Matches this repo's [[WAT Framework]] and the reasoning behind `/chunked`.

## Skills vs sub-agents vs agent teams
- **Skill** — runs in the main thread's context; knowledge/instructions loaded on demand (progressive: name+description first, full body only if triggered, reference files only if needed).
- **Sub-agent** — fresh/isolated context, can use a cheaper model (Haiku) for narrow tasks like scraping or lookups, protects main thread's context budget.
- **Agent team** (experimental, `/team create`) — multiple named teammates that share a task list and can message each other directly, each owning specific files. Requires an experimental settings.json flag. Not enabled in this repo — worth trying if a build ever needs true parallel multi-file work with cross-agent coordination (e.g. frontend/backend/QA split).
- **Agent-team debate panels:** the one agent-team use case both Nate Herk and Cole Medin independently landed on — spin up a handful of personas (CEO, skeptic, beginner, college student, etc.), have each independently research and form an opinion, then have them debate to consensus. Good for pricing/strategy decisions where a single Claude session's opinion is too sycophantic to trust; not meant for production builds (token-heavy, ~4-10% of a 5-hour limit per run, cross-agent communication still unrefined).
- Skill anatomy: YAML front matter (`name`, `description`, `disable_model_invocation`, `argument-hint`, `tools`, `model`) + step-by-step body. This repo's `.claude/skills/skill-creator/` already automates building these correctly — use it rather than hand-rolling.

## Deployment options (if this repo ever needs heavier scheduling/retry guarantees)
- **Modal** — Python, pay-per-execution, good for simple cron/webhook deploys.
- **Trigger.dev** — TypeScript, built-in automatic retries + queuing + orchestration, preferred by the course's end for anything that needs to not silently fail. This repo currently relies on Anthropic cloud triggers + systemd (see [[YouTube Intelligence Pipeline]]) — fine for now, but Trigger.dev is the documented upgrade path if retry reliability ever becomes a problem.

## Related
- [[WAT Framework]] (documented in root CLAUDE.md) — this course's CLAUDE.md + workflows/*.md + tools/*.py pattern is the same structure, independently validated.
- [[Build & Sell with Claude Code (10hr Course) - Nate Herk]] — full source.
- [[Being the Director of Your Coding Agents — Nate Herk x Cole Medin]] — second, independent source that reinforced the same patterns and added the dumb-zone token thresholds, hooks-for-security specifics, and the debate-panel agent-team use case.
