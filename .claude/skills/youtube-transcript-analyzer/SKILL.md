# YouTube Transcript Analyzer

Fetches YouTube video transcripts and extracts key insights, themes, and actionable takeaways. Use when you need to analyze video content for messaging, repurposing ideas, or strategic insights without watching the full video.

---

## Operations

### `/youtube-transcript-analyzer [url]` - Analyze a YouTube video

Provide a YouTube URL. The skill will:

1. Fetch the transcript (auto-generated captions if manual unavailable)
2. Extract summary (2-3 sentences of main message)
3. Identify key themes (3-5 major topics)
4. Pull memorable quotes or insights
5. Suggest repurposing ideas (social posts, blog, email, clips)
6. Flag messaging gaps or opportunities

**Example:** `/youtube-transcript-analyzer https://www.youtube.com/watch?v=abc123`

Output:
```
Title: "How to Scale Your Business"
Duration: 15:34
Summary: Founder shares 3 growth strategies: product-market fit, customer acquisition, and retention metrics.

Key Themes:
- Product-market fit (mentioned 4x)
- Unit economics
- Customer retention

Top Quotes:
"Growth without unit economics is just vanity." (5:22)

Repurposing:
- 30-sec clip: retention metrics segment
- LinkedIn post: quote + 3-line thread
- Blog: deep-dive on unit economics
```

---

## Analysis Rules

- Return transcript if available; skip paywalled/private videos
- Summarize objectively (no opinion)
- Extract direct quotes with timestamps
- Suggest 3+ repurposing angles
- Flag if transcript is auto-generated (may have errors)

---

## Setup

See `references/youtube-api-setup.md` for installing dependencies.

---

## Limitations

- Private, age-restricted, or deleted videos: skipped
- Manual captions only if auto-generated unavailable
- Analysis quality depends on transcript clarity (heavy accents may have errors)
