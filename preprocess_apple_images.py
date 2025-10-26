#!/usr/bin/env python3
"""
Apple Image Preprocessing - Background Removal & Cropping
Removes backgrounds and crops to apple region for better ML training

SAFETY: Original images are NEVER modified - all outputs go to new directories
"""

import numpy as np
from PIL import Image
import cv2
from pathlib import Path
import shutil
import json

# Directories
TRAINING_DIR = Path("data_repository/01_raw_images/first_collection_oct2025")
COMPARE_DIR = Path("data_repository/compare_images")

# Output directories (NEW - originals untouched!)
TRAINING_CROPPED_DIR = Path("data_repository/01_raw_images/first_collection_oct2025_cropped")
COMPARE_CROPPED_DIR = Path("data_repository/compare_images_cropped")

# Also create side-by-side comparison images
COMPARISON_DIR = Path("data_repository/cropping_comparison")

def remove_background_and_crop(image_path, debug=False):
    """
    Remove background and crop to apple region
    
    Strategy:
    1. Load image
    2. Convert to HSV color space
    3. Create mask for apple colors (red, green, yellow)
    4. Remove background (white/gray)
    5. Find bounding box around apple
    6. Crop with small padding
    7. Return cropped image
    """
    
    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"❌ Could not load: {image_path}")
        return None
    
    original = img.copy()
    height, width = img.shape[:2]
    
    # Convert to HSV for better color segmentation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create masks for different apple colors
    # Red apples (Gala, Red Delicious)
    lower_red1 = np.array([0, 30, 30])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 30, 30])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Green apples (Granny Smith)
    lower_green = np.array([35, 30, 30])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Yellow/brown (oxidized areas)
    lower_yellow = np.array([15, 30, 30])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Combine all apple color masks
    mask_apple = cv2.bitwise_or(mask_red, mask_green)
    mask_apple = cv2.bitwise_or(mask_apple, mask_yellow)
    
    # Clean up mask with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask_apple = cv2.morphologyEx(mask_apple, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask_apple = cv2.morphologyEx(mask_apple, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Fill holes
    contours, _ = cv2.findContours(mask_apple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"⚠️  No apple detected in: {image_path.name}")
        return None
    
    # Find largest contour (should be the apple)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Add padding (10% on each side)
    padding_x = int(w * 0.1)
    padding_y = int(h * 0.1)
    
    x1 = max(0, x - padding_x)
    y1 = max(0, y - padding_y)
    x2 = min(width, x + w + padding_x)
    y2 = min(height, y + h + padding_y)
    
    # Crop to bounding box
    cropped = original[y1:y2, x1:x2]
    
    # Debug visualization
    if debug:
        debug_img = original.copy()
        cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.drawContours(debug_img, [largest_contour], -1, (255, 0, 0), 2)
        return cropped, debug_img, mask_apple
    
    return cropped

def create_comparison_image(original_path, cropped_img, output_path):
    """Create side-by-side comparison image"""
    
    # Load original
    original = cv2.imread(str(original_path))
    if original is None:
        return
    
    # Resize cropped to match original height for comparison
    orig_h, orig_w = original.shape[:2]
    crop_h, crop_w = cropped_img.shape[:2]
    
    # Scale cropped to match original height
    scale = orig_h / crop_h
    new_w = int(crop_w * scale)
    cropped_resized = cv2.resize(cropped_img, (new_w, orig_h))
    
    # Create side-by-side
    comparison = np.hstack([original, cropped_resized])
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(comparison, 'ORIGINAL', (20, 40), font, 1, (0, 255, 0), 2)
    cv2.putText(comparison, 'CROPPED', (orig_w + 20, 40), font, 1, (0, 255, 0), 2)
    
    # Save
    cv2.imwrite(str(output_path), comparison)

