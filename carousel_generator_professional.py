#!/usr/bin/env python3
"""Professional carousel with Eitan Adar AI branding."""

from PIL import Image, ImageDraw
from pathlib import Path

# Colors
BG_DARK = (10, 14, 39)
BG_ACCENT = (15, 25, 60)
CYAN = (0, 255, 255)
PINK = (255, 0, 110)
GREEN = (57, 255, 20)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

# Top 5 prompts
PROMPTS = [
    {
        "title": "Lead Qualification",
        "emoji": "🎯",
        "prompt": '"Analyze this lead: Are they serious? What\'s their budget? What\'s next?"',
        "benefit": "Save 5 hours/week qualifying leads"
    },
    {
        "title": "Proposal Generation",
        "emoji": "📄",
        "prompt": '"Create a professional proposal for [property details]"',
        "benefit": "Go from 2 hours to 2 minutes"
    },
    {
        "title": "Email Sequences",
        "emoji": "📧",
        "prompt": '"Write follow-up emails that get responses for [situation]"',
        "benefit": "Higher response rates, consistent follow-up"
    },
    {
        "title": "CRM Organization",
        "emoji": "📊",
        "prompt": '"Analyze my CRM data. Who\'s stale? Who\'s hot? What\'s closing?"',
        "benefit": "Stay organized, never miss a lead"
    },
    {
        "title": "Client Communication",
        "emoji": "💬",
        "prompt": '"Help me handle [objection/situation] professionally"',
        "benefit": "Keep deals alive with the right words"
    }
]

def draw_gradient_background(draw, width, height):
    """Draw a subtle gradient background."""
    # Dark navy to slightly lighter blue
    for y in range(height):
        ratio = y / height
        r = int(10 + (20 * ratio))
        g = int(14 + (30 * ratio))
        b = int(39 + (50 * ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def create_slide(num, data):
    """Create professional carousel slide."""
    img = Image.new('RGB', (1080, 1350), BG_DARK)
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    draw_gradient_background(draw, 1080, 1350)
    
    # Top accent bar (colored line)
    draw.rectangle([(0, 0), (1080, 6)], fill=CYAN)
    
    # "Eitan Adar AI" branding (top right)
    draw.text((1040, 40), "Eitan Adar AI", fill=PINK, font=None, anchor="rt")
    
    # Slide number (top left)
    draw.text((40, 40), f"{num}/5", fill=GRAY, font=None)
    
    # Large emoji
    draw.text((540, 200), data["emoji"], fill=WHITE, font=None, anchor="mm")
    
    # Title
    draw.text((540, 320), data["title"], fill=CYAN, font=None, anchor="mm")
    
    # Separator
    draw.line([(100, 380), (980, 380)], fill=PINK, width=3)
    
    # Main prompt (in quotes, highlighted)
    draw.rectangle([(80, 450), (1000, 650)], outline=GREEN, width=2)
    draw.rectangle([(85, 455), (995, 645)], fill=(20, 30, 50))
    draw.text((540, 550), data["prompt"], fill=GREEN, font=None, anchor="mm")
    
    # Benefit section
    draw.text((540, 750), "💡 Key Benefit:", fill=CYAN, font=None, anchor="mm")
    draw.text((540, 850), data["benefit"], fill=WHITE, font=None, anchor="mm")
    
    # Bottom CTA bar
    draw.rectangle([(0, 1200), (1080, 1350)], fill=(15, 25, 60))
    draw.text((540, 1250), "Save 10+ hours/week with AI prompts", fill=CYAN, font=None, anchor="mm")
    draw.text((540, 1320), "@eitanadar.ai • Real Estate Automation", fill=GRAY, font=None, anchor="mm")
    
    return img

def main():
    """Generate carousel."""
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-5-slides" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("🎨 Creating professional carousel with Eitan Adar AI branding...")
    
    for i, data in enumerate(PROMPTS, 1):
        img = create_slide(i, data)
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        print(f"  ✓ Slide {i}/5: {data['title']}")
    
    print("\n✅ Professional carousel created!")
    print(f"📁 {carousel_dir}")
    print("\nPost to Instagram:")
    print("  /post realtor-prompts-5-slides")

if __name__ == "__main__":
    main()
