#!/usr/bin/env python3
"""
Model Testing and Inference Demo
Science Fair 2025 - Apple Oxidation Detection

This script shows how to load and test your trained model,
demonstrating exactly how your FastAPI backend will work.
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
import os

class ModelTester:
    """
    Test trained EfficientNet-B0 model.
    This demonstrates how your API will work.
    """
    
    def __init__(self, model_path):
        """Load trained model and metadata."""
        print(f"🔄 Loading model from: {model_path}")
        
        # Load the model
        self.model = tf.keras.models.load_model(model_path)
        
        # Load metadata
        metadata_path = os.path.join(model_path, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)
            self.class_names = self.metadata["class_names"]
            self.img_size = self.metadata["img_size"]
        else:
            # Default values if metadata not available
            self.class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
            self.img_size = 224
        
        print(f"✅ Model loaded successfully!")
        print(f"📊 Classes: {self.class_names}")
        print(f"🖼️ Input size: {self.img_size}x{self.img_size}")

    def preprocess_image(self, image_path):
        """
        Preprocess image for prediction.
        This is exactly what your API will do.
        """
        # Load image
        image = tf.keras.preprocessing.image.load_img(
            image_path, 
            target_size=(self.img_size, self.img_size)
        )
        
        # Convert to array
        image_array = tf.keras.preprocessing.image.img_to_array(image)
        image_array = tf.expand_dims(image_array, 0)  # Add batch dimension
        
        # EfficientNet preprocessing
        image_array = tf.keras.applications.efficientnet.preprocess_input(image_array)
        
        return image_array, image

    def predict(self, image_path):
        """
        Make prediction on a single image.
        This demonstrates your API prediction logic.
        """
        print(f"\n🔍 Analyzing image: {image_path}")
        
        # Preprocess image
        processed_image, original_image = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(processed_image, verbose=0)
        
        # Extract results
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        predicted_class = self.class_names[predicted_class_idx]
        
        # Create result dictionary (like your API response)
        result = {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "class_probabilities": {
                self.class_names[i]: float(predictions[0][i]) 
                for i in range(len(self.class_names))
            }
        }
        
        # Display results
        print(f"🎯 Prediction: {predicted_class}")
        print(f"🎲 Confidence: {confidence:.4f}")
        print("📊 All probabilities:")
        for class_name, prob in result["class_probabilities"].items():
            print(f"   {class_name}: {prob:.4f}")
        
        # Show image and prediction
        self._visualize_prediction(original_image, result)
        
        return result

    def _visualize_prediction(self, image, result):
        """Visualize the prediction result."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Show original image
        ax1.imshow(image)
        ax1.set_title("Input Image")
        ax1.axis('off')
        
        # Show prediction probabilities
        classes = list(result["class_probabilities"].keys())
        probs = list(result["class_probabilities"].values())
        
        bars = ax2.barh(classes, probs)
        ax2.set_xlabel('Probability')
        ax2.set_title(f'Prediction: {result["predicted_class"]}\nConfidence: {result["confidence"]:.4f}')
        ax2.set_xlim(0, 1)
        
        # Highlight the predicted class
        predicted_idx = classes.index(result["predicted_class"])
        bars[predicted_idx].set_color('orange')
        
        plt.tight_layout()
        plt.show()

    def batch_predict(self, image_paths):
        """Predict on multiple images."""
        results = []
        for image_path in image_paths:
            try:
                result = self.predict(image_path)
                results.append({
                    "image_path": image_path,
                    "prediction": result
                })
            except Exception as e:
                print(f"❌ Error processing {image_path}: {e}")
                results.append({
                    "image_path": image_path,
                    "error": str(e)
                })
        
        return results


def demo_inference(model_path):
    """
    Demonstrate model inference.
    This shows how your FastAPI backend will work.
    """
    print("🧪 Model Inference Demo")
    print("=" * 40)
    
    # Initialize tester
    tester = ModelTester(model_path)
    
    print("\n📝 This demonstrates exactly how your API will work:")
    print("1. Load trained model")
    print("2. Preprocess input image")
    print("3. Run inference")
    print("4. Return formatted results")
    
    print("\n💡 For your apple oxidation project:")
    print("- Replace flower classes with: Fresh, Light, Medium, Heavy")
    print("- Use the same preprocessing and prediction logic")
    print("- Return oxidation score (0-100) instead of flower type")
    
    return tester


if __name__ == "__main__":
    # You'll need to provide the path to your trained model
    # This will be available after running train_efficientnet.py
    
    print("To use this script:")
    print("1. First run: python train_efficientnet.py")
    print("2. Note the saved model path")
    print("3. Run: python test_model.py with the model path")
    print("\nExample:")
    print("model_path = './models/flower_classification_efficientnet_20250928_123456'")
    print("tester = demo_inference(model_path)")