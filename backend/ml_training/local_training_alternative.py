#!/usr/bin/env python3
"""
Lightweight Training Alternative - CPU-Optimized
Science Fair 2025 - Apple Oxidation Detection

This script provides a simpler training approach that works reliably
on macOS without the threading issues we encountered.
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# Disable GPU to avoid threading issues on macOS
tf.config.set_visible_devices([], 'GPU')

print("🍎 Local Training Alternative - CPU Optimized")
print("=" * 50)
print(f"TensorFlow version: {tf.__version__}")
print(f"Running on: CPU only (macOS optimized)")
print()

def create_mock_dataset():
    """Create a small mock dataset for quick training demonstration."""
    
    # Create synthetic data similar to flower classification
    # 4 classes for apple oxidation: Fresh, Light, Medium, Heavy
    num_classes = 4
    samples_per_class = 50  # Small dataset for quick training
    img_size = 64  # Smaller images for faster processing
    
    print(f"📊 Creating mock dataset:")
    print(f"   Classes: 4 (Fresh, Light, Medium, Heavy)")
    print(f"   Samples per class: {samples_per_class}")
    print(f"   Image size: {img_size}x{img_size}")
    print(f"   Total samples: {num_classes * samples_per_class}")
    
    # Generate synthetic images with different characteristics
    images = []
    labels = []
    
    for class_id in range(num_classes):
        for sample in range(samples_per_class):
            # Create synthetic image with class-specific characteristics
            base_color = [0.2 + class_id * 0.2, 0.8 - class_id * 0.15, 0.1 + class_id * 0.1]
            
            # Add some randomness
            image = np.random.normal(base_color, 0.1, (img_size, img_size, 3))
            image = np.clip(image, 0, 1)
            
            images.append(image)
            labels.append(class_id)
    
    # Convert to arrays
    images = np.array(images, dtype=np.float32)
    labels = np.array(labels, dtype=np.int32)
    
    # Shuffle the data
    indices = np.random.permutation(len(images))
    images = images[indices]
    labels = labels[indices]
    
    # Split into train/validation
    split_point = int(0.8 * len(images))
    train_images = images[:split_point]
    train_labels = labels[:split_point]
    val_images = images[split_point:]
    val_labels = labels[split_point:]
    
    print(f"   Training samples: {len(train_images)}")
    print(f"   Validation samples: {len(val_images)}")
    print()
    
    return (train_images, train_labels), (val_images, val_labels)

def create_simple_model(input_shape, num_classes):
    """Create a simple CNN model for quick training."""
    
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    """Train a simple model to demonstrate the complete pipeline."""
    
    print("🚀 Starting Local Training...")
    
    # Create dataset
    (train_images, train_labels), (val_images, val_labels) = create_mock_dataset()
    
    # Create model
    model = create_simple_model((64, 64, 3), 4)
    
    print("🏗️ Model Architecture:")
    model.summary()
    print()
    
    # Training callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            patience=5, 
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            factor=0.5, 
            patience=3,
            verbose=1
        )
    ]
    
    print("🔥 Training Model...")
    start_time = datetime.now()
    
    # Train the model
    history = model.fit(
        train_images, train_labels,
        batch_size=16,
        epochs=20,
        validation_data=(val_images, val_labels),
        callbacks=callbacks,
        verbose=1
    )
    
    training_time = (datetime.now() - start_time).total_seconds()
    
    # Evaluate
    val_loss, val_accuracy = model.evaluate(val_images, val_labels, verbose=0)
    
    print(f"\n✅ Training Complete!")
    print(f"   Training time: {training_time:.1f} seconds")
    print(f"   Final validation accuracy: {val_accuracy:.4f}")
    print(f"   Final validation loss: {val_loss:.4f}")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"local_model_{timestamp}"
    
    model.save(model_path)
    
    # Save metadata
    metadata = {
        "model_name": f"local_apple_demo_{timestamp}",
        "timestamp": timestamp,
        "architecture": "Simple CNN",
        "num_classes": 4,
        "class_names": ["Fresh", "Light", "Medium", "Heavy"],
        "img_size": 64,
        "training_time_seconds": training_time,
        "final_accuracy": float(val_accuracy),
        "epochs_trained": len(history.history['accuracy'])
    }
    
    with open(f"{model_path}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n💾 Model Saved!")
    print(f"   Path: {model_path}")
    print(f"   Metadata: {model_path}/metadata.json")
    print(f"   Training plot: training_results.png")
    
    return model, history, metadata

def test_inference(model):
    """Test model inference with sample data."""
    
    print("\n🧪 Testing Model Inference...")
    
    # Create a test image
    test_image = np.random.random((1, 64, 64, 3)).astype(np.float32)
    
    # Make prediction
    start_time = datetime.now()
    predictions = model.predict(test_image, verbose=0)
    inference_time = (datetime.now() - start_time).total_seconds() * 1000
    
    # Extract results
    predicted_class_idx = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    
    class_names = ["Fresh", "Light", "Medium", "Heavy"]
    predicted_class = class_names[predicted_class_idx]
    
    print(f"   Predicted class: {predicted_class}")
    print(f"   Confidence: {confidence:.4f}")
    print(f"   Inference time: {inference_time:.1f}ms")
    
    # Show API-style response
    api_response = {
        "analysis_id": f"local_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "predicted_class": predicted_class,
        "oxidation_score": predicted_class_idx * 25,  # 0, 25, 50, 75
        "confidence": confidence,
        "processing_time_ms": int(inference_time),
        "timestamp": datetime.now().isoformat(),
        "all_probabilities": {
            class_names[i]: float(predictions[0][i]) 
            for i in range(len(class_names))
        }
    }
    
    print(f"\n📱 FastAPI Response Format:")
    print(json.dumps(api_response, indent=2))
    
    return api_response

if __name__ == "__main__":
    print("🎯 This demonstrates the complete ML pipeline locally on macOS")
    print("   - Dataset creation and preprocessing")
    print("   - Model training with progress monitoring")
    print("   - Evaluation and visualization")
    print("   - Model saving and metadata")
    print("   - Inference testing")
    print()
    print("⚡ Advantages of this approach:")
    print("   ✅ Reliable (no connection issues)")
    print("   ✅ Fast (optimized for CPU)")
    print("   ✅ Educational (see every step)")
    print("   ✅ Ready for FastAPI integration")
    print()
    
    # Run the complete pipeline
    model, history, metadata = train_model()
    test_inference(model)
    
    print("\n🎉 Local Training Complete!")
    print("   You now have a working model trained locally on your Mac!")
    print("   This same process will work with your real apple images.")