---
name: video
description: Analyze any video file or URL for transcript, summary, scene breakdown, messaging, and insights.
---

# Video

Use this skill when the user wants to analyze a video asset, review its content, or derive actionable insights from visual/audio media.

---

## Operations

### `/video [url|file]` - analyze a video

When the user provides a video URL or uploads a video file:

1. Confirm the format and any context needed: purpose, audience, target use, language, and whether they want a transcript, summary, or creative/marketing review.
2. Extract or transcribe audio/dialogue. If subtitles/captions are available, use them too.
3. Produce a concise summary of the video.
4. Provide a chapter-style breakdown with timestamps for key scenes, topics, or sections.
5. Identify main speakers, themes, and emotional tone.
6. Note any visual or messaging issues: pacing, clarity, brand alignment, or accessibility concerns.
7. Share recommended improvements, next steps, or how to repurpose the video.

Example: `/video https://example.com/my-demo.mp4`

### `/video transcript` - get the transcript

Use when the user needs the dialogue or spoken content in text form.

1. Transcribe the full audio track.
2. Preserve speaker labels when possible.
3. Optionally annotate with timestamps and scene notes.

### `/video audit` - review messaging and creative quality

Use when the user wants a critique rather than just a summary.

1. Assess the video’s core message and audience fit.
2. Evaluate structure, storytelling, hooks, and calls to action.
3. Highlight strengths, weak points, and audience impact.
4. Suggest edits for clarity, engagement, or conversion.

### `/video insights` - extract key takeaways and reuse ideas

Use for generating reusable content from the video.

1. Compile top insights, quotes, and memorable moments.
2. Suggest social posts, blog topics, or ad copy based on the video.
3. Recommend how to turn the video into shorter clips, snippets, or supporting assets.

---

## Video Analysis Rules

- Always ask for the video source when not provided.
- Verify whether the user wants a neutral summary, a marketing critique, or a technical analysis.
- Keep answers structured: summary, scenes, insights, recommendations.
- Use timestamps whenever you reference specific moments.
- If the file is too large to process directly, explain the limitation and ask for an alternative upload or a shorter clip.
