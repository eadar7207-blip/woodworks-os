# YouTube Transcript Setup

## Dependencies

Install required packages:

```bash
pip install youtube-transcript-api requests
```

## How It Works

The skill uses the `youtube-transcript-api` library, which:
- Extracts video ID from YouTube URL
- Fetches auto-generated or manual captions
- Parses transcript into structured format
- No API key required (uses public YouTube captions)

## Usage in Scripts

```python
from youtube_transcript_api import YouTubeTranscriptApi

url = "https://www.youtube.com/watch?v=abc123"
video_id = url.split("v=")[1]
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Returns list of dicts: [{"text": "...", "start": 0.5, "duration": 5.2}, ...]
```

## Error Handling

- **Private/deleted video:** Returns "Video unavailable"
- **No captions:** Returns "No captions found"
- **Age-restricted:** Returns "Video restricted"

## Cost

Free. No YouTube API key needed.
