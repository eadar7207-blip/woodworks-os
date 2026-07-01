#!/usr/bin/env python3
"""
AI Space YouTube Intelligence Pipeline
Runs weekly: discovers trending AI videos, analyzes transcripts, generates a
slide deck, and emails it to eadar7207@gmail.com.

Usage:
  python tools/youtube_intelligence.py           # full run + send email
  python tools/youtube_intelligence.py --dry-run # full run, no email
  python tools/youtube_intelligence.py --test    # API check only, 5 videos
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
REPORTS_DIR = REPO_ROOT / "projects" / "youtube-intelligence" / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
SLIDE_BUILDER = REPO_ROOT / "tools" / "slide_builder.js"

# ── Search queries covering the AI/automation niche ──────────────────────────
SEARCH_QUERIES = [
    "AI automation 2026",
    "AI agents tutorial",
    "LLM tools workflow",
    "Claude AI agents",
    "n8n automation workflow",
    "AI for business automation",
    "ChatGPT workflow automation",
    "Make.com automation AI",
    "AI productivity tools",
    "autonomous AI agents",
]

RECIPIENT = "eadar7207@gmail.com"


# ── Phase 1: Discovery ────────────────────────────────────────────────────────

def discover_videos(test_mode: bool = False) -> list[dict]:
    from youtube_api import search_videos
    print("  Searching YouTube...")
    all_videos = []
    seen_ids = set()
    queries = SEARCH_QUERIES[:3] if test_mode else SEARCH_QUERIES

    for query in queries:
        results = search_videos(query, max_results=10, days_back=7)
        for v in results:
            if v["id"] not in seen_ids:
                seen_ids.add(v["id"])
                all_videos.append(v)

    # Deduplicate + sort by views
    all_videos.sort(key=lambda v: v["views"], reverse=True)
    cap = 30 if not test_mode else 5
    print(f"  Found {len(all_videos)} unique videos → keeping top {cap}")
    return all_videos[:cap]


def discover_channels(videos: list[dict]) -> list[dict]:
    from youtube_api import get_top_channels_from_videos
    print("  Fetching channel stats...")
    return get_top_channels_from_videos(videos, top_n=5)


# ── Phase 2: Transcript Analysis ─────────────────────────────────────────────

def fetch_and_analyze(videos: list[dict]) -> tuple[list[dict], dict]:
    """
    Returns (enriched_videos, analysis)
    analysis = {themes, key_takeaways, hooks, emerging_signals, recommendations}
    """
    from transcript_batch import fetch_transcripts_batch
    print("  Fetching transcripts...")
    enriched = fetch_transcripts_batch(videos, max_videos=20)
    has_transcripts = [v for v in enriched if v.get("transcript")]
    print(f"  Got transcripts for {len(has_transcripts)}/{len(enriched)} videos")

    analysis = synthesize_with_claude(enriched)
    return enriched, analysis


def synthesize_with_claude(videos: list[dict]) -> dict:
    """
    Calls Claude via subprocess (claude CLI) to synthesize insights.
    Falls back to keyword-based analysis if Claude CLI unavailable.
    """
    prompt_data = []
    for v in videos:
        entry = {
            "title": v["title"],
            "channel": v["channel"],
            "views": v["views"],
            "likes": v["likes"],
            "comments": v["comments"],
            "published_at": v["published_at"],
            "transcript_excerpt": (v.get("transcript") or "")[:1500],
        }
        prompt_data.append(entry)

    prompt = f"""You are analyzing YouTube videos in the AI/automation niche to produce a weekly intelligence report.

Here are the top videos from this week:

{json.dumps(prompt_data, indent=2)}

Produce a JSON object with exactly these keys:

{{
  "themes": [
    {{
      "name": "short theme name (3-5 words)",
      "description": "2-3 sentence description of what creators are saying about this",
      "score": <integer: estimate as video_count * avg_views_in_thousands>,
      "video_count": <how many videos above touch this theme>,
      "example_quotes": ["quote 1 from transcript", "quote 2", "quote 3"]
    }}
  ],
  "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3", "takeaway 4", "takeaway 5"],
  "hooks": ["title/thumbnail pattern 1", "pattern 2", "pattern 3", "pattern 4"],
  "emerging_signals": ["signal 1", "signal 2", "signal 3"],
  "recommendations": [
    "Specific video idea for @eitanadar.ai (who teaches AI automation to real estate agents)",
    "Specific video idea 2",
    "Specific video idea 3",
    "Specific video idea 4"
  ],
  "next_week_watch": ["topic to watch 1", "topic 2", "topic 3"]
}}

