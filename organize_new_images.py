#!/usr/bin/env python3
"""
Organize and rename new apple images from incoming folder.

This script:
1. Reads EXIF dates from images in incoming/
2. Groups them into sessions (AM/PM based on time)
3. Renames according to naming convention
4. Creates organized folder structure
5. Copies (preserves incoming/) to new location
"""

import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from collections import defaultdict

# Configuration
INCOMING_DIR = '/home/edster/projects/esahakian/science_fair_2026/data_repository/01_raw_images/incoming'
OUTPUT_DIR = '/home/edster/projects/esahakian/science_fair_2026/data_repository/01_raw_images/second_collection_nov2024'

# Apple types in order (each session has 24 images: 8 per type)
APPLE_TYPES = ['granny_smith', 'gala', 'red_delicious']

# Angle mapping (even index = top_down, odd index = angled_45)
ANGLES = ['top_down', 'angled_45']


def extract_exif_date(filepath):
    """Extract DateTimeOriginal from EXIF data."""
    try:
        img = Image.open(filepath)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'DateTimeOriginal':
                    img.close()
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        img.close()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return None


def group_into_sessions(file_dates, gap_hours=6):
    """Group files into sessions based on time gaps."""
    sessions = []
    current_session = []
    last_time = None

    for f, dt in file_dates:
        if last_time is None or (dt - last_time).total_seconds() > gap_hours * 3600:
            if current_session:
                sessions.append(current_session)
            current_session = [(f, dt)]
        else:
            current_session.append((f, dt))
        last_time = dt

    if current_session:
        sessions.append(current_session)

    return sessions


def get_session_info(session):
    """Get date, AM/PM, and baseline hours for a session."""
    first_dt = session[0][1]
    date_str = first_dt.strftime('%Y%m%d')
    am_pm = 'am' if first_dt.hour < 12 else 'pm'
    return date_str, am_pm, first_dt


def calculate_hours_from_baseline(session_dt, baseline_dt):
    """Calculate hours elapsed from baseline datetime."""
    delta = session_dt - baseline_dt
    return int(delta.total_seconds() / 3600)


