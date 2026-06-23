#!/usr/bin/env python3
"""Real carousel bot that ACTUALLY posts to Instagram."""

import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import tempfile
import os
import random

from carousel_content import CAROUSEL_CONTENT

BOT_TOKEN = "8779220832:AAEQKWGGntYISslIelMLUy6UH_IjFP0eZbc"
INSTAGRAM_USERNAME = "eitanadar.ai"
INSTAGRAM_PASSWORD = "T14082002d"

# Caption templates per topic
CAPTIONS = {
    "lead-qualification": {
        "hook": "5 prompts that save realtors 10+ hours/week 🤖",
        "body": "Stop wasting time on tire-kickers.\n\nThese Claude AI prompts instantly qualify leads so you focus on the hot prospects.\n\nJust copy & paste. Takes 2 minutes.",
        "benefit": "✓ Qualify leads in 30 seconds\n✓ Identify serious buyers\n✓ Never waste time again",
        "cta": "Done chasing the wrong leads? Swipe for the prompts →"
    },
    "proposal-generation": {
        "hook": "Write professional proposals in 2 minutes (not 2 hours) 📄",
        "body": "Your proposals are costing you time.\n\nThese 5 Claude prompts generate polished, personalized proposals that actually close deals.\n\nNo more generic templates.",
        "benefit": "✓ Professional proposals instantly\n✓ Impress buyers every time\n✓ Close deals faster",
        "cta": "Ready to stop the proposal grind? Swipe →"
    },
    "email-sequences": {
        "hook": "Email sequences that actually get responses 📧",
        "body": "Most real estate emails get ignored.\n\nThese 5 Claude prompts write follow-ups that feel personal, not salesy—and they actually move prospects forward.\n\nHigh response rates. Every time.",
        "benefit": "✓ Personal, not generic\n✓ Higher reply rates\n✓ Nurture on autopilot",
        "cta": "Want emails that actually work? Swipe →"
    },
    "crm-organization": {
        "hook": "Keep your CRM clean and never miss a follow-up 📊",
        "body": "Your CRM is a mess. I know because mine was too.\n\nThese 5 Claude prompts organize your leads, flag stale prospects, and tell you exactly who needs follow-up today.\n\nNo more lost opportunities.",
        "benefit": "✓ Clean CRM instantly\n✓ Never miss a hot lead\n✓ Know what to do next",
        "cta": "Ready to get organized? Swipe →"
    },
    "market-analysis": {
        "hook": "Market insights without the 2-hour research session 📈",
        "body": "Your clients want to know: Is this a good time to buy/sell?\n\nThese 5 Claude prompts analyze your market in minutes—with real data, trends, and talking points.\n\nPosition yourself as the expert.",
        "benefit": "✓ Instant market reports\n✓ Sound like an authority\n✓ Build buyer confidence",
        "cta": "Want market intelligence on demand? Swipe →"
    },
    "client-communication": {
        "hook": "Say the right thing at the right time 💬",
        "body": "Words matter in real estate.\n\nThese 5 Claude prompts help you handle objections, deliver bad news professionally, and keep deals from falling apart.\n\nAlways know what to say.",
        "benefit": "✓ Handle objections smoothly\n✓ Keep deals alive\n✓ Stay professional always",
        "cta": "Need the right words? Swipe →"
    },
    "negotiation-scripts": {
        "hook": "Negotiate like a pro (even on tough deals) 💰",
        "body": "Negotiations are where deals are won or lost.\n\nThese 5 Claude prompts give you scripts and strategies for handling lowballs, emotional sellers, and repair negotiations.\n\nClose more deals at better prices.",
        "benefit": "✓ Handle lowball offers\n✓ Manage seller emotions\n✓ Win negotiations",
        "cta": "Ready to negotiate better? Swipe →"
    }
}

