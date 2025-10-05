#!/usr/bin/env python3
"""
EfficientNet-B0 Transfer Learning Training Script
Science Fair 2025 - Apple Oxidation Detection

This script demonstrates the complete training process for transfer learning
using EfficientNet-B0. We'll use TensorFlow's flowers dataset as practice data
to understand the exact same process we'll use for apple oxidation images.

Learning Goals:
1. Understand how to load and prepare image datasets
2. Learn EfficientNet-B0 architecture and transfer learning
3. Implement training pipeline with validation
4. Visualize results and model performance
5. Save and load trained models
"""

import os
# Set threading and memory environment variables before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Reduce TensorFlow logging
os.environ['OMP_NUM_THREADS'] = '1'       # Fix threading issues on macOS
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'

import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from datetime import datetime
import json

# Configure TensorFlow for macOS stability
tf.config.threading.set_inter_op_parallelism_threads(1)
tf.config.threading.set_intra_op_parallelism_threads(1)

# Set up GPU memory growth (prevents TensorFlow from allocating all GPU memory)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(f"GPU setup error: {e}")

# Use CPU-only mode to avoid GPU threading issues on macOS
tf.config.set_visible_devices([], 'GPU')

class FlowerClassificationTrainer:
    """
    Training class for EfficientNet-B0 transfer learning on flowers dataset.
    This demonstrates the exact same process we'll use for apple oxidation detection.
    """
    
    def __init__(self, data_dir="./data", model_dir="./models"):
        self.data_dir = data_dir
        self.model_dir = model_dir
        self.img_size = 224  # EfficientNet-B0 input size
        self.batch_size = 16  # Reduced for macOS stability
        self.num_classes = 5  # flowers dataset has 5 classes
        
        # Create directories
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(model_dir, exist_ok=True)
        
        # Dataset will have these classes (similar to our apple oxidation categories)
        self.class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
        
        print("🌸 EfficientNet-B0 Transfer Learning Trainer Initialized")
        print(f"📁 Data directory: {data_dir}")
        print(f"🤖 Model directory: {model_dir}")
        print(f"📊 Image size: {self.img_size}x{self.img_size}")
        print(f"📦 Batch size: {self.batch_size}")

    def load_and_prepare_data(self):
        """
        Load and prepare the flowers dataset.
        This shows exactly how we'll prepare your apple oxidation images.
        """
        print("\n🔄 Loading and preparing flowers dataset...")
        
        # Download the flowers dataset (similar to loading your apple images)
        (train_ds, val_ds), info = tfds.load(
            "tf_flowers",
            split=["train[:80%]", "train[80%:]"],  # 80% train, 20% validation
            shuffle_files=True,
            as_supervised=True,  # Returns (image, label) pairs
            with_info=True,
            data_dir=self.data_dir
        )
        
        # Get dataset info
        self.num_classes = info.features['label'].num_classes
        self.class_names = info.features['label'].names
        
        print(f"📊 Dataset info:")
        print(f"   - Classes: {self.num_classes}")
        print(f"   - Class names: {self.class_names}")
        print(f"   - Training samples: {len(train_ds)}")
        print(f"   - Validation samples: {len(val_ds)}")
        
        # Prepare datasets with preprocessing
        self.train_ds = train_ds.map(self._preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
        self.val_ds = val_ds.map(self._preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
        
        # Optimize for performance
        self.train_ds = self.train_ds.cache().shuffle(1000).batch(self.batch_size).prefetch(tf.data.AUTOTUNE)
        self.val_ds = self.val_ds.cache().batch(self.batch_size).prefetch(tf.data.AUTOTUNE)
        
        print("✅ Dataset prepared successfully!")
        return self.train_ds, self.val_ds

    def _preprocess_image(self, image, label):
        """
        Preprocess images for EfficientNet-B0.
        This is exactly what we'll do with your apple photos.
        """
        # Resize to EfficientNet input size
        image = tf.image.resize(image, [self.img_size, self.img_size])
        
        # Normalize to [0,1] range
        image = tf.cast(image, tf.float32) / 255.0
        
        # EfficientNet preprocessing (ImageNet normalization)
        image = tf.keras.applications.efficientnet.preprocess_input(image * 255.0)
        
        return image, label

    def create_model(self):
        """
        Create EfficientNet-B0 model with transfer learning.
        This shows the exact architecture we'll use for apple oxidation detection.
        """
        print("\n🏗️ Creating EfficientNet-B0 model...")
        
        # Load pre-trained EfficientNet-B0 (trained on ImageNet)
        base_model = tf.keras.applications.EfficientNetB0(
            weights='imagenet',  # Use ImageNet pre-trained weights
            include_top=False,   # Remove the final classification layer
            input_shape=(self.img_size, self.img_size, 3)
        )
        
        # Freeze the base model (transfer learning step 1)
        base_model.trainable = False
        
        print(f"📊 Base model info:")
        print(f"   - Total layers: {len(base_model.layers)}")
        print(f"   - Trainable parameters: {base_model.count_params()}")
        print(f"   - Input shape: {base_model.input_shape}")
        
        # Add custom classification head for our task
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation='relu', name='feature_layer'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(self.num_classes, activation='softmax', name='prediction_layer')
        ])
        
        # Compile the model
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', 'top_2_accuracy']
        )
        
        self.model = model
        
        print("✅ Model created successfully!")
        print(f"📊 Total parameters: {model.count_params():,}")
        
        # Print model summary
        model.summary()
        
        return model

    def train_phase_1(self, epochs=10):
        """
        Phase 1: Train only the classification head (base model frozen).
        This is the first step of transfer learning.
        """
        print(f"\n🚀 Starting Phase 1 Training (Frozen Base Model) - {epochs} epochs...")
        
        # Create callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7
            )
        ]
        
        # Train the model
        history_1 = self.model.fit(
            self.train_ds,
            epochs=epochs,
            validation_data=self.val_ds,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate Phase 1 performance
        val_loss, val_accuracy, val_top2 = self.model.evaluate(self.val_ds, verbose=0)
        print(f"📊 Phase 1 Results:")
        print(f"   - Validation Accuracy: {val_accuracy:.4f}")
        print(f"   - Validation Top-2 Accuracy: {val_top2:.4f}")
        print(f"   - Validation Loss: {val_loss:.4f}")
        
        self.history_phase1 = history_1
        return history_1

    def train_phase_2(self, epochs=10, fine_tune_layers=20):
        """
        Phase 2: Fine-tune the top layers of the base model.
        This is the second step of transfer learning for better accuracy.
        """
        print(f"\n🔥 Starting Phase 2 Training (Fine-tuning top {fine_tune_layers} layers) - {epochs} epochs...")
        
        # Unfreeze the top layers of the base model
        base_model = self.model.layers[0]
        base_model.trainable = True
        
        # Freeze all layers except the top ones
        for layer in base_model.layers[:-fine_tune_layers]:
            layer.trainable = False
        
        print(f"📊 Fine-tuning info:")
        print(f"   - Total layers in base model: {len(base_model.layers)}")
        print(f"   - Layers being fine-tuned: {fine_tune_layers}")
        print(f"   - Frozen layers: {len(base_model.layers) - fine_tune_layers}")
        
        # Recompile with lower learning rate for fine-tuning
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),  # Lower learning rate
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy', 'top_2_accuracy']
        )
        
        # Create callbacks
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=7,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-8
            )
        ]
        
        # Continue training with fine-tuning
        history_2 = self.model.fit(
            self.train_ds,
            epochs=epochs,
            validation_data=self.val_ds,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate final performance
        val_loss, val_accuracy, val_top2 = self.model.evaluate(self.val_ds, verbose=0)
        print(f"📊 Phase 2 (Final) Results:")
        print(f"   - Validation Accuracy: {val_accuracy:.4f}")
        print(f"   - Validation Top-2 Accuracy: {val_top2:.4f}")
        print(f"   - Validation Loss: {val_loss:.4f}")
        
        self.history_phase2 = history_2
        return history_2

    def evaluate_model(self):
        """
        Comprehensive model evaluation with visualizations.
        This shows how we'll evaluate your apple oxidation model.
        """
        print("\n📊 Evaluating model performance...")
        
        # Get predictions for confusion matrix
        predictions = []
        true_labels = []
        
        for images, labels in self.val_ds:
            preds = self.model.predict(images, verbose=0)
            predictions.extend(np.argmax(preds, axis=1))
            true_labels.extend(labels.numpy())
        
        # Create confusion matrix
        cm = confusion_matrix(true_labels, predictions)
        
        # Plot results
        self._plot_training_history()
        self._plot_confusion_matrix(cm)
        
        # Print classification report
        print("\n📋 Classification Report:")
        print(classification_report(true_labels, predictions, target_names=self.class_names))
        
        return cm

    def _plot_training_history(self):
        """Plot training history from both phases."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Combine histories if we have both phases
        if hasattr(self, 'history_phase2'):
            # Combine phase 1 and phase 2 histories
            acc = self.history_phase1.history['accuracy'] + self.history_phase2.history['accuracy']
            val_acc = self.history_phase1.history['val_accuracy'] + self.history_phase2.history['val_accuracy']
            loss = self.history_phase1.history['loss'] + self.history_phase2.history['loss']
            val_loss = self.history_phase1.history['val_loss'] + self.history_phase2.history['val_loss']
            
            phase1_epochs = len(self.history_phase1.history['accuracy'])
            total_epochs = len(acc)
        else:
            # Only phase 1
            acc = self.history_phase1.history['accuracy']
            val_acc = self.history_phase1.history['val_accuracy']
            loss = self.history_phase1.history['loss']
            val_loss = self.history_phase1.history['val_loss']
            phase1_epochs = len(acc)
            total_epochs = len(acc)
        
        epochs = range(1, total_epochs + 1)
        
        # Plot accuracy
        axes[0, 0].plot(epochs, acc, 'b-', label='Training Accuracy')
        axes[0, 0].plot(epochs, val_acc, 'r-', label='Validation Accuracy')
        if hasattr(self, 'history_phase2'):
            axes[0, 0].axvline(x=phase1_epochs, color='g', linestyle='--', alpha=0.7, label='Fine-tuning starts')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot loss
        axes[0, 1].plot(epochs, loss, 'b-', label='Training Loss')
        axes[0, 1].plot(epochs, val_loss, 'r-', label='Validation Loss')
        if hasattr(self, 'history_phase2'):
            axes[0, 1].axvline(x=phase1_epochs, color='g', linestyle='--', alpha=0.7, label='Fine-tuning starts')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot learning rate (if available)
        if hasattr(self, 'history_phase1') and 'lr' in self.history_phase1.history:
            lr = self.history_phase1.history['lr']
            if hasattr(self, 'history_phase2'):
                lr += self.history_phase2.history['lr']
            axes[1, 0].plot(epochs, lr, 'g-')
            axes[1, 0].set_title('Learning Rate')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Learning Rate')
            axes[1, 0].set_yscale('log')
            axes[1, 0].grid(True, alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, 'Learning Rate\nNot Available', 
                          ha='center', va='center', transform=axes[1, 0].transAxes)
        
        # Summary text
        final_acc = val_acc[-1]
        final_loss = val_loss[-1]
        axes[1, 1].text(0.1, 0.8, f'Final Validation Accuracy: {final_acc:.4f}', 
                       transform=axes[1, 1].transAxes, fontsize=12, fontweight='bold')
        axes[1, 1].text(0.1, 0.6, f'Final Validation Loss: {final_loss:.4f}', 
                       transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].text(0.1, 0.4, f'Total Training Epochs: {total_epochs}', 
                       transform=axes[1, 1].transAxes, fontsize=12)
        if hasattr(self, 'history_phase2'):
            axes[1, 1].text(0.1, 0.2, f'Phase 1 Epochs: {phase1_epochs}', 
                           transform=axes[1, 1].transAxes, fontsize=12)
            axes[1, 1].text(0.1, 0.0, f'Phase 2 Epochs: {total_epochs - phase1_epochs}', 
                           transform=axes[1, 1].transAxes, fontsize=12)
        axes[1, 1].set_xlim(0, 1)
        axes[1, 1].set_ylim(0, 1)
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig(f'{self.model_dir}/training_history.png', dpi=300, bbox_inches='tight')
        plt.show()

    def _plot_confusion_matrix(self, cm):
        """Plot confusion matrix."""
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.tight_layout()
        plt.savefig(f'{self.model_dir}/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()

    def save_model(self, model_name="flower_classification_efficientnet"):
        """
        Save the trained model.
        This shows how we'll save your apple oxidation model.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"{self.model_dir}/{model_name}_{timestamp}"
        
        print(f"\n💾 Saving model to: {model_path}")
        
        # Save the full model
        self.model.save(model_path)
        
        # Save model metadata
        metadata = {
            "model_name": model_name,
            "timestamp": timestamp,
            "num_classes": self.num_classes,
            "class_names": self.class_names,
            "img_size": self.img_size,
            "batch_size": self.batch_size,
            "architecture": "EfficientNet-B0",
            "training_phases": 2 if hasattr(self, 'history_phase2') else 1
        }
        
        with open(f"{model_path}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Model saved successfully!")
        return model_path

    def load_model(self, model_path):
        """Load a saved model."""
        print(f"\n📂 Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        
        # Load metadata if available
        metadata_path = f"{model_path}/metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            print(f"📊 Model metadata: {metadata}")
        
        print("✅ Model loaded successfully!")
        return self.model

    def predict_single_image(self, image_path):
        """
        Predict a single image.
        This demonstrates how your app will work in practice.
        """
        # Load and preprocess image
        image = tf.keras.preprocessing.image.load_img(image_path, target_size=(self.img_size, self.img_size))
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)  # Add batch dimension
        
        # Preprocess for EfficientNet
        image_array = tf.keras.applications.efficientnet.preprocess_input(image_array)
        
        # Make prediction
        predictions = self.model.predict(image_array, verbose=0)
        
        # Get results
        predicted_class = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        result = {
            "predicted_class": self.class_names[predicted_class],
            "confidence": confidence,
            "all_predictions": {
                self.class_names[i]: float(predictions[0][i]) 
                for i in range(len(self.class_names))
            }
        }
        
        return result


def main():
    """
    Main training pipeline demonstration.
    This shows the complete process we'll use for apple oxidation detection.
    """
    print("🍎 EfficientNet-B0 Transfer Learning Demo")
    print("=" * 50)
    print("This demonstrates the exact training process we'll use for apple oxidation detection!")
    
    # Initialize trainer
    trainer = FlowerClassificationTrainer()
    
    # Step 1: Load and prepare dataset
    train_ds, val_ds = trainer.load_and_prepare_data()
    
    # Step 2: Create model
    model = trainer.create_model()
    
    # Step 3: Train Phase 1 (frozen base model)
    print("\n" + "="*50)
    print("PHASE 1: Training classification head only")
    print("="*50)
    history1 = trainer.train_phase_1(epochs=3)  # Reduced epochs for demo stability
    
    # Step 4: Train Phase 2 (fine-tuning)
    print("\n" + "="*50)
    print("PHASE 2: Fine-tuning top layers")
    print("="*50)
    history2 = trainer.train_phase_2(epochs=3, fine_tune_layers=10)  # Reduced for stability
    
    # Step 5: Evaluate model
    print("\n" + "="*50)
    print("EVALUATION: Model performance analysis")
    print("="*50)
    cm = trainer.evaluate_model()
    
    # Step 6: Save model
    model_path = trainer.save_model()
    
    print("\n" + "="*50)
    print("🎉 TRAINING COMPLETE!")
    print("="*50)
    print("You now understand the complete EfficientNet-B0 transfer learning process!")
    print("This exact same process will work for your apple oxidation images.")
    print(f"📁 Model saved to: {model_path}")
    print(f"📊 Training plots saved to: {trainer.model_dir}/")
    
    return trainer, model_path


if __name__ == "__main__":
    # Run the complete training demonstration
    trainer, model_path = main()
    
    print("\n🎓 Learning Summary:")
    print("- ✅ Dataset loading and preprocessing")
    print("- ✅ EfficientNet-B0 architecture setup")
    print("- ✅ Transfer learning (2-phase training)")
    print("- ✅ Model evaluation and visualization")
    print("- ✅ Model saving and loading")
    print("\nNext step: Replace flowers dataset with your apple oxidation images!")