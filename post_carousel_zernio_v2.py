#!/usr/bin/env python3
"""Post carousel to Instagram via Zernio API - v2 (improved)."""

import requests
import json
from pathlib import Path
import base64

# Configuration
ZERNIO_API_KEY = "sk_e408f417d0a321a0e6503486412dc0d5abac8fa6b592d6794825bdd48600bc55"
ZERNIO_API_URL = "https://api.zernio.com/v1"

# Carousel images directory
IMAGES_DIR = Path.home() / "Desktop" / "Woodworks-OS" / "projects" / "instagram-carousels" / "realtor-prompts-10-slides" / "images"

def get_carousel_images():
    """Get all carousel images sorted by slide number."""
    images = sorted(IMAGES_DIR.glob("slide-*.jpg"))
    return [str(img) for img in images]

def upload_images_to_zernio():
    """Upload carousel images to Zernio and get media IDs."""
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
    }
    
    image_paths = get_carousel_images()
    media_ids = []
    
    print("📤 Uploading carousel images to Zernio...")
    
    for i, image_path in enumerate(image_paths, 1):
        try:
            with open(image_path, 'rb') as img_file:
                files = {
                    'file': (f'slide-{i:02d}.jpg', img_file, 'image/jpeg')
                }
                
                response = requests.post(
                    f"{ZERNIO_API_URL}/media/upload",
                    headers=headers,
                    files=files,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    media_id = result.get('id') or result.get('media_id')
                    media_ids.append(media_id)
                    print(f"  ✓ Slide {i}/10 uploaded (ID: {media_id})")
                else:
                    print(f"  ⚠ Slide {i} upload failed: {response.status_code}")
                    # Continue with what we have
                    
        except Exception as e:
            print(f"  ❌ Error uploading slide {i}: {str(e)}")
    
    return media_ids

def post_carousel_v2(media_ids):
    """Post carousel using uploaded media IDs."""
    
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    caption = "15 powerful prompts every realtor should use for lead automation, CRM, proposals, and client communication. Save 10+ hours/week. 🤖 #RealEstate #Automation #RealEstateMarketing"
    
    # Try different payload formats for carousel
    payloads = [
        # Format 1: Direct carousel with media IDs
        {
            "type": "carousel",
            "media_ids": media_ids,
            "caption": caption,
            "platform": "instagram",
            "account": "eitanadar.ai"
        },
        # Format 2: Album format
        {
            "type": "album",
            "media": media_ids,
            "caption": caption,
            "platform": "instagram"
        },
        # Format 3: Simple post with carousel flag
        {
            "media_ids": media_ids,
            "caption": caption,
            "is_carousel": True,
            "platforms": ["instagram"]
        }
    ]
    
    for attempt, payload in enumerate(payloads, 1):
        print(f"\n📤 Attempt {attempt}: Posting carousel...")
        
        try:
            response = requests.post(
                f"{ZERNIO_API_URL}/posts",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"\n✅ SUCCESS! Carousel posted!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    return False

def post_via_dashboard_api():
    """Alternative: Post via Zernio dashboard API endpoint."""
    
    headers = {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    image_paths = get_carousel_images()
    
    # Read images and convert to base64
    image_data = []
    for path in image_paths:
        with open(path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            image_data.append({
                "data": f"data:image/jpeg;base64,{b64}",
                "type": "image"
            })
    
    payload = {
        "caption": "15 powerful prompts every realtor should use for lead automation, CRM, proposals, and client communication. Save 10+ hours/week. 🤖 #RealEstate #Automation #RealEstateMarketing",
        "media": image_data,
        "platform": "instagram",
        "type": "carousel"
    }
    
    print("\n📤 Attempting dashboard-style API post...")
    
    try:
        response = requests.post(
            f"{ZERNIO_API_URL}/carousel",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"\n✅ SUCCESS! Carousel posted via dashboard API!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return False

def main():
    print("🎨 Zernio Carousel Posting - v2")
    print("=" * 60)
    print(f"Images ready: {len(list(IMAGES_DIR.glob('slide-*.jpg')))}/10")
    print(f"API Key: {ZERNIO_API_KEY[:20]}...")
    print(f"Account: @eitanadar.ai")
    print("=" * 60)
    
    # Try method 1: Upload images first, then post
    print("\n🔄 Method 1: Upload images, then post...")
    media_ids = upload_images_to_zernio()
    
    if media_ids:
        print(f"\n✓ Uploaded {len(media_ids)} images")
        success = post_carousel_v2(media_ids)
        if success:
            return
    
    # Try method 2: Dashboard API with base64
    print("\n🔄 Method 2: Direct dashboard API with base64...")
    if post_via_dashboard_api():
        return
    
    print("\n⚠️ All API methods failed. Zernio API may require different authentication.")
    print("Please post manually through Zernio dashboard or try again in a few minutes.")

if __name__ == "__main__":
    main()