def process_directory(input_dir, output_dir, comparison_subdir, description):
    """Process all images in a directory"""
    
    print(f"\n{'='*70}")
    print(f"Processing: {description}")
    print(f"{'='*70}")
    
    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison_dir = COMPARISON_DIR / comparison_subdir
    comparison_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all JPG images
    image_paths = list(input_dir.rglob("*.JPG")) + list(input_dir.rglob("*.jpg"))
    
    if not image_paths:
        print(f"⚠️  No images found in {input_dir}")
        return
    
    print(f"📸 Found {len(image_paths)} images")
    
    stats = {
        'total': len(image_paths),
        'successful': 0,
        'failed': 0,
        'failed_files': []
    }
    
    for i, img_path in enumerate(image_paths, 1):
        print(f"[{i}/{len(image_paths)}] Processing: {img_path.name}...", end=' ')
        
        # Process image
        result = remove_background_and_crop(img_path, debug=False)
        
        if result is None:
            print("❌ Failed")
            stats['failed'] += 1
            stats['failed_files'].append(str(img_path.name))
            continue
        
        cropped = result
        
        # Recreate directory structure in output
        relative_path = img_path.relative_to(input_dir)
        output_path = output_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save cropped image (convert back to PIL for saving)
        cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        cropped_pil.save(output_path)
        
        # Create comparison image
        comparison_path = comparison_dir / f"compare_{img_path.name}"
        create_comparison_image(img_path, cropped, comparison_path)
        
        print(f"✅ Saved")
        stats['successful'] += 1
    
    # Summary
    print(f"\n{'='*70}")
    print(f"✅ Successfully processed: {stats['successful']}/{stats['total']}")
    if stats['failed'] > 0:
        print(f"❌ Failed: {stats['failed']}")
        print(f"   Failed files: {', '.join(stats['failed_files'][:5])}")
        if len(stats['failed_files']) > 5:
            print(f"   ... and {len(stats['failed_files']) - 5} more")
    print(f"{'='*70}\n")
    
    return stats

def main():
    """Main preprocessing pipeline"""
    
    print("\n🍎 Apple Image Preprocessing - Background Removal & Cropping")
    print("="*70)
    print("SAFETY: All original images remain untouched!")
    print("         Cropped images saved to new directories")
    print("="*70)
    
    all_stats = {}
    
    # Process training images (organized by variety)
    if TRAINING_DIR.exists():
        stats = process_directory(
            TRAINING_DIR,
            TRAINING_CROPPED_DIR,
            "training_images",
            "Training Images (first_collection_oct2025)"
        )
        all_stats['training'] = stats
    else:
        print(f"⚠️  Training directory not found: {TRAINING_DIR}")
    
    # Process comparison/test images
    if COMPARE_DIR.exists():
        stats = process_directory(
            COMPARE_DIR,
            COMPARE_CROPPED_DIR,
            "compare_images",
            "Test/Comparison Images"
        )
        all_stats['compare'] = stats
    else:
        print(f"⚠️  Compare directory not found: {COMPARE_DIR}")
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 PREPROCESSING COMPLETE!")
    print("="*70)
    print("\n📊 Summary:")
    
    total_processed = sum(s['successful'] for s in all_stats.values())
    total_failed = sum(s['failed'] for s in all_stats.values())
    
    print(f"   Total images processed: {total_processed}")
    print(f"   Total failed: {total_failed}")
    
    print("\n📁 Output Locations:")
    print(f"   Cropped training images: {TRAINING_CROPPED_DIR}")
    print(f"   Cropped test images: {COMPARE_CROPPED_DIR}")
    print(f"   Side-by-side comparisons: {COMPARISON_DIR}")
    
    print("\n🔍 Next Steps:")
    print("   1. Review comparison images to verify cropping quality:")
    print(f"      open {COMPARISON_DIR}")
    print("   2. If cropping looks good, retrain model:")
    print("      python train_regression_model.py")
    print("   3. Re-test with cropped images:")
    print("      python test_single_apple.py add <cropped_image> <days>")
    
    # Save stats
    stats_file = Path("data_repository/cropping_stats.json")
    with open(stats_file, 'w') as f:
        json.dump(all_stats, f, indent=2)
    print(f"\n📈 Statistics saved to: {stats_file}")

if __name__ == "__main__":
    main()