Return ONLY valid JSON, no other text. Identify 5-8 themes. Be specific and concrete."""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, timeout=120,
            cwd=str(REPO_ROOT)
        )
        if result.returncode == 0:
            raw = result.stdout.strip()
            # Strip markdown code block if present
            if raw.startswith("```"):
                raw = "\n".join(raw.split("\n")[1:])
                raw = raw.rsplit("```", 1)[0].strip()
            return json.loads(raw)
    except Exception as e:
        print(f"  Claude synthesis warning: {e} — using keyword fallback")

    return _keyword_fallback(videos)


def _keyword_fallback(videos: list[dict]) -> dict:
    """Simple keyword-based fallback when Claude CLI isn't available."""
    all_text = " ".join(
        (v.get("transcript") or v["title"] + " " + v.get("description", ""))
        for v in videos
    ).lower()

    theme_keywords = {
        "AI Agents & Autonomy": ["agent", "autonomous", "agentic"],
        "Workflow Automation": ["workflow", "automation", "automate", "n8n", "make"],
        "LLM Capabilities": ["llm", "language model", "gpt", "claude", "gemini"],
        "AI for Business": ["business", "roi", "productivity", "revenue", "client"],
        "Prompting Techniques": ["prompt", "prompting", "system prompt", "few-shot"],
        "No-Code AI Tools": ["no-code", "zapier", "airtable", "notion", "tool"],
        "AI in Real Estate": ["real estate", "realtor", "property", "listing"],
    }

    themes = []
    for name, kws in theme_keywords.items():
        count = sum(all_text.count(kw) for kw in kws)
        if count > 0:
            matching_videos = [
                v for v in videos
                if any(kw in (v.get("transcript") or v["title"]).lower() for kw in kws)
            ]
            avg_views = (
                sum(v["views"] for v in matching_videos) / len(matching_videos)
                if matching_videos else 0
            )
            themes.append({
                "name": name,
                "description": f"Multiple creators are discussing {name.lower()} this week.",
                "score": int(len(matching_videos) * avg_views / 1000),
                "video_count": len(matching_videos),
                "example_quotes": [v["title"] for v in matching_videos[:3]],
            })

    themes.sort(key=lambda t: t["score"], reverse=True)

    top_titles = [v["title"] for v in sorted(videos, key=lambda v: v["views"], reverse=True)[:5]]
    return {
        "themes": themes[:7],
        "key_takeaways": [
            f"Top video this week: '{videos[0]['title']}' with {videos[0]['views']:,} views" if videos else "No videos found",
            f"{len(videos)} unique AI/automation videos published this week",
            f"Most active theme: {themes[0]['name']}" if themes else "Analysis in progress",
            "Automation workflow content continues to perform well",
            "AI agent content is gaining significant traction",
        ],
        "hooks": [
            "How to [specific AI task] in under 10 minutes",
            "I replaced [X hours] of work with this AI workflow",
            "Stop using [old method] — do this instead with AI",
            "The AI tool that [dramatic claim]",
        ],
        "emerging_signals": [
            "Multi-agent systems for business operations",
            "AI voice agents for client communication",
            "Local AI models (privacy-first automation)",
        ],
        "recommendations": [
            "Create a 'AI automation for real estate agents' walkthrough using n8n or Make.com",
            "Film: 'How I saved 10 hours/week as a real estate agent using AI'",
            "Tutorial: Setting up an AI lead qualification bot for real estate",
            "Comparison: Top 3 AI tools every real estate agent needs in 2026",
        ],
        "next_week_watch": [
            "OpenAI new model releases",
            "Agent framework comparisons (AutoGPT vs LangChain vs CrewAI)",
            "AI in CRM and sales automation",
        ],
    }


# ── Phase 3: Charts ───────────────────────────────────────────────────────────

def generate_charts(videos: list[dict], channels: list[dict], themes: list[dict]) -> dict:
    from chart_generator import (
        trending_topics_chart, top_videos_chart,
        channel_subscribers_chart, engagement_scatter,
    )
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    print("  Generating charts...")

    ts = datetime.now().strftime("%Y%m%d")
    chart_paths = {}

    if themes:
        p = str(CHARTS_DIR / f"trending_topics_{ts}.png")
        chart_paths["trending_topics"] = trending_topics_chart(themes, p)

    if videos:
        p = str(CHARTS_DIR / f"top_videos_{ts}.png")
        chart_paths["top_videos"] = top_videos_chart(videos, p)

    if channels:
        p = str(CHARTS_DIR / f"channels_{ts}.png")
        chart_paths["channels"] = channel_subscribers_chart(channels, p)

    if videos:
        p = str(CHARTS_DIR / f"engagement_{ts}.png")
        result = engagement_scatter(videos, p)
        if result:
            chart_paths["engagement"] = result

    print(f"  Generated {len(chart_paths)} charts")
    return chart_paths


# ── Phase 4: Slide Deck ───────────────────────────────────────────────────────

