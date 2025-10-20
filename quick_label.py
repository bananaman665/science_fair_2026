#!/usr/bin/env python3
"""
Quick Auto-Labeling Tool
Automatically suggests labels based on time, but lets you review and adjust
"""

import json
from pathlib import Path
import shutil

SOURCE_DIR = Path("data_repository/01_raw_images/first_collection_oct2025")
OUTPUT_DIR = Path("data_repository/02_processed_images/labeled_training_set")

def auto_label_by_time():
    """
    Auto-label photos based on hours since start
    You can manually adjust these later if needed
    """
    
    print("\n🤖 Auto-Labeling Apple Photos Based on Time")
    print("=" * 70)
    print("\nThis will automatically label photos based on oxidation time:")
    print("  • 0-20h:   FRESH")
    print("  • 21-50h:  LIGHT OXIDATION")
    print("  • 51-90h:  MEDIUM OXIDATION")
    print("  • 91h+:    HEAVY OXIDATION")
    print("\n⚠️  These are estimates - you should review a few photos to verify!")
    
    proceed = input("\nProceed with auto-labeling? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Cancelled.")
        return
    
    # Collect all photos
    labels = {}
    stats = {'fresh': 0, 'light_oxidation': 0, 'medium_oxidation': 0, 'heavy_oxidation': 0}
    
    for apple_type in ['gala', 'granny_smith']:
        apple_dir = SOURCE_DIR / apple_type
        if not apple_dir.exists():
            continue
        
        for photo in apple_dir.rglob("*.JPG"):
            # Parse filename to get hours
            # Format: gala_fruit1_day0_000h_top_down_20251005-pm.JPG
            filename = photo.name
            parts = filename.replace('.JPG', '').split('_')
            
            # Handle granny_smith vs gala
            if parts[0] == 'granny':
                offset = 1
            else:
                offset = 0
            
            try:
                hours = int(parts[3 + offset].replace('h', ''))
                
                # Auto-classify based on hours
                if hours <= 20:
                    category = 'fresh'
                elif hours <= 50:
                    category = 'light_oxidation'
                elif hours <= 90:
                    category = 'medium_oxidation'
                else:
                    category = 'heavy_oxidation'
                
                photo_key = str(photo.relative_to(SOURCE_DIR))
                labels[photo_key] = category
                stats[category] += 1
                
                print(f"  ✅ {hours:3d}h → {category:20s} | {photo.name}")
                
            except (IndexError, ValueError) as e:
                print(f"  ⚠️  Skipped {photo.name}: {e}")
    
    # Save labels
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    labels_file = OUTPUT_DIR / "labels.json"
    
    with open(labels_file, 'w') as f:
        json.dump(labels, f, indent=2)
    
    print(f"\n✅ Auto-labeled {len(labels)} photos!")
    print("\n📊 Label Distribution:")
    print("=" * 50)
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} photos")
    
    print(f"\n💾 Saved to: {labels_file}")
    
    return labels

def organize_labeled_photos(labels):
    """Copy photos into category folders"""
    
    print("\n📁 Organizing photos into category folders...")
    
    for photo_key, category in labels.items():
        source_path = SOURCE_DIR / photo_key
        if not source_path.exists():
            print(f"  ⚠️  Not found: {source_path}")
            continue
        
        # Create category directory
        category_dir = OUTPUT_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy photo
        dest_path = category_dir / source_path.name
        shutil.copy2(source_path, dest_path)
    
    print(f"\n✅ Photos organized in: {OUTPUT_DIR}")
    
    # Show summary
    print("\n📂 Directory Structure:")
    for category in ['fresh', 'light_oxidation', 'medium_oxidation', 'heavy_oxidation']:
        category_dir = OUTPUT_DIR / category
        if category_dir.exists():
            count = len(list(category_dir.glob("*.JPG")))
            print(f"  {category}/: {count} photos")

def show_sample_photos():
    """Show a few sample photos from each category for review"""
    
    print("\n👀 Sample Photos to Review:")
    print("=" * 70)
    print("Open these photos to verify the auto-labeling is reasonable:\n")
    
    labels_file = OUTPUT_DIR / "labels.json"
    if not labels_file.exists():
        print("❌ No labels file found. Run auto-labeling first.")
        return
    
    with open(labels_file, 'r') as f:
        labels = json.load(f)
    
    # Get samples from each category
    by_category = {}
    for photo_key, category in labels.items():
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(photo_key)
    
    for category in ['fresh', 'light_oxidation', 'medium_oxidation', 'heavy_oxidation']:
        if category in by_category and by_category[category]:
            print(f"\n🔍 {category.upper()}:")
            # Show first 3 examples
            for photo_key in by_category[category][:3]:
                photo_path = SOURCE_DIR / photo_key
                print(f"   {photo_path}")
    
    print("\n💡 TIP: Open these in Finder to visually verify the categories")
    print("If they look wrong, you can manually adjust the labels.json file")

if __name__ == "__main__":
    import sys
    
    print("\n🍎 Apple Photo Auto-Labeling Tool")
    print("=" * 70)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'samples':
        show_sample_photos()
    else:
        # Auto-label
        labels = auto_label_by_time()
        
        if labels:
            # Organize
            print("\n" + "=" * 70)
            organize = input("Organize photos into category folders now? (y/n): ").strip().lower()
            if organize == 'y':
                organize_labeled_photos(labels)
            
            # Show samples to review
            print("\n" + "=" * 70)
            show_sample_photos()
            
            print("\n\n✅ DONE!")
            print("\n📋 Next Steps:")
            print("  1. Review sample photos to verify labeling is reasonable")
            print("  2. If good, proceed to ML training!")
            print("  3. If not, adjust labels.json or re-run with different time thresholds")
