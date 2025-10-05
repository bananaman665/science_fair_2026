#!/usr/bin/env python3
"""
Minimal TensorFlow Training - macOS Safe Version
Science Fair 2025 - Apple Oxidation Detection

Ultra-simplified training to avoid threading issues while still learning TensorFlow concepts.
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

print("🍎 Minimal TensorFlow Training Demo")
print("=" * 50)

try:
    import tensorflow as tf
    print(f"✅ TensorFlow imported successfully: v{tf.__version__}")
    
    # Force CPU-only and single-threaded
    tf.config.set_visible_devices([], 'GPU')
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(1)
    
    print("🔧 Configured for macOS stability (CPU-only, single-threaded)")
    
except Exception as e:
    print(f"❌ TensorFlow import failed: {e}")
    print("🔄 Falling back to conceptual demo...")
    exit(1)

def create_minimal_model():
    """Create the simplest possible EfficientNet model."""
    print("\n🏗️ Creating minimal EfficientNet-B0 model...")
    
    try:
        # Create a very simple model (no actual EfficientNet to avoid issues)
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(5, activation='softmax')  # 5 flower classes
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✅ Simple model created (simulating EfficientNet concepts)")
        print(f"📊 Parameters: {model.count_params():,}")
        return model
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return None

def create_dummy_data():
    """Create dummy training data."""
    print("\n📊 Creating dummy training data...")
    
    try:
        # Small dummy dataset
        batch_size = 8
        num_samples = 32
        
        # Random image data (simulating flower photos)
        images = tf.random.normal((num_samples, 224, 224, 3))
        labels = tf.random.uniform((num_samples,), maxval=5, dtype=tf.int32)
        
        # Create datasets
        dataset = tf.data.Dataset.from_tensor_slices((images, labels))
        train_ds = dataset.take(24).batch(batch_size)
        val_ds = dataset.skip(24).batch(batch_size)
        
        print(f"✅ Dummy data created: {num_samples} samples, batch size {batch_size}")
        return train_ds, val_ds
        
    except Exception as e:
        print(f"❌ Data creation failed: {e}")
        return None, None

def minimal_training():
    """Run minimal training demo."""
    print("\n🚀 Starting minimal training...")
    
    # Create model
    model = create_minimal_model()
    if not model:
        return None
    
    # Create data
    train_ds, val_ds = create_dummy_data()
    if not train_ds:
        return None
    
    try:
        print("\n🔄 Training for 2 epochs (minimal demo)...")
        
        # Very short training
        history = model.fit(
            train_ds,
            epochs=2,
            validation_data=val_ds,
            verbose=1
        )
        
        print("✅ Training completed successfully!")
        
        # Show results
        final_acc = history.history['accuracy'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        
        print(f"\n📊 Results:")
        print(f"   Training Accuracy: {final_acc:.4f}")
        print(f"   Validation Accuracy: {final_val_acc:.4f}")
        
        # Save model
        model_path = "./models/minimal_demo_model"
        os.makedirs("./models", exist_ok=True)
        model.save(model_path)
        print(f"💾 Model saved to: {model_path}")
        
        return model, history
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        print("💡 But you still learned the concepts!")
        return None, None

def main():
    """Run the minimal TensorFlow demo."""
    print("🎯 Goal: Experience actual TensorFlow training (even if simplified)")
    print("📚 Learning: Model creation, compilation, training, saving")
    print()
    
    result = minimal_training()
    
    if result[0] is not None:
        print("\n🎉 SUCCESS! You experienced real TensorFlow training!")
        print("\n🎓 What you learned:")
        print("   ✅ TensorFlow model creation")
        print("   ✅ Model compilation (optimizer, loss, metrics)")
        print("   ✅ Training loop (fit method)")
        print("   ✅ Training/validation accuracy tracking")
        print("   ✅ Model saving for deployment")
        
        print("\n🔄 For your apple project:")
        print("   - Replace dummy data with your apple images")
        print("   - Use EfficientNet-B0 instead of simple model")
        print("   - Same training process and concepts")
        
    else:
        print("\n🤔 Training didn't work, but that's OK!")
        print("You still understand all the concepts from the conceptual demo.")
        
    print("\n🚀 Ready to move on to FastAPI backend!")
    
    return result

if __name__ == "__main__":
    main()