def build_slide_deck(report: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d")
    report_json_path = output_dir / f"report_{ts}.json"
    pptx_path = output_dir / f"AI_Space_Weekly_{ts}.pptx"

    report_json_path.write_text(json.dumps(report, indent=2))
    print(f"  Building slide deck → {pptx_path.name}")

    result = subprocess.run(
        ["node", str(SLIDE_BUILDER), str(report_json_path), str(pptx_path)],
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if result.returncode != 0:
        print(f"  slide_builder error: {result.stderr}")
        raise RuntimeError("Slide deck build failed")

    print(f"  Deck built: {pptx_path}")
    return pptx_path


def convert_to_pdf(pptx_path: Path):
    """Try LibreOffice or soffice conversion. Returns PDF path or None."""
    pdf_path = pptx_path.with_suffix(".pdf")
    for cmd in ["libreoffice", "soffice"]:
        if shutil.which(cmd):
            result = subprocess.run(
                [cmd, "--headless", "--convert-to", "pdf", "--outdir",
                 str(pptx_path.parent), str(pptx_path)],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0 and pdf_path.exists():
                print(f"  PDF: {pdf_path.name}")
                return pdf_path
    print("  LibreOffice not found — attaching PPTX directly")
    return None


# ── Phase 5: Email Delivery ───────────────────────────────────────────────────

def send_report_email(report: dict, attachment: Path, dry_run: bool = False):
    top3 = report.get("key_takeaways", [])[:3]
    bullets = "\n".join(f"• {t}" for t in top3)
    week = report.get("week_label", "this week")
    subject = f"AI Space Weekly Report — Week of {week}"
    body = f"""Hi Eitan,

Your AI Space Intelligence Report for the week of {week} is attached.

Top 3 insights:
{bullets}

{len(report.get('themes', []))} trending themes identified across {report.get('video_count', 0)} videos.
{len(report.get('recommendations', []))} content recommendations for @eitanadar.ai included.

— Adar Realty Studio AI System
"""

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Sending to {RECIPIENT}...")
    print(f"  Subject: {subject}")
    if dry_run:
        print("  (Email not sent — dry run)")
        return

    try:
        import importlib.util
        send_script = REPO_ROOT / "tools" / "send_email.py"
        if send_script.exists():
            spec = importlib.util.spec_from_file_location("send_email", send_script)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.send_email(
                to=RECIPIENT,
                subject=subject,
                body=body,
                attachment=str(attachment),
            )
            print("  Email sent via Gmail API")
        else:
            print("  send_email.py not found — manual send required")
    except Exception as e:
        print(f"  Email error: {e}")
        print(f"  Deck saved at: {attachment}")


# ── Main ──────────────────────────────────────────────────────────────────────

def build_week_label() -> str:
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    fmt = "%b %d"
    return f"{monday.strftime(fmt)} - {sunday.strftime(fmt)}, {sunday.year}"


def run(dry_run: bool = False, test_mode: bool = False):
    print("\n=== AI Space Weekly Intelligence Pipeline ===\n")
    week_label = build_week_label()
    today = datetime.now().strftime("%B %d, %Y")
    print(f"Week: {week_label}")

    # Phase 1
    print("\n[1/5] Discovering trending videos...")
    videos = discover_videos(test_mode=test_mode)
    if not videos:
        print("  No videos found. Check YOUTUBE_API_KEY and quota.")
        return

    channels = discover_channels(videos)

    # Phase 2
    print("\n[2/5] Analyzing content...")
    enriched_videos, analysis = fetch_and_analyze(videos)

    # Phase 3
    print("\n[3/5] Generating charts...")
    chart_paths = generate_charts(
        enriched_videos,
        channels,
        analysis.get("themes", []),
    )

    # Assemble report payload
    report = {
        "week_label": week_label,
        "generated_at": today,
        "video_count": len(videos),
        "top_videos": videos[:10],
        "top_channels": channels,
        "charts": chart_paths,
        **analysis,
    }

    # Phase 4
    print("\n[4/5] Building slide deck...")
    output_dir = REPORTS_DIR / datetime.now().strftime("%Y-%m-%d")
    pptx_path = build_slide_deck(report, output_dir)
    attachment = convert_to_pdf(pptx_path) or pptx_path

    # Phase 5
    print("\n[5/5] Sending email...")
    send_report_email(report, attachment, dry_run=dry_run)

    print(f"\n=== Done. Report at: {attachment} ===\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Space YouTube Intelligence Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Full run but skip email send")
    parser.add_argument("--test", action="store_true", help="Quick API check: 5 videos, no email")
    args = parser.parse_args()

    if args.test:
        run(dry_run=True, test_mode=True)
    else:
        run(dry_run=args.dry_run, test_mode=False)