def get_image_info(index_in_session):
    """
    Given an index (0-23) within a session, return:
    - apple_type: granny_smith, gala, or red_delicious
    - fruit_num: 1-4
    - angle: top_down or angled_45
    """
    # Determine apple type (0-7: granny_smith, 8-15: gala, 16-23: red_delicious)
    type_index = index_in_session // 8
    apple_type = APPLE_TYPES[type_index]

    # Position within the 8 images for this apple type
    pos_in_type = index_in_session % 8

    # Fruit number (0-1: fruit1, 2-3: fruit2, 4-5: fruit3, 6-7: fruit4)
    fruit_num = (pos_in_type // 2) + 1

    # Angle (even: top_down, odd: angled_45)
    angle = ANGLES[pos_in_type % 2]

    return apple_type, fruit_num, angle


def generate_new_filename(apple_type, fruit_num, day_num, hours, angle, date_str, am_pm):
    """Generate the new filename according to naming convention."""
    return f"{apple_type}_fruit{fruit_num}_day{day_num}_{hours:03d}h_{angle}_{date_str}-{am_pm}.JPG"


def main():
    print("=" * 80)
    print("Apple Image Organizer - Second Collection Nov 2024")
    print("=" * 80)

    # Get all JPG files
    files = sorted([f for f in os.listdir(INCOMING_DIR) if f.upper().endswith('.JPG')])
    print(f"\nFound {len(files)} images in incoming folder")

    # Extract EXIF dates
    print("\nExtracting EXIF dates...")
    file_dates = []
    for f in files:
        path = os.path.join(INCOMING_DIR, f)
        dt = extract_exif_date(path)
        if dt:
            file_dates.append((f, dt))
        else:
            print(f"  Warning: Could not extract date from {f}")

    # Sort by datetime
    file_dates.sort(key=lambda x: x[1])
    print(f"Successfully extracted dates from {len(file_dates)} images")

    # Group into sessions
    sessions = group_into_sessions(file_dates)
    print(f"\nIdentified {len(sessions)} sessions")

    # Use first session as baseline
    baseline_dt = sessions[0][0][1]
    print(f"Baseline datetime: {baseline_dt}")

    # Create output directory structure
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process each session
    copy_operations = []
    session_summary = []

    for session_idx, session in enumerate(sessions):
        date_str, am_pm, session_dt = get_session_info(session)
        hours_from_baseline = calculate_hours_from_baseline(session_dt, baseline_dt)
        day_num = hours_from_baseline // 24

        session_summary.append({
            'session': session_idx + 1,
            'date': session_dt.strftime('%Y-%m-%d'),
            'am_pm': am_pm.upper(),
            'hours': hours_from_baseline,
            'day': day_num,
            'count': len(session)
        })

        print(f"\nSession {session_idx + 1}: {session_dt.strftime('%Y-%m-%d')} {am_pm.upper()}")
        print(f"  Hours from baseline: {hours_from_baseline}h (Day {day_num})")
        print(f"  Images: {len(session)}")

        if len(session) != 24:
            print(f"  WARNING: Expected 24 images, got {len(session)}")

        # Process each image in session
        for img_idx, (filename, img_dt) in enumerate(session):
            apple_type, fruit_num, angle = get_image_info(img_idx)

            new_filename = generate_new_filename(
                apple_type, fruit_num, day_num, hours_from_baseline,
                angle, date_str, am_pm
            )

            # Create directory structure: OUTPUT_DIR/apple_type/fruit_N/
            dest_dir = os.path.join(OUTPUT_DIR, apple_type, f'fruit_{fruit_num}')
            os.makedirs(dest_dir, exist_ok=True)

            src_path = os.path.join(INCOMING_DIR, filename)
            dest_path = os.path.join(dest_dir, new_filename)

            copy_operations.append((src_path, dest_path, filename, new_filename))

    # Print session summary
    print("\n" + "=" * 80)
    print("SESSION SUMMARY")
    print("=" * 80)
    print(f"{'Session':<8} {'Date':<12} {'Time':<6} {'Hours':<8} {'Day':<6} {'Count':<6}")
    print("-" * 50)
    for s in session_summary:
        print(f"{s['session']:<8} {s['date']:<12} {s['am_pm']:<6} {s['hours']:<8} {s['day']:<6} {s['count']:<6}")

    # Execute copy operations
    print("\n" + "=" * 80)
    print(f"COPYING {len(copy_operations)} FILES")
    print("=" * 80)

    for i, (src, dest, old_name, new_name) in enumerate(copy_operations):
        shutil.copy2(src, dest)
        if (i + 1) % 50 == 0 or i == len(copy_operations) - 1:
            print(f"  Copied {i + 1}/{len(copy_operations)} files...")

    # Final summary
    print("\n" + "=" * 80)
    print("ORGANIZATION COMPLETE")
    print("=" * 80)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total files copied: {len(copy_operations)}")
    print(f"\nDirectory structure created:")
    for apple_type in APPLE_TYPES:
        type_dir = os.path.join(OUTPUT_DIR, apple_type)
        if os.path.exists(type_dir):
            count = sum(len(files) for _, _, files in os.walk(type_dir))
            print(f"  {apple_type}/: {count} images")

    # Create metadata file
    metadata_path = os.path.join(OUTPUT_DIR, 'COLLECTION_METADATA.md')
    with open(metadata_path, 'w') as f:
        f.write("# Second Collection - November 2024\n\n")
        f.write("## Collection Details\n\n")
        f.write(f"- **Collection Period:** {sessions[0][0][1].strftime('%Y-%m-%d')} to {sessions[-1][0][1].strftime('%Y-%m-%d')}\n")
        f.write(f"- **Total Sessions:** {len(sessions)}\n")
        f.write(f"- **Total Images:** {len(copy_operations)}\n")
        f.write(f"- **Apple Varieties:** Granny Smith, Gala, Red Delicious\n")
        f.write(f"- **Apples per Variety:** 4\n")
        f.write(f"- **Angles per Apple:** 2 (top_down, angled_45)\n")
        f.write(f"- **Baseline:** {baseline_dt.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Session Log\n\n")
        f.write("| Session | Date | Time | Hours | Day | Images |\n")
        f.write("|---------|------|------|-------|-----|--------|\n")
        for s in session_summary:
            f.write(f"| {s['session']} | {s['date']} | {s['am_pm']} | {s['hours']}h | {s['day']} | {s['count']} |\n")
        f.write("\n## Naming Convention\n\n")
        f.write("```\n")
        f.write("[apple_type]_fruit[N]_day[N]_[hours]h_[angle]_[date]-[am|pm].JPG\n")
        f.write("```\n\n")
        f.write("Example: `granny_smith_fruit1_day0_000h_top_down_20241101-am.JPG`\n")

    print(f"\nMetadata saved to: {metadata_path}")
    print("\nDone!")


if __name__ == '__main__':
    main()
