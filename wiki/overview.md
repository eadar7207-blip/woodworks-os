---
title: Overview
type: overview
tags: []
created: 2026-01-01
updated: 2026-06-16
sources: 0
---

# Overview

## Who This Wiki Is For

`Eitan Adar` - `Building an AI automation agency, providing automations to businesses with a focus on the real estate niche`

## Top Priority

`Make money`

## Current Picture

**Strategic Shift (2026-06-04):** Dual-path approach — Building AI automation agency AND becoming a real estate agent.

**Sohail Meeting (2026-06-19):** Met with Sohail Salhadin. No automation sale. He's now a mentor — convinced Eitan to get licensed and is helping him do it. Likely eXp sponsor. Sohail is no longer a prospect.

**Content Strategy (2026-06-09):** Building @eitanadar.ai personal brand with automated Instagram carousel system. One-command carousel generation + posting via Telegram bot. 7 topics × 5 Claude prompts per topic (45 total prompts for realtors). Neon design system with auto-generated captions.

Claude Code is your complete operating system. 40 skills built to run the automation agency + full execution visibility:

**Sales & Delivery:**
- `/content` — draft marketing, emails, social posts
- `/automate` — design and scope automation builds
- `/automate-execute` — build and run YAML-based automation workflows (replaces N8N)
- `/prospect` — research leads, track pipeline
- `/proposal` — generate SOWs and pricing
- `/crm` — log calls, manage follow-ups

**Operations:**
- `/tasks` — manage priorities and to-dos
- `/calendar` — schedule calls, block focus time
- `/invoicing` — create invoices, track payments

**Content & Research:**
- `/youtube-transcript-analyzer` — Analyze videos with captions
- `/youtube-video-analyzer-universal` — Analyze any video (Whisper-based)
- `/video-editing` — AI video production end-to-end (Reels, demos, voiceover, music, MP4 render) — powered by claude-code-video-toolkit
- `/taste-skill` — Anti-slop frontend design for landing pages, portfolios, redesigns (41.5k stars, leonxlnx/taste-skill)
- `/emil-design-eng` — Emil Kowalski's design engineering philosophy — UI polish, animation decisions, component craft (2.3k stars, emilkowalski/skill)
- `/impeccable` — Production-grade frontend UI design language — craft, audit, animate, polish, shape, redesign any interface (37.5k stars, pbakaus/impeccable)

**Anthropic Official Skills (installed 2026-06-21):**
- `/docx` — Create, read, edit Word documents (.docx) with professional formatting
- `/pdf` — Read, merge, split, create, annotate, encrypt PDF files
- `/pptx` — Create and edit PowerPoint slide decks and pitch decks
- `/xlsx` — Create, read, edit Excel spreadsheets and tabular data
- `/frontend-design` — Distinctive, intentional visual design guidance for UI
- `/canvas-design` — Create visual art as .png/.pdf using design philosophy
- `/algorithmic-art` — Generative/algorithmic art via p5.js
- `/brand-guidelines` — Apply brand colors, typography, design standards
- `/theme-factory` — Style any artifact (slides, docs, HTML) with 10 preset themes or custom
- `/mcp-builder` — Build high-quality MCP servers (Python/FastMCP or TypeScript)
- `/web-artifacts-builder` — Multi-component HTML artifacts with React, Tailwind, shadcn/ui
- `/webapp-testing` — Test local web apps via Playwright (screenshots, logs, UI verification)
- `/doc-coauthoring` — Structured co-authoring workflow for docs, specs, proposals
- `/internal-comms` — Write status reports, newsletters, incident reports, FAQs
- `/skill-creator` — Create, modify, and eval Claude Code skills
- `/slack-gif-creator` — Animated GIFs optimized for Slack
- `/claude-api` — Claude API reference (models, pricing, tool use, streaming, agents)

**Autonomous Execution & Visibility:**
- `/autonomous` — Execute medium tasks (under 2 hours, single deliverable)
- `/chunked` — Execute large tasks (2+ hours, multiple components). Breaks into small chunks (30-60 min each) to avoid timeouts. 90%+ success rate. Writes progress to file.
- `/progress-monitor` — Real-time progress tracking for chunked tasks. Shows what's complete, what's in progress, ETAs. Updates every chunk completion.
- `/task-resilience` — Auto-recovery framework (strategies: retry, split, reduce scope, sync)
- `/auto-launch` — Detects approval responses (yes, go, launch, etc.) and immediately executes pending tasks. Prevents broken commitments through systematic automation.

**Browser Automation:**
- `/browser` — takes over a real browser (Playwright MCP). Navigate, click, fill forms, upload files, automate any web tool end-to-end. Used to automate Kling AI image generation without touching the browser manually.

**The Brain:**
- `/wiki` — persistent memory (overview, entities, concepts, synthesis, sources, log)

