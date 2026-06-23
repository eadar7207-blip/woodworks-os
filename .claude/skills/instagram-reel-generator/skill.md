---
name: instagram-reel-generator
description: Create Instagram reels from real estate property videos and photos. Add music, text overlays, transitions. Output ready-to-post vertical video.
usage: /instagram-reel-generator "{property_address}" "{video_file}" "{property_details}"
examples:
  - /instagram-reel-generator "123 Oak St, Chicago" "property.mp4" "3BR/2BA • $450K • Lincoln Park"
  - /instagram-reel-generator "456 Lake View Drive" "photos/" "Luxury waterfront • 4BR/3BA • Dock included"
---

# Instagram Reel Generator

Turn real estate property videos and photos into viral Instagram reels. Automatically adds music, text overlays, transitions, and formats for maximum engagement.

**What it does:**
- 🎥 **Takes your video** — Property walkthrough, neighborhood tour, or photo slideshow
- 🎵 **Adds trending music** — Royalty-free tracks matched to mood
- 📝 **Adds text overlays** — Property address, price, beds/baths, call-to-action
- ✨ **Adds effects** — Transitions, zooms, color grading
- 📱 **Optimizes for Instagram** — 9:16 aspect ratio, 15-60 seconds, captions
- 💾 **Outputs MP4** — Ready to post directly to Instagram

---

## How to Use

### Basic Usage
```
/instagram-reel-generator "{address}" "{video_file}" "{property_details}"
```

### Examples

**Example 1: Property Walkthrough**
```
/instagram-reel-generator "123 Oak St, Chicago" "walkthrough.mp4" "3BR/2BA • Renovated • $450K • Lincoln Park"
```

Output: 60-second reel with:
- Address overlay at start
- Property details fade-in
- Price highlight mid-video
- "Schedule Showing" CTA at end
- Trending background music
- 9:16 format ready for Instagram

**Example 2: Photo Slideshow**
```
/instagram-reel-generator "456 Lake View" "property-photos/" "Luxury waterfront • 4BR/3BA • Private dock"
```

Output: Photo slideshow converted to reel with:
- 2-3 second per photo
- Smooth zoom/pan transitions
- Text overlays for each room
- Music sync
- Total 45 seconds

**Example 3: Neighborhood Tour**
```
/instagram-reel-generator "Lincoln Park Area" "neighborhood.mp4" "Up-and-coming • Great schools • Transit access"
```

Output: Area showcase reel with location highlights

---

## Features

✅ **Smart music selection** — Picks trending tracks based on mood (upscale, cozy, modern, luxury)  
✅ **Auto text placement** — Overlays positioned for maximum readability  
✅ **Aspect ratio optimization** — Perfect 9:16 for Instagram  
✅ **Duration tuning** — Stretches/compresses to 15-60 seconds  
✅ **Color grading** — Enhances property visibility  
✅ **Captions** — Auto-generated from property details  
✅ **CTA overlays** — "Schedule Showing" / "DM for info" / "Learn More"  
✅ **Batch processing** — Generate 10 reels from 1 property  

---

## Input Formats

**Video inputs:**
- MP4, MOV, AVI
- Single file (will trim to 60s optimal)
- Or folder of photos (creates slideshow)

**Property details:**
```
"{Beds}BR/{Baths}BA • ${Price} • {Location}"
"{Feature1} • {Feature2} • {Feature3}"
"{Vibe}" (e.g., "Luxury", "Cozy", "Modern", "Family-friendly")
```

---

## Output

Files created in `output/`:
- `{address}_reel.mp4` — Main reel (ready to post)
- `{address}_reel_captions.srt` — Auto captions (for accessibility)
- `{address}_metadata.json` — Analytics tags

**Ready to post on Instagram Stories, Reels, or Feed.**

---

## Real Estate Use Cases

- **Listing showcase** — New property listing
- **Open house promo** — "This Sunday, 1-4 PM"
- **Neighborhood tour** — "Why Lincoln Park?" / "Why this area?"
- **Client testimonial** — "See what our clients love"
- **Before/after** — Renovation showcase
- **Market update** — "Homes selling in 3 days" / "Price trends"

---

## Customization

### Music Mood
```
/instagram-reel-generator "address" "video.mp4" "details" mood=luxury
```
Options: luxury, modern, cozy, energetic, peaceful, professional

### Duration
```
/instagram-reel-generator "address" "video.mp4" "details" duration=30
```
Range: 15-60 seconds (default: auto-optimized)

### Text Style
```
/instagram-reel-generator "address" "video.mp4" "details" style=bold
```
Options: bold, elegant, modern, playful

### CTA (Call to Action)
```
/instagram-reel-generator "address" "video.mp4" "details" cta="Schedule Tour"
```
Default options: "Schedule Showing", "DM for Info", "Learn More", "Call Now"

---

## Output Quality

- **Resolution:** 1080 × 1920 (Instagram standard)
- **Bitrate:** 8 Mbps (high quality, small file)
- **Codec:** H.264 (universal compatibility)
- **File size:** 20-50 MB per reel
- **Processing time:** 2-5 minutes per video

---

## Integration with Automation

Use in workflows:

```yaml
# .claude/automations/listing-to-reels.yml
steps:
  - skill: instagram-reel-generator
    input: 
      address: "{{ listing.address }}"
      video: "{{ listing.video_path }}"
      details: "{{ listing.beds }}BR/{{ listing.baths }}BA • ${{ listing.price }}"
    capture: reel_file
  
  - skill: instagram
    action: upload_reel
    video: "{{ reel_file }}"
    caption: "New listing! 🏡 Link in bio"
    
  - skill: send
    action: email_agent
    subject: "Your reel is ready to post"
    attachment: "{{ reel_file }}"
```

Then post directly or review first.

---

## Tips

- **Best video:** Bright, steady footage (use gimbal/tripod)
- **Audio:** Can be silent; skill adds music
- **Duration:** Aim for 30-90 seconds input (will compress to 60s)
- **Photos:** Min 5-10 for good slideshow
- **Text:** Keep property details short (fits on screen)

---

## Pricing Model

Sell to agents:
- **Setup:** $200-500 per property (generate first 5 reels)
- **Per reel:** $20-50 (recurring for new listings)
- **Monthly package:** $200-500 (unlimited reels that month)

Your cost: ~$2-5 per reel (music licenses, processing). 5-10x margin.

---

Built for Eitan Adar's real estate automation agency.
