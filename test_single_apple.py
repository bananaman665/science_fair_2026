#!/usr/bin/env python3
"""
Single Apple Test - Validation Tool
Test the model's predictions on a fresh apple over multiple days
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np
from PIL import Image
import tensorflow as tf

# Paths
MODEL_PATH = Path("backend/apple_oxidation_days_model.h5")
TEST_DIR = Path("data_repository/validation_test")
RESULTS_FILE = TEST_DIR / "test_results.json"

def load_model():
    """Load the trained regression model"""
    if not MODEL_PATH.exists():
        print(f"❌ Model not found at {MODEL_PATH}")
        print("   Please train the model first: python train_regression_model.py")
        return None
    
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"✅ Model loaded: {model.count_params():,} parameters")
    return model

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return None

def predict_apple_age(model, image_path):
    """Predict days since cut for an apple photo"""
    img_array = preprocess_image(image_path)
    if img_array is None:
        return None
    
    prediction = model.predict(img_array, verbose=0)
    predicted_days = float(prediction[0][0])
    
    return predicted_days

def load_test_results():
    """Load existing test results"""
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return {
        'start_date': None,
        'apple_type': None,
        'predictions': []
    }

def save_test_results(results):
    """Save test results to JSON"""
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

def add_new_photo(image_path, actual_days, apple_type=None):
    """Add a new photo to the test"""
    
    print("\n🍎 Single Apple Validation Test")
    print("=" * 70)
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    # Load existing results
    results = load_test_results()
    
    # Initialize if first photo
    if results['start_date'] is None:
        results['start_date'] = datetime.now().strftime('%Y-%m-%d')
        results['apple_type'] = apple_type or 'unknown'
        print(f"🎬 Starting new test with {results['apple_type']} apple")
        print(f"📅 Start date: {results['start_date']}")
    
    # Make prediction
    predicted_days = predict_apple_age(model, image_path)
    
    if predicted_days is None:
        print("❌ Prediction failed")
        return
    
    # Calculate error
    error = abs(predicted_days - actual_days)
    
    # Store result
    result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'actual_days': actual_days,
        'predicted_days': round(predicted_days, 2),
        'error': round(error, 2),
        'photo': str(image_path)
    }
    
    results['predictions'].append(result)
    save_test_results(results)
    
    # Display result
    print(f"\n📸 Photo: {Path(image_path).name}")
    print(f"📅 Actual days since cut: {actual_days:.1f}")
    print(f"🤖 Model prediction: {predicted_days:.2f} days")
    print(f"📊 Error: {error:.2f} days ({abs(error * 24):.1f} hours)")
    
    # Interpretation
    if error < 0.5:
        print("✅ Excellent prediction!")
    elif error < 1.0:
        print("✅ Good prediction")
    elif error < 1.5:
        print("⚠️  Fair prediction")
    else:
        print("❌ Needs improvement")
    
    print(f"\n💾 Results saved to: {RESULTS_FILE}")

def show_summary():
    """Show summary of all test predictions"""
    
    results = load_test_results()
    
    if not results['predictions']:
        print("❌ No test results found")
        print("   Add a photo first: python test_single_apple.py add <photo_path> <days>")
        return
    
    print("\n🍎 Single Apple Validation Test - Summary")
    print("=" * 70)
    print(f"Apple Type: {results['apple_type']}")
    print(f"Start Date: {results['start_date']}")
    print(f"Total Photos: {len(results['predictions'])}")
    print()
    
    print("📊 Prediction Results:")
    print("-" * 70)
    print(f"{'Date':<12} | {'Actual':>8} | {'Predicted':>10} | {'Error':>8} | {'Status':>12}")
    print("-" * 70)
    
    errors = []
    for pred in results['predictions']:
        actual = pred['actual_days']
        predicted = pred['predicted_days']
        error = pred['error']
        errors.append(error)
        
        # Status
        if error < 0.5:
            status = "✅ Excellent"
        elif error < 1.0:
            status = "✅ Good"
        elif error < 1.5:
            status = "⚠️  Fair"
        else:
            status = "❌ Poor"
        
        date = pred['date'].split()[0]
        print(f"{date:<12} | {actual:>7.1f}d | {predicted:>9.2f}d | {error:>7.2f}d | {status}")
    
    print("-" * 70)
    
    # Statistics
    if errors:
        mean_error = np.mean(errors)
        max_error = max(errors)
        min_error = min(errors)
        
        print(f"\n📈 Statistics:")
        print(f"   Mean Absolute Error: {mean_error:.2f} days ({mean_error * 24:.1f} hours)")
        print(f"   Min Error: {min_error:.2f} days")
        print(f"   Max Error: {max_error:.2f} days")
        
        if mean_error < 0.5:
            print("\n🏆 Overall Performance: EXCELLENT!")
        elif mean_error < 1.0:
            print("\n✅ Overall Performance: GOOD")
        elif mean_error < 1.5:
            print("\n⚠️  Overall Performance: FAIR")
        else:
            print("\n❌ Overall Performance: NEEDS IMPROVEMENT")

def visualize_results():
    """Create a visualization of test results"""
    results = load_test_results()
    
    if len(results['predictions']) < 2:
        print("❌ Need at least 2 photos for visualization")
        return
    
    import matplotlib.pyplot as plt
    
    actuals = [p['actual_days'] for p in results['predictions']]
    predicted = [p['predicted_days'] for p in results['predictions']]
    
    plt.figure(figsize=(10, 6))
    
    # Plot actual vs predicted
    plt.subplot(1, 2, 1)
    plt.plot(actuals, label='Actual Days', marker='o', linewidth=2)
    plt.plot(predicted, label='Predicted Days', marker='s', linewidth=2)
    plt.xlabel('Photo Number')
    plt.ylabel('Days Since Cut')
    plt.title('Actual vs Predicted Days')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot error
    plt.subplot(1, 2, 2)
    errors = [p['error'] for p in results['predictions']]
    plt.bar(range(len(errors)), errors, color='coral')
    plt.axhline(y=0.5, color='green', linestyle='--', label='Good (<0.5d)')
    plt.axhline(y=1.0, color='orange', linestyle='--', label='Fair (<1.0d)')
    plt.xlabel('Photo Number')
    plt.ylabel('Prediction Error (days)')
    plt.title('Prediction Errors')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = TEST_DIR / 'test_results_plot.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Visualization saved to: {plot_path}")
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n🍎 Single Apple Validation Test")
        print("=" * 70)
        print("\nUsage:")
        print("  Add new photo:")
        print("    python test_single_apple.py add <photo_path> <actual_days> [apple_type]")
        print()
        print("  Show summary:")
        print("    python test_single_apple.py summary")
        print()
        print("  Visualize results:")
        print("    python test_single_apple.py plot")
        print()
        print("Example:")
        print("  Day 0: python test_single_apple.py add day0.jpg 0 gala")
        print("  Day 1: python test_single_apple.py add day1.jpg 1")
        print("  Day 2: python test_single_apple.py add day2.jpg 2")
        print("  Summary: python test_single_apple.py summary")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 4:
            print("❌ Usage: python test_single_apple.py add <photo_path> <actual_days> [apple_type]")
            sys.exit(1)
        
        photo_path = sys.argv[2]
        actual_days = float(sys.argv[3])
        apple_type = sys.argv[4] if len(sys.argv) > 4 else None
        
        add_new_photo(photo_path, actual_days, apple_type)
    
    elif command == 'summary':
        show_summary()
    
    elif command == 'plot':
        visualize_results()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("   Valid commands: add, summary, plot")
