#!/usr/bin/env python3
"""
Simple EfficientNet-B0 Training Demo (macOS Optimized)
Science Fair 2025 - Apple Oxidation Detection

Simplified version to avoid macOS threading issues while learning the concepts.
"""

import os
# macOS stability settings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['OMP_NUM_THREADS'] = '1'

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Configure TensorFlow for macOS
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.set_visible_devices([], 'GPU')  # Use CPU only for stability

print("🍎 Simple EfficientNet-B0 Training Demo")
print("=" * 50)
print("macOS Optimized Version - Learning Transfer Learning Concepts")
print("=" * 50)

def create_simple_model():
    """Create a simple EfficientNet-B0 model for demonstration."""
    print("\n🏗️ Creating EfficientNet-B0 model...")
    
    # Load pre-trained EfficientNet-B0
    base_model = tf.keras.applications.EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3)
    )
    
    # Freeze base model for transfer learning
    base_model.trainable = False
    
    # Add custom classification head
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(5, activation='softmax')  # 5 flower classes
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print(f"✅ Model created successfully!")
    print(f"📊 Total parameters: {model.count_params():,}")
    print(f"📊 Trainable parameters: {sum([tf.keras.backend.count_params(w) for w in model.trainable_weights]):,}")
    
    return model

def load_simple_dataset():
    """Load a simple subset of the flowers dataset."""
    print("\n🔄 Loading flowers dataset...")
    
    try:
        # Load flowers dataset
        (train_ds, val_ds), info = tf.keras.utils.get_file(
            'flower_photos',
            'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
            untar=True,
            cache_dir='./data'
        ), None
        
        # Create dataset from directory
        train_ds = tf.keras.utils.image_dataset_from_directory(
            './data/flower_photos',
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(224, 224),
            batch_size=8,  # Small batch for stability
            shuffle=True
        )
        
        val_ds = tf.keras.utils.image_dataset_from_directory(
            './data/flower_photos',
            validation_split=0.2,
            subset="validation", 
            seed=123,
            image_size=(224, 224),
            batch_size=8
        )
        
        # Optimize datasets
        train_ds = train_ds.cache().prefetch(tf.data.AUTOTUNE)
        val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)
        
        # Normalize images for EfficientNet
        def preprocess(image, label):
            image = tf.cast(image, tf.float32)
            image = tf.keras.applications.efficientnet.preprocess_input(image)
            return image, label
        
        train_ds = train_ds.map(preprocess)
        val_ds = val_ds.map(preprocess)
        
        print("✅ Dataset loaded successfully!")
        return train_ds, val_ds
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        print("📝 Creating dummy dataset for concept demonstration...")
        
        # Create dummy data if download fails
        def create_dummy_data():
            # Create random image data
            images = tf.random.normal((100, 224, 224, 3))
            labels = tf.random.uniform((100,), maxval=5, dtype=tf.int32)
            
            dataset = tf.data.Dataset.from_tensor_slices((images, labels))
            dataset = dataset.batch(8).cache().prefetch(tf.data.AUTOTUNE)
            
            return dataset
        
        train_ds = create_dummy_data()
        val_ds = create_dummy_data()
        
        print("✅ Dummy dataset created for learning!")
        return train_ds, val_ds

def simple_training_demo():
    """Run a simple training demonstration."""
    print("\n🚀 Starting Training Demo...")
    
    # Create model
    model = create_simple_model()
    
    # Load dataset
    train_ds, val_ds = load_simple_dataset()
    
    # Training Phase 1: Classification head only
    print("\n" + "="*40)
    print("PHASE 1: Training classification head (2 epochs)")
    print("="*40)
    
    try:
        history1 = model.fit(
            train_ds,
            epochs=2,
            validation_data=val_ds,
            verbose=1
        )
        
        print("✅ Phase 1 complete!")
        
        # Training Phase 2: Fine-tuning
        print("\n" + "="*40)
        print("PHASE 2: Fine-tuning (2 epochs)")
        print("="*40)
        
        # Unfreeze top layers
        model.layers[0].trainable = True
        for layer in model.layers[0].layers[:-10]:
            layer.trainable = False
        
        # Recompile with lower learning rate
        model.compile(
            optimizer=tf.keras.optimizers.Adam(0.0001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        history2 = model.fit(
            train_ds,
            epochs=2,
            validation_data=val_ds,
            verbose=1
        )
        
        print("✅ Phase 2 complete!")
        
        # Save model
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"./models/simple_flower_model_{timestamp}"
        os.makedirs("./models", exist_ok=True)
        model.save(model_path)
        
        print(f"\n💾 Model saved to: {model_path}")
        print("\n🎉 Training demonstration complete!")
        print("\n📚 What you learned:")
        print("- ✅ EfficientNet-B0 architecture and setup")
        print("- ✅ Transfer learning with frozen base model")
        print("- ✅ Two-phase training strategy")
        print("- ✅ Fine-tuning with lower learning rate")
        print("- ✅ Model compilation and training loop")
        print("- ✅ Model saving for deployment")
        
        print("\n🔄 Next steps:")
        print("- Replace flowers with your apple oxidation images")
        print("- Use same EfficientNet-B0 architecture")
        print("- Apply same two-phase training process")
        print("- Integrate with FastAPI backend")
        
        return model, model_path
        
    except Exception as e:
        print(f"❌ Training error: {e}")
        print("💡 This demonstrates the concepts even if training fails")
        print("   The important part is understanding the process!")
        return None, None

if __name__ == "__main__":
    print("🎓 Learning Objectives:")
    print("1. Understand EfficientNet-B0 model creation")
    print("2. See transfer learning in action")
    print("3. Experience two-phase training")
    print("4. Learn model saving and deployment prep")
    print("\nStarting demo...\n")
    
    model, model_path = simple_training_demo()
    
    if model:
        print(f"\n🏆 Success! You now understand the complete training process.")
        print(f"📁 Your trained model: {model_path}")
    else:
        print(f"\n📚 Even if training failed, you learned the key concepts!")
    
    print(f"\n🍎 Ready to apply this to apple oxidation detection!")