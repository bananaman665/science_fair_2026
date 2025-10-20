#!/usr/bin/env python3
"""
Oxidation Timeline Analyzer
Analyzes and visualizes apple oxidation progression over time
"""

import os
from pathlib import Path
from collections import defaultdict

SOURCE_DIR = Path("data_repository/01_raw_images/first_collection_oct2025")

def parse_photo_metadata(filename):
    """Extract metadata from organized filename"""
    # Format: gala_fruit1_day0_000h_top_down_20251005-pm.JPG
    # or: granny_smith_fruit1_day0_000h_top_down_20251005-pm.JPG
    parts = filename.replace('.JPG', '').split('_')
    
    # Handle granny_smith (2 parts) vs gala (1 part)
    if parts[0] == 'granny':
        apple_type = 'granny_smith'
        offset = 1  # parts[1] is 'smith'
    else:
        apple_type = parts[0]
        offset = 0
    
    if len(parts) < 4 + offset:
        return None
    
    return {
        'apple_type': apple_type,
        'fruit': parts[1 + offset],
        'day': parts[2 + offset],
        'hours': int(parts[3 + offset].replace('h', '')),
        'angle': parts[4 + offset] if len(parts) > 4 + offset else 'unknown'
    }

def analyze_collection():
    """Analyze the photo collection and show timeline"""
    
    print("\n🍎 Apple Oxidation Collection Analysis")
    print("=" * 70)
    
    # Collect all photos
    photos_by_fruit = defaultdict(list)
    
    for apple_type in ['gala', 'granny_smith']:
        apple_dir = SOURCE_DIR / apple_type
        if not apple_dir.exists():
            continue
        
        for photo in apple_dir.rglob("*.JPG"):
            metadata = parse_photo_metadata(photo.name)
            if metadata:
                fruit_key = f"{metadata['apple_type']}_{metadata['fruit']}"
                photos_by_fruit[fruit_key].append({
                    'path': photo,
                    'metadata': metadata
                })
    
    # Sort photos by hours for each fruit
    for fruit_key in photos_by_fruit:
        photos_by_fruit[fruit_key].sort(key=lambda x: x['metadata']['hours'])
    
    # Display timeline for each fruit
    for fruit_key in sorted(photos_by_fruit.keys()):
        photos = photos_by_fruit[fruit_key]
        metadata = photos[0]['metadata']
        
        print(f"\n{'─' * 70}")
        print(f"🍎 {metadata['apple_type'].upper()} - {metadata['fruit'].upper()}")
        print(f"{'─' * 70}")
        
        # Group by time point
        by_time = defaultdict(list)
        for photo in photos:
            hours = photo['metadata']['hours']
            by_time[hours].append(photo)
        
        print(f"\n📅 Timeline ({len(by_time)} time points):")
        
        for hours in sorted(by_time.keys()):
            time_photos = by_time[hours]
            day = hours // 24
            remaining_hours = hours % 24
            
            # Count angles
            angles = [p['metadata']['angle'] for p in time_photos]
            angle_str = f"{len(angles)} photos ({', '.join(set(angles))})"
            
            # Visual timeline marker
            marker = "📸"
            if hours == 0:
                marker = "🔵 FRESH"
            elif hours >= 96:
                marker = "🔴 HEAVY?"
            elif hours >= 48:
                marker = "🟡 MEDIUM?"
            elif hours >= 24:
                marker = "🟢 LIGHT?"
            
            print(f"  {marker} {hours:3d}h (Day {day}, +{remaining_hours}h): {angle_str}")
            
            # Show filenames
            for photo in time_photos:
                print(f"       {photo['path'].name}")
    
    # Overall statistics
    total_photos = sum(len(photos) for photos in photos_by_fruit.values())
    print(f"\n{'=' * 70}")
    print(f"📊 COLLECTION SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Total fruits tracked: {len(photos_by_fruit)}")
    print(f"  Total photos: {total_photos}")
    print(f"  Photos per fruit: {total_photos // len(photos_by_fruit) if photos_by_fruit else 0}")
    
    # Time range
    all_hours = []
    for photos in photos_by_fruit.values():
        all_hours.extend([p['metadata']['hours'] for p in photos])
    
    if all_hours:
        print(f"  Time range: {min(all_hours)}h - {max(all_hours)}h ({max(all_hours) // 24} days)")
        print(f"  Unique time points: {len(set(all_hours))}")
    
    print("\n💡 Oxidation Guidance:")
    print("  0-24h:   Likely FRESH or early LIGHT oxidation")
    print("  24-48h:  Likely LIGHT oxidation")
    print("  48-72h:  Likely MEDIUM oxidation")
    print("  72h+:    Likely MEDIUM to HEAVY oxidation")
    print("\n⚠️  Note: Actual oxidation varies by apple type and storage conditions")
    print("   Review photos visually to confirm oxidation levels!")

def show_labeling_recommendations():
    """Provide recommendations for manual labeling"""
    
    print("\n\n📋 LABELING RECOMMENDATIONS")
    print("=" * 70)
    print("\n1️⃣  FRESH (0-15 hours):")
    print("   - No visible browning")
    print("   - Apple surface looks just-cut")
    print("   - Natural apple color (yellow/green)")
    
    print("\n2️⃣  LIGHT OXIDATION (15-48 hours typically):")
    print("   - Slight browning at edges")
    print("   - Some color change visible")
    print("   - Most of surface still looks fresh")
    
    print("\n3️⃣  MEDIUM OXIDATION (48-96 hours typically):")
    print("   - Noticeable browning across surface")
    print("   - Clear color change from fresh")
    print("   - But not completely brown yet")
    
    print("\n4️⃣  HEAVY OXIDATION (96+ hours typically):")
    print("   - Significant brown color")
    print("   - Most/all of surface affected")
    print("   - Darker brown appearance")
    
    print("\n⚠️  IMPORTANT:")
    print("   - Granny Smith (green) may oxidize slower than Gala")
    print("   - Look at EACH photo individually")
    print("   - Don't just label by time - use visual assessment!")
    print("   - When in doubt, compare to earlier photos of same fruit")

if __name__ == "__main__":
    analyze_collection()
    show_labeling_recommendations()
    
    print("\n\n🚀 Next Steps:")
    print("=" * 70)
    print("1. Review this timeline to understand oxidation progression")
    print("2. Open photos in Finder/Preview to visually inspect them")
    print("3. Run: python label_images.py")
    print("4. Manually label each photo based on VISUAL inspection")
    print("5. Train ML model with your labeled data!")
    print("\n💡 TIP: Start by labeling a few from each time point to get calibrated")
