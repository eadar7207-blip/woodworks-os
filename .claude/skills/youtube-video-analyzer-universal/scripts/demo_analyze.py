#!/usr/bin/env python3
"""
Demo of what the youtube-video-analyzer-universal produces.
Shows realistic output without requiring Whisper installation.
"""

import json
from urllib.parse import urlparse, parse_qs

DEMO_VIDEOS = {
    "NHFbAg2b54U": {
        "title": "How to Grow Your Agency Fast",
        "duration": "18:45",
        "themes": ["growth", "scaling", "marketing", "sales", "automation"],
        "quotes": [
            "The best time to optimize is when you're already making money (12:34)",
            "Don't chase vanity metrics, focus on unit economics (7:22)",
            "Your first hire should be someone who does what you hate (14:15)"
        ],
        "summary": "Founder shares framework for scaling an agency from 0 to 7-figures. Covers customer acquisition, pricing strategy, operational leverage, and team building.",
        "repurposing": [
            "30-sec clip: 'unit economics' quote",
            "LinkedIn thread: 3 scaling principles",
            "Email: Growth framework for prospects",
            "Ad copy: 'First hire' quote as hook"
        ]
    }
}

def analyze_demo(url):
    """Demo analysis output."""
    try:
        if "youtube.com" in url:
            video_id = url.split("v=")[1].split("&")[0]
        else:
            video_id = url.split("/")[-1].split("?")[0]
    except:
        return {"error": "Invalid YouTube URL"}

    # Check if we have demo data
    if video_id in DEMO_VIDEOS:
        data = DEMO_VIDEOS[video_id]
        return {
            "status": "demo",
            "video_id": video_id,
            "title": data["title"],
            "duration": data["duration"],
            "key_themes": data["themes"],
            "sample_quotes": data["quotes"],
            "summary": data["summary"],
            "repurposing_ideas": data["repurposing"],
            "note": "This is a DEMO output. Full skill requires Whisper installation."
        }
    else:
        return {
            "status": "demo",
            "video_id": video_id,
            "message": f"Demo data not available for {video_id}",
            "example_output": {
                "title": "[Video Title]",
                "duration": "[Minutes:Seconds]",
                "key_themes": ["topic1", "topic2", "topic3"],
                "sample_quotes": ["'Important quote' (timestamp)"],
                "summary": "2-3 sentence overview of video content",
                "repurposing_ideas": ["30-sec clip idea", "LinkedIn post", "Blog post", "Ad copy"]
            },
            "note": "Real analyzer requires: pip install openai-whisper yt-dlp"
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python demo_analyze.py <youtube_url>"}))
        sys.exit(1)

    url = sys.argv[1]
    result = analyze_demo(url)
    print(json.dumps(result, indent=2))
