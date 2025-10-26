#!/usr/bin/env python3
"""
Improved Apple Preprocessing for Cell Phone Photos
Uses more aggressive segmentation for noisy backgrounds
"""

import numpy as np
from PIL import Image
import cv2
from pathlib import Path

COMPARE_DIR = Path("data_repository/compare_images")
OUTPUT_DIR = Path("data_repository/compare_images_cropped_v2")
COMPARISON_DIR = Path("data_repository/cropping_comparison/compare_images_v2")

def aggressive_apple_segmentation(image_path):
    """
    More aggressive segmentation for phone photos with complex backgrounds
    """
    
    # Load image
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    original = img.copy()
    height, width = img.shape[:2]
    
    # Convert to different color spaces for better segmentation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Strategy 1: HSV color-based (broader ranges for phone photos)
    lower_green = np.array([30, 20, 20])  # Broader green range
    upper_green = np.array([90, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    
    # Red apples (if any in test)
    lower_red1 = np.array([0, 20, 20])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 20, 20])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )
    
    # Yellow/brown oxidation
    lower_yellow = np.array([10, 20, 20])
    upper_yellow = np.array([40, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Combine color masks
    mask_color = cv2.bitwise_or(mask_green, mask_red)
    mask_color = cv2.bitwise_or(mask_color, mask_yellow)
    
    # Strategy 2: Brightness-based (remove very bright/dark areas)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask_bright = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)  # Remove very bright
    _, mask_dark = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)  # Remove very dark
    mask_brightness = cv2.bitwise_and(mask_bright, mask_dark)
    
    # Combine strategies
    mask_combined = cv2.bitwise_and(mask_color, mask_brightness)
    
    # Aggressive morphological operations to clean mask
    kernel_large = np.ones((15, 15), np.uint8)
    kernel_small = np.ones((5, 5), np.uint8)
    
    # Close gaps
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_CLOSE, kernel_large, iterations=3)
    # Remove small noise
    mask_combined = cv2.morphologyEx(mask_combined, cv2.MORPH_OPEN, kernel_small, iterations=2)
    # Dilate slightly to ensure we get all of apple
    mask_combined = cv2.dilate(mask_combined, kernel_small, iterations=1)
    
    # Find contours
    contours, _ = cv2.findContours(mask_combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("⚠️  No apple detected")
        return None
    
    # Get largest contour (apple should be prominent in phone photos)
    largest_contour = max(contours, key=cv2.contourArea)
    contour_area = cv2.contourArea(largest_contour)
    
    # Check if contour is reasonable size (should be significant portion of image)
    image_area = width * height
    if contour_area < image_area * 0.05:  # Less than 5% of image
        print(f"⚠️  Detected region too small: {contour_area/image_area*100:.1f}% of image")
        return None
    
    # Get bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Add generous padding for phone photos (15% vs 10%)
    padding_x = int(w * 0.15)
    padding_y = int(h * 0.15)
    
    x1 = max(0, x - padding_x)
    y1 = max(0, y - padding_y)
    x2 = min(width, x + w + padding_x)
    y2 = min(height, y + h + padding_y)
    
    # Crop
    cropped = original[y1:y2, x1:x2]
    
    # Return cropped image and debug info
    debug_img = original.copy()
    cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 5)
    cv2.drawContours(debug_img, [largest_contour], -1, (255, 0, 0), 3)
    
    return cropped, debug_img, mask_combined

def create_comparison_triple(original_path, cropped_img, debug_img, mask, output_path):
    """Create triple comparison: original | detection | cropped"""
    
    original = cv2.imread(str(original_path))
    if original is None:
        return
    
    orig_h, orig_w = original.shape[:2]
    
    # Resize everything to same height
    target_h = 800
    
    # Original
    scale = target_h / orig_h
    orig_resized = cv2.resize(original, (int(orig_w * scale), target_h))
    
    # Debug/detection view
    debug_resized = cv2.resize(debug_img, (int(orig_w * scale), target_h))
    
    # Mask visualization (convert to color)
    mask_color = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_resized = cv2.resize(mask_color, (int(orig_w * scale), target_h))
    
    # Cropped (scale to target height)
    crop_h, crop_w = cropped_img.shape[:2]
    crop_scale = target_h / crop_h
    crop_resized = cv2.resize(cropped_img, (int(crop_w * crop_scale), target_h))
    
    # Stack horizontally
    comparison = np.hstack([orig_resized, mask_resized, debug_resized, crop_resized])
    
    # Add labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(comparison, 'ORIGINAL', (20, 40), font, 1, (0, 255, 0), 2)
    cv2.putText(comparison, 'MASK', (orig_resized.shape[1] + 20, 40), font, 1, (0, 255, 0), 2)
    cv2.putText(comparison, 'DETECTION', (orig_resized.shape[1] + mask_resized.shape[1] + 20, 40), font, 1, (0, 255, 0), 2)
    cv2.putText(comparison, 'CROPPED', (orig_resized.shape[1] + mask_resized.shape[1] + debug_resized.shape[1] + 20, 40), font, 1, (0, 255, 0), 2)
    
    # Save
    cv2.imwrite(str(output_path), comparison)

def main():
    print("\n🍎 Improved Apple Preprocessing for Phone Photos")
    print("="*70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    COMPARISON_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_paths = list(COMPARE_DIR.glob("*.jpg")) + list(COMPARE_DIR.glob("*.JPG"))
    
    if not image_paths:
        print(f"❌ No images found in {COMPARE_DIR}")
        return
    
    print(f"📸 Found {len(image_paths)} images to process\n")
    
    stats = {'success': 0, 'failed': 0}
    
    for i, img_path in enumerate(sorted(image_paths), 1):
        print(f"[{i}/{len(image_paths)}] {img_path.name}...", end=' ')
        
        result = aggressive_apple_segmentation(img_path)
        
        if result is None:
            print("❌ FAILED")
            stats['failed'] += 1
            continue
        
        cropped, debug_img, mask = result
        
        # Save cropped
        output_path = OUTPUT_DIR / img_path.name
        cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        cropped_pil.save(output_path)
        
        # Save comparison
        comparison_path = COMPARISON_DIR / f"compare_{img_path.name}"
        create_comparison_triple(img_path, cropped, debug_img, mask, comparison_path)
        
        print(f"✅ OK")
        stats['success'] += 1
    
    print(f"\n{'='*70}")
    print(f"✅ Success: {stats['success']}/{len(image_paths)}")
    print(f"❌ Failed: {stats['failed']}/{len(image_paths)}")
    print(f"\n📁 Outputs:")
    print(f"   Cropped: {OUTPUT_DIR}")
    print(f"   Comparisons: {COMPARISON_DIR}")
    print(f"\n🔍 Review: open {COMPARISON_DIR}")

if __name__ == "__main__":
    main()
