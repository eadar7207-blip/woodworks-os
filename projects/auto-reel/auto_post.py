#!/usr/bin/env python3
"""
Auto Reel Pipeline for @eitanadar.ai
Film → AirDrop to ~/Desktop/drop-here/ → posts itself.

Pipeline:
  1. Detect new video in watch folder
  2. Strip silence (ffmpeg)
  3. Transcribe (Whisper)
  4. Burn bold white captions (ffmpeg)
  5. Write Instagram caption (Claude)
  6. Post as Reel (Instagrapi)
"""

import os
import time
import shutil
import subprocess
import sys
import json
import tempfile
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
DROP_FOLDER   = Path.home() / "Desktop" / "drop-here"
PROCESSED_DIR = Path(__file__).parent / "processed"
SESSION_FILE  = Path(__file__).parent / "ig_session.json"

IG_USERNAME = "eitanadar.ai"
IG_PASSWORD = "T14082002d"

ANTHROPIC_API_KEY = os.environ.get(
    "ANTHROPIC_API_KEY",
    "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"
)

VIDEO_EXTENSIONS = {'.mp4', '.mov'}

# ── Dependencies (lazy import for speed) ────────────────────────────────
def get_ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def get_ffprobe():
    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    return str(Path(exe).parent / "ffprobe")

# ── Step 1: Strip silence + normalize, encode for Instagram ─────────────
def prepare_video(input_path: Path, output_path: Path):
    """Remove silence, normalize audio, encode H.264/AAC for Instagram."""
    ffmpeg = get_ffmpeg()
    cmd = [
        ffmpeg, '-y', '-i', str(input_path),
        # Silence removal + loudness normalization
        '-af', (
            'silenceremove=start_periods=1:start_silence=0.5:start_threshold=-40dB'
            ':stop_periods=-1:stop_silence=0.5:stop_threshold=-40dB,'
            'loudnorm'
        ),
        # Video: H.264, fast encode, keep resolution
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
        # Audio: AAC 128k
        '-c:a', 'aac', '-b:a', '128k',
        # Instagram Reel: 9:16, max 90s
        '-t', '90',
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg prepare failed:\n{result.stderr[-500:]}")

# ── Step 2: Transcribe with Whisper ─────────────────────────────────────
def transcribe(video_path: Path) -> tuple[str, list]:
    """Return (full_transcript, segments_list)."""
    import whisper
    print("  Loading Whisper model...")
    model = whisper.load_model("base")
    result = model.transcribe(str(video_path))
    transcript = result['text'].strip()
    segments = result['segments']
    return transcript, segments

# ── Step 3: Build SRT ────────────────────────────────────────────────────
def build_srt(segments: list, srt_path: Path):
    def fmt(t: float) -> str:
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t % 1) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    lines = []
    for i, seg in enumerate(segments, 1):
        text = seg['text'].strip()
        if not text:
            continue
        # Split long lines into max ~6 words per subtitle card
        words = text.split()
        chunks = [' '.join(words[j:j+6]) for j in range(0, len(words), 6)]
        duration = seg['end'] - seg['start']
        chunk_dur = duration / len(chunks)
        for k, chunk in enumerate(chunks):
            start = seg['start'] + k * chunk_dur
            end   = start + chunk_dur
            lines += [str(i * 10 + k), f"{fmt(start)} --> {fmt(end)}", chunk, ""]
    srt_path.write_text('\n'.join(lines), encoding='utf-8')

