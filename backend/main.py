#!/usr/bin/env python3
"""
Minimal FastAPI Backend for ML Model Serving
Science Fair 2025 - Apple Oxidation Detection

This demonstrates how your trained EfficientNet-B0 model will be served
through a REST API for your Flutter mobile app.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
from datetime import datetime
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(
    title="Apple Oxidation Detection API",
    description="EfficientNet-B0 based API for detecting apple oxidation levels",
    version="1.0.0"
)

# Global model variable (will be loaded on startup)
model = None
model_metadata = None

class ModelPredictor:
    """Model inference class for the API."""
    
    def __init__(self, model_path: str):
        """Load model and metadata."""
        self.model = tf.keras.models.load_model(model_path)
        
        # Load metadata if available
        metadata_path = os.path.join(model_path, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            # Default metadata for flowers demo
            self.metadata = {
                "class_names": ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips'],
                "img_size": 224,
                "model_name": "flower_classification_demo"
            }
        
        self.class_names = self.metadata["class_names"]
        self.img_size = self.metadata["img_size"]
        
        print(f"✅ Model loaded: {self.metadata.get('model_name', 'Unknown')}")
        print(f"📊 Classes: {self.class_names}")

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for EfficientNet-B0 inference."""
        # Resize image
        image = image.resize((self.img_size, self.img_size))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to array
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        
        # EfficientNet preprocessing
        image_array = tf.keras.applications.efficientnet.preprocess_input(image_array)
        
        return image_array

    def predict(self, image: Image.Image) -> dict:
        """Make prediction on image."""
        # Preprocess
        processed_image = self.preprocess_image(image)
        
        # Inference
        start_time = datetime.now()
        predictions = self.model.predict(processed_image, verbose=0)
        inference_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Extract results
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        predicted_class = self.class_names[predicted_class_idx]
        
        # For apple oxidation, we'd convert this to oxidation score
        # This is just demo logic for flowers
        oxidation_score = int(predicted_class_idx * 25)  # 0, 25, 50, 75, 100
        
        result = {
            "analysis_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "predicted_class": predicted_class,
            "oxidation_score": oxidation_score,  # Demo: convert class to score
            "confidence": confidence,
            "processing_time_ms": int(inference_time),
            "timestamp": datetime.now().isoformat(),
            "model_version": self.metadata.get("model_name", "v1.0.0"),
            "all_probabilities": {
                self.class_names[i]: float(predictions[0][i]) 
                for i in range(len(self.class_names))
            }
        }
        
        return result

# Global predictor instance
predictor: Optional[ModelPredictor] = None

@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    global predictor
    
    # In production, you'd load your trained apple oxidation model here
    # For now, this is just demo setup
    print("🚀 Starting up FastAPI backend...")
    print("💡 To load your trained model, set MODEL_PATH environment variable")
    
    model_path = os.getenv("MODEL_PATH")
    if model_path and os.path.exists(model_path):
        try:
            predictor = ModelPredictor(model_path)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("🔄 Running without model (health check only)")
    else:
        print("🔄 No model path provided. Running in demo mode.")
        print("   Set MODEL_PATH environment variable to load your trained model.")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "🍎 Apple Oxidation Detection API",
        "status": "running",
        "model_loaded": predictor is not None,
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": predictor is not None,
        "model_info": predictor.metadata if predictor else None
    }

@app.post("/api/v1/analyze-apple")
async def analyze_apple(file: UploadFile = File(...)):
    """
    Analyze apple image for oxidation level.
    This is the main endpoint your Flutter app will call.
    """
    if not predictor:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Please set MODEL_PATH environment variable and restart."
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    try:
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Make prediction
        result = predictor.predict(image)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing image: {str(e)}"
        )

@app.get("/api/v1/model-info")
async def model_info():
    """Get information about the loaded model."""
    if not predictor:
        raise HTTPException(status_code=503, detail="No model loaded")
    
    return {
        "model_metadata": predictor.metadata,
        "classes": predictor.class_names,
        "input_size": predictor.img_size,
        "status": "ready"
    }

@app.get("/api/v1/demo")
async def demo_endpoint():
    """Demo endpoint showing API structure."""
    return {
        "message": "This is how your API will work!",
        "workflow": [
            "1. Flutter app takes photo of apple",
            "2. App sends image to /api/v1/analyze-apple",
            "3. Backend preprocesses image",
            "4. EfficientNet-B0 analyzes oxidation",
            "5. API returns oxidation score and category",
            "6. App displays results to user"
        ],
        "example_response": {
            "analysis_id": "demo_20250928_123456",
            "oxidation_score": 35,
            "oxidation_category": "Light",
            "confidence": 0.89,
            "processing_time_ms": 156,
            "timestamp": "2025-09-28T12:34:56"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Apple Oxidation Detection API")
    print("📚 Learning Goals:")
    print("   - Understand FastAPI structure")
    print("   - See how ML models integrate with APIs")
    print("   - Learn request/response handling")
    print("   - Understand image preprocessing pipeline")
    print("")
    print("🔧 To test with your trained model:")
    print("   1. Train model: python ml_training/train_efficientnet.py")
    print("   2. Set MODEL_PATH: export MODEL_PATH=./ml_training/models/your_model")
    print("   3. Start API: python main.py")
    print("   4. Visit: http://localhost:8000/docs")
    print("")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)