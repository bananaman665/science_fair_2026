#!/usr/bin/env python3
"""
Optimal Strategy Test: Train on Original, Test on Cropped
Tests BOTH hypotheses: Smith vs Gala
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image

# Paths
MODEL_DIR = Path("backend")
TEST_DIR = Path("data_repository/compare_images_cropped_manual")

# Model paths
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
    print(f"\nTesting: {model_name} Model")
    print("-" * 70)
    
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
    
    print(f"\n📊 MAE: {mae:.3f} days | MSE: {mse:.3f}")
    
    return mae, mse

def main():
    print("\n" + "="*70)
    print("🎯 OPTIMAL STRATEGY TEST - BOTH HYPOTHESES")
    print("="*70)
    print("Strategy: Train on ORIGINAL images, Test on CROPPED images")
    print("Testing both Smith and Gala to determine apple variety")
    print("="*70)
    
    # Find test images
    test_images = [img for img in TEST_DIR.glob("*.jpg") if img.name in GROUND_TRUTH]
    print(f"\n📸 Found {len(test_images)} test images")
    
    # Test both hypotheses
    print("\n" + "="*70)
    print("HYPOTHESIS 1: Compare images are GRANNY SMITH")
    print("="*70)
    smith_mae, smith_mse = test_model(SMITH_MODEL, "Granny Smith", test_images)
    
    print("\n" + "="*70)
    print("HYPOTHESIS 2: Compare images are GALA")
    print("="*70)
    gala_mae, gala_mse = test_model(GALA_MODEL, "Gala", test_images)
    
    # Determine winner
    print("\n" + "="*70)
    print("🎯 VARIETY DETERMINATION")
    print("="*70)
    print(f"\nGranny Smith Model: MAE = {smith_mae:.3f} days")
    print(f"Gala Model:         MAE = {gala_mae:.3f} days")
    
    if smith_mae < gala_mae:
        winner = "Granny Smith"
        winner_mae = smith_mae
        diff = gala_mae - smith_mae
    else:
        winner = "Gala"
        winner_mae = gala_mae
        diff = smith_mae - gala_mae
    
    print(f"\n✅ WINNER: Compare images are likely {winner.upper()}")
    print(f"   ({winner} model performed {diff:.3f} days better)")
    
    # Compare to baseline
    print("\n" + "="*70)
    print("📈 COMPARISON TO BASELINE")
    print("="*70)
    print(f"\nOriginal test (uncropped):     MAE = 1.470 days")
    print(f"Optimal strategy ({winner}):   MAE = {winner_mae:.3f} days")
    
    if winner_mae < 1.47:
        improvement = 1.47 - winner_mae
        pct = (improvement / 1.47) * 100
        print(f"\n✅ IMPROVEMENT: {improvement:.3f} days better ({pct:.1f}% improvement)")
    else:
        print(f"\n❌ No improvement over baseline")
    
    print("\n" + "="*70)
    print("📊 COMPLETE RESULTS TABLE")
    print("="*70)
    print()
    print("Test Strategy                                    | MAE (days) | Result")
    print("-" * 70)
    print(f"1. Original train + Original test (baseline)    |     1.470  | Baseline")
    print(f"2. Cropped train + Cropped test (Smith)         |     1.900  | ❌ Worse")
    print(f"3. Cropped train + Cropped test (Gala)          |     2.244  | ❌ Much worse")
    print(f"4. Original train + Cropped test (Smith)        |     {smith_mae:.3f}  | {'✅ BEST!' if smith_mae == winner_mae and winner_mae < 1.47 else ('✅ Good' if smith_mae < 1.47 else '❌')}")
    print(f"5. Original train + Cropped test (Gala)         |     {gala_mae:.3f}  | {'✅ BEST!' if gala_mae == winner_mae and winner_mae < 1.47 else ('✅ Good' if gala_mae < 1.47 else '❌')}")
    
    print("\n" + "="*70)
    print("💡 FINAL CONCLUSION")
    print("="*70)
    
    if winner_mae < 1.47:
        print(f"✅ HYPOTHESIS CONFIRMED!")
        print(f"   - Compare images are {winner} apples")
        print(f"   - Training on original + Testing on cropped = BEST strategy")
        print(f"   - Improvement: {((1.47 - winner_mae) / 1.47 * 100):.1f}% better than baseline")
        print(f"\n🎓 Scientific Finding: Domain shift solved!")
        print(f"   - Background differences were the problem (not noise in training)")
        print(f"   - Solution: Keep rich training context, preprocess test images")
    else:
        print(f"⚠️ No improvement over baseline found")
        print(f"   Cropping does not help in this case")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