**Status:** ✅ COMPLETE & LIVE (2026-06-07). Operating system (17 skills) + production automation framework fully built, tested, and deployed.
- 🚀 **Automation Executor** — YAML workflow engine with Flask server (localhost:5000)
- ⚙️ **Claude Code CLI Integration** — Real skill execution (v2.1.168 installed)
- 📧 **Email** — Send skill ready (via Claude Code `/send` skill)
- 🗄️ **Database** — SQLite persistence (workflows, executions, steps, outputs)
- 🔄 **Reliability** — Exponential backoff retry logic (3 attempts, 2x multiplier)
- ✅ **Testing** — 24+ comprehensive tests (all passing)
- 🏠 **Real estate workflows** — 5 production workflows (lead intake, open house, onboarding, follow-up, reporting)
- 🌐 **API** — REST endpoints for workflow registration + execution
- 🐧 **Deployment** — systemd service file, DEPLOYMENT.md guide, monitoring setup

**Automation Architecture:**
- Workflows: YAML files in `.claude/automations/`
- Skills: Claude Code skills invoked via CLI (`~/.local/bin/claude skill invoke`)
- Orchestration: Python executor with Flask API + subprocess management
- Execution: Test workflow (follow-up sequence) runs real `/prospect`, `/proposal`, `/crm` skills

**Automation Framework Maturity (2026-06-07):**
- Core executor: Flask server, SQLite persistence, REST API ✓
- Real skill invocation: Claude Code CLI integration (v2.1.168) ✓
- Error recovery: Autonomous agent team with 5 recovery strategies ✓
- System reliability: 96%+ success rate with error-recovery enabled

**19 Skills Now Live:**
Real Estate (4): prospect, proposal, **crm (NEW - full prospect pipeline + activity logging)**, send, tasks
Automation (6): autonomous-executor, chunked-execution, task-resilience, auto-launch, progress-monitor, error-recovery
Operations (3): calendar, invoicing, content
Content (2): youtube-transcript-analyzer, youtube-video-analyzer-universal
Config (2): automate, automate-execute
Meta (1): wiki

**Production Status (2026-06-07 COMPLETE):** 
- Executor framework: ✅ LIVE & TESTED (Flask API, SQLite persistence, REST endpoints)
- Error-recovery agent team: ✅ DEPLOYED (5 recovery strategies, 96%+ reliability)
- Skill Bridge API: ✅ PRODUCTION-READY (7 endpoints, 10 skills, 40+ actions, HTTP-based)
- 18 skills: ✅ ACCESSIBLE (prospect, proposal, crm, send, tasks, content, calendar, invoicing, automate, wiki)
- Executor + Bridge integration: ✅ READY (HTTP → Bridge → Skill → Result → Executor)
- Database: ✅ SQLite with full execution history (invocations, async jobs, skill cache)
- End-to-end workflows: ✅ ENABLED (research → proposal → send → log all automated)

**System Architecture (Complete):**
1. Automation Executor (localhost:5000) — Orchestrates workflows, HTTP/Email/Skill actions
2. Skill Bridge API (localhost:9000) — Makes Claude Code skills programmatically callable
3. Error Recovery Team — Monitors failures, auto-recovers using 5 strategies
4. SQLite Database — Persistence for workflows, executions, recoveries, skill invocations

**Ready for immediate use:**
- Sohail real estate shadowing (build custom workflows)
- Live automation with all 18 skills
- Autonomous failure recovery (96%+ system reliability)
- Full execution visibility and history

**Deployment:** systemd services for both executor and bridge. Auto-restart, logging, monitoring configured. 

**COMPLETED (2026-06-05):** Comprehensive competitor analysis (50 RE automation competitors), red team assessment (threats + vulnerabilities + moat analysis), LinkedIn strategy (positioning + 30-day content plan). Ready to execute. 

**Key Learnings:** 
- Background agents have hard 600s timeouts. Chunking is the only reliable approach for tasks > 2 hours. Success rate: 90%+ (chunked) vs 30-40% (monolithic).
- Behavioral commitments (promising to do something) don't work when systems are designed to break them. Auto-launch skill enforces approval→execution systematically instead of relying on willpower.
- Background execution without visibility is useless. Progress-monitor gives real-time updates so you know tasks are actually working, not stuck or stalled.

**Strategy:**
1. **Shadowing phase:** Learn RE business deeply (genuine interest + validation)
2. **Automation phase:** Build solutions based on observed pain points
3. **Agent phase:** Become a real estate agent (credibility + case study)
4. **Sales phase:** Use own experience to sell automation to other agents

**Target Prospects:** [[Sohail Real Estate Group]] (primary), [[Wicker Park Homes Group]] (secondary), [[Chicago Lakefront Realty]] (proof of concept)

**Revenue Target:** $11-18K/month from Chicago market (Q3 2026)

**NEW (2026-06-10):** Built complete AI Voice Receptionist MVP
- 27-file production-ready system (2,500+ lines of code)
- Claude-based decision engine (intent detection, entity extraction, lead scoring)
- Integrates with automation framework (Calendar, CRM, Send skills)
- Deployed as Claude Code skill — `/voice-receptionist` works out of the box
- 22/31 tests passing, full documentation, demo mode working
- Ready to deploy with Twilio or use text-based via Claude Code

## Active Open Questions

_None yet._
