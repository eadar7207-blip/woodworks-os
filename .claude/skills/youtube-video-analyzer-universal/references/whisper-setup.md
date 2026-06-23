# Whisper Setup Guide

## Dependencies

Install required packages:

```bash
pip install openai-whisper yt-dlp
```

## How It Works

**yt-dlp:**
- Downloads audio from any YouTube video
- Works even if video is not embeddable or has restrictions
- Extracts as .mp3 or .wav

**Whisper:**
- OpenAI's open-source speech-to-text model
- Runs locally (no API key, no cost, no internet required after download)
- Supports 99+ languages
- Handles accents, background noise, music

## Model Sizes

Whisper comes in 5 sizes (trade-off between speed and accuracy):

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 39M | Fast | 60% |
| base | 140M | Good | 80% |
| small | 244M | Good | 85% |
| medium | 769M | Slower | 90% |
| large | 2.9GB | Slowest | 95% |

**Recommended:** `base` (140MB, ~30 sec for 1 min of audio)

## Usage in Scripts

```python
import whisper
from yt_dlp import YoutubeDL

# Download audio
ydl_opts = {"format": "bestaudio", "postprocessors": [...]}
with YoutubeDL(ydl_opts) as ydl:
    ydl.download(["https://youtube.com/watch?v=abc123"])

# Transcribe
model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
transcript = result["text"]
```

## Cost

Free. All processing happens on your machine.

## Performance

- 1 minute video → ~1 minute to transcribe (base model, M1/M2 Mac)
- 30 minute video → ~30 minutes to transcribe
- Longer videos benefit from async processing
