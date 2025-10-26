#!/usr/bin/env python3
"""
Test Both Hypotheses: Are the compare images Granny Smith or Gala?
Tests cropped images against both variety-specific models
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from PIL import Image
import json

# Paths
MODEL_DIR = Path("backend")
TEST_DIR = Path("data_repository/compare_images_cropped_manual")

# Model paths
SMITH_MODEL = MODEL_DIR / "apple_oxidation_days_model_smith.h5"
GALA_MODEL = MODEL_DIR / "apple_oxidation_days_model_gala.h5"

# Image settings
IMG_HEIGHT = 224
IMG_WIDTH = 224

# Ground truth labels for test images
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

def calculate_metrics(predictions, actuals):
    """Calculate MAE and MSE"""
    errors = [abs(p - a) for p, a in zip(predictions, actuals)]
    mae = np.mean(errors)
    mse = np.mean([e**2 for e in errors])
    return mae, mse, errors

def test_model(model_path, model_name, test_images):
    """Test a model on test images"""
    print(f"\n{'='*70}")
    print(f"Testing: {model_name} Model")
    print(f"{'='*70}")
    
    # Load model
    model = keras.models.load_model(model_path)
    
    predictions = []
    actuals = []
    results = []
    
    print("\n📸 Processing test images...")
    for img_path in sorted(test_images):
        # Load image
        img = load_and_preprocess_image(img_path)
        
        # Predict
        pred_days = model.predict(img, verbose=0)[0][0]
        actual_days = GROUND_TRUTH[img_path.name]
        error = abs(pred_days - actual_days)
        
        predictions.append(pred_days)
        actuals.append(actual_days)
        results.append({
            'filename': img_path.name,
            'actual': actual_days,
            'predicted': pred_days,
            'error': error
        })
        
        print(f"  {img_path.name:20s} | Actual: {actual_days:.2f} | Predicted: {pred_days:.2f} | Error: {error:.2f}")
    
    # Calculate metrics
    mae, mse, errors = calculate_metrics(predictions, actuals)
    
    print(f"\n📊 Results:")
    print(f"   MAE: {mae:.3f} days")
    print(f"   MSE: {mse:.3f}")
    print(f"   Min Error: {min(errors):.3f} days")
    print(f"   Max Error: {max(errors):.3f} days")
    
    return {
        'model': model_name,
        'mae': mae,
        'mse': mse,
        'results': results
    }

def main():
    print("\n🍎 Cropped Images Hypothesis Testing")
    print("="*70)
    print("Testing both hypotheses:")
    print("  1. Compare images are Granny Smith apples")
    print("  2. Compare images are Gala apples")
    print("="*70)
    
    # Find test images
    test_images = list(TEST_DIR.glob("*.jpg")) + list(TEST_DIR.glob("*.JPG"))
    test_images = [img for img in test_images if img.name in GROUND_TRUTH]
    
    if not test_images:
        print(f"❌ No test images found in {TEST_DIR}")
        return
    
    print(f"\n📸 Found {len(test_images)} test images")
    
    # Test Hypothesis 1: Granny Smith
    smith_results = test_model(SMITH_MODEL, "Granny Smith", test_images)
    
    # Test Hypothesis 2: Gala
    gala_results = test_model(GALA_MODEL, "Gala", test_images)
    
    # Compare results
    print("\n" + "="*70)
    print("🎯 COMPARISON SUMMARY")
    print("="*70)
    print(f"\nHypothesis 1 (Granny Smith): MAE = {smith_results['mae']:.3f} days")
    print(f"Hypothesis 2 (Gala):         MAE = {gala_results['mae']:.3f} days")
    
    if smith_results['mae'] < gala_results['mae']:
        winner = "Granny Smith"
        diff = gala_results['mae'] - smith_results['mae']
        print(f"\n✅ WINNER: Compare images are likely {winner}")
        print(f"   {winner} model performed {diff:.3f} days better")
    else:
        winner = "Gala"
        diff = smith_results['mae'] - gala_results['mae']
        print(f"\n✅ WINNER: Compare images are likely {winner}")
        print(f"   {winner} model performed {diff:.3f} days better")
    
    # Save results
    results_file = Path("cropped_hypothesis_test_results.json")
    with open(results_file, 'w') as f:
        json.dump({
            'granny_smith': smith_results,
            'gala': gala_results,
            'winner': winner
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: {results_file}")
    
    print("\n" + "="*70)
    print("🔍 COMPARISON TO ORIGINAL (UNCROPPED) RESULTS")
    print("="*70)
    print("\nOriginal test (uncropped images, Smith model): MAE = 1.47 days")
    print(f"New test (cropped images, Smith model):       MAE = {smith_results['mae']:.3f} days")
    
    if smith_results['mae'] < 1.47:
        improvement = 1.47 - smith_results['mae']
        pct = (improvement / 1.47) * 100
        print(f"\n✅ IMPROVEMENT: {improvement:.3f} days better ({pct:.1f}% improvement)")
        print("   Cropping backgrounds DID help!")
    else:
        degradation = smith_results['mae'] - 1.47
        pct = (degradation / 1.47) * 100
        print(f"\n❌ DEGRADATION: {degradation:.3f} days worse ({pct:.1f}% worse)")
        print("   Cropping backgrounds did NOT help")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