# ── Step 4: Burn captions ────────────────────────────────────────────────
def burn_captions(input_path: Path, srt_path: Path, output_path: Path):
    """Burn bold white captions — Kayvon style."""
    ffmpeg = get_ffmpeg()
    # Escape path for ffmpeg subtitles filter (colons, backslashes)
    srt_escaped = str(srt_path).replace('\\', '/').replace(':', '\\:')
    style = (
        "FontName=Arial,"
        "Bold=1,"
        "FontSize=18,"
        "PrimaryColour=&H00FFFFFF,"   # white
        "OutlineColour=&H00000000,"   # black outline
        "Outline=2,"
        "Shadow=1,"
        "Alignment=2,"                # bottom-center
        "MarginV=80"
    )
    cmd = [
        ffmpeg, '-y', '-i', str(input_path),
        '-vf', f"subtitles='{srt_escaped}':force_style='{style}'",
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
        '-c:a', 'copy',
        str(output_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # If subtitles filter fails (font issue), skip captions and continue
        print(f"  ⚠️  Caption burn failed, posting without captions: {result.stderr[-200:]}")
        shutil.copy(str(input_path), str(output_path))

# ── Step 5: Generate Instagram caption ──────────────────────────────────
def generate_caption(transcript: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": f"""Write an Instagram Reels caption for @eitanadar.ai — AI automation for real estate agents.

Copy this exact style from @kayvon.ai:
- Line 1: Punchy hook (max 12 words, no emojis in first line)
- Blank line
- 3-5 numbered steps extracted from the video
- Blank line
- "Follow me for daily AI tips for real estate agents."
- Blank line
- Hashtags: #AIRealEstate #RealtorTips #RealEstateAutomation #AITools #RealEstate #RealtorLife #PropTech

Video transcript:
{transcript}

Return the caption only. No intro text."""
        }]
    )
    return msg.content[0].text.strip()

# ── Step 6: Post as Reel ─────────────────────────────────────────────────
def post_reel(video_path: Path, caption: str):
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, BadPassword

    cl = Client()
    cl.delay_range = [2, 5]

    if SESSION_FILE.exists():
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.get_timeline_feed()  # verify session is alive
        except (LoginRequired, Exception):
            cl = Client()
            cl.delay_range = [2, 5]
            cl.login(IG_USERNAME, IG_PASSWORD)
    else:
        cl.login(IG_USERNAME, IG_PASSWORD)

    cl.dump_settings(SESSION_FILE)
    cl.clip_upload(video_path, caption)

# ── Main pipeline ────────────────────────────────────────────────────────
def process_video(video_path: Path):
    print(f"\n{'='*50}")
    print(f"🎬  {video_path.name}")
    print(f"{'='*50}")

    with tempfile.TemporaryDirectory(prefix="autoreel_") as tmp_dir:
        tmp = Path(tmp_dir)

        try:
            # 1. Prepare
            print("✂️   Stripping silence + encoding...")
            prepared = tmp / "prepared.mp4"
            prepare_video(video_path, prepared)

            # 2. Transcribe
            print("🎙️   Transcribing...")
            transcript, segments = transcribe(prepared)
            print(f"    \"{transcript[:80]}{'...' if len(transcript)>80 else ''}\"")

            # 3. SRT
            srt_path = tmp / "captions.srt"
            build_srt(segments, srt_path)

            # 4. Burn captions
            print("📝  Burning captions...")
            final = tmp / "final.mp4"
            burn_captions(prepared, srt_path, final)

            # 5. Caption
            print("✍️   Writing caption...")
            caption = generate_caption(transcript)
            print(f"\n--- CAPTION ---\n{caption}\n---------------\n")

            # 6. Post
            print("📤  Posting to @eitanadar.ai...")
            post_reel(final, caption)
            print("✅  Posted!")

            # Archive original
            PROCESSED_DIR.mkdir(exist_ok=True)
            dest = PROCESSED_DIR / f"{int(time.time())}_{video_path.name}"
            shutil.move(str(video_path), str(dest))
            print(f"📁  Archived to processed/")

        except Exception as e:
            print(f"❌  Failed: {e}")
            import traceback
            traceback.print_exc()

# ── Watch folder ─────────────────────────────────────────────────────────
def watch():
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                print(f"\n📥  Detected: {path.name}")
                time.sleep(4)  # wait for AirDrop to finish writing
                if path.exists() and path.stat().st_size > 0:
                    process_video(path)

    DROP_FOLDER.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)

    print(f"""
╔══════════════════════════════════════╗
║      Auto Reel — @eitanadar.ai       ║
╠══════════════════════════════════════╣
║  Drop a video here:                  ║
║  ~/Desktop/drop-here/                ║
║                                      ║
║  It will post itself.                ║
║  Ctrl+C to stop.                     ║
╚══════════════════════════════════════╝
""")

    observer = Observer()
    observer.schedule(Handler(), str(DROP_FOLDER), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Direct file mode: python auto_post.py video.mp4
        process_video(Path(sys.argv[1]).expanduser().resolve())
    else:
        # Watch mode
        watch()
