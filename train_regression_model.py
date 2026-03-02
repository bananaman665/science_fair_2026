#!/usr/bin/env python3
"""
Regression Model Training - Days Since Cut Prediction
Predicts continuous days of oxidation instead of discrete categories
SUPPORTS VARIETY-SPECIFIC MODELS: gala, smith, red_delicious, combined
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
import json
import io
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Paths - Second collection November 2024 (3 varieties)
DATA_DIR = Path("data_repository/01_raw_images/second_collection_nov2024")
MODEL_DIR = Path("backend")

# Model paths for different varieties (4 models total)
MODEL_PATHS = {
    'combined': MODEL_DIR / "apple_oxidation_days_model_combined.h5",
    'gala': MODEL_DIR / "apple_oxidation_days_model_gala.h5",
    'smith': MODEL_DIR / "apple_oxidation_days_model_smith.h5",
    'red_delicious': MODEL_DIR / "apple_oxidation_days_model_red_delicious.h5"
}

METADATA_PATHS = {
    'combined': MODEL_DIR / "model_metadata_regression_combined.json",
    'gala': MODEL_DIR / "model_metadata_regression_gala.json",
    'smith': MODEL_DIR / "model_metadata_regression_smith.json",
    'red_delicious': MODEL_DIR / "model_metadata_regression_red_delicious.json"
}

# Image settings
IMG_HEIGHT = 224
IMG_WIDTH = 224


def phone_augment(img_array):
    """
    Apply random augmentations to simulate phone camera conditions.
    Takes a normalized numpy array (0-1, shape 224x224x3), applies random
    transformations, returns augmented array in same format.
    """
    # Convert back to PIL Image for augmentation (0-255 uint8)
    img = Image.fromarray((img_array * 255).astype(np.uint8))

    # 1. Brightness shift (±30%)
    factor = np.random.uniform(0.7, 1.3)
    img = ImageEnhance.Brightness(img).enhance(factor)

    # 2. Contrast shift (±30%)
    factor = np.random.uniform(0.7, 1.3)
    img = ImageEnhance.Contrast(img).enhance(factor)

    # 3. Color temperature - random per-channel scaling to simulate warm/cool lighting
    arr = np.array(img, dtype=np.float32)
    r_scale = np.random.uniform(0.85, 1.15)
    g_scale = np.random.uniform(0.90, 1.10)
    b_scale = np.random.uniform(0.85, 1.15)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * r_scale, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] * g_scale, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * b_scale, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8))

    # 4. Gaussian blur (0-1.5px radius)
    radius = np.random.uniform(0, 1.5)
    if radius > 0.3:  # skip very small blurs
        img = img.filter(ImageFilter.GaussianBlur(radius=radius))

    # 5. Horizontal flip (50% chance)
    if np.random.random() > 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    # 6. Rotation (±15 degrees)
    angle = np.random.uniform(-15, 15)
    if abs(angle) > 1:
        img = img.rotate(angle, resample=Image.BILINEAR, fillcolor=(0, 0, 0))

    # 7. JPEG compression (quality 50-95%)
    quality = np.random.randint(50, 96)
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=quality)
    buffer.seek(0)
    img = Image.open(buffer).convert('RGB')

    # 8. Gaussian noise (sigma 0-15)
    arr = np.array(img, dtype=np.float32)
    sigma = np.random.uniform(0, 15)
    noise = np.random.normal(0, sigma, arr.shape)
    arr = np.clip(arr + noise, 0, 255)

    # Convert back to normalized array (0-1)
    return arr.astype(np.float32) / 255.0


class AugmentedDataGenerator(keras.utils.Sequence):
    """
    Custom data generator that applies phone_augment() on-the-fly.
    Each epoch, every training image gets a fresh random augmentation,
    so the model sees thousands of variations over the full training run.
    """

    def __init__(self, images, labels, batch_size=8, augment=True):
        self.images = images
        self.labels = labels
        self.batch_size = batch_size
        self.augment = augment
        self.indices = np.arange(len(images))

    def __len__(self):
        return int(np.ceil(len(self.images) / self.batch_size))

    def __getitem__(self, idx):
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_images = []
        batch_labels = self.labels[batch_indices]

        for i in batch_indices:
            img = self.images[i]
            if self.augment:
                img = phone_augment(img)
            batch_images.append(img)

        return np.array(batch_images), batch_labels

    def on_epoch_end(self):
        np.random.shuffle(self.indices)


def parse_photo_metadata(filename):
    """Extract days from filename"""
    # Format: gala_fruit1_day0_000h_top_down_20241101-am.JPG
    # Format: granny_smith_fruit1_day0_000h_top_down_20241101-am.JPG
    # Format: red_delicious_fruit1_day0_000h_top_down_20241101-am.JPG
    parts = filename.replace('.JPG', '').split('_')

    # Handle multi-word apple types (granny_smith, red_delicious)
    if parts[0] == 'granny':
        offset = 1
        apple_type = 'granny_smith'
    elif parts[0] == 'red':
        offset = 1
        apple_type = 'red_delicious'
    else:
        offset = 0
        apple_type = parts[0]

    try:
        hours = int(parts[3 + offset].replace('h', ''))
        days = hours / 24.0  # Convert to days (continuous)
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

def collect_training_data(variety_filter=None):
    """
    Collect all photos with their days labels

    Args:
        variety_filter: 'gala', 'smith', 'red_delicious', or None for all
    """

    print(f"\n📸 Collecting training data from photos...")
    if variety_filter:
        print(f"   Filtering for: {variety_filter}")
    else:
        print(f"   Using ALL varieties (combined model)")

    images = []
    labels = []  # Days since cut (continuous)
    filenames = []

    # All three apple varieties in new collection
    all_varieties = ['gala', 'granny_smith', 'red_delicious']

    # Map variety filter to directory name
    variety_to_dir = {
        'gala': 'gala',
        'smith': 'granny_smith',
        'red_delicious': 'red_delicious'
    }

    for apple_type in all_varieties:
        # Skip if filtering and this isn't the target variety
        if variety_filter:
            target_dir = variety_to_dir.get(variety_filter)
            if apple_type != target_dir:
                continue

        apple_dir = DATA_DIR / apple_type
        if not apple_dir.exists():
            print(f"   ⚠️  Directory not found: {apple_dir}")
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

        # Show count per variety
        variety_count = sum(1 for f in filenames if f.startswith(apple_type.replace('_', ' ').split()[0]))
        print(f"   📁 {apple_type}: loaded images from {apple_dir}")

    print(f"✅ Loaded {len(images)} images total")
    if len(labels) > 0:
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

def train_model(variety='combined'):
    """
    Train the regression model for a specific variety

    Args:
        variety: 'combined', 'gala', 'smith', or 'red_delicious'
    """

    variety_names = {
        'combined': 'All Varieties (Gala, Granny Smith, Red Delicious)',
        'gala': 'Gala Apples Only',
        'smith': 'Granny Smith Apples Only',
        'red_delicious': 'Red Delicious Apples Only'
    }
    
    print("\n🍎 Apple Oxidation Days Prediction - Regression Training")
    print("=" * 70)
    print(f"   Training model: {variety_names.get(variety, variety)}")
    print("=" * 70)
    
    # Collect data with variety filter
    variety_filter = None if variety == 'combined' else variety
    images, labels, filenames = collect_training_data(variety_filter)
    
    if len(images) == 0:
        print("❌ No training data found!")
        return None, None
    
    # Split into train/validation sets (80/20)
    X_train, X_val, y_train, y_val = train_test_split(
        images, labels, test_size=0.2, random_state=42
    )
    
    print(f"\n📊 Dataset split:")
    print(f"   Training: {len(X_train)} images")
    print(f"   Validation: {len(X_val)} images")

    # Create augmented data generator for training
    # Validation data is NOT augmented - we want to measure real accuracy
    train_gen = AugmentedDataGenerator(X_train, y_train, batch_size=8, augment=True)
    print(f"   Augmentation: ENABLED (phone simulation)")
    print(f"   Each image gets random brightness, contrast, color temp, blur,")
    print(f"   noise, JPEG compression, rotation, and flip per epoch")

    # Create model
    print("\n🏗️  Building regression model...")
    model = create_regression_model()

    print(f"   Total parameters: {model.count_params():,}")

    # Train model - more epochs since augmentation makes learning harder
    print("\n🚀 Training model with augmentation...")

    history = model.fit(
        train_gen,
        validation_data=(X_val, y_val),
        epochs=80,
        verbose=1
    )
    
    # Evaluate
    print("\n📊 Evaluation Results:")
    val_loss, val_mae = model.evaluate(X_val, y_val, verbose=0)
    print(f"   Validation MAE: {val_mae:.3f} days")
    print(f"   Validation MSE: {val_loss:.3f}")
    
    # Save model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_PATHS[variety]
    model.save(model_path)
    print(f"\n💾 Model saved to: {model_path}")
    
    # Save metadata
    metadata = {
        'model_type': 'regression',
        'variety': variety,
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
        'parameters': model.count_params(),
        'augmentation': 'phone_simulation',
        'augmentation_types': [
            'brightness', 'contrast', 'color_temperature',
            'gaussian_blur', 'horizontal_flip', 'rotation',
            'jpeg_compression', 'gaussian_noise'
        ]
    }
    
    metadata_path = METADATA_PATHS[variety]
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Metadata saved to: {metadata_path}")
    
    # Plot training history
    plot_training_history(history, variety)
    
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
    
    print(f"\n✅ Training complete for {variety} model!")
    
    return model, history

def plot_training_history(history, variety='combined'):
    """Plot training history"""
    
    plt.figure(figsize=(12, 4))
    
    # Plot MAE
    plt.subplot(1, 2, 1)
    plt.plot(history.history['mae'], label='Training MAE')
    plt.plot(history.history['val_mae'], label='Validation MAE')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error (days)')
    plt.title(f'Model MAE Over Time ({variety})')
    plt.legend()
    plt.grid(True)
    
    # Plot Loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error')
    plt.title(f'Model Loss Over Time ({variety})')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = MODEL_DIR / f'training_history_regression_{variety}.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Training plot saved to: {plot_path}")
    
    plt.close()

if __name__ == "__main__":
    print("🍎 Apple Oxidation Days Prediction Model - Variety-Specific Training")
    print("Trains regression models to predict days since apple was cut")
    print("Data: Second Collection November 2024 (3 apple varieties)")
    print()

    import sys

    ALL_VARIETIES = ['combined', 'gala', 'smith', 'red_delicious']

    # Check if user wants specific variety
    if len(sys.argv) > 1:
        variety = sys.argv[1].lower()
        if variety not in ALL_VARIETIES:
            print(f"❌ Unknown variety: {variety}")
            print(f"   Usage: python train_regression_model.py [{' | '.join(ALL_VARIETIES)}]")
            print("   Or run without args to train all four models")
            sys.exit(1)

        print(f"Training single model: {variety}")
        train_model(variety)
    else:
        # Train all four models
        print(f"Training ALL FOUR models: {', '.join(ALL_VARIETIES)}")
        print("=" * 70)

        for variety in ALL_VARIETIES:
            print(f"\n\n{'='*70}")
            print(f"STARTING: {variety.upper()} MODEL")
            print(f"{'='*70}\n")

            train_model(variety)

            print(f"\n{'='*70}")
            print(f"COMPLETED: {variety.upper()} MODEL")
            print(f"{'='*70}\n")

    print("\n🎯 Training Complete!")
    print("\n📊 Models saved:")
    for variety, path in MODEL_PATHS.items():
        exists = "✅" if path.exists() else "❌"
        print(f"   {exists} {variety}: {path}")
