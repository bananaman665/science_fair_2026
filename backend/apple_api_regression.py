#!/usr/bin/env python3
"""
Apple Oxidation API - Regression Version with Variety-Specific Models
Returns days since apple was cut using variety-specific or combined models
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path
from typing import Optional

app = FastAPI(title="Apple Oxidation Days API - Variety Specific")

# Model paths for different varieties
MODEL_PATHS = {
    'combined': Path("apple_oxidation_days_model_combined.h5"),
    'gala': Path("apple_oxidation_days_model_gala.h5"),
    'smith': Path("apple_oxidation_days_model_smith.h5")
}

METADATA_PATHS = {
    'combined': Path("model_metadata_regression_combined.json"),
    'gala': Path("model_metadata_regression_gala.json"),
    'smith': Path("model_metadata_regression_smith.json")
}

# Store loaded models
models = {}
metadata_store = {}

@app.on_event("startup")
async def load_models():
    """Load all available models on startup"""
    global models, metadata_store
    
    print("\n🍎 Loading Apple Oxidation Models...")
    print("=" * 50)
    
    for variety, model_path in MODEL_PATHS.items():
        if model_path.exists():
            try:
                models[variety] = tf.keras.models.load_model(model_path)
                print(f"✅ {variety.upper():10} model loaded: {models[variety].count_params():,} parameters")
                
                metadata_path = METADATA_PATHS[variety]
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata_store[variety] = json.load(f)
                    mae = metadata_store[variety].get('validation_mae', 'N/A')
                    print(f"   {'':10} MAE = {mae:.3f} days")
            except Exception as e:
                print(f"❌ {variety.upper():10} failed to load: {e}")
        else:
            print(f"⚠️  {variety.upper():10} model not found at {model_path}")
    
    print("=" * 50)
    print(f"Total models loaded: {len(models)}/3\n")

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
    available_models = list(models.keys())
    return {
        "name": "Apple Oxidation Days Prediction API - Variety Specific",
        "version": "3.0",
        "model_type": "regression",
        "description": "Upload an apple photo to predict how many days since it was cut",
        "available_models": available_models,
        "usage": "Add ?variety=gala or ?variety=smith to use variety-specific models"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if len(models) > 0 else "no_models_loaded",
        "models_loaded": list(models.keys()),
        "metadata": {k: v for k, v in metadata_store.items()}
    }

@app.post("/analyze")
async def analyze_apple(
    file: UploadFile = File(...),
    variety: Optional[str] = Query('combined', description="Apple variety: 'combined', 'gala', or 'smith'")
):
    """
    Analyze apple photo and predict days since cut
    
    Args:
        file: Image file of the apple
        variety: Which model to use - 'combined' (default), 'gala', or 'smith'
    
    Returns:
    - days: Predicted days since apple was cut
    - confidence_interval: Estimated range based on validation MAE
    - interpretation: Human-readable interpretation
    - model_used: Which variety model was used
    """
    
    # Validate variety
    variety = variety.lower()
    if variety not in ['combined', 'gala', 'smith']:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid variety. Must be 'combined', 'gala', or 'smith'. Got: {variety}"
        )
    
    # Check if model is loaded
    if variety not in models:
        available = list(models.keys())
        raise HTTPException(
            status_code=503, 
            detail=f"Model '{variety}' not loaded. Available models: {available}"
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image_array = preprocess_image(image_bytes)
        
        # Make prediction using selected model
        model = models[variety]
        metadata = metadata_store.get(variety, {})
        
        prediction = model.predict(image_array, verbose=0)
        predicted_days = float(prediction[0][0])
        
        # Calculate confidence interval based on validation MAE
        mae = metadata.get('validation_mae', 0.5)
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
                "variety_used": variety,
                "validation_mae": metadata.get('validation_mae'),
                "training_samples": metadata.get('training_samples')
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@app.post("/batch_analyze")
async def batch_analyze(
    files: list[UploadFile] = File(...),
    variety: Optional[str] = Query('combined', description="Apple variety: 'combined', 'gala', or 'smith'")
):
    """
    Analyze multiple apple photos at once
    
    Useful for comparing oxidation progression
    """
    
    # Validate variety
    variety = variety.lower()
    if variety not in ['combined', 'gala', 'smith']:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid variety. Must be 'combined', 'gala', or 'smith'"
        )
    
    if variety not in models:
        available = list(models.keys())
        raise HTTPException(
            status_code=503, 
            detail=f"Model '{variety}' not loaded. Available models: {available}"
        )
    
    model = models[variety]
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
        "variety_used": variety,
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    print("🍎 Starting Apple Oxidation Days Prediction API")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
