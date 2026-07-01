# Wiki Index

> Catalog of every page in the wiki. Updated automatically by the `wiki` skill.

## Entities - People

- [[Eitan Adar]](entities/eitan-adar.md) - owner (updated: 2026-05-29)

## Entities - Companies & Products

- [[Sohail Real Estate Group]](entities/sohail-real-estate-group.md) - eXp Realty group leader, Sohail Salhadin (updated: 2026-06-04)
- [[Chicago Lakefront Realty]](entities/chicago-lakefront-realty.md) - Lincoln Park team, 5 agents (updated: 2026-06-04)
- [[Wicker Park Homes Group]](entities/wicker-park-homes-group.md) - Bucktown team, first-time buyer focus (updated: 2026-06-04)
- [[AI Voice Receptionist]](entities/voice-receptionist-product.md) - Claude-powered receptionist for real estate agents. Schedules appointments, qualifies leads, takes messages. MVP complete, deployed as Claude Code skill. (created: 2026-06-10)
- [[Claude Code Video Toolkit]](entities/claude-code-video-toolkit.md) - MIT open-source AI video production system (1.4k stars). Script → voiceover → visuals → MP4 from a prompt. Full Reel costs ~$0.50–$1. Powers `/video-editing` skill. (created: 2026-06-10)

## Concepts

- [[Automation Framework]] - YAML-based workflow orchestrator (replaces N8N). Chains skills + APIs + logic. Triggers: webhooks, schedules, events. (updated: 2026-06-05)
- [[Instagram Carousel Automation System]] - Telegram bot that generates, previews, posts neon-styled Instagram carousels with auto-generated captions. 25 topics × 5 prompts each. (updated: 2026-06-09)
- [[Lead Finder Skill]] - Automated prospecting tool that finds & qualifies real estate leads by market (20+ prospects in Chicago/Skokie), gathers decision-maker contact info, assesses fit (1-10), exports to wiki. (updated: 2026-06-09)
- [[Email Campaign Automation System]] - Production-ready Python system for automating email sequences. Segmentation, personalization, scheduling, analytics, CRM sync. Built with TDD (11 passing tests). (created: 2026-06-09)
- [[Superpowers Development Framework]] - Community framework (150K GitHub stars) that enforces senior-dev workflows: plan → test → code → review → deliver. Reduces production bugs 40%. (created: 2026-06-09)
- [[Get Shit Done (GSD) Framework]] - Spec-driven development system (64K GitHub stars). 91 workflows, 36 templates, 62 references. Complements superpowers with specs, validation, autonomous execution. (created: 2026-06-09)
- AI Automation Agency (real estate niche focus) — verticals: agents, brokerages, RE tech, property management
- Revenue model: $2,500-$50,000 per project + $500-$2,000/month retainers
- Dual-path strategy: Build automation + become real estate agent (credibility + case study)
- Autonomous execution models: `/autonomous` (small tasks), `/chunked` (large tasks, splits into chunks), `/task-resilience` (recovery strategies)
- Chunking strategy: Break tasks into 30-60 min independent chunks to avoid 600s background agent timeouts. Success rate: 90%+ vs 30-40% for monolithic tasks
- Behavioral vs systematic solutions: Commitments fail when system is designed to break them. Auto-launch enforces approval→execution automatically instead of relying on willpower
- Visibility in background execution: Without progress tracking, background tasks are invisible (could be working or stalled). Progress-monitor solves this with real-time updates.

## Sources

- YouTube: "How to Grow Your Agency Fast" (analyzed 2026-06-04) — Scaling framework applicable to RE automation agency

