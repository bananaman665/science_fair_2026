#!/usr/bin/env python3
"""
Ultra-fast local apple training script
Should complete in under 5 minutes on most machines
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

def main():
    print(f"🚀 Starting local training: {datetime.now().strftime('%H:%M:%S')}")
    
    # Check TensorFlow setup
    print(f"TensorFlow: {tf.__version__}")
    gpus = tf.config.list_physical_devices('GPU')
    print(f"GPUs available: {len(gpus)}")
    if gpus:
        print(f"GPU: {gpus[0].name}")
    
    # Use CPU-optimized settings
    tf.config.threading.set_intra_op_parallelism_threads(0)  # Use all cores
    tf.config.threading.set_inter_op_parallelism_threads(0)
    
    # Download tiny dataset (much faster than flowers)
    print("📁 Creating synthetic apple dataset...")
    
    # Create synthetic data instead of downloading
    IMG_SIZE = 128  # Even smaller for speed
    NUM_SAMPLES = 200  # Tiny dataset
    NUM_CLASSES = 4  # apple states
    
    # Generate synthetic images (much faster than downloading)
    np.random.seed(42)
    X = np.random.rand(NUM_SAMPLES, IMG_SIZE, IMG_SIZE, 3).astype(np.float32)
    y = np.random.randint(0, NUM_CLASSES, NUM_SAMPLES)
    
    # Add some pattern to make classes distinguishable
    for i in range(NUM_SAMPLES):
        class_id = y[i]
        # Add class-specific color bias
        if class_id == 0:  # Fresh - more green
            X[i, :, :, 1] += 0.3
        elif class_id == 1:  # Light oxidation - slight brown
            X[i, :, :, 0] += 0.2
            X[i, :, :, 1] += 0.1
        elif class_id == 2:  # Medium oxidation - more brown
            X[i, :, :, 0] += 0.4
            X[i, :, :, 1] += 0.2
        else:  # Heavy oxidation - very brown/dark
            X[i, :, :, 0] += 0.2
    
    # Normalize
    X = np.clip(X, 0, 1)
    
    # Split data
    split_idx = int(0.8 * NUM_SAMPLES)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    class_names = ['fresh', 'light_oxidation', 'medium_oxidation', 'heavy_oxidation']
    print(f"✅ Dataset ready: {len(X_train)} train, {len(X_val)} val samples")
    
    # Create simple CNN (no transfer learning for speed)
    print("🔧 Building lightweight CNN...")
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(16, 3, activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(2),
        tf.keras.layers.Conv2D(64, 3, activation='relu'),
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"Model parameters: {model.count_params():,}")
    
    # Super fast training
    print("⚡ Starting training...")
    start_time = datetime.now()
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        batch_size=32,
        verbose=1
    )
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"✅ Training completed in: {duration}")
    
    # Save model
    model_name = f'apple_model_local_{datetime.now().strftime("%H%M")}.h5'
    model.save(model_name)
    print(f"💾 Model saved: {model_name}")
    
    # Quick evaluation
    final_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    print(f"🎯 Final training accuracy: {final_acc:.3f}")
    print(f"🎯 Final validation accuracy: {final_val_acc:.3f}")
    
    # Plot results
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], 'b-', label='Training')
    plt.plot(history.history['val_accuracy'], 'r-', label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], 'b-', label='Training')
    plt.plot(history.history['val_loss'], 'r-', label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Test predictions
    print("🧪 Testing predictions...")
    test_predictions = model.predict(X_val[:4], verbose=0)
    predicted_classes = np.argmax(test_predictions, axis=1)
    
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for i in range(4):
        axes[i].imshow(X_val[i])
        true_class = class_names[y_val[i]]
        pred_class = class_names[predicted_classes[i]]
        confidence = test_predictions[i][predicted_classes[i]]
        
        color = 'green' if y_val[i] == predicted_classes[i] else 'red'
        axes[i].set_title(f'True: {true_class}\\nPred: {pred_class}\\n({confidence:.2f})', 
                         color=color, fontsize=10)
        axes[i].axis('off')
    
    plt.suptitle('Sample Predictions')
    plt.tight_layout()
    plt.savefig('predictions.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Save metadata
    import json
    metadata = {
        'class_names': class_names,
        'model_info': {
            'architecture': 'Simple CNN',
            'input_size': IMG_SIZE,
            'parameters': model.count_params(),
            'training_duration': str(duration),
            'final_accuracy': float(final_val_acc)
        }
    }
    
    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\\n🎉 Local training completed successfully!")
    print(f"📁 Files created:")
    print(f"   • {model_name} (trained model)")
    print(f"   • model_metadata.json (model info)")
    print(f"   • training_results.png (training plots)")
    print(f"   • predictions.png (sample predictions)")
    print(f"\\n⚡ Total time: {duration}")
    print(f"🎯 Final accuracy: {final_val_acc:.1%}")

if __name__ == "__main__":
    main()