#!/usr/bin/env python3
"""
Manual Apple Cropping Tool
Interactive GUI to manually crop apples from phone photos
Much more reliable than automatic segmentation for complex backgrounds
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image
import json

COMPARE_DIR = Path("data_repository/compare_images")
OUTPUT_DIR = Path("data_repository/compare_images_cropped_manual")
CROPS_FILE = OUTPUT_DIR / "crop_coordinates.json"

# Global variables for mouse interaction
points = []
current_img = None
display_img = None
window_name = "Manual Apple Cropping - Click 4 corners around apple"

def mouse_callback(event, x, y, flags, param):
    """Handle mouse clicks to select crop region"""
    global points, display_img
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            # Draw point
            cv2.circle(display_img, (x, y), 5, (0, 255, 0), -1)
            cv2.putText(display_img, str(len(points)), (x+10, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # If we have 2+ points, draw lines
            if len(points) > 1:
                cv2.line(display_img, points[-2], points[-1], (0, 255, 0), 2)
            
            # If 4 points, complete the rectangle
            if len(points) == 4:
                cv2.line(display_img, points[3], points[0], (0, 255, 0), 2)
                cv2.putText(display_img, "Press ENTER to save, 'r' to reset, 'q' to quit", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            cv2.imshow(window_name, display_img)

def get_crop_rectangle(points):
    """Convert 4 points to rectangle coordinates"""
    # Find min/max x and y
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    x1, x2 = min(xs), max(xs)
    y1, y2 = min(ys), max(ys)
    
    return (x1, y1, x2, y2)

def crop_image(img, crop_coords):
    """Crop image to specified coordinates"""
    x1, y1, x2, y2 = crop_coords
    return img[y1:y2, x1:x2]

def manual_crop_workflow():
    """Interactive workflow for manually cropping all images"""
    global points, current_img, display_img
    
    print("\n🍎 Manual Apple Cropping Tool")
    print("="*70)
    print("\nInstructions:")
    print("  1. Click 4 corners around the apple (roughly rectangular)")
    print("  2. Press ENTER to save and move to next image")
    print("  3. Press 'r' to reset points and try again")
    print("  4. Press 'q' to quit")
    print("  5. Press 's' to skip current image")
    print("="*70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_paths = sorted(list(COMPARE_DIR.glob("*.jpg")) + list(COMPARE_DIR.glob("*.JPG")))
    
    if not image_paths:
        print(f"❌ No images found in {COMPARE_DIR}")
        return
    
    print(f"\n📸 Found {len(image_paths)} images to crop\n")
    
    # Load existing crop coordinates if available
    crop_data = {}
    if CROPS_FILE.exists():
        with open(CROPS_FILE, 'r') as f:
            crop_data = json.load(f)
        print(f"📋 Loaded {len(crop_data)} existing crop coordinates\n")
    
    # Create window
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback)
    
    completed = 0
    skipped = 0
    
    for i, img_path in enumerate(image_paths, 1):
        # Check if already processed
        if img_path.name in crop_data:
            print(f"[{i}/{len(image_paths)}] {img_path.name} - Already processed, skipping")
            completed += 1
            continue
        
        print(f"\n[{i}/{len(image_paths)}] Processing: {img_path.name}")
        
        # Load image
        current_img = cv2.imread(str(img_path))
        if current_img is None:
            print(f"  ❌ Could not load image")
            continue
        
        # Resize for display if too large
        display_h, display_w = current_img.shape[:2]
        max_display = 1200
        if max(display_h, display_w) > max_display:
            scale = max_display / max(display_h, display_w)
            display_h = int(display_h * scale)
            display_w = int(display_w * scale)
            display_img = cv2.resize(current_img, (display_w, display_h))
            scale_factor = scale
        else:
            display_img = current_img.copy()
            scale_factor = 1.0
        
        # Reset points
        points = []
        
        # Instructions overlay
        overlay = display_img.copy()
        cv2.putText(overlay, f"Image {i}/{len(image_paths)}: {img_path.name}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(overlay, "Click 4 corners around apple", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        display_img = overlay.copy()
        
        cv2.imshow(window_name, display_img)
        
        # Wait for user input
        while True:
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('\r') or key == ord('\n'):  # Enter
                if len(points) == 4:
                    # Scale points back to original image size
                    original_points = [(int(x/scale_factor), int(y/scale_factor)) 
                                      for x, y in points]
                    
                    # Get crop rectangle
                    crop_coords = get_crop_rectangle(original_points)
                    
                    # Crop original image
                    cropped = crop_image(current_img, crop_coords)
                    
                    # Save cropped image
                    output_path = OUTPUT_DIR / img_path.name
                    cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
                    cropped_pil.save(output_path)
                    
                    # Save coordinates
                    crop_data[img_path.name] = {
                        'points': original_points,
                        'rectangle': crop_coords
                    }
                    
                    with open(CROPS_FILE, 'w') as f:
                        json.dump(crop_data, f, indent=2)
                    
                    print(f"  ✅ Saved cropped image: {cropped.shape[1]}x{cropped.shape[0]} pixels")
                    completed += 1
                    break
                else:
                    print("  ⚠️  Need 4 points! Currently have:", len(points))
            
            elif key == ord('r'):  # Reset
                points = []
                display_img = overlay.copy()
                cv2.imshow(window_name, display_img)
                print("  🔄 Reset points")
            
            elif key == ord('s'):  # Skip
                print(f"  ⏭️  Skipped")
                skipped += 1
                break
            
            elif key == ord('q'):  # Quit
                print("\n👋 Quitting...")
                cv2.destroyAllWindows()
                return
    
    cv2.destroyAllWindows()
    
    print("\n" + "="*70)
    print("🎉 Manual Cropping Complete!")
    print("="*70)
    print(f"✅ Completed: {completed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"\n📁 Cropped images: {OUTPUT_DIR}")
    print(f"📋 Crop coordinates: {CROPS_FILE}")

if __name__ == "__main__":
    manual_crop_workflow()