- [Business Profile](../business-profile.json) - Single source of truth: brand, pricing, services, owner, differentiators. Read by skills + cloud routines. (created: 2026-06-23)
- [[Build & Sell with Claude Code (10hr Course) - Nate Herk]](sources/build-sell-with-claude-code.md) - Full 10hr transcript ingested. Validated WAT framework, added Context7 MCP, captured pricing/client-acquisition frameworks. (created: 2026-07-01)
- [[Being the Director of Your Coding Agents — Nate Herk x Cole Medin]](sources/directing-coding-agents-cole-medin.md) - Podcast: dumb-zone token thresholds, hooks for security (agent-can-touch-it-will-do-it), harness engineering/Ralph loop, agent-team debate panels. Reinforces WAT + deployment-security rule. (created: 2026-07-01)
- [[Meta Officially Integrated Claude Into Facebook Ads (YouTube ingest)]](sources/meta-ads-claude-integration.md) - Built the `/ads` Meta Ads Media Buyer skill from this video. (created: 2026-07-01)
- [[Stanford's Method Turns Claude Into a PHD Level Research Team]](sources/storm-research-method.md) - Built the storm-research skill (5-persona verified research pipeline) from this video. (created: 2026-07-01)
- [[Competitor Analysis Skill]](concepts/competitor-analysis-skill.md) - Monthly automated workflow: web research → branded PDF → GitHub commit → Gmail draft. Runs 1st of every month. (created: 2026-06-23)
- [[DailyRemote Job Scraper]](concepts/dailyremote-scraper.md) - Python scraper for remote job listings. Current output: 500 UK sales jobs → Excel + Google Sheet. (created: 2026-06-24)
- [[YouTube Intelligence Pipeline]](concepts/youtube-intelligence-pipeline.md) - Weekly automated YouTube research: 10 search queries → transcripts → Claude synthesis → 4 charts → 9-page PPTX → Gmail. Fires every Monday 7:03am. (created: 2026-06-29)
- [[Frontend Slides Skill]](concepts/frontend-slides-skill.md) - HTML presentation generator. 12 presets + 34 bold templates. Zero deps, single-file output. Converts PPTX to web. (created: 2026-06-29)
- [[Awesome Claude Skills (Composio)]](concepts/awesome-claude-skills.md) - 832 Composio app integration skills + 33 standalone skills. Installed at .claude/skills/awesome-claude-skills/. (created: 2026-06-29)
- [[WAT Framework]](concepts/wat-framework.md) - Workflows/Agent/Tools split documented in root CLAUDE.md; independently validated by the Nate Herk course's identical 3-layer pattern. (created: 2026-07-01)
- [[Claude Code Power Techniques]](concepts/claude-code-power-techniques.md) - Cheat sheet: context management, CLAUDE.md discipline, build habits, skills vs sub-agents vs agent teams, deployment options. (created: 2026-07-01)
- [[AI Agency Client Acquisition and Pricing]](concepts/ai-agency-client-acquisition-pricing.md) - PRICE framework, value-based retainer pricing (10-15% of yr-1 savings), Trojan horse partner method, 7-day cold-to-closed framework. (created: 2026-07-01)
- [[STORM Multi-Perspective Research Method]](concepts/storm-research-method.md) - 5-persona parallel research + contradiction mapping + adversarial peer review. Implemented as `/storm-research` skill. (created: 2026-07-01)
- [[Meta Ads Media Buyer Skill]](concepts/meta-ads-media-buyer-skill.md) - `/ads` skill: audit, build, and manage Meta ad campaigns via the official Meta Ads MCP connector. Real estate lead-gen focused. (created: 2026-07-01)

## Synthesis

- [[Chicago Prospect Analysis]](synthesis/chicago-prospect-analysis.md) - Comparison of 3 Chicago prospects, strategy prioritization (updated: 2026-06-04)
- [[Sohail Shadowing Plan]](synthesis/sohail-shadowing-plan.md) - Detailed plan for shadowing Sohail/his agents, observation checklist, follow-up strategy (updated: 2026-06-04)
- [[Competitor Analysis — Adar Realty Studios — 2026-06-22]](synthesis/competitor-analysis-2026-06-22.md) - 6 competitors profiled, gap analysis, recommended actions, branded PDF generated (created: 2026-06-23)
- [[Competitor Landscape]](synthesis/competitor-landscape.md) - 50 RE automation competitors analyzed, pricing tiers, competitive gaps, Eitan's positioning (created: 2026-06-05)
- [[Red Team Assessment]](synthesis/red-team-assessment.md) - Competitive threats, vulnerabilities, realistic moat candidates, how competitors could win (created: 2026-06-05)
- [[LinkedIn Strategy]](synthesis/linkedin-strategy.md) - Positioning statement, target audience, 5 content pillars, 30-day content calendar (created: 2026-06-05)
- [[Real Estate Carousel Design Blueprint]](synthesis/real-estate-carousel-design-blueprint.md) - Top creator analysis, color palettes, typography system, layout structure, visual elements, professional design signals (created: 2026-06-09)
