"""
Batch transcript fetcher.
Pulls transcripts for a list of YouTube video IDs using youtube-transcript-api.
Falls back gracefully on private/age-restricted/captionless videos.
"""

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


def fetch_transcript(video_id: str):
    """Return full transcript text for a video, or None if unavailable."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(entry["text"] for entry in transcript_list)
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None


def fetch_transcripts_batch(videos: list[dict], max_videos: int = 20) -> list[dict]:
    """
    Add transcript text to each video dict.
    Skips videos where transcripts are unavailable.
    Returns only videos that have transcripts (up to max_videos).
    """
    enriched = []
    for video in videos:
        if len(enriched) >= max_videos:
            break
        transcript = fetch_transcript(video["id"])
        if transcript:
            enriched.append({**video, "transcript": transcript})
        else:
            enriched.append({**video, "transcript": None})
    return enriched
