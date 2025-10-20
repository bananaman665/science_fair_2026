#!/usr/bin/env python3
"""
Manual Image Labeling Tool
Helps manually classify apple photos into oxidation categories for ML training
"""

import os
import shutil
from pathlib import Path
from PIL import Image
import json

# Paths
SOURCE_DIR = Path("data_repository/01_raw_images/first_collection_oct2025")
OUTPUT_DIR = Path("data_repository/02_processed_images/labeled_training_set")

# Oxidation categories
CATEGORIES = {
    '1': 'fresh',
    '2': 'light_oxidation',
    '3': 'medium_oxidation',
    '4': 'heavy_oxidation',
    's': 'skip'  # Skip this image
}

def get_all_photos():
    """Get all photos from organized collection"""
    photos = []
    
    for apple_type in ['gala', 'granny_smith']:
        apple_dir = SOURCE_DIR / apple_type
        if apple_dir.exists():
            for photo in apple_dir.rglob("*.JPG"):
                photos.append(photo)
    
    # Sort by filename for consistent ordering
    photos.sort()
    return photos

def display_photo_info(photo_path):
    """Display information about the photo"""
    # Parse filename to extract metadata
    filename = photo_path.name
    parts = filename.replace('.JPG', '').split('_')
    
    print("\n" + "=" * 70)
    print(f"📸 Photo: {filename}")
    print("=" * 70)
    
    if len(parts) >= 4:
        apple_type = parts[0]
        fruit_num = parts[1]
        day_num = parts[2]
        hours = parts[3]
        
        print(f"  🍎 Apple Type: {apple_type}")
        print(f"  🔢 Fruit: {fruit_num}")
        print(f"  📅 {day_num} ({hours} since baseline)")
        print(f"  📁 Path: {photo_path.relative_to(SOURCE_DIR)}")
    
    # Try to display image size
    try:
        with Image.open(photo_path) as img:
            print(f"  📏 Size: {img.width}x{img.height}")
    except Exception as e:
        print(f"  ⚠️  Could not read image: {e}")

def label_photos():
    """Interactive photo labeling"""
    photos = get_all_photos()
    print(f"\n🍎 Apple Photo Labeling Tool")
    print(f"Found {len(photos)} photos to label\n")
    
    # Load existing labels if available
    labels_file = OUTPUT_DIR / "labels.json"
    if labels_file.exists():
        with open(labels_file, 'r') as f:
            labels = json.load(f)
        print(f"📂 Loaded {len(labels)} existing labels")
    else:
        labels = {}
    
    print("\n" + "=" * 70)
    print("LABELING INSTRUCTIONS")
    print("=" * 70)
    print("Look at each photo and classify the oxidation level:")
    print("  1 = Fresh (no browning)")
    print("  2 = Light oxidation (slight browning at edges)")
    print("  3 = Medium oxidation (noticeable browning across surface)")
    print("  4 = Heavy oxidation (significant brown color)")
    print("  s = Skip this photo")
    print("  q = Quit and save")
    print("  b = Go back to previous photo")
    print("=" * 70)
    
    current_idx = 0
    
    while current_idx < len(photos):
        photo = photos[current_idx]
        photo_key = str(photo.relative_to(SOURCE_DIR))
        
        # Check if already labeled
        if photo_key in labels:
            print(f"\n✅ Already labeled as: {labels[photo_key]}")
        
        display_photo_info(photo)
        
        print(f"\n📍 Progress: {current_idx + 1}/{len(photos)}")
        print(f"\n💡 TIP: Open the photo in Preview/Finder to see it")
        print(f"   File: {photo}")
        
        # Get user input
        choice = input("\n➡️  Label (1/2/3/4/s/q/b): ").strip().lower()
        
        if choice == 'q':
            print("\n💾 Saving and quitting...")
            break
        elif choice == 'b':
            if current_idx > 0:
                current_idx -= 1
                print("⬅️  Going back...")
            else:
                print("❌ Already at first photo")
            continue
        elif choice in CATEGORIES:
            category = CATEGORIES[choice]
            labels[photo_key] = category
            print(f"✅ Labeled as: {category}")
            current_idx += 1
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, s, q, or b")
    
    # Save labels
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(labels_file, 'w') as f:
        json.dump(labels, f, indent=2)
    
    print(f"\n💾 Saved {len(labels)} labels to {labels_file}")
    
    # Print summary
    print("\n📊 Labeling Summary:")
    print("=" * 50)
    category_counts = {}
    for label in labels.values():
        category_counts[label] = category_counts.get(label, 0) + 1
    
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} photos")
    
    return labels

def organize_labeled_photos(labels):
    """Organize photos into category folders based on labels"""
    print("\n📁 Organizing labeled photos into category folders...")
    
    for photo_key, category in labels.items():
        if category == 'skip':
            continue
        
        source_path = SOURCE_DIR / photo_key
        if not source_path.exists():
            print(f"⚠️  Source not found: {source_path}")
            continue
        
        # Create category directory
        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy photo to category folder
        dest_path = category_dir / source_path.name
        shutil.copy2(source_path, dest_path)
        print(f"  ✅ {category}/{source_path.name}")
    
    print(f"\n✅ Photos organized in: {OUTPUT_DIR}")

def show_stats():
    """Show statistics about labeled photos"""
    labels_file = OUTPUT_DIR / "labels.json"
    
    if not labels_file.exists():
        print("❌ No labels file found. Run labeling first.")
        return
    
    with open(labels_file, 'r') as f:
        labels = json.load(f)
    
    print("\n📊 Current Labeling Statistics")
    print("=" * 50)
    print(f"Total labeled: {len(labels)} photos")
    
    # Count by category
    category_counts = {}
    for label in labels.values():
        category_counts[label] = category_counts.get(label, 0) + 1
    
    for category in ['fresh', 'light_oxidation', 'medium_oxidation', 'heavy_oxidation', 'skip']:
        count = category_counts.get(category, 0)
        print(f"  {category}: {count} photos")
    
    # Analyze by apple type
    print("\n📊 By Apple Type:")
    gala_labels = [v for k, v in labels.items() if 'gala' in k]
    smith_labels = [v for k, v in labels.items() if 'granny_smith' in k]
    
    print(f"  Gala: {len(gala_labels)} labeled")
    print(f"  Granny Smith: {len(smith_labels)} labeled")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'stats':
        show_stats()
    elif len(sys.argv) > 1 and sys.argv[1] == 'organize':
        labels_file = OUTPUT_DIR / "labels.json"
        if labels_file.exists():
            with open(labels_file, 'r') as f:
                labels = json.load(f)
            organize_labeled_photos(labels)
        else:
            print("❌ No labels found. Run labeling first.")
    else:
        labels = label_photos()
        
        # Ask if user wants to organize photos
        print("\n" + "=" * 70)
        organize = input("Organize labeled photos into category folders? (y/n): ").strip().lower()
        if organize == 'y':
            organize_labeled_photos(labels)
        
        print("\n🎉 Labeling complete!")
        print("\n💡 Next steps:")
        print("  1. Review labels: python label_images.py stats")
        print("  2. Organize photos: python label_images.py organize")
        print("  3. Train model with labeled data")
