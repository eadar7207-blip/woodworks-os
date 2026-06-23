---
title: Instagram Carousel Automation System
type: concept
tags: [content, automation, instagram, @eitanadar.ai, telegram]
created: 2026-06-09
updated: 2026-06-09
sources: 0
---

# Instagram Carousel Automation System

Telegram bot that generates, previews, and posts professional neon-styled Instagram carousels to @eitanadar.ai. One-command content creation for real estate automation prompts.

## What It Does

**Command format:** `/generate topic style` → `/preview` → `/post`

1. **Generate**: Creates 5-slide carousel based on topic (lead-qualification, proposal-generation, email-sequences, crm-organization, market-analysis, client-communication, negotiation-scripts)
2. **Preview**: Shows all 5 slides + auto-generated Instagram caption
3. **Post**: Actually uploads carousel to @eitanadar.ai with caption

## Design System

**Neon Styles (3 options):**
- **Luxury**: Cyan (#00FFFF) + Hot Pink (#FF006E)
- **Modern**: Neon Green (#39FF14) + Cyan
- **Warm**: Neon Orange (#FFA500) + Magenta (#FF1493)

**All styles use:**
- Dark navy background (#0a0e27) with gradient
- Text directly on gradient (no white boxes)
- Double neon borders on content areas
- Bold neon accent lines separating sections
- Readable typography hierarchy

**Slide Structure:**
1. Title slide (emoji + topic + CTA)
2-4. Content slides (1 Claude prompt each, neon border frame)
5. CTA slide (save prompt + brand)

## Caption Generation

Each topic auto-generates a compelling Instagram caption with:
- Hook (5-7 words, stops scroll)
- Body (benefit statement)
- 3 specific benefits (✓ bullets)
- Clear CTA
- Relevant hashtags (#RealEstate, #RealEstateAutomation, #AIForRealtors, etc.)

**Caption templates:** One unique caption per topic (lead-qualification, proposal-generation, email-sequences, crm-organization, market-analysis, client-communication, negotiation-scripts)

## Content Source

**25 Topics** with 5 real, actionable Claude AI prompts each:

**Core Workflows (7):**
- Lead Qualification: Instantly qualify leads (30 sec screening)
- Proposal Generation: Professional proposals in 2 minutes
- Email Sequences: Follow-ups that get responses
- CRM Organization: Keep pipeline clean & organized
- Market Analysis: Market insights without 2-hour research
- Client Communication: Handle objections professionally
- Negotiation Scripts: Win negotiations on tough deals

**Property Marketing (3):**
- Listing Descriptions: Compelling, scannable property descriptions
- Open House Scripts: Scripts for showing properties & qualifying buyers
- Luxury Home Marketing: High-net-worth buyer positioning & strategies

**Sales & Conversion (5):**
- Objection Handling: Scripts for common buyer/seller concerns
- Buyer Personas: Segment & target the right buyers
- Pricing Strategy: Data-driven pricing recommendations
- Closing Checklist: Step-by-step closing process & timeline
- Referral Generation: Post-closing referral requests & incentives

**Content & Branding (3):**
- Social Media Content: Instagram, LinkedIn, TikTok, Facebook posts
- Video Scripts: Property tours, market updates, agent intros
- Team Training: Training guides, role-plays, coaching scripts

**Specialized Topics (7):**
- Lead Nurture Campaigns: 12-week nurture email sequences
- Inspection Handling: Negotiating repairs & inspection issues
- Investor Outreach: Off-market deals & investment analysis
- Home Staging Advice: Staging recommendations & curb appeal tips
- First-Time Buyer Guide: Education guides & step-by-step process
- Relocation Services: Corporate relocation packages & area guides
- (Custom/future topics expandable)

Each topic designed to save realtors 10+ hours/week.

## Technical Stack

- **Bot**: Python Telegram bot (python-telegram-bot library)
- **Image generation**: PIL/Pillow (1080x1350px Instagram carousel format)
- **Instagram posting**: Instagrapi (unofficial Instagram API, no Meta app review needed)
- **Storage**: Temporary files for carousel images (cleaned up after posting)
- **Authentication**: Instagram credentials (eitanadar.ai account)

## Workflow

**Manual selection:**
```
User in Telegram
  ↓
/generate lead-qualification luxury
  ↓ (bot generates 5 slides + caption)
/preview
  ↓ (shows carousel images + caption)
/post
  ↓ (uploads to Instagram, shows confirmation)
Carousel appears on @eitanadar.ai feed
```

**Auto-random (fastest):**
```
User in Telegram
  ↓
/random
  ↓ (picks random topic + random style from 25 topics × 3 styles)
/preview
  ↓ (shows carousel images + caption)
/post
  ↓ (uploads to Instagram)
Carousel appears on @eitanadar.ai feed
```

**Repeat `/random` 25 times → Full content library across all topics**

## Why This Works

1. **No manual design work** — Bot handles all visual/layout decisions
2. **Consistent branding** — Neon color system + accent lines create signature look
3. **Smart captions** — Topic-specific, proven structure (hook → benefit → CTA → hashtags)
4. **One command to post** — From generation to Instagram in 3 commands
5. **Content is real value** — Each prompt is genuinely useful to realtors (saves 10+ hours/week)

## Research Foundation

Design patterns extracted from [[Real Estate Carousel Design Blueprint]] — analyzed top creators (Bryan Casella, Joyce Rey, Ryan Serhant), identified professional signals (60/40 whitespace rule, typography hierarchy, visual contrast, neon color psychology for 2026 trends).

## Future Enhancements

- Custom captions (override auto-generated)
- Schedule posts (post at optimal times)
- Batch generation (create multiple carousels at once)
- Analytics tracking (clicks, saves, shares per carousel)
- A/B testing (test different color schemes/captions)
- User-submitted prompts (community-generated content)
