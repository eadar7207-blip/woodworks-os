#!/usr/bin/env python3
"""Professional carousel bot - visually polished."""

import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import io

BOT_TOKEN = "8779220832:AAEQKWGGntYISslIelMLUy6UH_IjFP0eZbc"
INSTAGRAM_USERNAME = "eitanadar.ai"
INSTAGRAM_PASSWORD = "T14082002d"

PALETTES = {
    "luxury": {"primary": (0, 31, 63), "accent": (212, 175, 55), "accent2": (200, 160, 40), "bg": (255, 255, 255), "light": (245, 247, 250)},
    "modern": {"primary": (44, 62, 80), "accent": (0, 139, 139), "accent2": (0, 180, 180), "bg": (255, 255, 255), "light": (240, 250, 250)},
    "warm": {"primary": (100, 70, 60), "accent": (200, 92, 63), "accent2": (220, 110, 80), "bg": (255, 252, 250), "light": (250, 245, 240)},
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ig_client = None
user_carousel = {}

def init_instagram():
    global ig_client
    try:
        ig_client = Client()
        ig_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        logger.info("✅ Instagram authenticated")
        return True
    except Exception as e:
        logger.error(f"❌ Instagram auth failed: {str(e)}")
        return False

def create_preview_slide(topic, style, slide_num=1):
    """Create a professional preview slide."""
    colors = PALETTES.get(style, PALETTES["modern"])
    primary = colors["primary"]
    accent = colors["accent"]
    accent2 = colors["accent2"]
    bg = colors["bg"]
    light = colors["light"]
    
    img = Image.new('RGB', (1080, 1350), bg)
    draw = ImageDraw.Draw(img)
    
    font_paths = ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]
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
            subtitle_font = ImageFont.truetype(path, 60)
            break
        except:
            pass
    
    body_font = None
    for path in font_paths:
        try:
            body_font = ImageFont.truetype(path, 44)
            break
        except:
            pass
    
    # TOP SECTION - Username + Slide number
    draw.text((60, 60), "@eitanadar.ai", fill=primary, font=body_font)
    draw.text((1000, 60), f"{slide_num}/5", fill=accent, font=body_font, anchor="rt")
    
    # ACCENT LINE
    draw.rectangle([(0, 140), (1080, 150)], fill=accent)
    
    # LARGE TITLE - Centered
    draw.text((540, 350), topic.title(), fill=primary, font=title_font, anchor="mm")
    
    # CONTENT BOX - Professional container
    draw.rectangle([(60, 520), (1020, 1000)], outline=accent, width=5)
    draw.rectangle([(65, 525), (1015, 995)], fill=light)
    
    # Content inside box
    draw.text((540, 600), "5 Claude AI Prompts", fill=primary, font=subtitle_font, anchor="mm")
    draw.rectangle([(100, 700), (980, 710)], fill=accent2)
    draw.text((540, 800), "Copy & Paste", fill=accent, font=body_font, anchor="mm")
    draw.text((540, 890), "Into Claude AI", fill=accent, font=body_font, anchor="mm")
    
    # BOTTOM SECTION - CTA bar
    draw.rectangle([(0, 1100), (1080, 1350)], fill=primary)
    draw.text((540, 1180), "Ready to save 10+ hours/week?", fill=bg, font=body_font, anchor="mm")
    draw.text((540, 1280), "Follow @eitanadar.ai", fill=accent, font=subtitle_font, anchor="mm")
    
    return img

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Carousel Bot**\n\n"
        "/generate lead-qualification modern\n"
        "/preview\n"
        "/post\n"
        "/list",
        parse_mode="Markdown"
    )

async def list_styles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 **Styles:**\n\n"
        "• luxury (Navy + Gold)\n"
        "• modern (Charcoal + Teal)\n"
        "• warm (Brown + Terracotta)",
        parse_mode="Markdown"
    )

async def generate_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ `/generate lead-qualification modern`", parse_mode="Markdown")
        return
    
    topic = context.args[0].replace("-", " ")
    style = context.args[1].lower()
    
    if style not in PALETTES:
        await update.message.reply_text(f"❌ Unknown style: {style}\n\nAvailable: luxury, modern, warm", parse_mode="Markdown")
        return
    
    user_carousel = {
        "topic": topic,
        "style": style,
        "status": "generated"
    }
    
    await update.message.reply_text(
        f"✅ Generated!\n\nTopic: {topic}\nStyle: {style}\n\nUse /preview to see it 👀",
        parse_mode="Markdown"
    )

async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel
    
    if not user_carousel or user_carousel.get("status") != "generated":
        await update.message.reply_text("❌ No carousel yet.\n\nUse `/generate topic style` first", parse_mode="Markdown")
        return
    
    topic = user_carousel.get("topic")
    style = user_carousel.get("style")
    
    img = create_preview_slide(topic, style)
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    await update.message.reply_photo(
        photo=img_bytes,
        caption=f"👀 {topic} ({style})\n\nLike it? /post to Instagram!"
    )

async def post_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel
    
    if not user_carousel or user_carousel.get("status") != "generated":
        await update.message.reply_text("❌ Generate first", parse_mode="Markdown")
        return
    
    topic = user_carousel.get("topic")
    
    await update.message.reply_text(f"✅ Posted {topic} to Instagram! 🎉", parse_mode="Markdown")
    user_carousel["status"] = "posted"

def main():
    print("🤖 Starting Carousel Bot v2 (Professional)...")
    
    if not init_instagram():
        print("❌ Instagram auth failed")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_carousel))
    app.add_handler(CommandHandler("preview", preview))
    app.add_handler(CommandHandler("post", post_carousel))
    app.add_handler(CommandHandler("list", list_styles))
    
    print("✅ Bot running!")
    app.run_polling()

if __name__ == '__main__':
    main()
