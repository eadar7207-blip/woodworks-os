"""
YouTube Data API v3 wrapper.
Handles search, video metadata, and channel stats.
Requires YOUTUBE_API_KEY in .env
"""

import os
from datetime import datetime, timedelta, timezone
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def _client():
    if not API_KEY:
        raise EnvironmentError(
            "YOUTUBE_API_KEY not set. Add it to .env\n"
            "Get one free at: console.cloud.google.com → YouTube Data API v3"
        )
    return build("youtube", "v3", developerKey=API_KEY)


def search_videos(query: str, max_results: int = 10, days_back: int = 7) -> list[dict]:
    """Search for videos published in the last N days. Returns list of video dicts."""
    youtube = _client()
    published_after = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    response = youtube.search().list(
        q=query,
        part="id,snippet",
        type="video",
        order="viewCount",
        publishedAfter=published_after,
        maxResults=max_results,
        relevanceLanguage="en",
    ).execute()

    video_ids = [item["id"]["videoId"] for item in response.get("items", [])]
    if not video_ids:
        return []
    return get_video_stats(video_ids)


def get_video_stats(video_ids: list[str]) -> list[dict]:
    """Fetch title, channel, views, likes, comments, duration for a list of video IDs."""
    youtube = _client()
    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids),
    ).execute()

    videos = []
    for item in response.get("items", []):
        stats = item.get("statistics", {})
        snippet = item["snippet"]
        videos.append(
            {
                "id": item["id"],
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "channel_id": snippet["channelId"],
                "published_at": snippet["publishedAt"],
                "description": snippet.get("description", "")[:300],
                "thumbnail": snippet["thumbnails"].get("high", {}).get("url", ""),
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                "duration": item["contentDetails"]["duration"],
                "url": f"https://www.youtube.com/watch?v={item['id']}",
            }
        )
    return sorted(videos, key=lambda v: v["views"], reverse=True)


def get_channel_stats(channel_ids: list[str]) -> list[dict]:
    """Fetch subscriber count, video count, and view count for channels."""
    youtube = _client()
    response = youtube.channels().list(
        part="snippet,statistics",
        id=",".join(channel_ids),
    ).execute()

    channels = []
    for item in response.get("items", []):
        stats = item.get("statistics", {})
        snippet = item["snippet"]
        channels.append(
            {
                "id": item["id"],
                "name": snippet["title"],
                "description": snippet.get("description", "")[:200],
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "video_count": int(stats.get("videoCount", 0)),
                "url": f"https://www.youtube.com/channel/{item['id']}",
            }
        )
    return sorted(channels, key=lambda c: c["subscribers"], reverse=True)


def get_top_channels_from_videos(videos: list[dict], top_n: int = 5) -> list[dict]:
    """Extract unique channels from video list and fetch their stats."""
    seen = {}
    for v in videos:
        cid = v["channel_id"]
        if cid not in seen:
            seen[cid] = v["channel"]
    top_ids = list(seen.keys())[:top_n * 3]
    channels = get_channel_stats(top_ids)
    return channels[:top_n]
