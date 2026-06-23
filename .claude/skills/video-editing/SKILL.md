---
name: video-editing
description: AI-native video production using claude-code-video-toolkit — script, voiceover, visuals, music, and MP4 render from a single prompt
---

# Video Editing

AI-native video production powered by [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit). Tell Claude what video you want — it writes the script, generates voiceover, music, and visuals, then renders the MP4.

**Cost profile:** ~$0.01 voiceover, ~$0.23 AI video clips, $0 music (ACE-Step free tier)

---

## Setup (one-time)

If the toolkit isn't installed yet:

```bash
git clone https://github.com/digitalsamba/claude-code-video-toolkit.git ~/video-toolkit
cd ~/video-toolkit
python3 -m pip install -r tools/requirements.txt
```

Then from inside the toolkit directory run `claude` and execute:
- `/setup` — configure cloud GPU (Modal recommended), storage, voice settings
- `/brand` — create a brand profile for @eitanadar.ai (colors, voice, logo)

---

## Operations

### `/video-editing new [concept]` — Create a new video

Use when Eitan describes a video idea.

1. Clarify: format (vertical 9:16 Reel vs widescreen), length, template type, brand
2. Choose the right template:
   - **concept-explainer-short** — vertical Reels/TikTok, social media
   - **product-demo** — agency demo or automation walkthrough
   - **sprint-review** — project update or client delivery
3. Open the toolkit directory and run `/video` inside Claude Code
4. Edit `VOICEOVER-SCRIPT.md` with the content outline
5. Walk through phases: planning → assets → audio → editing → render

### `/video-editing reel [topic]` — Generate an Instagram Reel

For @eitanadar.ai content.

1. Use `concept-explainer-short` template (9:16 vertical)
2. Hook in first 3 seconds — confirm hook before scripting the rest
3. Script: hook → problem → insight → CTA (45–90 seconds max)
4. Generate voiceover: `/generate-voiceover` (use cloned Eitan voice if set up)
5. Generate visuals: FLUX.2 title cards + Ideogram4 scene cards
6. Render and export for Instagram

Common Reel topics for @eitanadar.ai:
- AI automation explainers for realtors
- "What I built this week" dev logs
- Real estate + AI thought leadership
- Client result case studies

### `/video-editing demo [automation]` — Build an agency demo video

For pitching automation builds to prospects.

1. Use `product-demo` template
2. Record screen walkthrough with `/record-demo` (Playwright-powered)
3. Layer AI voiceover over the recording
4. Add background music: `python tools/addmusic.py`
5. Brand it: add logo, consistent colors from brand profile
6. Render as MP4 for email attachment or Loom-style delivery

### `/video-editing voiceover [script]` — Generate AI voiceover only

Use when the video is already edited and just needs narration.

```bash
python tools/voiceover.py --provider elevenlabs --scene-dir ./audio/scenes
# or self-hosted (free):
python tools/voiceover.py --provider qwen3 --speaker Ryan --scene-dir ./audio/scenes
```

### `/video-editing music [vibe]` — Generate background music

```bash
python tools/music_gen.py --preset corporate-bg --duration 120 --output music.mp3
# presets: corporate-bg, cinematic, upbeat, ambient, dramatic
```

### `/video-editing redub [file]` — Replace voice on existing video

Useful for rebranding client videos or translating content.

```bash
python tools/redub.py --input video.mp4 --voice-id [ID] --output dubbed.mp4
```

### `/video-editing image [prompt]` — Generate a visual asset

```bash
# FLUX.2 (photorealistic)
python tools/flux2.py --preset title-bg --brand eitanadar-ai --cloud modal

# Ideogram4 (text rendering in images)
python tools/image_edit.py --input photo.jpg --prompt "Add gradient overlay" --cloud modal
```

---

## Brand Setup for @eitanadar.ai

Run `/brand` inside the toolkit and configure:

```
brands/eitanadar-ai/
├── brand.json     # Colors (neon palette), typography, logo rules
├── voice.json     # ElevenLabs voice ID or cloned voice
└── assets/        # Logo, background imagery
```

To clone Eitan's voice: record a 30-second clean audio sample, then run `/voice-clone`.

---

## Video Workflow (full production)

```
1. /video-editing new [concept]     → choose template + brand
2. Edit VOICEOVER-SCRIPT.md         → outline scenes and talking points
3. /record-demo or gather assets    → screen recording or stock/AI visuals
4. /scene-review                    → verify frames in Remotion Studio
5. /design                          → polish individual scene aesthetics
6. /generate-voiceover              → AI narration
7. npm run studio                   → live preview, timing adjustments
8. npm run render                   → final MP4 output
```

---

## Toolkit Capabilities Quick Ref

| Tool | What It Does | Cost |
|------|-------------|------|
| Qwen3-TTS voiceover | AI narration (self-hosted) | ~$0.01 |
| ElevenLabs voiceover | High-quality voice | ~$0.01 |
| FLUX.2 image gen | Photorealistic visuals | ~$0.02 |
| ACE-Step music | Background tracks | Free–$0.05 |
| LTX-2 video gen | AI video clips | ~$0.23 |
| SadTalker | Animated talking head | ~$0.10 |
| Playwright | Browser screen recording | Free |
| Remotion | React video composition | Free |

---

## File Locations

- Toolkit: `~/video-toolkit/` (or wherever cloned)
- Projects: `~/video-toolkit/projects/` (git-ignored)
- Brand profiles: `~/video-toolkit/brands/`
- Templates: `~/video-toolkit/templates/`
- Tools: `~/video-toolkit/tools/`
- Output Reels: save finished MP4s to `projects/content/reels/`
