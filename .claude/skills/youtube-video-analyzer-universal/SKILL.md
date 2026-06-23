# YouTube Video Analyzer (Universal)

Analyzes any YouTube video by extracting audio and converting to transcript using speech recognition, then extracts key insights, themes, quotes, and repurposing ideas. Use when you need to analyze video content regardless of caption availability, for competitor research, or content repurposing.

---

## How It Works

1. **Download video** — yt-dlp extracts audio from any public YouTube video
2. **Transcribe** — OpenAI Whisper converts audio to text (works with any language/audio quality)
3. **Analyze** — Extract themes, quotes, key insights
4. **Output** — Repurposing ideas (clips, posts, blogs, ads)

No YouTube API key needed. Works on videos with or without captions.

---

## Operations

### `/youtube-video-analyzer-universal [url]` - Analyze any video

Provide any public YouTube URL. Returns:

- **Duration** (minutes)
- **Full transcript** (text)
- **Key themes** (top 5 topics)
- **Memorable quotes** (5+ excerpts with timestamps)
- **Summary** (2-3 sentence overview)
- **Repurposing ideas** (social clips, blog posts, email, ads)

**Example:** `/youtube-video-analyzer-universal https://www.youtube.com/watch?v=abc123`

Output:
```
Title: "How to Build a Startup"
Duration: 28:15
Transcript: [Full text of video]

Key Themes:
- Product-market fit (mentioned 8x)
- Customer acquisition
- Unit economics

Top Quotes:
"If you're not embarrassed by v1, you launched too late." (12:34)
"Growth without retention is just a leaky bucket." (19:22)

Repurposing:
- 30-sec clip: "embarrassed by v1" quote
- LinkedIn thread: 3 tips from the video
- Blog post: Deep dive on unit economics
- Ad copy: Hook from quote above
```

---

## Setup

See `references/whisper-setup.md` for installing dependencies.

---

## Rules

- Analyzes any public YouTube video (no captions required)
- Whisper transcription works best with clear audio
- Heavy accents or low audio quality may have minor errors
- Transcript quality improves with video length (longer = more context)
- No cost (Whisper runs locally, yt-dlp is free)

---

## Limitations

- Private or deleted videos: skipped
- Age-restricted videos: may fail
- Video duration: tested up to 2+ hours
- Audio-only YouTube content: works perfectly
