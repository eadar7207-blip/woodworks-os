---
title: Competitor Analysis Skill
type: concept
tags: [skill, competitor-analysis, pdf, automation, brand]
created: 2026-06-23
updated: 2026-06-23
sources: 1
---

# Competitor Analysis Skill

## What It Is

A reusable `/competitor-analysis` Claude Code skill that researches competitors for any business and outputs a branded PDF report. Works for Adar's own agency or as a deliverable for clients.

## How It Works

1. Takes business info (name, description, industry) + brand inputs (logo path, hex colors) per run
2. Runs WebSearch to find 6-8 competitors in the space
3. Uses WebFetch to profile each competitor (pricing, strengths, weaknesses, target market)
4. Synthesizes gap analysis + recommended actions
5. Generates a branded PDF via reportlab (cover page, 6 sections)
6. Saves synthesis page to wiki
7. Drafts Gmail notification with highlights

## Files

- `.claude/skills/competitor-analysis/SKILL.md` — full execution instructions
- `.claude/skills/competitor-analysis/scripts/generate_pdf.py` — reportlab PDF generator
- `.claude/skills/competitor-analysis/scripts/generate_logo.py` — Adar logo generator
- `.claude/commands/competitor-analysis.md` — slash command

## PDF Structure

1. Cover — logo + brand color background + date
2. Executive Summary — 3-5 bullets
3. Competitor Profiles — one section per competitor
4. Competitive Gap Analysis — where you win, underserved needs, trends
5. Recommended Actions — 3-5 concrete steps
6. Sources

## Adar Brand Defaults

- Primary: `#1B3A6B` (deep navy blue)
- Accent: `#4A9EDB` (bright blue)
- Logo: regenerated on each cloud run via `generate_logo.py`

## Monthly Automation

Cloud routine `trig_01BMexRt2dGAgM7MLjTiqAsw` runs on the 1st of every month:
- Clones repo from `github.com/eadar7207-blip/woodworks-os`
- Runs full research + PDF generation
- Commits PDF to `reports/` folder in repo
- Drafts Gmail summary to eadar7207@gmail.com

Manage at: https://claude.ai/code/routines/trig_01BMexRt2dGAgM7MLjTiqAsw

## First Run Results (2026-06-22)

Competitors profiled: Lofty, Ylopo, Structurely, Follow Up Boss, Luxury Presence, SmartZip

Top finding: every major competitor targets teams ($500+/mo) — solo agents are almost entirely underserved. Recommended immediate move: $299–399/mo solo agent package.

See [[Competitor Analysis — Adar Realty Studios — 2026-06-22]](../synthesis/competitor-analysis-2026-06-22.md)
