---
name: meeting-insights
description: Pull the latest call transcript from Fathom and analyze it. Works for Google Meet, Zoom, and Teams. No Zapier needed.
---

# Meeting Insights

Analyze call transcripts using the meeting-insights-analyzer skill at `.claude/skills/awesome-claude-skills/meeting-insights-analyzer/SKILL.md`.

## Default Flow (no arguments)

1. Use Playwright to open fathom.video
2. Log in if needed (credentials in .env as FATHOM_EMAIL and FATHOM_PASSWORD)
3. Navigate to the most recent call recording
4. Copy the full transcript text
5. Run analysis per the skill instructions below

## If user provides a source

- Google Drive link → use Google Drive MCP to fetch the doc
- Local file path → read directly
- Pasted text → analyze as-is

## Analysis

After pulling the transcript, invoke the meeting-insights-analyzer skill. Always surface:

- Full summary of what was discussed
- What the other person said about budget, timeline, or pain points
- Objections raised
- Action items and next steps
- Any commitments made by either party

If the user asks a specific question ("what did he say about X"), answer that directly first, then give the summary.

## Setup (one-time)

Add to `.env`:
```
FATHOM_EMAIL=your@email.com
FATHOM_PASSWORD=yourpassword
```

Fathom is free at fathom.video. It auto-joins and transcribes every Google Meet, Zoom, and Teams call with no setup per call.

## Usage Examples

```
/meeting-insights
/meeting-insights - what did he say about pricing?
/meeting-insights - pull the call with Sohail
/meeting-insights [Google Drive link]
```