# NEON color palettes
PALETTES = {
    "luxury": {
        "primary": (10, 14, 39),
        "accent": (0, 255, 255),
        "accent2": (255, 0, 110),
        "bg_top": (10, 14, 39),
        "bg_bottom": (15, 25, 60),
        "text": (255, 255, 255)
    },
    "modern": {
        "primary": (10, 14, 39),
        "accent": (57, 255, 20),
        "accent2": (0, 255, 255),
        "bg_top": (10, 14, 39),
        "bg_bottom": (15, 25, 60),
        "text": (255, 255, 255)
    },
    "warm": {
        "primary": (10, 14, 39),
        "accent": (255, 165, 0),
        "accent2": (255, 20, 147),
        "bg_top": (10, 14, 39),
        "bg_bottom": (15, 25, 60),
        "text": (255, 255, 255)
    },
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
        logger.error(f"❌ Instagram auth failed: {e}")
        return False

def draw_gradient(draw, width, height, color1, color2):
    """Draw gradient background."""
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def generate_caption(topic):
    """Generate Instagram caption for topic."""
    if topic not in CAPTIONS:
        return "Check out these AI prompts for realtors! #RealEstate #Automation"
    
    cap = CAPTIONS[topic]
    hashtags = "\n\n#RealEstate #RealEstateAutomation #AIForRealtors #RealtorTips #PropTech #RealEstateTech #Automation"
    
    caption = f"{cap['hook']}\n\n{cap['body']}\n\n{cap['benefit']}\n\n{cap['cta']}{hashtags}"
    return caption

def create_carousel_slide(slide_num, total_slides, content, style, is_title=False, is_cta=False):
    """Create cool NEON carousel slide."""
    colors = PALETTES.get(style, PALETTES["modern"])
    
    img = Image.new('RGB', (1080, 1350), colors["primary"])
    draw = ImageDraw.Draw(img)
    
    draw_gradient(draw, 1080, 1350, colors["bg_top"], colors["bg_bottom"])
    
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
            subtitle_font = ImageFont.truetype(path, 56)
            break
        except:
            pass
    
    body_font = None
    for path in font_paths:
        try:
            body_font = ImageFont.truetype(path, 42)
            break
        except:
            pass
    
    small_font = None
    for path in font_paths:
        try:
            small_font = ImageFont.truetype(path, 32)
            break
        except:
            pass
    
    if is_title:
        draw.rectangle([(0, 0), (1080, 150)], fill=colors["primary"])
        draw.rectangle([(0, 80), (1080, 95)], fill=colors["accent"])
        draw.rectangle([(0, 100), (1080, 115)], fill=colors["accent2"])
        
        draw.text((540, 40), "@eitanadar.ai", fill=colors["accent"], font=subtitle_font, anchor="mm")
        
        draw.text((540, 300), content["emoji"], fill=colors["accent"], font=None, anchor="mm")
        
        draw.text((540, 500), content["title"], fill=colors["accent"], font=title_font, anchor="mm")
        
        draw.rectangle([(100, 660), (980, 675)], fill=colors["accent"])
        draw.rectangle([(120, 690), (960, 705)], fill=colors["accent2"])
        
        draw.text((540, 850), "5 AI Prompts", fill=colors["accent2"], font=subtitle_font, anchor="mm")
        draw.text((540, 950), "That Actually Work", fill=colors["accent"], font=body_font, anchor="mm")
        
        draw.rectangle([(0, 1250), (1080, 1270)], fill=colors["accent"])
        draw.rectangle([(0, 1270), (1080, 1290)], fill=colors["accent2"])
        draw.text((540, 1320), "→ Swipe to see them", fill=colors["accent"], font=small_font, anchor="mm")
        
    elif is_cta:
        draw.text((540, 250), "💾", fill=colors["accent"], font=None, anchor="mm")
        
        draw.text((540, 400), "Save & Use", fill=colors["accent"], font=title_font, anchor="mm")
        draw.text((540, 550), "These Prompts", fill=colors["accent2"], font=title_font, anchor="mm")
        
        draw.rectangle([(100, 680), (980, 695)], fill=colors["accent"])
        draw.rectangle([(100, 710), (980, 725)], fill=colors["accent2"])
        
        cta_text = content["cta"]
        wrapped = textwrap.fill(cta_text, width=35)
        lines = wrapped.split('\n')
        
        y = 800
        for line in lines:
            draw.text((540, y), line, fill=colors["text"], font=body_font, anchor="mm")
            y += 70
        
        draw.rectangle([(0, 1200), (1080, 1220)], fill=colors["accent"])
        draw.rectangle([(0, 1220), (1080, 1240)], fill=colors["accent2"])
        
        draw.text((540, 1300), "@eitanadar.ai", fill=colors["accent"], font=subtitle_font, anchor="mm")
        
    else:
        draw.rectangle([(0, 0), (1080, 150)], fill=colors["primary"])
        draw.rectangle([(0, 80), (1080, 95)], fill=colors["accent"])
        draw.rectangle([(0, 100), (1080, 115)], fill=colors["accent2"])
        
        draw.text((60, 40), f"Slide {slide_num}", fill=colors["accent"], font=small_font)
        draw.text((1000, 40), f"{slide_num}/5", fill=colors["accent2"], font=small_font, anchor="rt")
        
        draw.rectangle([(50, 200), (1030, 1100)], outline=colors["accent"], width=5)
        draw.rectangle([(60, 210), (1020, 1090)], outline=colors["accent2"], width=2)
        
        prompt_text = content
        wrapped = textwrap.fill(prompt_text, width=50)
        lines = wrapped.split('\n')
        
        y = 350
        for line in lines:
            draw.text((540, y), line, fill=colors["accent"], font=body_font, anchor="mm")
            y += 80
        
        draw.rectangle([(0, 1100), (1080, 1350)], fill=colors["primary"])
        draw.rectangle([(0, 1100), (1080, 1120)], fill=colors["accent"])
        draw.rectangle([(0, 1120), (1080, 1140)], fill=colors["accent2"])
        
        draw.text((540, 1250), "Copy this prompt into Claude", fill=colors["accent"], font=small_font, anchor="mm")
    
    return img

def create_full_carousel(topic, style):
    """Create all 5 slides for a carousel."""
    if topic not in CAROUSEL_CONTENT:
        return None
    
    content = CAROUSEL_CONTENT[topic]
    slides = []
    
    slides.append(create_carousel_slide(1, 5, content, style, is_title=True))
    
    for i, prompt in enumerate(content["prompts"][:3], start=2):
        slides.append(create_carousel_slide(i, 5, prompt, style))
    
    slides.append(create_carousel_slide(5, 5, content, style, is_cta=True))
    
    return slides

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 **NEON Bot**\n\n/generate topic style\n/preview\n/post", parse_mode="Markdown")

async def list_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topics = "\n".join([f"• {t.replace('-', ' ').title()}" for t in CAROUSEL_CONTENT.keys()])
    styles = "luxury  |  modern  |  warm"
    await update.message.reply_text(f"📋 **Topics:**\n\n{topics}\n\n**Styles:**\n{styles}", parse_mode="Markdown")

async def generate_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel
    
    if len(context.args) < 2:
        await update.message.reply_text("❌ `/generate topic style`", parse_mode="Markdown")
        return
    
    topic = context.args[0]
    style = context.args[1].lower()
    
    if topic not in CAROUSEL_CONTENT or style not in PALETTES:
        await update.message.reply_text("❌ Unknown topic or style", parse_mode="Markdown")
        return
    
    slides = create_full_carousel(topic, style)
    if not slides:
        await update.message.reply_text("❌ Error", parse_mode="Markdown")
        return
    
    caption = generate_caption(topic)
    
    user_carousel = {"topic": topic, "style": style, "slides": slides, "caption": caption, "status": "generated"}
    await update.message.reply_text(f"✅ Generated!\n\nUse /preview 👀", parse_mode="Markdown")

async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel
    
    if not user_carousel or user_carousel.get("status") != "generated":
        await update.message.reply_text("❌ Generate first", parse_mode="Markdown")
        return
    
    slides = user_carousel.get("slides", [])
    caption = user_carousel.get("caption", "")
    
    await update.message.reply_text("📸 **Carousel Preview:**", parse_mode="Markdown")
    
    for i, slide in enumerate(slides, 1):
        img_bytes = io.BytesIO()
        slide.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        await update.message.reply_photo(photo=img_bytes)
    
    await update.message.reply_text(f"\n📝 **Caption:**\n\n{caption}", parse_mode="Markdown")

async def post_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_carousel, ig_client
    
    if not user_carousel or user_carousel.get("status") != "generated":
        await update.message.reply_text("❌ Generate first", parse_mode="Markdown")
        return
    
    if not ig_client:
        await update.message.reply_text("❌ Instagram not connected", parse_mode="Markdown")
        return
    
    slides = user_carousel.get("slides", [])
    caption = user_carousel.get("caption", "")
    topic = user_carousel.get("topic", "carousel")
    
    await update.message.reply_text("📤 Posting to Instagram...", parse_mode="Markdown")
    
    try:
        # Save slides to temp files
        temp_dir = tempfile.mkdtemp()
        image_paths = []
        
        for i, slide in enumerate(slides):
            path = os.path.join(temp_dir, f"slide_{i}.jpg")
            slide.save(path, "JPEG", quality=95)
            image_paths.append(path)
        
        # Post carousel to Instagram
        ig_client.album_upload(image_paths, caption=caption)
        
        # Clean up temp files
        for path in image_paths:
            os.remove(path)
        os.rmdir(temp_dir)
        
        await update.message.reply_text(f"✅ **Posted to @eitanadar.ai!** 🎉\n\n📝 Caption:\n\n{caption}", parse_mode="Markdown")
        user_carousel["status"] = "posted"
        logger.info(f"✅ Posted {topic} carousel to Instagram")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error posting: {str(e)}", parse_mode="Markdown")
        logger.error(f"Error posting carousel: {e}")

async def random_carousel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate random real estate AI carousel."""
    global user_carousel

    # Pick random topic and style
    topic = random.choice(list(CAROUSEL_CONTENT.keys()))
    style = random.choice(["luxury", "modern", "warm"])

    slides = create_full_carousel(topic, style)
    if not slides:
        await update.message.reply_text("❌ Error", parse_mode="Markdown")
        return

    caption = generate_caption(topic)

    user_carousel = {"topic": topic, "style": style, "slides": slides, "caption": caption, "status": "generated"}
    await update.message.reply_text(
        f"🎲 **Random Real Estate AI Carousel Generated!**\n\n"
        f"Topic: {topic.replace('-', ' ').title()}\n"
        f"Style: {style.title()}\n\n"
        f"Use /preview to see it 👀",
        parse_mode="Markdown"
    )

def main():
    print("🤖 NEON Bot (Real Instagram Posting)...")
    
    if not init_instagram():
        print("⚠️ Instagram auth failed - preview only")
    else:
        print("✅ Instagram connected")
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_carousel))
    app.add_handler(CommandHandler("random", random_carousel))
    app.add_handler(CommandHandler("preview", preview))
    app.add_handler(CommandHandler("post", post_carousel))
    app.add_handler(CommandHandler("topics", list_topics))
    
    print("✅ Bot running!")
    app.run_polling()

if __name__ == '__main__':
    main()
