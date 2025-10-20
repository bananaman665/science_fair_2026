#!/usr/bin/env python3
"""
Image Organization Script
Organizes raw apple photos into proper ML training structure
Handles naming convention: [date]-[am|pm]-[gala|smith]-[fruit-index]-[angle-index]
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

# Paths
SOURCE_DIR = Path("data_repository/ImageSet")
TARGET_BASE = Path("data_repository/01_raw_images/first_collection_oct2025")

def parse_filename(filename):
    """
    Parse filename to extract metadata
    Format: [date]-[am|pm]-[gala|smith]-[fruit-index]-[angle-index].JPG
    Example: 20251005-pm-gala-1-1.JPG
    """
    # Remove .JPG extension
    name = filename.replace('.JPG', '')
    
    # Split by dash
    parts = name.split('-')
    
    if len(parts) < 5:
        print(f"⚠️  Warning: Unexpected filename format: {filename}")
        return None
    
    try:
        date_str = parts[0]  # 20251005
        time_period = parts[1]  # am or pm
        apple_type = parts[2]  # gala or smith
        fruit_index = parts[3]  # 1 or 2
        angle_index = parts[4]  # 1 or 2
        
        # Parse date
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        
        # Calculate hours since start (Oct 5 PM is baseline)
        start_date = datetime(2025, 10, 5, 18, 0)  # Oct 5, 6 PM
        
        # Set time based on am/pm
        if time_period == 'am':
            current_time = date_obj.replace(hour=9, minute=0)  # 9 AM
        else:
            current_time = date_obj.replace(hour=18, minute=0)  # 6 PM
        
        hours_since_start = int((current_time - start_date).total_seconds() / 3600)
        
        # Normalize apple type
        apple_type_full = 'gala' if apple_type == 'gala' else 'granny_smith'
        
        # Angle description
        angle_desc = 'top_down' if angle_index == '1' else 'angled_45'
        
        return {
            'date': date_str,
            'time_period': time_period,
            'apple_type': apple_type_full,
            'fruit_index': fruit_index,
            'angle_index': angle_index,
            'angle_desc': angle_desc,
            'hours_since_start': hours_since_start,
            'day_number': hours_since_start // 24,
            'original_filename': filename
        }
    except Exception as e:
        print(f"❌ Error parsing {filename}: {e}")
        return None

def organize_images():
    """Organize images into structured directories"""
    
    if not SOURCE_DIR.exists():
        print(f"❌ Source directory not found: {SOURCE_DIR}")
        return
    
    # Get all JPG files
    jpg_files = list(SOURCE_DIR.glob("*.JPG"))
    print(f"📸 Found {len(jpg_files)} images in {SOURCE_DIR}")
    
    # Parse all filenames
    parsed_files = []
    for jpg_file in jpg_files:
        metadata = parse_filename(jpg_file.name)
        if metadata:
            metadata['source_path'] = jpg_file
            parsed_files.append(metadata)
    
    print(f"✅ Successfully parsed {len(parsed_files)} filenames")
    
    # Create organized structure
    print(f"\n📁 Organizing into: {TARGET_BASE}")
    
    # Group by apple type and day
    for file_info in parsed_files:
        apple_type = file_info['apple_type']
        day_num = file_info['day_number']
        fruit_idx = file_info['fruit_index']
        
        # Create directory structure:
        # 01_raw_images/first_collection_oct2025/gala/fruit_1/day_0/
        target_dir = TARGET_BASE / apple_type / f"fruit_{fruit_idx}" / f"day_{day_num}"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Create new filename with metadata
        # Format: gala_fruit1_day0_15h_top_down_20251005-pm.JPG
        new_filename = (
            f"{file_info['apple_type']}_"
            f"fruit{file_info['fruit_index']}_"
            f"day{file_info['day_number']}_"
            f"{file_info['hours_since_start']:03d}h_"
            f"{file_info['angle_desc']}_"
            f"{file_info['date']}-{file_info['time_period']}.JPG"
        )
        
        target_path = target_dir / new_filename
        
        # Copy file
        shutil.copy2(file_info['source_path'], target_path)
        print(f"  📄 {file_info['original_filename']} → {target_path.relative_to(TARGET_BASE)}")
    
    print(f"\n✅ Organization complete!")
    
    # Print summary
    print("\n📊 Collection Summary:")
    print("=" * 50)
    
    for apple_type in ['gala', 'granny_smith']:
        type_dir = TARGET_BASE / apple_type
        if type_dir.exists():
            fruit_dirs = sorted([d for d in type_dir.iterdir() if d.is_dir()])
            print(f"\n🍎 {apple_type.upper()}:")
            for fruit_dir in fruit_dirs:
                day_dirs = sorted([d for d in fruit_dir.iterdir() if d.is_dir()])
                print(f"  {fruit_dir.name}:")
                for day_dir in day_dirs:
                    photo_count = len(list(day_dir.glob("*.JPG")))
                    print(f"    {day_dir.name}: {photo_count} photos")

def create_metadata_file():
    """Create metadata file with collection information"""
    
    metadata_content = """# First Apple Collection - October 2025
## Collection Metadata

**Collection Period:** October 5-10, 2025  
**Duration:** 6 days  
**Sessions:** 2 per day (AM/PM)  
**Apple Varieties:** Gala, Granny Smith  
**Apples per Variety:** 2  
**Angles per Photo:** 2 (top-down, 45°)  
**Total Photos:** 96

---

## Collection Schedule

**Baseline:** October 5, 2025 - 6:00 PM  
**Sessions:**
- AM sessions: ~9:00 AM
- PM sessions: ~6:00 PM

**Timeline:**
- Day 0: Oct 5 PM (baseline/fresh)
- Day 1: Oct 6 AM/PM (~15h, ~24h)
- Day 2: Oct 7 AM/PM (~39h, ~48h)
- Day 3: Oct 8 AM/PM (~63h, ~72h)
- Day 4: Oct 9 AM/PM (~87h, ~96h)
- Day 5: Oct 10 AM/PM (~111h, ~120h)

---

## Naming Convention

**Original Format:** `[date]-[am|pm]-[gala|smith]-[fruit-index]-[angle-index].JPG`

**Example:** `20251005-pm-gala-1-1.JPG`
- Date: October 5, 2025
- Time: PM (evening)
- Apple: Gala
- Fruit: #1
- Angle: 1 (top-down)

**Organized Format:** `[apple]_fruit[N]_day[N]_[hours]h_[angle]_[date]-[time].JPG`

**Example:** `gala_fruit1_day0_000h_top_down_20251005-pm.JPG`

---

## Photo Angles

1. **Angle 1 (top-down):** 90° perpendicular view of apple surface
2. **Angle 2 (45°):** Angled view for depth and dimension

---

## Storage

All photos stored at room temperature for natural oxidation progression.

---

## Next Steps

1. Visual inspection and manual labeling (fresh/light/medium/heavy oxidation)
2. Data preprocessing and augmentation
3. ML model training with real apple data
4. Model evaluation and comparison to synthetic data results
"""
    
    metadata_file = TARGET_BASE / "COLLECTION_METADATA.md"
    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(metadata_content)
    print(f"\n📝 Created metadata file: {metadata_file}")

if __name__ == "__main__":
    print("🍎 Apple Photo Organization Tool")
    print("=" * 50)
    
    # Organize images
    organize_images()
    
    # Create metadata file
    create_metadata_file()
    
    print("\n🎉 All done! Your images are now properly organized for ML training!")
    print(f"📁 Check: {TARGET_BASE}")
