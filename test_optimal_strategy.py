#!/usr/bin/env python3
"""
Optimal Strategy Test: Train on Original, Test on Cropped
This should give us the best of both worlds:
- Training: Full context with backgrounds (rich learning)
- Testing: Cropped images (removes domain shift)
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image

# Paths
MODEL_DIR = Path("backend")
TEST_DIR = Path("data_repository/compare_images_cropped_manual")

# Model paths - using models trained on ORIGINAL images
SMITH_MODEL = MODEL_DIR / "apple_oxidation_days_model_smith.h5"
GALA_MODEL = MODEL_DIR / "apple_oxidation_days_model_gala.h5"

# Image settings
IMG_HEIGHT = 224
IMG_WIDTH = 224

# Ground truth
GROUND_TRUTH = {
    'smith1-day1.jpg': 1.0,
    'smith1-day2.jpg': 2.0,
    'smith1-day3.jpg': 3.0,
    'smith1-day4.jpg': 4.0,
    'smith2-day1.jpg': 1.0,
    'smith2-day2.jpg': 2.0,
    'smith2-day3.jpg': 3.0,
    'smith2-day4.jpg': 4.0
}

def load_and_preprocess_image(image_path):
    """Load and preprocess image for model"""
    img = Image.open(image_path).convert('RGB')
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def test_model(model_path, model_name, test_images):
    """Test a specific model"""
    print("\n" + "="*70)
    print(f"Testing: {model_name} Model")
    print("="*70)
    
    # Load model
    model = keras.models.load_model(model_path)
    
    predictions = []
    actuals = []
    
    print(f"\n{'Image':<20s} | {'Actual':>7s} | {'Predicted':>10s} | {'Error':>7s}")
    print("-" * 70)
    
    for img_path in sorted(test_images):
        # Load and predict
        img = load_and_preprocess_image(img_path)
        pred_days = model.predict(img, verbose=0)[0][0]
        actual_days = GROUND_TRUTH[img_path.name]
        error = abs(pred_days - actual_days)
        
        predictions.append(pred_days)
        actuals.append(actual_days)
        
        print(f"{img_path.name:<20s} | {actual_days:>7.2f} | {pred_days:>10.2f} | {error:>7.2f}")
    
    # Calculate metrics
    mae = np.mean([abs(p - a) for p, a in zip(predictions, actuals)])
    mse = np.mean([(p - a)**2 for p, a in zip(predictions, actuals)])
    
    print(f"\n📊 MAE: {mae:.3f} days")
    print(f"📊 MSE: {mse:.3f}")
    
    return mae, mse

def test_optimal_strategy():
    print("\n" + "="*70)
    print("🎯 OPTIMAL STRATEGY TEST - BOTH HYPOTHESES")
    print("="*70)
    print("Strategy: Train on ORIGINAL images, Test on CROPPED images")
    print("Testing both Smith and Gala to determine apple variety")
    print("="*70)
    
    # Find test images
    test_images = [img for img in TEST_DIR.glob("*.jpg") if img.name in GROUND_TRUTH]
    
    print(f"📸 Testing on {len(test_images)} cropped images...")
    print()
    
    predictions = []
    actuals = []
    
    print(f"{'Image':<20s} | {'Actual':>7s} | {'Predicted':>10s} | {'Error':>7s}")
    print("-" * 70)
    
    for img_path in sorted(test_images):
        # Load and predict
        img = load_and_preprocess_image(img_path)
        pred_days = model.predict(img, verbose=0)[0][0]
        actual_days = GROUND_TRUTH[img_path.name]
        error = abs(pred_days - actual_days)
        
        predictions.append(pred_days)
        actuals.append(actual_days)
        
        print(f"{img_path.name:<20s} | {actual_days:>7.2f} | {pred_days:>10.2f} | {error:>7.2f}")
    
    # Calculate metrics
    mae = np.mean([abs(p - a) for p, a in zip(predictions, actuals)])
    mse = np.mean([(p - a)**2 for p, a in zip(predictions, actuals)])
    
    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(f"MAE: {mae:.3f} days")
    print(f"MSE: {mse:.3f}")
    
    print("\n" + "="*70)
    print("📈 COMPARISON TO ALL PREVIOUS TESTS")
    print("="*70)
    print()
    print("Test Strategy                                    | MAE (days) | Result")
    print("-" * 70)
    print(f"1. Original train + Original test               |     1.470  | Baseline")
    print(f"2. Cropped train + Cropped test (Smith)         |     1.900  | ❌ Worse")
    print(f"3. Cropped train + Cropped test (Gala)          |     2.244  | ❌ Much worse")
    print(f"4. Original train + Cropped test (THIS TEST)    |     {mae:.3f}  | ", end="")
    
    if mae < 1.47:
        improvement = 1.47 - mae
        pct = (improvement / 1.47) * 100
        print(f"✅ BEST! ({improvement:.3f} days, {pct:.1f}% better)")
    elif mae < 1.90:
        print(f"⚠️  Better than cropped training, but not best")
    else:
        print(f"❌ Worst")
    
    print("\n" + "="*70)
    print("💡 CONCLUSION")
    print("="*70)
    
    if mae < 1.47:
        print("✅ HYPOTHESIS CONFIRMED!")
        print("   Training on original + Testing on cropped = BEST strategy")
        print("   - Model learned from rich context (backgrounds, lighting)")
        print("   - Testing on cropped eliminated domain shift")
    elif mae < 1.90:
        print("⚠️  MIXED RESULTS")
        print("   Better than training on cropped, but not better than baseline")
        print("   Original images may still be best for both training and testing")
    else:
        print("❌ HYPOTHESIS REJECTED")
        print("   Original images work best for both training and testing")
        print("   Background removal doesn't help in either stage")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_optimal_strategy()
