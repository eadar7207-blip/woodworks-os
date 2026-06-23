import json
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path('instagram_carousel_output')
OUTPUT_DIR.mkdir(exist_ok=True)

WIDTH, HEIGHT = 1080, 1080
BACKGROUND = '#F7FAFC'
PRIMARY = '#0A74FF'
TEXT = '#111827'
SECOND = '#475569'
CARD = '#FFFFFF'

try:
    FONT_BOLD = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 72)
    FONT_REGULAR = ImageFont.truetype('/Library/Fonts/Arial.ttf', 42)
except OSError:
    FONT_BOLD = ImageFont.load_default()
    FONT_REGULAR = ImageFont.load_default()

slides = [
    {
        'filename': 'slide_01_hook.png',
        'title': 'Why agents lose leads before follow-up',
        'body': 'Most leads go cold when the first reply is delayed, generic, or lost in the system.',
        'note': 'Hook slide with branded headline and simple layout.'
    },
    {
        'filename': 'slide_02_slow_followup.png',
        'title': 'Slow follow-up kills interest',
        'body': 'Leads expect a response fast. Delayed replies let competitors step in.',
        'note': 'Show a clock or timing visual.'
    },
    {
        'filename': 'slide_03_generic_messages.png',
        'title': 'Generic replies feel robotic',
        'body': 'Personalization is the difference between a lead and a lost contact.',
        'note': 'Compare generic vs tailored messaging visually.'
    },
    {
        'filename': 'slide_04_no_tracking.png',
        'title': 'Leads disappear without tracking',
        'body': 'When follow-ups are untagged, nobody owns the lead and it falls through cracks.',
        'note': 'Show a CRM pipeline or lead list gone missing.'
    },
    {
        'filename': 'slide_05_one_channel.png',
        'title': 'One channel is not enough',
        'body': 'Relying on a single contact method means one missed message can lose the deal.',
        'note': 'Use phone + email + text icon cluster.'
    },
    {
        'filename': 'slide_06_quick_fixes.png',
        'title': 'Fix it with four simple habits',
        'body': 'Fast response, tailored follow-up, lead tagging, and multi-channel reach.',
        'note': 'Checklist style layout.'
    },
    {
        'filename': 'slide_07_proof.png',
        'title': 'Faster follow-up wins more deals',
        'body': 'Agents who improve response time see better lead conversion and stronger pipeline control.',
        'note': 'Stat card with percentage improvement.'
    },
    {
        'filename': 'slide_08_brand_awareness.png',
        'title': 'Build trust before the first meeting',
        'body': 'Consistent, confident lead handling makes you the obvious choice.',
        'note': 'Strong closing statement without CTA.'
    }
]

for slide in slides:
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)

    padding = 100
    draw.rectangle((padding, padding, WIDTH - padding, HEIGHT - padding), fill=CARD, outline=PRIMARY, width=8)

    header = 'Slide'
    draw.text((padding + 10, padding + 10), header, font=FONT_REGULAR, fill=PRIMARY)

    title_y = padding + 140
    draw.text((padding + 20, title_y), slide['title'], font=FONT_BOLD, fill=TEXT)

    body_y = title_y + 180
    wrapped_body = textwrap.fill(slide['body'], width=30)
    draw.multiline_text((padding + 20, body_y), wrapped_body, font=FONT_REGULAR, fill=SECOND, spacing=10)

    badge_text = 'No CTA included'
    badge_w, badge_h = draw.textbbox((0, 0), badge_text, font=FONT_REGULAR)[2:]
    badge_x = WIDTH - padding - (badge_w - 0)
    badge_y = HEIGHT - padding - badge_h - 20
    draw.rectangle((badge_x - 20, badge_y - 14, badge_x + badge_w + 20, badge_y + badge_h + 14), fill=CARD)
    draw.text((badge_x, badge_y), badge_text, font=FONT_REGULAR, fill=PRIMARY)

    filename = OUTPUT_DIR / slide['filename']
    img.save(filename)

caption = (
    'Agents are losing leads in plain sight. Swipe through the 8 common breakdowns and learn the quick fixes that keep more conversations alive.'
)
hashtags = [
    '#RealEstateAgents', '#LeadFollowUp', '#LeadLoss', '#AgentGrowth', '#CRM',
    '#SalesOps', '#MarketingForAgents', '#LeadManagement', '#RealEstateMarketing', '#AgentTips'
]

with (OUTPUT_DIR / 'carousel_slides.md').open('w', encoding='utf-8') as md:
    md.write('# Instagram Carousel: Agents Losing Leads\n\n')
    md.write('**Style:** clean, no CTA, blue accent (#0A74FF).\n\n')
    md.write('## Caption\n\n')
    md.write(caption + '\n\n')
    md.write('## Hashtags\n\n')
    md.write(' '.join(hashtags) + '\n\n')
    for i, slide in enumerate(slides, start=1):
        md.write(f'### Slide {i} — {slide["title"]}\n\n')
        md.write(f'{slide["body"]}\n\n')
        md.write(f'VisualNotes: {slide["note"]} Use blue accent #0A74FF, clean layout, white/gray background.\n\n')

manifest = {
    'slides': [
        {
            'slide': i,
            'image': slide['filename'],
            'title': slide['title'],
            'body': slide['body'],
            'visualNotes': slide['note']
        }
        for i, slide in enumerate(slides, start=1)
    ],
    'caption': caption,
    'hashtags': hashtags,
    'style': 'clean',
    'accent_color': '#0A74FF',
    'note': 'No CTA included',
}
with (OUTPUT_DIR / 'carousel_manifest.json').open('w', encoding='utf-8') as jf:
    json.dump(manifest, jf, indent=2)

print('Generated', len(slides), 'slides in', OUTPUT_DIR)
