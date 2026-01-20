#!/usr/bin/env python3
"""
Image downloader for Space Invaders Political Edition
Downloads political figure images from Wikimedia Commons
"""

import urllib.request
import os
import sys

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Image URLs from Wikimedia Commons and other public domain sources
images = {
    "zohran_mamdani.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Zohran_Mamdani_2025.jpg/800px-Zohran_Mamdani_2025.jpg",
    "andrew_cuomo.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Andrew_Cuomo_by_Pat_Arnow.jpeg/800px-Andrew_Cuomo_by_Pat_Arnow.jpeg",
    "donald_trump.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/800px-Donald_Trump_official_portrait.jpg",
    "jd_vance.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/JD_Vance_official_VP_portrait.jpg/800px-JD_Vance_official_VP_portrait.jpg"
}

def download_image(filename, url):
    """Download an image from a URL"""
    filepath = os.path.join("images", filename)

    if os.path.exists(filepath):
        print(f"✓ {filename} already exists, skipping...")
        return True

    try:
        print(f"Downloading {filename}...", end=" ")
        urllib.request.urlretrieve(url, filepath)
        print("✓ Success!")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Space Invaders Political Edition - Image Downloader")
    print("=" * 60)
    print()

    success_count = 0
    total_count = len(images)

    for filename, url in images.items():
        if download_image(filename, url):
            success_count += 1

    print()
    print("=" * 60)
    print(f"Downloaded {success_count}/{total_count} images successfully")

    if success_count == total_count:
        print("All images downloaded! You can now run the game:")
        print("  python space_invaders.py")
    else:
        print("\nSome images failed to download. The game will use fallback")
        print("graphics for missing images.")
        print("\nYou can manually download images and place them in images/:")
        for filename in images.keys():
            filepath = os.path.join("images", filename)
            if not os.path.exists(filepath):
                print(f"  - {filename}")

    print("=" * 60)

if __name__ == "__main__":
    main()
