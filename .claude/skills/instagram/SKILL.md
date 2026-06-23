# /instagram — Post Carousels to Instagram

Post carousel images to your Instagram Business Account using the Zernio API.

## Use when

- You want to post a carousel to Instagram
- You have carousel images ready (JPG/PNG)
- You want to automate Instagram posting in workflows

## Syntax

```
/instagram post [carousel_path] [caption] [api_key]
```

## Parameters

- **carousel_path**: Path to folder with images (slide-01.jpg, slide-02.jpg, etc.)
- **caption**: Post caption/description (max 2200 chars)
- **api_key**: Your Zernio API key (from zernio.com dashboard)

## Example

```
/instagram post ~/Desktop/Woodworks-OS/projects/instagram-carousels/realtor-prompts-10-slides/images/ "15 powerful prompts realtors should use. Save 10+ hours/week. #RealEstate" sk_e408f417d0a321a0e6503486412dc0d5abac8fa6b592d6794825bdd48600bc55
```

## What it does

1. Validates carousel images (JPG/PNG only)
2. Uploads images to Zernio
3. Creates carousel post with your caption
4. Posts to your connected Instagram account
5. Returns post URL and status

## Setup

1. Create a Zernio account (free tier: 2 accounts, unlimited posts)
2. Connect your Instagram Business Account
3. Copy your API key from zernio.com/dashboard
4. Store API key securely (or pass to skill each time)

## Output

Returns:
- ✅ Post ID (if successful)
- ✅ Post URL
- ✅ Status (published/pending)
- Or ❌ Error message

## Notes

- Images must be 1080×1350px (Instagram carousel standard)
- Max 10 images per carousel
- Caption limited to 2200 characters
- Requires Zernio account with connected Instagram

## Troubleshooting

**"No images found"** → Check carousel_path directory has JPG/PNG files

**"Upload failed"** → Verify images are JPG/PNG format and under 8MB each

**"API error"** → Check API key is valid and not expired
