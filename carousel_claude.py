#!/usr/bin/env python3
"""5 slides, 1 prompt each. Claude-specific."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

WHITE = (255, 255, 255)
BLACK = (15, 15, 15)
GRAY = (120, 120, 120)
LIGHT_GRAY = (245, 245, 245)
ACCENT = (80, 160, 240)
CLAUDE_PURPLE = (155, 89, 182)

PROMPTS = [
    {
        "title": "Lead Qualification",
        "emoji": "🎯",
        "prompt": '"Analyze this lead\'s profile and tell me: (1) Are they a serious buyer or just browsing? (2) What\'s their likely budget range? (3) What\'s the best next step?"'
    },
    {
        "title": "Proposal Generation",
        "emoji": "📄",
        "prompt": '"Create a professional real estate proposal for a [property type] in [location]. Client: [name]. Price: [price]. Key selling points: [list]. Make it impressive and concise."'
    },
    {
        "title": "Email Sequences",
        "emoji": "📧",
        "prompt": '"Write a follow-up email sequence for prospects who viewed properties but haven\'t made offers. [Prospect context]. Make it feel personal, not salesy."'
    },
    {
        "title": "CRM Organization",
        "emoji": "📊",
        "prompt": '"Analyze my CRM data and tell me: How many leads are stale? Which should get follow-up calls today? What deals are close to closing? [Paste summary]"'
    },
    {
        "title": "Client Communication",
        "emoji": "💬",
        "prompt": '"Write an email to a buyer who\'s getting cold feet about [concern]. Reassure them without being pushy. Keep them confident but realistic."'
    }
]

def create_slide(num, data):
    """Create Claude-specific prompt slide."""
    img = Image.new('RGB', (1080, 1350), WHITE)
    draw = ImageDraw.Draw(img)
    
    font_paths = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]
    
    title_font = None
    for path in font_paths:
        try:
            title_font = ImageFont.truetype(path, 120)
            break
        except:
            pass
    
    prompt_font = None
    for path in font_paths:
        try:
            prompt_font = ImageFont.truetype(path, 48)
            break
        except:
            pass
    
    username_font = None
    for path in font_paths:
        try:
            username_font = ImageFont.truetype(path, 32)
            break
        except:
            pass
    
    # Top bar
    draw.text((60, 50), "@eitanadar.ai", fill=GRAY, font=username_font)
    draw.text((1000, 50), f"{num}/5", fill=LIGHT_GRAY, font=username_font, anchor="rt")
    draw.rectangle([(0, 130), (1080, 140)], fill=CLAUDE_PURPLE)
    
    # Emoji
    draw.text((540, 220), data["emoji"], fill=BLACK, font=None, anchor="mm")
    
    # Title
    draw.text((540, 320), data["title"], fill=BLACK, font=title_font, anchor="mm")
    
    # THE PROMPT
    draw.rectangle([(80, 480), (1000, 1100)], outline=CLAUDE_PURPLE, width=3)
    draw.rectangle([(85, 485), (995, 1095)], fill=(250, 250, 250))
    
    prompt = data["prompt"]
    words = prompt.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 40:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    
    y = 530
    for line in lines:
        draw.text((540, y), line, fill=BLACK, font=prompt_font, anchor="mm")
        y += 70
    
    # Bottom: Claude-specific CTA
    draw.rectangle([(0, 1150), (1080, 1350)], fill=LIGHT_GRAY)
    draw.text((540, 1230), "Copy & paste into Claude AI", fill=CLAUDE_PURPLE, font=username_font, anchor="mm")
    draw.text((540, 1310), "Follow @eitanadar.ai for more prompts", fill=BLACK, font=username_font, anchor="mm")
    
    return img

def main():
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides-final" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("=" * 60)
    print("🎨 BUILDING: 5 SLIDES, 1 CLAUDE PROMPT EACH")
    print("=" * 60)
    
    created = []
    for i, data in enumerate(PROMPTS, 1):
        img = create_slide(i, data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        created.append(path)
        print(f"  ✓ Slide {i}: {data['title']}")
    
    print(f"\n✅ VERIFIED: {len(created)} slides created")
    for path in created:
        size = path.stat().st_size / 1024
        print(f"   ✓ {path.name} ({size:.0f} KB)")
    
    print(f"\n📤 Ready to post:")
    print(f"   /post realtor-prompts-5-slides-final")

if __name__ == "__main__":
    main()
