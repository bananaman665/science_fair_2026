#!/usr/bin/env python3
"""
Pilot Study Model Tester
Tests current ML model on pilot study photos to identify improvements needed
"""

import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_dir))

def load_model():
    """Load the current trained model"""
    model_path = backend_dir / "apple_model_local_1819.h5"
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        return None
    
    model = tf.keras.models.load_model(model_path)
    print(f"✅ Model loaded: {model.count_params()} parameters")
    return model

def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    try:
        # Load and resize image
        image = Image.open(image_path)
        image = image.convert('RGB')
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def predict_oxidation(model, image_path):
    """Predict oxidation level for an image"""
    image_array = preprocess_image(image_path)
    if image_array is None:
        return None
    
    # Make prediction
    prediction = model.predict(image_array, verbose=0)
    
    # Class labels (matching our training)
    classes = ['fresh', 'light_oxidation', 'medium_oxidation', 'heavy_oxidation']
    
    # Get predicted class and confidence
    predicted_class_idx = np.argmax(prediction[0])
    predicted_class = classes[predicted_class_idx]
    confidence = prediction[0][predicted_class_idx]
    
    return {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'all_probabilities': {classes[i]: prediction[0][i] for i in range(len(classes))}
    }

def test_pilot_photos():
    """Test all photos in pilot study directory"""
    pilot_dir = Path("data_repository/01_raw_images/pilot_study_oct2025")
    
    if not pilot_dir.exists():
        print(f"❌ Pilot directory not found: {pilot_dir}")
        return
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    print("\n🧪 Testing Pilot Study Photos")
    print("=" * 50)
    
    # Test photos from each apple variety
    for apple_dir in pilot_dir.iterdir():
        if apple_dir.is_dir() and apple_dir.name != "__pycache__":
            print(f"\n📁 Testing {apple_dir.name.upper()} photos:")
            
            # Get all jpg files
            jpg_files = list(apple_dir.glob("*.jpg")) + list(apple_dir.glob("*.jpeg"))
            
            if not jpg_files:
                print("   No photos found yet")
                continue
            
            # Sort by filename (should include timestamp info)
            jpg_files.sort()
            
            for photo_path in jpg_files:
                result = predict_oxidation(model, photo_path)
                
                if result:
                    print(f"   📸 {photo_path.name}")
                    print(f"      Prediction: {result['predicted_class']} ({result['confidence']:.2f})")
                    
                    # Show all probabilities for analysis
                    print("      All probabilities:")
                    for class_name, prob in result['all_probabilities'].items():
                        print(f"        {class_name}: {prob:.3f}")
                    print()

def analyze_pilot_results():
    """Analyze pilot study results and provide recommendations"""
    print("\n📊 Pilot Study Analysis")
    print("=" * 50)
    print("After collecting pilot photos, this function will:")
    print("1. Compare model predictions to visual assessment")
    print("2. Identify where the model struggles")
    print("3. Recommend improvements for main collection")
    print("4. Suggest optimal photo timing based on oxidation progression")

if __name__ == "__main__":
    print("🤖 Apple Oxidation Model - Pilot Study Tester")
    print("This script tests our current model on pilot study photos")
    print("Run this after each pilot photo session to track model performance")
    
    test_pilot_photos()
    analyze_pilot_results()
    
    print("\n💡 Usage Tips:")
    print("- Run this script after each 8-hour photo session")
    print("- Compare predictions to your visual assessment")
    print("- Note where the model fails - this guides improvements")
    print("- Use results to plan main data collection strategy")