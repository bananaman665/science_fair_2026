#!/usr/bin/env python3
"""
Apple Oxidation API - Regression Version
Returns days since apple was cut instead of categories
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path

app = FastAPI(title="Apple Oxidation Days API")

# Load model at startup
MODEL_PATH = Path("apple_oxidation_days_model.h5")
METADATA_PATH = Path("model_metadata_regression.json")

model = None
metadata = None

@app.on_event("startup")
async def load_model():
    """Load the trained model on startup"""
    global model, metadata
    
    if MODEL_PATH.exists():
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"✅ Model loaded: {model.count_params():,} parameters")
        
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r') as f:
                metadata = json.load(f)
            print(f"✅ Metadata loaded: MAE = {metadata.get('validation_mae', 'N/A'):.3f} days")
    else:
        print(f"⚠️  Model not found at {MODEL_PATH}")

def preprocess_image(image_bytes):
    """Preprocess uploaded image for prediction"""
    try:
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')
        
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    """API info"""
    return {
        "name": "Apple Oxidation Days Prediction API",
        "version": "2.0",
        "model_type": "regression",
        "description": "Upload an apple photo to predict how many days since it was cut"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "model_loaded": model is not None,
        "metadata": metadata
    }

@app.post("/analyze")
async def analyze_apple(file: UploadFile = File(...)):
    """
    Analyze apple photo and predict days since cut
    
    Returns:
    - days: Predicted days since apple was cut
    - confidence_interval: Estimated range based on validation MAE
    - interpretation: Human-readable interpretation
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image_array = preprocess_image(image_bytes)
        
        # Make prediction
        prediction = model.predict(image_array, verbose=0)
        predicted_days = float(prediction[0][0])
        
        # Calculate confidence interval based on validation MAE
        mae = metadata.get('validation_mae', 0.5) if metadata else 0.5
        confidence_interval = {
            'lower': max(0, predicted_days - mae),
            'upper': predicted_days + mae
        }
        
        # Interpretation
        if predicted_days < 0.5:
            interpretation = "Fresh - just cut"
            oxidation_level = "none"
        elif predicted_days < 1.5:
            interpretation = "Very fresh - less than 1.5 days old"
            oxidation_level = "minimal"
        elif predicted_days < 2.5:
            interpretation = "Light oxidation - about 2 days old"
            oxidation_level = "light"
        elif predicted_days < 3.5:
            interpretation = "Medium oxidation - about 3 days old"
            oxidation_level = "medium"
        elif predicted_days < 4.5:
            interpretation = "Significant oxidation - about 4 days old"
            oxidation_level = "medium-heavy"
        else:
            interpretation = f"Heavy oxidation - {predicted_days:.1f} days old"
            oxidation_level = "heavy"
        
        return {
            "success": True,
            "prediction": {
                "days_since_cut": round(predicted_days, 2),
                "confidence_interval": {
                    "lower": round(confidence_interval['lower'], 2),
                    "upper": round(confidence_interval['upper'], 2)
                },
                "interpretation": interpretation,
                "oxidation_level": oxidation_level
            },
            "model_info": {
                "validation_mae": metadata.get('validation_mae') if metadata else None,
                "training_samples": metadata.get('training_samples') if metadata else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@app.post("/batch_analyze")
async def batch_analyze(files: list[UploadFile] = File(...)):
    """
    Analyze multiple apple photos at once
    
    Useful for comparing oxidation progression
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    
    for file in files:
        try:
            image_bytes = await file.read()
            image_array = preprocess_image(image_bytes)
            
            prediction = model.predict(image_array, verbose=0)
            predicted_days = float(prediction[0][0])
            
            results.append({
                "filename": file.filename,
                "days_since_cut": round(predicted_days, 2),
                "success": True
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "success": False
            })
    
    return {
        "total_files": len(files),
        "successful": sum(1 for r in results if r["success"]),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    print("🍎 Starting Apple Oxidation Days Prediction API")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
