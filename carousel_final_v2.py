#!/usr/bin/env python3
"""Professional carousel with proper fonts."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
LIGHT_GRAY = (240, 240, 240)
ACCENT = (70, 150, 220)

PROMPTS = [
    {"headline": "Lead\nQualification", "subtitle": "Ask 3 questions. Instantly know if they're serious.", "detail": "Save 5+ hours qualifying leads every week"},
    {"headline": "Proposal\nGeneration", "subtitle": "2 minutes. Not 2 hours.", "detail": "Professional proposals that close deals faster"},
    {"headline": "Email\nSequences", "subtitle": "Write follow-ups that actually get responses.", "detail": "Higher reply rates. Consistent follow-up."},
    {"headline": "CRM\nOrganization", "subtitle": "Analyze your data. Find hot leads.", "detail": "Know who's stale, who's hot, who's closing"},
    {"headline": "Client\nCommunication", "subtitle": "Say the right thing at the right time.", "detail": "Handle objections. Keep deals alive."}
]

def create_slide(num, data):
    """Create professional slide."""
    img = Image.new('RGB', (1080, 1350), WHITE)
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load system fonts with larger sizes
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        detail_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        username_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
    except:
        # Fallback if fonts not found
        title_font = None
        subtitle_font = None
        detail_font = None
        username_font = None
    
    # Username
    draw.text((80, 60), "@eitanadar.ai", fill=GRAY, font=username_font)
    draw.text((900, 60), f"{num}/5", fill=LIGHT_GRAY, font=username_font, anchor="rt")
    
    # Accent line
    draw.rectangle([(0, 120), (1080, 125)], fill=ACCENT)
    
    # LARGE headline
    draw.text((80, 250), data["headline"], fill=BLACK, font=title_font)
    
    # Subtitle
    draw.text((80, 600), data["subtitle"], fill=ACCENT, font=subtitle_font)
    
    # Detail
    draw.text((80, 800), data["detail"], fill=GRAY, font=detail_font)
    
    # Bottom CTA
    draw.rectangle([(0, 1150), (1080, 1350)], fill=LIGHT_GRAY)
    draw.text((540, 1220), "AI Prompts for Real Estate Pros", fill=BLACK, font=detail_font, anchor="mm")
    draw.text((540, 1300), "@eitanadar.ai", fill=ACCENT, font=subtitle_font, anchor="mm")
    
    return img

def main():
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides-final" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("🎨 Creating carousel with LARGE readable text...")
    
    for i, data in enumerate(PROMPTS, 1):
        img = create_slide(i, data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        print(f"  ✓ Slide {i}/5")
    
    print("\n✅ Done! Post to Instagram:")
    print("  /post realtor-prompts-5-slides-final")

if __name__ == "__main__":
    main()
