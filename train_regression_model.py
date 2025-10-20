#!/usr/bin/env python3
"""
Regression Model Training - Days Since Cut Prediction
Predicts continuous days of oxidation instead of discrete categories
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import json
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Paths
DATA_DIR = Path("data_repository/01_raw_images/first_collection_oct2025")
MODEL_DIR = Path("backend")
MODEL_PATH = MODEL_DIR / "apple_oxidation_days_model.h5"
METADATA_PATH = MODEL_DIR / "model_metadata_regression.json"

# Image settings
IMG_HEIGHT = 224
IMG_WIDTH = 224

def parse_photo_metadata(filename):
    """Extract days from filename"""
    # Format: gala_fruit1_day0_000h_top_down_20251005-pm.JPG
    parts = filename.replace('.JPG', '').split('_')
    
    # Handle granny_smith vs gala
    if parts[0] == 'granny':
        offset = 1
    else:
        offset = 0
    
    try:
        hours = int(parts[3 + offset].replace('h', ''))
        days = hours / 24.0  # Convert to days (continuous)
        apple_type = 'granny_smith' if parts[0] == 'granny' else parts[0]
        return days, apple_type
    except (IndexError, ValueError):
        return None, None

def load_and_preprocess_image(image_path):
    """Load and preprocess image for training"""
    try:
        # Load image
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((IMG_WIDTH, IMG_HEIGHT))
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        
        return img_array
    except Exception as e:
        print(f"❌ Error loading {image_path}: {e}")
        return None

def collect_training_data():
    """Collect all photos with their days labels"""
    
    print("\n📸 Collecting training data from photos...")
    
    images = []
    labels = []  # Days since cut (continuous)
    filenames = []
    
    for apple_type in ['gala', 'granny_smith']:
        apple_dir = DATA_DIR / apple_type
        if not apple_dir.exists():
            continue
        
        for photo_path in apple_dir.rglob("*.JPG"):
            days, apple = parse_photo_metadata(photo_path.name)
            
            if days is None:
                continue
            
            # Load and preprocess image
            img_array = load_and_preprocess_image(photo_path)
            
            if img_array is not None:
                images.append(img_array)
                labels.append(days)
                filenames.append(photo_path.name)
    
    print(f"✅ Loaded {len(images)} images")
    print(f"   Days range: {min(labels):.2f} - {max(labels):.2f}")
    
    return np.array(images), np.array(labels), filenames

def create_regression_model():
    """Create CNN model for days prediction (regression)"""
    
    model = keras.Sequential([
        # Input layer
        keras.layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        
        # Convolutional layers
        keras.layers.Conv2D(32, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        
        # Dense layers
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(64, activation='relu'),
        
        # Output layer - single neuron for regression (predicts days)
        keras.layers.Dense(1, activation='linear')  # Linear activation for continuous output
    ])
    
    # Compile with Mean Squared Error for regression
    model.compile(
        optimizer='adam',
        loss='mean_squared_error',  # MSE for regression
        metrics=['mae']  # Mean Absolute Error
    )
    
    return model

def train_model():
    """Train the regression model"""
    
    print("\n🍎 Apple Oxidation Days Prediction - Regression Training")
    print("=" * 70)
    
    # Collect data
    images, labels, filenames = collect_training_data()
    
    if len(images) == 0:
        print("❌ No training data found!")
        return
    
    # Split into train/validation sets (80/20)
    X_train, X_val, y_train, y_val = train_test_split(
        images, labels, test_size=0.2, random_state=42
    )
    
    print(f"\n📊 Dataset split:")
    print(f"   Training: {len(X_train)} images")
    print(f"   Validation: {len(X_val)} images")
    
    # Create model
    print("\n🏗️  Building regression model...")
    model = create_regression_model()
    
    print(f"   Total parameters: {model.count_params():,}")
    
    # Train model
    print("\n🚀 Training model...")
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=8,
        verbose=1
    )
    
    # Evaluate
    print("\n📊 Evaluation Results:")
    val_loss, val_mae = model.evaluate(X_val, y_val, verbose=0)
    print(f"   Validation MAE: {val_mae:.3f} days")
    print(f"   Validation MSE: {val_loss:.3f}")
    
    # Save model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model.save(MODEL_PATH)
    print(f"\n💾 Model saved to: {MODEL_PATH}")
    
    # Save metadata
    metadata = {
        'model_type': 'regression',
        'output_type': 'days_since_cut',
        'training_samples': len(X_train),
        'validation_samples': len(X_val),
        'validation_mae': float(val_mae),
        'validation_mse': float(val_loss),
        'days_range': {
            'min': float(labels.min()),
            'max': float(labels.max())
        },
        'image_size': [IMG_HEIGHT, IMG_WIDTH],
        'parameters': model.count_params()
    }
    
    with open(METADATA_PATH, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Metadata saved to: {METADATA_PATH}")
    
    # Plot training history
    plot_training_history(history)
    
    # Test predictions on validation set
    print("\n🔍 Sample Predictions:")
    print("-" * 70)
    print(f"{'Actual Days':>12} | {'Predicted Days':>15} | {'Error':>10}")
    print("-" * 70)
    
    # Show first 10 validation predictions
    predictions = model.predict(X_val[:10], verbose=0)
    for i in range(min(10, len(y_val))):
        actual = y_val[i]
        predicted = predictions[i][0]
        error = abs(actual - predicted)
        print(f"{actual:12.2f} | {predicted:15.2f} | {error:10.2f}")
    
    print("\n✅ Training complete!")
    
    return model, history

def plot_training_history(history):
    """Plot training history"""
    
    plt.figure(figsize=(12, 4))
    
    # Plot MAE
    plt.subplot(1, 2, 1)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error (days)')
    plt.title('Model MAE Over Time')
    plt.legend()
    plt.grid(True)
    
    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error')
    plt.title('Model Loss Over Time')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = MODEL_DIR / 'training_history_regression.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Training plot saved to: {plot_path}")
    
    plt.close()

if __name__ == "__main__":
    print("🍎 Apple Oxidation Days Prediction Model")
    print("Trains a regression model to predict days since apple was cut")
    print()
    
    train_model()
    
    print("\n🎯 Next Steps:")
    print("  1. Update FastAPI backend to use regression model")
    print("  2. API will return: 'This apple was cut X.X days ago'")
    print("  3. Much more useful than category labels!")
