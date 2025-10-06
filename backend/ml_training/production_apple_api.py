#!/usr/bin/env python3
"""
FastAPI Apple Analysis Backend - Production Ready
Uses locally trained CNN model for apple oxidation detection
"""

import tensorflow as tf
import numpy as np
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Apple Oxidation Detection API",
    description="Real-time apple freshness analysis using CNN",
    version="2.0.0"
)

# Global variables for model
model = None
model_metadata = None

def load_model():
    """Load the trained model and metadata"""
    global model, model_metadata
    
    model_path = Path(__file__).parent / "apple_model_local_1808.h5"
    metadata_path = Path(__file__).parent / "model_metadata.json"
    
    try:
        # Load model
        model = tf.keras.models.load_model(model_path)
        logger.info(f"✅ Model loaded: {model_path}")
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            model_metadata = json.load(f)
        logger.info(f"✅ Metadata loaded: {metadata_path}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return False

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    try:
        # Resize to model input size
        img_size = model_metadata['model_info']['input_size']
        image = image.resize((img_size, img_size))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array and normalize
        img_array = np.array(image, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {e}")

def analyze_apple_oxidation(image: Image.Image) -> dict:
    """Analyze apple oxidation level"""
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get class name
        class_names = model_metadata['class_names']
        predicted_class = class_names[predicted_class_idx]
        
        # Create detailed response
        result = {
            "oxidation_level": predicted_class,
            "confidence": confidence,
            "all_probabilities": {
                class_names[i]: float(predictions[0][i]) 
                for i in range(len(class_names))
            },
            "freshness_score": calculate_freshness_score(predicted_class, confidence),
            "recommendation": get_recommendation(predicted_class, confidence),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Apple analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

def calculate_freshness_score(oxidation_level: str, confidence: float) -> float:
    """Calculate freshness score (0-100)"""
    base_scores = {
        "fresh": 95,
        "light_oxidation": 75,
        "medium_oxidation": 50,
        "heavy_oxidation": 25
    }
    
    base_score = base_scores.get(oxidation_level, 0)
    # Adjust based on confidence
    adjusted_score = base_score * confidence
    
    return round(adjusted_score, 1)

def get_recommendation(oxidation_level: str, confidence: float) -> str:
    """Get recommendation based on oxidation level"""
    if confidence < 0.7:
        return "Low confidence prediction - please try a clearer image"
    
    recommendations = {
        "fresh": "✅ Apple is fresh and safe to eat! Store in refrigerator for best quality.",
        "light_oxidation": "🟡 Apple shows slight browning but is still good to eat. Use soon for best taste.",
        "medium_oxidation": "🟠 Apple has moderate oxidation. Safe to eat but may taste less fresh.",
        "heavy_oxidation": "🔴 Apple shows significant oxidation. Check for off flavors before eating."
    }
    
    return recommendations.get(oxidation_level, "Unable to determine apple condition")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    if not load_model():
        logger.error("❌ Failed to load model on startup")
        raise RuntimeError("Model loading failed")
    logger.info("🚀 Apple Analysis API ready!")

@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "🍎 Apple Oxidation Detection API",
        "version": "2.0.0",
        "status": "ready" if model is not None else "loading",
        "model_info": model_metadata['model_info'] if model_metadata else None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "model_info": {
            "architecture": model_metadata['model_info']['architecture'] if model_metadata else None,
            "parameters": model_metadata['model_info']['parameters'] if model_metadata else None,
            "classes": model_metadata['class_names'] if model_metadata else None
        }
    }

@app.post("/analyze_apple")
async def analyze_apple(file: UploadFile = File(...)):
    """
    Analyze apple oxidation from uploaded image
    
    Returns:
    - oxidation_level: fresh, light_oxidation, medium_oxidation, heavy_oxidation
    - confidence: prediction confidence (0-1)
    - freshness_score: overall freshness score (0-100)
    - recommendation: actionable advice
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Analyze apple
        result = analyze_apple_oxidation(image)
        
        logger.info(f"Analysis completed: {result['oxidation_level']} ({result['confidence']:.3f})")
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/model_info")
async def get_model_info():
    """Get detailed model information"""
    if model is None or model_metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_metadata": model_metadata,
        "model_summary": {
            "total_parameters": model.count_params() if model else 0,
            "input_shape": model.input_shape if model else None,
            "output_shape": model.output_shape if model else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")