#!/usr/bin/env python3
"""
Single Apple Test - Validation Tool with Variety-Specific Models
Test all three models' predictions on a fresh apple over multiple days
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import numpy as np
from PIL import Image
import tensorflow as tf

# Model paths for different varieties
MODEL_PATHS = {
    'combined': Path("backend/apple_oxidation_days_model_combined.h5"),
    'gala': Path("backend/apple_oxidation_days_model_gala.h5"),
    'smith': Path("backend/apple_oxidation_days_model_smith.h5")
}

TEST_DIR = Path("data_repository/validation_test")
RESULTS_FILE = TEST_DIR / "test_results_comparison.json"

def load_models():
    """Load all available regression models"""
    models = {}
    
    print("\n🍎 Loading Apple Oxidation Models...")
    print("=" * 70)
    
    for variety, model_path in MODEL_PATHS.items():
        if model_path.exists():
            try:
                models[variety] = tf.keras.models.load_model(model_path)
                params = models[variety].count_params()
                print(f"✅ {variety.upper():10} model loaded: {params:,} parameters")
            except Exception as e:
                print(f"❌ {variety.upper():10} failed to load: {e}")
        else:
            print(f"⚠️  {variety.upper():10} model not found")
    
    print("=" * 70)
    
    if not models:
        print("\n❌ No models loaded!")
        print("   Please train models first: python train_regression_model.py")
        return None
    
    return models

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

def predict_apple_age(models, image_path):
    """Predict days since cut for an apple photo using all models"""
    img_array = preprocess_image(image_path)
    if img_array is None:
        return None
    
    predictions = {}
    for variety, model in models.items():
        prediction = model.predict(img_array, verbose=0)
        predictions[variety] = float(prediction[0][0])
    
    return predictions

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
    
    print("\n🍎 Single Apple Validation Test - Multi-Model Comparison")
    print("=" * 70)
    
    # Load models
    models = load_models()
    if models is None:
        return
    
    # Load existing results
    results = load_test_results()
    
    # Initialize if first photo
    if results['start_date'] is None:
        results['start_date'] = datetime.now().strftime('%Y-%m-%d')
        results['apple_type'] = apple_type or 'unknown'
        print(f"🎬 Starting new test with {results['apple_type']} apple")
        print(f"📅 Start date: {results['start_date']}")
    
    # Make predictions with all models
    predictions = predict_apple_age(models, image_path)
    
    if predictions is None:
        print("❌ Prediction failed")
        return
    
    # Store result
    result = {
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'actual_days': actual_days,
        'predictions': {},
        'errors': {},
        'photo': str(image_path)
    }
    
    # Display results for each model
    print(f"\n📸 Photo: {Path(image_path).name}")
    print(f"📅 Actual days since cut: {actual_days:.1f}")
    print()
    print("🤖 Model Predictions:")
    print("-" * 70)
    print(f"{'Model':<12} | {'Predicted':>10} | {'Error':>10} | {'Status':<15}")
    print("-" * 70)
    
    for variety in ['combined', 'gala', 'smith']:
        if variety in predictions:
            predicted = predictions[variety]
            error = abs(predicted - actual_days)
            
            # Status
            if error < 0.5:
                status = "✅ Excellent"
            elif error < 1.0:
                status = "✅ Good"
            elif error < 1.5:
                status = "⚠️  Fair"
            else:
                status = "❌ Poor"
            
            result['predictions'][variety] = round(predicted, 2)
            result['errors'][variety] = round(error, 2)
            
            print(f"{variety:<12} | {predicted:>9.2f}d | {error:>9.2f}d | {status}")
        else:
            print(f"{variety:<12} | {'N/A':>10} | {'N/A':>10} | Not loaded")
    
    print("-" * 70)
    
    # Find best model
    if result['errors']:
        best_model = min(result['errors'], key=result['errors'].get)
        best_error = result['errors'][best_model]
        print(f"\n🏆 Best Model: {best_model.upper()} (error: {best_error:.2f} days)")
    
    results['predictions'].append(result)
    save_test_results(results)
    
    print(f"\n💾 Results saved to: {RESULTS_FILE}")

def show_summary():
    """Show summary of all test predictions comparing all models"""
    
    results = load_test_results()
    
    if not results['predictions']:
        print("❌ No test results found")
        print("   Add a photo first: python test_single_apple.py add <photo_path> <days>")
        return
    
    print("\n🍎 Single Apple Validation Test - Multi-Model Comparison Summary")
    print("=" * 70)
    print(f"Apple Type: {results['apple_type']}")
    print(f"Start Date: {results['start_date']}")
    print(f"Total Photos: {len(results['predictions'])}")
    print()
    
    # Collect errors for each model
    model_errors = {'combined': [], 'gala': [], 'smith': []}
    
    for pred in results['predictions']:
        actual = pred['actual_days']
        
        # Display each photo
        print(f"\n📸 Day {actual:.0f} ({Path(pred['photo']).name}):")
        print("-" * 70)
        
        for variety in ['combined', 'gala', 'smith']:
            if variety in pred.get('predictions', {}):
                predicted = pred['predictions'][variety]
                error = pred['errors'][variety]
                model_errors[variety].append(error)
                
                # Status
                if error < 0.5:
                    status = "✅ Excellent"
                elif error < 1.0:
                    status = "✅ Good"
                elif error < 1.5:
                    status = "⚠️  Fair"
                else:
                    status = "❌ Poor"
                
                print(f"  {variety:10} | Predicted: {predicted:5.2f}d | Error: {error:5.2f}d | {status}")
    
    print("\n" + "=" * 70)
    print("\n📊 OVERALL STATISTICS BY MODEL:")
    print("=" * 70)
    
    for variety in ['combined', 'gala', 'smith']:
        errors = model_errors[variety]
        
        if errors:
            mean_error = np.mean(errors)
            max_error = max(errors)
            min_error = min(errors)
            
            print(f"\n{variety.upper()} Model:")
            print(f"  Mean Absolute Error: {mean_error:.2f} days ({mean_error * 24:.1f} hours)")
            print(f"  Min Error: {min_error:.2f} days")
            print(f"  Max Error: {max_error:.2f} days")
            
            # Performance rating
            if mean_error < 0.5:
                print(f"  Performance: 🏆 EXCELLENT!")
            elif mean_error < 1.0:
                print(f"  Performance: ✅ GOOD")
            elif mean_error < 1.5:
                print(f"  Performance: ⚠️  FAIR")
            else:
                print(f"  Performance: ❌ NEEDS IMPROVEMENT")
        else:
            print(f"\n{variety.upper()} Model:")
            print(f"  No predictions available")
    
    # Find best overall model
    print("\n" + "=" * 70)
    valid_models = {v: np.mean(errs) for v, errs in model_errors.items() if errs}
    if valid_models:
        best_model = min(valid_models, key=valid_models.get)
        best_mae = valid_models[best_model]
        print(f"🏆 BEST MODEL: {best_model.upper()} (MAE: {best_mae:.2f} days)")
        
        # Show comparison
        print(f"\n📈 Model Comparison:")
        for variety, mae in sorted(valid_models.items(), key=lambda x: x[1]):
            improvement = ((max(valid_models.values()) - mae) / max(valid_models.values())) * 100
            print(f"  {variety:10} | MAE: {mae:.2f}d | {improvement:5.1f}% better than worst")

def visualize_results():
    """Create a visualization comparing all models"""
    results = load_test_results()
    
    if len(results['predictions']) < 2:
        print("❌ Need at least 2 photos for visualization")
        return
    
    import matplotlib.pyplot as plt
    
    # Collect data
    actuals = [p['actual_days'] for p in results['predictions']]
    model_preds = {
        'combined': [],
        'gala': [],
        'smith': []
    }
    
    for pred in results['predictions']:
        for variety in ['combined', 'gala', 'smith']:
            if variety in pred.get('predictions', {}):
                model_preds[variety].append(pred['predictions'][variety])
            else:
                model_preds[variety].append(None)
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: All predictions vs actual
    ax = axes[0, 0]
    ax.plot(actuals, label='Actual', marker='o', linewidth=2, markersize=8)
    colors = {'combined': 'blue', 'gala': 'green', 'smith': 'red'}
    markers = {'combined': 's', 'gala': '^', 'smith': 'v'}
    
    for variety, preds in model_preds.items():
        if any(p is not None for p in preds):
            ax.plot(preds, label=f'{variety.capitalize()}', 
                   marker=markers[variety], linewidth=2, markersize=6,
                   color=colors[variety], alpha=0.7)
    
    ax.set_xlabel('Photo Number')
    ax.set_ylabel('Days Since Cut')
    ax.set_title('All Models: Actual vs Predicted Days')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Error comparison
    ax = axes[0, 1]
    x_pos = np.arange(len(actuals))
    width = 0.25
    
    for i, (variety, color) in enumerate([('combined', 'blue'), ('gala', 'green'), ('smith', 'red')]):
        errors = []
        for pred in results['predictions']:
            if variety in pred.get('errors', {}):
                errors.append(pred['errors'][variety])
            else:
                errors.append(0)
        
        ax.bar(x_pos + i * width, errors, width, label=variety.capitalize(), 
               color=color, alpha=0.7)
    
    ax.set_xlabel('Photo Number')
    ax.set_ylabel('Absolute Error (days)')
    ax.set_title('Error Comparison by Model')
    ax.set_xticks(x_pos + width)
    ax.set_xticklabels(range(len(actuals)))
    ax.axhline(y=0.5, color='green', linestyle='--', alpha=0.5, label='Good (<0.5d)')
    ax.axhline(y=1.0, color='orange', linestyle='--', alpha=0.5, label='Fair (<1.0d)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: Mean Absolute Error by model
    ax = axes[1, 0]
    model_mae = {}
    for variety in ['combined', 'gala', 'smith']:
        errors = [p['errors'][variety] for p in results['predictions'] 
                 if variety in p.get('errors', {})]
        if errors:
            model_mae[variety] = np.mean(errors)
    
    if model_mae:
        varieties = list(model_mae.keys())
        maes = list(model_mae.values())
        colors_list = [colors[v] for v in varieties]
        
        bars = ax.bar(varieties, maes, color=colors_list, alpha=0.7)
        ax.set_ylabel('Mean Absolute Error (days)')
        ax.set_title('Overall Performance Comparison')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, mae in zip(bars, maes):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{mae:.2f}d',
                   ha='center', va='bottom')
    
    # Plot 4: Scatter plot - predicted vs actual for each model
    ax = axes[1, 1]
    for variety, color in [('combined', 'blue'), ('gala', 'green'), ('smith', 'red')]:
        actual_vals = []
        pred_vals = []
        for pred in results['predictions']:
            if variety in pred.get('predictions', {}):
                actual_vals.append(pred['actual_days'])
                pred_vals.append(pred['predictions'][variety])
        
        if actual_vals:
            ax.scatter(actual_vals, pred_vals, label=variety.capitalize(),
                      alpha=0.6, s=100, color=color)
    
    # Perfect prediction line
    max_val = max(actuals)
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Perfect')
    
    ax.set_xlabel('Actual Days')
    ax.set_ylabel('Predicted Days')
    ax.set_title('Predicted vs Actual (closer to line = better)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = TEST_DIR / 'test_results_comparison_plot.png'
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
