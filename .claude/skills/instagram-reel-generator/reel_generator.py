#!/usr/bin/env python3
"""
Instagram Reel Generator for Real Estate
Converts property videos/photos into Instagram-ready reels
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Try to import video libraries
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not installed. Install with: pip install moviepy")

try:
    import ffmpeg
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False
    print("⚠️  FFmpeg not installed. Install with: brew install ffmpeg")


class InstagramReelGenerator:
    """Generate Instagram reels from property videos/photos"""

    # Instagram specs
    WIDTH = 1080
    HEIGHT = 1920
    ASPECT_RATIO = 9 / 16
    FPS = 30
    OPTIMAL_DURATION = 60  # seconds

    # Music tracks (royalty-free samples)
    MUSIC_TRACKS = {
        'luxury': 'https://example.com/luxury-bg.mp3',
        'modern': 'https://example.com/modern-bg.mp3',
        'cozy': 'https://example.com/cozy-bg.mp3',
        'energetic': 'https://example.com/energetic-bg.mp3',
    }

    def __init__(self, address, video_path, property_details, mood='modern', duration=None, style='bold', cta='Schedule Showing'):
        self.address = address
        self.video_path = video_path
        self.property_details = property_details
        self.mood = mood
        self.duration = duration or self.OPTIMAL_DURATION
        self.style = style
        self.cta = cta
        self.output_dir = Path('output')
        self.output_dir.mkdir(exist_ok=True)

    def validate_input(self):
        """Check if video file exists"""
        if not Path(self.video_path).exists():
            return {'success': False, 'error': f'Video file not found: {self.video_path}'}
        return {'success': True}

    def trim_video(self, input_path, output_path, duration=60):
        """Trim video to optimal length (60 seconds)"""
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-t', str(duration),
                '-c:v', 'libx264', '-preset', 'fast',
                '-c:a', 'aac',
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {'success': True, 'output': str(output_path)}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def scale_to_instagram(self, input_path, output_path):
        """Scale video to Instagram 9:16 format (1080x1920)"""
        try:
            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-vf', f'scale={self.WIDTH}:{self.HEIGHT}:force_original_aspect_ratio=decrease,pad={self.WIDTH}:{self.HEIGHT}:(ow-iw)/2:(oh-ih)/2:black',
                '-c:v', 'libx264', '-preset', 'fast',
                '-c:a', 'aac',
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def add_text_overlays(self, input_path, output_path):
        """Add property address, details, and CTA as text overlays"""
        try:
            # Build FFmpeg filter complex for text overlays
            filters = [
                # Address at top (0-5 seconds)
                f"drawtext=text='{self.address}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h*0.1:enable='between(t,0,5)':box=1:boxcolor=black@0.5",
                # Details in middle
                f"drawtext=text='{self.property_details}':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=h*0.45:box=1:boxcolor=black@0.5",
                # CTA at end (last 5 seconds)
                f"drawtext=text='{self.cta}':fontsize=50:fontcolor=yellow:x=(w-text_w)/2:y=h*0.85:enable='gte(t,55)':box=1:boxcolor=black@0.7"
            ]

            cmd = [
                'ffmpeg', '-i', str(input_path),
                '-vf', ','.join(filters),
                '-c:v', 'libx264', '-preset', 'fast',
                '-c:a', 'aac',
                str(output_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def generate(self):
        """Generate the Instagram reel"""
        try:
            # Validate input
            validation = self.validate_input()
            if not validation['success']:
                return validation

            # Clean address for filename
            safe_address = self.address.replace('/', '-').replace(' ', '_')[:30]
            temp_trimmed = self.output_dir / f'{safe_address}_trimmed.mp4'
            temp_scaled = self.output_dir / f'{safe_address}_scaled.mp4'
            final_output = self.output_dir / f'{safe_address}_reel.mp4'

            print(f'📹 Trimming video to {self.duration}s...')
            trim_result = self.trim_video(self.video_path, temp_trimmed, self.duration)
            if not trim_result['success']:
                return trim_result

            print(f'📐 Scaling to Instagram 9:16 format...')
            scale_result = self.scale_to_instagram(temp_trimmed, temp_scaled)
            if not scale_result['success']:
                return scale_result

            print(f'📝 Adding text overlays...')
            overlay_result = self.add_text_overlays(temp_scaled, final_output)
            if not overlay_result['success']:
                return overlay_result

            # Cleanup temp files
            temp_trimmed.unlink(missing_ok=True)
            temp_scaled.unlink(missing_ok=True)

            print(f'✅ Reel generated: {final_output}')

            return {
                'success': True,
                'reel_file': str(final_output),
                'address': self.address,
                'details': self.property_details,
                'duration': self.duration,
                'format': f'{self.WIDTH}x{self.HEIGHT}',
                'ready_to_post': True,
                'message': f'Your Instagram reel is ready! Upload to Instagram Reels or Stories.'
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}


def main():
    """CLI interface"""
    if len(sys.argv) < 4:
        print('Usage: python reel_generator.py "<address>" "<video_file>" "<details>"')
        print('Example: python reel_generator.py "123 Oak St" "property.mp4" "3BR/2BA • $450K"')
        sys.exit(1)

    address = sys.argv[1]
    video_file = sys.argv[2]
    details = sys.argv[3]
    mood = sys.argv[4] if len(sys.argv) > 4 else 'modern'

    # Check dependencies
    if not FFMPEG_AVAILABLE:
        print('Error: FFmpeg not installed. Run: brew install ffmpeg')
        sys.exit(1)

    # Generate reel
    generator = InstagramReelGenerator(address, video_file, details, mood=mood)
    result = generator.generate()

    # Output result
    print(json.dumps(result, indent=2))

    if not result['success']:
        sys.exit(1)


if __name__ == '__main__':
    main()
