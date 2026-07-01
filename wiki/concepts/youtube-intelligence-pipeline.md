---
title: YouTube Intelligence Pipeline
type: concept
tags: [automation, youtube, content-strategy, weekly-report]
created: 2026-06-29
updated: 2026-06-29
sources: 0
---

# YouTube Intelligence Pipeline

Weekly automated research system that monitors the AI/automation YouTube niche and delivers a branded 9-page slide deck to eadar7207@gmail.com every Monday morning.

## Purpose

Keeps Eitan current on what's trending in AI/automation YouTube without manual research. Feeds content strategy for @eitanadar.ai.

## Pipeline Phases

1. **Discovery** — YouTube Data API v3 searches 10 AI/automation queries, collects top 30 videos from past 7 days sorted by views
2. **Transcripts** — `youtube-transcript-api` fetches transcripts for top 20 videos
3. **Synthesis** — Claude CLI analyzes transcripts to extract themes, hooks, emerging signals, recommendations (falls back to keyword analysis if CLI unavailable)
4. **Charts** — matplotlib generates 4 brand-colored PNGs: trending topics (bar), top videos (bar), channel subscribers (bar), engagement (scatter)
5. **Slide Deck** — PptxGenJS builds 9-page PPTX with dark brand theme
6. **Email** — Gmail API sends deck to eadar7207@gmail.com with 3-bullet summary

## Slide Deck Structure (9 pages)

| Page | Content |
|------|---------|
| 1 | Title — full-bleed primary, "AI SPACE Weekly Intelligence Report" |
| 2 | Executive Summary — 5 numbered takeaways |
| 3 | Top 10 Videos — chart or fallback list |
| 4 | Top Channels — subscribers chart or list |
| 5 | Engagement — views vs like rate scatter |
| 6 | Trending Topics — horizontal bar chart |
| 7 | Posting Patterns — title hook cards |
| 8 | Recommendations — 4 content ideas for @eitanadar.ai |
| 9 | Thank You / Closing — stats, next week watch |

## Brand Colors

- Primary: `#1B3A6B` (dark navy)
- Accent: `#4A9EDB` (bright blue)
- Dark BG: `#0F2347`

## Search Queries (10)

AI automation 2026, AI agents tutorial, LLM tools workflow, Claude AI agents, n8n automation workflow, AI for business automation, ChatGPT workflow automation, Make.com automation AI, AI productivity tools, autonomous AI agents

## Files

- `tools/youtube_intelligence.py` — main pipeline orchestrator
- `tools/youtube_api.py` — YouTube Data API v3 wrapper
- `tools/transcript_batch.py` — batch transcript fetcher
- `tools/chart_generator.py` — matplotlib chart generator
- `tools/slide_builder.js` — PptxGenJS 9-page deck builder
- `projects/youtube-intelligence/reports/` — output directory

## Schedule

Cloud trigger `trig_01LBg5zbehmwaNkbhSoY8d6Z` — every Monday at 7:03am, creates fresh session, push notification on completion.

## Manual Run

```bash
# From repo root
python3 tools/youtube_intelligence.py          # full run + email
python3 tools/youtube_intelligence.py --dry-run  # full run, no email
python3 tools/youtube_intelligence.py --test     # 5 videos, no email
```

## API Key

YouTube Data API v3: `AIzaSyAO8rCwEmGpqW8uZQ4UYsfIA4REJmwPbhw` (in `.env`)
Free quota: 10,000 units/day. Weekly run uses ~500 units.

## Dependencies

- Python: `youtube-transcript-api`, `matplotlib`, `python-dotenv`, `google-api-python-client`
- Node: `pptxgenjs` (installed locally in `tools/node_modules/`)
