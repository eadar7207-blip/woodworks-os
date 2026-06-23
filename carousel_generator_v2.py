#!/usr/bin/env python3
"""Generate Instagram carousels with readable design."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Colors
BG = (10, 14, 39)        # Dark navy
CYAN = (0, 255, 255)     # Neon cyan
PINK = (255, 0, 110)     # Neon pink
GREEN = (57, 255, 20)    # Neon green
WHITE = (255, 255, 255)  # White

# Carousel slides
SLIDES = [
    {"num": "1", "title": "Lead Qualification", "emoji": "🎯", "text": "Ask 3 questions instantly to qualify leads\n\n1) Serious buyer or browser?\n2) Likely budget range?\n3) Best next step?\n\nSave 5 hours/week"},
    {"num": "2", "title": "Proposal Generation", "emoji": "📄", "text": "Generate custom proposals\nin 2 minutes instead of 2 hours\n\nProfessional • Impressive • Personalized"},
    {"num": "3", "title": "Email Sequences", "emoji": "📧", "text": "5 templates that actually\nget responses\n\nNot generic. Not spammy.\nJust honest & helpful."},
    {"num": "4", "title": "CRM Organization", "emoji": "📊", "text": "Keep your lead data clean:\n\n• Which leads are stale?\n• Who needs follow-up?\n• What's close to closing?"},
    {"num": "5", "title": "Listing Descriptions", "emoji": "🏠", "text": "Write compelling descriptions\nthat SELL homes\n\nTell the story.\nNot just the features."},
    {"num": "6", "title": "Negotiation Scripts", "emoji": "💰", "text": "Master these scripts:\n\n• Handle low-ball offers\n• Manage emotional sellers\n• Close deals faster"},
    {"num": "7", "title": "Market Analysis", "emoji": "📈", "text": "Instant market reports\n(no 2-hour research)\n\nPrice trends • Buyer profiles\nEmerging opportunities"},
    {"num": "8", "title": "Social Media Content", "emoji": "📱", "text": "5 daily posts that build\nyour authority\n\nInsightful. Not salesy.\nConsistent."},
    {"num": "9", "title": "Client Communication", "emoji": "💬", "text": "Say the right thing\nat the right time:\n\n• Cold feet? Got the script.\n• Bad news? Here's how.\n• Closing? Celebrate right."},
    {"num": "10", "title": "Save These", "emoji": "⭐", "text": "@eitanadar.ai\n\nMore real estate automation\nstrategy & prompts in bio\n\n🚀 Follow for daily tips"},
]

def create_slide(num, title, emoji, text):
    """Create a carousel slide."""
    img = Image.new('RGB', (1080, 1350), BG)
    draw = ImageDraw.Draw(img)
    
    # Draw colored border
    for i in range(8):
        draw.rectangle([i, i, 1080-i, 1350-i], outline=CYAN)
    
    # Slide number (top left)
    draw.text((40, 40), f"SLIDE {num}/10", fill=PINK, font=None)
    
    # Emoji (large, top center)
    draw.text((540, 180), emoji, fill=WHITE, font=None, anchor="mm")
    
    # Title (large, bold)
    draw.text((540, 280), title, fill=CYAN, font=None, anchor="mm")
    
    # Separator line
    draw.line([(100, 350), (980, 350)], fill=CYAN, width=2)
    
    # Main text (centered)
    lines = text.split('\n')
    y = 500
    for line in lines:
        if line.strip():
            draw.text((540, y), line.strip(), fill=WHITE, font=None, anchor="mm")
        y += 80
    
    # Bottom CTA
    draw.text((540, 1250), "@eitanadar.ai", fill=GREEN, font=None, anchor="mm")
    
    return img

def main():
    """Generate all slides."""
    carousel_dir = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-10-slides" / "images"
    carousel_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old images
    for f in carousel_dir.glob("*.jpg"):
        f.unlink()
    
    print("🎨 Regenerating carousels with readable design...")
    
    for i, slide_data in enumerate(SLIDES, 1):
        img = create_slide(
            slide_data["num"],
            slide_data["title"],
            slide_data["emoji"],
            slide_data["text"]
        )
        
        path = carousel_dir / f"slide-{i:02d}.jpg"
        img.save(path, "JPEG", quality=95)
        print(f"  ✓ Slide {i}/10 created")
    
    print("\n✅ Carousel regenerated!")
    print(f"📁 {carousel_dir}")
    print("\nNow post to Instagram:")
    print("  /post realtor-prompts-10-slides")

if __name__ == "__main__":
    main()
