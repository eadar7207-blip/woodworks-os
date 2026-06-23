#!/usr/bin/env python3
"""
Fetch YouTube transcript and analyze for key insights.
"""

import sys
import json
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api not installed. Run: pip install youtube-transcript-api")
    sys.exit(1)


def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    try:
        if "youtube.com" in url:
            return parse_qs(urlparse(url).query)["v"][0]
        elif "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
    except:
        return None


def fetch_transcript(video_id):
    """Fetch transcript for video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return None


def analyze_transcript(transcript):
    """Extract key insights from transcript."""
    if not transcript:
        return None

    # Join all text
    full_text = " ".join([item["text"] for item in transcript])

    # Simple analysis: extract sentences with high-value keywords
    sentences = full_text.split(".")

    # Extract key themes (common words/phrases)
    words = full_text.lower().split()
    word_freq = {}
    for word in words:
        if len(word) > 4:  # Filter short words
            word_freq[word] = word_freq.get(word, 0) + 1

    top_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    themes = [word for word, _ in top_themes]

    # Extract quotes (sentences over 20 words)
    quotes = [s.strip() for s in sentences if 20 < len(s.split()) < 50][:3]

    # Calculate duration
    total_duration = sum([item["duration"] for item in transcript])

    return {
        "duration_seconds": int(total_duration),
        "text_summary": full_text[:500] + "...",
        "key_themes": themes,
        "sample_quotes": quotes,
        "transcript_length": len(transcript),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_and_analyze.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    video_id = extract_video_id(url)

    if not video_id:
        print(json.dumps({"error": "Invalid YouTube URL"}))
        sys.exit(1)

    transcript = fetch_transcript(video_id)
    if not transcript:
        print(json.dumps({"error": "Could not fetch transcript (private/restricted/no captions)"}))
        sys.exit(1)

    analysis = analyze_transcript(transcript)
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
