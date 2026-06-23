#!/usr/bin/env python3
"""
UGC Studio - Local Video Composition Server
Runs ffmpeg locally to compose UGC ads for free.
Start with: python3 server.py
"""

import os
import json
import uuid
import subprocess
import shutil
import time
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

BASE = Path(__file__).parent
UPLOADS = BASE / "uploads" / "characters"
EXPORTS = BASE / "uploads" / "exports"
DATA = BASE / "data"

for d in [UPLOADS, EXPORTS, DATA]:
    d.mkdir(parents=True, exist_ok=True)

ALLOWED = {'mp4', 'mov', 'webm', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

def ffmpeg_available():
    return shutil.which('ffmpeg') is not None

# ── ROUTES ──────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory(BASE, 'index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'online',
        'ffmpeg': ffmpeg_available(),
        'version': '1.0.0'
    })

@app.route('/api/upload-character', methods=['POST'])
def upload_character():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400

    f = request.files['video']
    name = request.form.get('name', 'character')
    niche = request.form.get('niche', 'custom')

    if not allowed_file(f.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    char_id = 'char_' + str(int(time.time()))
    ext = f.filename.rsplit('.', 1)[1].lower()
    filename = secure_filename(f'{char_id}.{ext}')
    filepath = UPLOADS / filename
    f.save(str(filepath))

    # Generate thumbnail
    thumb_path = UPLOADS / f'{char_id}_thumb.jpg'
    if ffmpeg_available():
        subprocess.run([
            'ffmpeg', '-i', str(filepath),
            '-ss', '00:00:01',
            '-frames:v', '1',
            '-vf', 'scale=360:-1',
            str(thumb_path), '-y'
        ], capture_output=True)

    char_data = {
        'id': char_id,
        'name': name,
        'niche': niche,
        'filename': filename,
        'thumbnailUrl': f'/uploads/characters/{char_id}_thumb.jpg' if thumb_path.exists() else None,
        'createdAt': time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    chars_file = DATA / 'characters.json'
    chars = json.loads(chars_file.read_text()) if chars_file.exists() else []
    chars.insert(0, char_data)
    chars_file.write_text(json.dumps(chars, indent=2))

    return jsonify({
        'success': True,
        'url': f'/uploads/characters/{filename}',
        'charId': char_id,
        'thumbnail': char_data['thumbnailUrl']
    })

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json or {}
    char_video_url = data.get('charVideoUrl')
    script = data.get('script', '')
    hook = data.get('hook', '')
    cta = data.get('cta', '')
    style = data.get('style', 'ugc')
    caption_style = data.get('captionStyle', 'subtitle')
    ratio = data.get('ratio', '9:16')
    music = data.get('music', 'none')
    name = data.get('name', 'ugc_ad')

    if not ffmpeg_available():
        return jsonify({'error': 'ffmpeg not installed', 'hint': 'brew install ffmpeg'}), 503

    project_id = 'proj_' + str(uuid.uuid4())[:8]
    output_path = EXPORTS / f'{project_id}.mp4'

    # Resolve local character video path
    char_file = None
    if char_video_url and char_video_url.startswith('/uploads/'):
        char_file = BASE / char_video_url.lstrip('/')

    if char_file and char_file.exists():
        result = compose_video(
            char_file=str(char_file),
            script=script,
            hook=hook,
            cta=cta,
            style=style,
            caption_style=caption_style,
            ratio=ratio,
            output=str(output_path)
        )
        if result:
            return jsonify({
                'success': True,
                'projectId': project_id,
                'videoUrl': f'/exports/{project_id}.mp4',
                'downloadUrl': f'/exports/{project_id}.mp4'
            })

    # Fallback: return the character video as-is (with captions in caption list)
    if char_file and char_file.exists():
        shutil.copy(str(char_file), str(output_path))
        return jsonify({
            'success': True,
            'projectId': project_id,
            'videoUrl': f'/exports/{project_id}.mp4',
            'note': 'Raw character video returned — captions are overlay only'
        })

    return jsonify({'error': 'No character video found', 'note': 'Upload a character video first'}), 400

@app.route('/api/export', methods=['POST'])
def export_video():
    data = request.json or {}
    project_id = data.get('id', 'proj_' + str(uuid.uuid4())[:8])
    char_id = data.get('charId')
    script = data.get('script', '')
    hook = data.get('hook', '')
    cta = data.get('cta', '')
    style = data.get('style', 'ugc')
    caption_style = data.get('captionStyle', 'subtitle')
    ratio = data.get('ratio', '9:16')
    captions = data.get('captions', [])

    if not ffmpeg_available():
        return jsonify({'error': 'ffmpeg not installed. Run: brew install ffmpeg'}), 503

    # Find character video
    char_files = list(UPLOADS.glob(f'{char_id}.*'))
    char_files = [f for f in char_files if not f.name.endswith('_thumb.jpg')]

    if not char_files:
        return jsonify({'error': 'Character video not found on server'}), 404

    output_path = EXPORTS / f'{project_id}_export.mp4'
    result = compose_video(
        char_file=str(char_files[0]),
        script=script,
        hook=hook,
        cta=cta,
        style=style,
        caption_style=caption_style,
        ratio=ratio,
        output=str(output_path)
    )

    if result:
        return jsonify({'success': True, 'downloadUrl': f'/exports/{project_id}_export.mp4'})
    return jsonify({'error': 'Composition failed'}), 500

@app.route('/exports/<filename>')
def serve_export(filename):
    return send_from_directory(EXPORTS, filename)

@app.route('/uploads/characters/<filename>')
def serve_character(filename):
    return send_from_directory(UPLOADS, filename)

# ── FFMPEG COMPOSITION ──────────────────────────────────────

def compose_video(char_file, script, hook, cta, style, caption_style, ratio, output):
    """Compose the final UGC ad using ffmpeg."""
    try:
        # Get video duration
        probe = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', char_file
        ], capture_output=True, text=True)
        info = json.loads(probe.stdout)
        duration = float(next(
            (s['duration'] for s in info.get('streams', []) if s.get('codec_type') == 'video'),
            30
        ))

        # Resolution by ratio
        res_map = {'9:16': '1080x1920', '1:1': '1080x1080', '16:9': '1920x1080'}
        res = res_map.get(ratio, '1080x1920')
        w, h = map(int, res.split('x'))

        # Build subtitle file
        srt_path = output.replace('.mp4', '.srt')
        srt = build_srt(script, duration)
        Path(srt_path).write_text(srt)

        # Caption style filter
        style_filters = {
            'subtitle': f"subtitles={srt_path}:force_style='FontName=Inter,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=3,Outline=2,Shadow=1,Alignment=2'",
            'bold': f"subtitles={srt_path}:force_style='FontName=Inter,FontSize=22,PrimaryColour=&H00000000,BackColour=&H00FFFFFF,BorderStyle=4,Alignment=2,Bold=1'",
            'outline': f"subtitles={srt_path}:force_style='FontName=Inter,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=2,Bold=1'",
            'highlight': f"subtitles={srt_path}:force_style='FontName=Inter,FontSize=20,PrimaryColour=&H00FFFFFF,BackColour=&H00F06030,BorderStyle=4,Alignment=2,Bold=1'",
            'none': None
        }

        sub_filter = style_filters.get(caption_style)

        # Hook and CTA drawtext
        text_filters = []
        if hook:
            safe_hook = hook.replace("'", "").replace(":", "")[:60]
            text_filters.append(
                f"drawtext=text='{safe_hook}':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=60:box=1:boxcolor=black@0.7:boxborderw=8:enable='lt(t,3)'"
            )
        if cta:
            safe_cta = cta.replace("'", "").replace(":", "")[:50]
            text_filters.append(
                f"drawtext=text='{safe_cta}':fontsize=18:fontcolor=white:x=(w-text_w)/2:y=h-80:box=1:boxcolor=black@0.7:boxborderw=8:enable='gte(t,{max(0, duration-5)})'"
            )

        # Build complete filter chain
        vf_parts = [f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2']
        if sub_filter:
            vf_parts.append(sub_filter)
        vf_parts.extend(text_filters)
        vf = ','.join(vf_parts)

        cmd = [
            'ffmpeg', '-y',
            '-i', char_file,
            '-vf', vf,
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            output
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return True
        else:
            # Fallback: just copy without filters if sub failed
            cmd_simple = ['ffmpeg', '-y', '-i', char_file, '-c', 'copy', output]
            r = subprocess.run(cmd_simple, capture_output=True, timeout=60)
            return r.returncode == 0
    except Exception as e:
        print(f'Compose error: {e}')
        return False

def build_srt(script, total_duration):
    """Generate SRT subtitle file from script."""
    if not script.strip():
        return ''

    sentences = []
    import re
    parts = re.split(r'([.!?]+)', script)
    temp = ''
    for part in parts:
        temp += part
        if re.search(r'[.!?]$', temp.strip()):
            sentences.append(temp.strip())
            temp = ''
    if temp.strip():
        sentences.append(temp.strip())

    if not sentences:
        sentences = [script]

    lines = []
    words_per_sec = 2.3
    t = 0.0
    idx = 1

    for sent in sentences:
        words = sent.split()
        chunks = [' '.join(words[i:i+5]) for i in range(0, len(words), 5)]
        for chunk in chunks:
            dur = max(1.2, len(chunk.split()) / words_per_sec)
            start = t
            end = t + dur
            lines.append(f'{idx}')
            lines.append(f'{srt_time(start)} --> {srt_time(end)}')
            lines.append(chunk)
            lines.append('')
            t = end
            idx += 1

    return '\n'.join(lines)

def srt_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'

# ── START ────────────────────────────────────────────────────

if __name__ == '__main__':
    print('─' * 50)
    print('  UGC Studio Server')
    print(f'  http://localhost:8765')
    print(f'  ffmpeg: {"✓ installed" if ffmpeg_available() else "✗ missing — run: brew install ffmpeg"}')
    print('─' * 50)
    app.run(host='0.0.0.0', port=8765, debug=False)
