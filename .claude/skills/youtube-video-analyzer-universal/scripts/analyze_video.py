#!/usr/bin/env python3
"""
Analyze any YouTube video by downloading, transcribing with Whisper, and extracting insights.
"""

import sys
import json
import subprocess
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    import whisper
except ImportError:
    print("Error: openai-whisper not installed. Run: pip install openai-whisper yt-dlp")
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


def download_audio(url):
    """Download audio from YouTube video using yt-dlp."""
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return None

        audio_path = f"/tmp/{video_id}.mp3"

        # Use yt-dlp to download audio
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-x",
            "--audio-format", "mp3",
            "-o", audio_path,
            url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return None

        if os.path.exists(audio_path):
            return audio_path

        return None
    except Exception as e:
        return None


def transcribe_audio(audio_path):
    """Transcribe audio using Whisper."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return None


def analyze_transcript(transcript):
    """Extract insights from transcript."""
    if not transcript:
        return None

    # Extract sentences
    sentences = [s.strip() for s in transcript.split(".") if s.strip()]

    # Extract key words (frequency-based)
    words = transcript.lower().split()
    word_freq = {}
    for word in words:
        if len(word) > 5 and word not in ["the", "that", "this", "with", "from"]:
            word_freq[word] = word_freq.get(word, 0) + 1

    top_themes = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    themes = [word for word, _ in top_themes]

    # Extract longer quotes (meaningful sentences)
    quotes = [s for s in sentences if 15 < len(s.split()) < 50][:5]

    # Summary
    summary = " ".join(sentences[:3]) if sentences else ""

    return {
        "transcript_length": len(transcript),
        "sentence_count": len(sentences),
        "key_themes": themes,
        "sample_quotes": quotes,
        "summary": summary[:500] + "..." if len(summary) > 500 else summary
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_video.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]

    print("Downloading audio...")
    audio_path = download_audio(url)

    if not audio_path:
        print(json.dumps({"error": "Failed to download video (private/restricted or yt-dlp not installed)"}))
        sys.exit(1)

    print("Transcribing with Whisper (this may take a moment)...")
    transcript = transcribe_audio(audio_path)

    if not transcript:
        print(json.dumps({"error": "Failed to transcribe audio"}))
        sys.exit(1)

    analysis = analyze_transcript(transcript)
    analysis["status"] = "success"
    analysis["full_transcript"] = transcript[:1000] + "..." if len(transcript) > 1000 else transcript

    print(json.dumps(analysis, indent=2))

    # Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)


if __name__ == "__main__":
    main()
