---
title: Claude Code Video Toolkit
type: entity
tags: [tool, video, content, ai, production]
created: 2026-06-10
updated: 2026-06-10
sources: 1
---

# Claude Code Video Toolkit

**Repo:** github.com/digitalsamba/claude-code-video-toolkit
**License:** MIT | **Stars:** 1.4k | **Status:** Active (v0.17.0, updated Jun 2026)

AI-native video production system built for Claude Code. You describe the video you want, and it handles the full pipeline: script → voiceover → music → visuals → MP4.

---

## What It Does

End-to-end video production inside Claude Code:
- Script writing and scene planning
- AI voiceover (ElevenLabs or self-hosted Qwen3-TTS, ~$0.01/video)
- AI image generation (FLUX.2, Ideogram4, ~$0.02/image)
- AI video clips (LTX-2, ~$0.23/clip)
- Music generation (ACE-Step, free–$0.05)
- Animated talking heads (SadTalker, ~$0.10)
- React-based video composition (Remotion → renders MP4)
- Browser recording for product demos (Playwright)

---

## Key Commands (inside toolkit's Claude Code session)

| Command | What It Does |
|---------|-------------|
| `/setup` | Configure cloud GPU, voice, storage |
| `/video` | Create/manage video projects |
| `/generate-voiceover` | AI narration synthesis |
| `/voice-clone` | Record and save custom voice |
| `/scene-review` | Preview in Remotion Studio |
| `/design` | Refine individual scene aesthetics |
| `/brand` | Manage visual identity profiles |
| `/record-demo` | Playwright browser recording |
| `/template` | Access/create video templates |

---

## Available Templates

- **concept-explainer-short** — vertical 9:16 shorts for Instagram Reels/TikTok
- **product-demo** — dark tech styling, marketing videos
- **sprint-review** — project/delivery updates
- **sprint-review-v2** — modular, composable scenes

---

## Cost Breakdown

| Output | Tool | Typical Cost |
|--------|------|--------------|
| Voiceover | Qwen3-TTS (self-hosted) | ~$0.01 |
| Voiceover (premium) | ElevenLabs | ~$0.01 |
| Title card / visual | FLUX.2 image gen | ~$0.02 |
| Image editing | Qwen-Image-Edit | ~$0.03 |
| Background music | ACE-Step | Free–$0.05 |
| Talking head video | SadTalker | ~$0.10 |
| AI video clip | LTX-2.3 | ~$0.23 |
| Full short Reel | All combined | ~$0.50–$1.00 |

---

## Cloud GPU Options

- **Modal** (recommended) — $30/month free tier, auto-deploys via `/setup`
- **RunPod** (alternative) — pay-per-second, no monthly minimum

---

## How It's Used Here

Mapped to [`/video-editing` skill](.claude/skills/video-editing/SKILL.md), which tailors it to:
- **Instagram Reels** for @eitanadar.ai personal brand
- **Agency demos** for pitching automation to real estate prospects
- **Property tour videos** for client delivery
- **Automation explainers** for content marketing

---

## Production Workflow

```
describe concept
  → /video (select template + brand)
  → edit VOICEOVER-SCRIPT.md
  → gather assets (or /record-demo)
  → /scene-review (verify frames)
  → /design (polish aesthetics)
  → /generate-voiceover (AI narration)
  → npm run studio (live preview)
  → npm run render (final MP4)
```

---

## Relevance to Eitan

- Cheapest path to consistent, professional video content for @eitanadar.ai
- Lets him produce Reels without a video editor or studio
- Agency demo videos can be produced per-prospect for personalized outreach
- Talking head mode (SadTalker) enables avatar-based explainers without being on camera
- Voice cloning means his voice can narrate at scale without re-recording

---

## Setup Notes

- Requires: Node.js 18+, Python 3.9+, Claude Code
- FFmpeg optional (for some tools)
- Clone to `~/video-toolkit/` then run `/setup` to configure cloud GPU
- Create brand profile `brands/eitanadar-ai/` for consistent visual identity
