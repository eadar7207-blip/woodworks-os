#!/usr/bin/env python3
"""Build professional carousel with verification."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

WHITE = (255, 255, 255)
BLACK = (15, 15, 15)
GRAY = (120, 120, 120)
LIGHT_GRAY = (245, 245, 245)
ACCENT = (80, 160, 240)

PROMPTS = [
    {"headline": "Lead\nQualification", "subtitle": "Ask 3 questions. Instantly know if they're serious.", "detail": "Save 5+ hours qualifying leads every week"},
    {"headline": "Proposal\nGeneration", "subtitle": "2 minutes. Not 2 hours.", "detail": "Professional proposals that close deals faster"},
    {"headline": "Email\nSequences", "subtitle": "Write follow-ups that actually get responses.", "detail": "Higher reply rates. Consistent follow-up."},
    {"headline": "CRM\nOrganization", "subtitle": "Analyze your data. Find hot leads.", "detail": "Know who's stale, who's hot, who's closing"},
    {"headline": "Client\nCommunication", "subtitle": "Say the right thing at the right time.", "detail": "Handle objections. Keep deals alive."}
]

def create_slide(num, data):
    """Create professional carousel slide."""
    img = Image.new('RGB', (1080, 1350), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Load fonts - try multiple paths
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Avenir.ttc"
    ]
    
    title_font = None
    for path in font_paths:
        try:
            title_font = ImageFont.truetype(path, 140)
            break
        except:
            pass
    
    subtitle_font = None
    for path in font_paths:
        try:
            subtitle_font = ImageFont.truetype(path, 56)
            break
        except:
            pass
    
    detail_font = None
    for path in font_paths:
        try:
            detail_font = ImageFont.truetype(path, 44)
            break
        except:
            pass
    
    username_font = None
    for path in font_paths:
        try:
            username_font = ImageFont.truetype(path, 36)
            break
        except:
            pass
    
    # Username top left
    draw.text((60, 50), "@eitanadar.ai", fill=GRAY, font=username_font)
    draw.text((1000, 50), f"{num}/5", fill=LIGHT_GRAY, font=username_font, anchor="rt")
    
    # Accent line under username
    draw.rectangle([(0, 130), (1080, 140)], fill=ACCENT)
    
    # LARGE headline centered
    headline_y = 280
    draw.text((540, headline_y), data["headline"], fill=BLACK, font=title_font, anchor="mm")
    
    # Subtitle in accent color
    subtitle_y = 650
    draw.text((540, subtitle_y), data["subtitle"], fill=ACCENT, font=subtitle_font, anchor="mm")
    
    # Detail text
    detail_y = 850
    draw.text((540, detail_y), data["detail"], fill=GRAY, font=detail_font, anchor="mm")
    
    # Bottom section
    draw.rectangle([(0, 1150), (1080, 1350)], fill=LIGHT_GRAY)
    draw.text((540, 1220), "AI Prompts for Real Estate", fill=BLACK, font=detail_font, anchor="mm")
    draw.text((540, 1300), "@eitanadar.ai", fill=ACCENT, font=subtitle_font, anchor="mm")
    
    return img

def main():
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides-final" / "images"
    
    print("=" * 60)
    print("🎨 BUILDING CAROUSEL - WITH VERIFICATION")
    print("=" * 60)
    
    # Clean directory
    carousel_dir.mkdir(parents=True, exist_ok=True)
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    print(f"✓ Cleared old images from {carousel_dir}")
    
    # Create slides
    print(f"\n📝 Creating {len(PROMPTS)} slides...")
    created_files = []
    
    for i, data in enumerate(PROMPTS, 1):
        img = create_slide(i, data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        created_files.append(path)
        print(f"  ✓ Slide {i}: {path.name}")
    
    # VERIFY files exist and have content
    print(f"\n✅ VERIFICATION:")
    print(f"   Total files expected: {len(PROMPTS)}")
    print(f"   Total files created: {len(created_files)}")
    
    all_exist = True
    for path in created_files:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"   ✓ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {path.name} MISSING!")
            all_exist = False
    
    if all_exist and len(created_files) == len(PROMPTS):
        print(f"\n🎉 SUCCESS! All {len(PROMPTS)} slides created and verified!")
        print(f"\n📤 Ready to post:")
        print(f"   /post realtor-prompts-5-slides-final")
    else:
        print(f"\n❌ FAILED! Files missing or not created correctly")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
