---
title: Frontend Slides Skill
type: concept
tags: [skill, presentations, html, design]
created: 2026-06-29
updated: 2026-06-29
sources: 0
---

# Frontend Slides Skill

Claude skill for generating polished HTML presentations without design expertise. Source: `github.com/zarazhangrui/frontend-slides`.

## What It Does

- Generates zero-dependency single HTML files with embedded CSS/JS
- Shows style previews so you pick the look visually, not by describing it
- Converts PPTX files to web presentations
- Outputs production-ready 16:9 slides with animations

## Design Options

- 12 built-in style presets (see `STYLE_PRESETS.md`)
- 34 additional systems in `bold-template-pack/`

## Invoke

`/frontend-slides`

## Use Cases for Eitan

- Client pitches and agency proposals
- YouTube Intelligence report (HTML alternative to the weekly PPTX)
- Personal brand decks for @eitanadar.ai
- Converting existing PPTX deliverables to shareable web format

## Files

- `.claude/skills/frontend-slides/SKILL.md` — main skill
- `.claude/skills/frontend-slides/STYLE_PRESETS.md` — preset reference
- `.claude/skills/frontend-slides/bold-template-pack/` — 34 extended designs
- `.claude/skills/frontend-slides/animation-patterns.md` — animation reference
- `.claude/skills/frontend-slides/scripts/` — PPT conversion, PDF export, deploy
