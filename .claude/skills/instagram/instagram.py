#!/usr/bin/env python3
"""Instagram carousel posting skill via Zernio API."""

import sys
import json
import requests
from pathlib import Path
from datetime import datetime

def validate_images(carousel_path):
    """Validate carousel images exist and are valid format."""
    path = Path(carousel_path).expanduser()
    
    if not path.exists():
        return None, f"Carousel path not found: {carousel_path}"
    
    images = sorted(list(path.glob("*.jpg")) + list(path.glob("*.png")))
    
    if not images:
        return None, f"No JPG/PNG images found in {carousel_path}"
    
    if len(images) > 10:
        return images[:10], f"Found {len(images)} images, using first 10"
    
    return images, None

def upload_carousel_zernio(image_paths, caption, api_key):
    """Upload carousel to Zernio API."""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare image paths for upload
    images_list = [str(img) for img in image_paths]
    
    # Payload for Zernio API
    payload = {
        "type": "carousel",
        "images": images_list,
        "caption": caption,
        "platform": "instagram"
    }
    
    try:
        response = requests.post(
            "https://api.zernio.com/v1/posts",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            return {
                "success": True,
                "post_id": result.get("id"),
                "status": result.get("status", "published"),
                "url": result.get("url"),
                "images_posted": len(image_paths)
            }
        else:
            return {
                "success": False,
                "error": f"API error {response.status_code}: {response.text[:200]}"
            }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Request timeout - API took too long"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

def main():
    if len(sys.argv) < 4:
        print(json.dumps({
            "error": "Usage: instagram.py <carousel_path> <caption> <api_key>"
        }))
        sys.exit(1)
    
    carousel_path = sys.argv[1]
    caption = sys.argv[2]
    api_key = sys.argv[3]
    
    # Validate images
    images, error = validate_images(carousel_path)
    if error:
        print(json.dumps({
            "error": error,
            "carousel_path": carousel_path
        }))
        sys.exit(1)
    
    # Upload carousel
    result = upload_carousel_zernio(images, caption, api_key)
    
    # Add metadata
    result["timestamp"] = datetime.now().isoformat()
    result["images_count"] = len(images)
    result["carousel_path"] = carousel_path
    
    print(json.dumps(result, indent=2))
    
    if result.get("success"):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
