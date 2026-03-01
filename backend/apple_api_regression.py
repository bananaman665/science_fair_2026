#!/usr/bin/env python3
"""
Apple Oxidation API - Regression Version with Variety-Specific Models
Returns days since apple was cut using variety-specific or combined models
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
from pathlib import Path
from typing import Optional

app = FastAPI(title="Apple Oxidation Days API - Variety Specific")

# CORS Configuration
# Allow requests from frontend (local dev, production, and mobile apps)
origins = [
    "http://localhost:5173",              # Vite dev server
    "http://localhost:4173",              # Vite preview
    "http://127.0.0.1:5173",              # Alternative localhost
    "capacitor://localhost",              # iOS Capacitor app
    "ionic://localhost",                  # iOS alternative
    "http://localhost",                   # Android Capacitor app
    "com.sciencefair.appleoxidation://localhost",  # iOS custom scheme
    "https://apple-oxidation-api-213429152907.us-central1.run.app",  # Cloud Run
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # Allowed origins
    allow_credentials=True,               # Allow cookies/auth headers
    allow_methods=["*"],                  # Allow all HTTP methods
    allow_headers=["*"],                  # Allow all headers
)

# Resolve paths relative to this script so it works from any working directory
BASE_DIR = Path(__file__).resolve().parent

# Model paths for different varieties (4 models total)
MODEL_PATHS = {
    'combined': BASE_DIR / "apple_oxidation_days_model_combined.h5",
    'gala': BASE_DIR / "apple_oxidation_days_model_gala.h5",
    'smith': BASE_DIR / "apple_oxidation_days_model_smith.h5",
    'red_delicious': BASE_DIR / "apple_oxidation_days_model_red_delicious.h5"
}

METADATA_PATHS = {
    'combined': BASE_DIR / "model_metadata_regression_combined.json",
    'gala': BASE_DIR / "model_metadata_regression_gala.json",
    'smith': BASE_DIR / "model_metadata_regression_smith.json",
    'red_delicious': BASE_DIR / "model_metadata_regression_red_delicious.json"
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
    print(f"Total models loaded: {len(models)}/4\n")

def auto_crop_apple(image):
    """
    Auto-crop apple from background by detecting the foreground object.
    Samples the image border to determine background color, then finds
    regions that differ from it. Works with any background color.
    Returns (cropped_image, was_cropped) tuple.
    """
    orig_w, orig_h = image.size

    # Downscale for analysis to save memory (full-res images can be 5000x3000+)
    max_analysis_dim = 512
    if max(orig_w, orig_h) > max_analysis_dim:
        scale = max_analysis_dim / max(orig_w, orig_h)
        analysis_img = image.resize((int(orig_w * scale), int(orig_h * scale)))
    else:
        scale = 1.0
        analysis_img = image

    img_array = np.array(analysis_img, dtype=np.float32)
    h, w = img_array.shape[:2]

    # Sample border pixels (top/bottom 5% of rows, left/right 5% of cols)
    border_size = max(int(min(h, w) * 0.05), 1)
    border_pixels = np.concatenate([
        img_array[:border_size, :].reshape(-1, 3),     # top
        img_array[-border_size:, :].reshape(-1, 3),    # bottom
        img_array[:, :border_size].reshape(-1, 3),     # left
        img_array[:, -border_size:].reshape(-1, 3),    # right
    ])

    # Background color = median of border pixels (robust to outliers)
    bg_color = np.median(border_pixels, axis=0)

    # Mask: pixels that differ from background by more than threshold
    diff = np.sqrt(np.sum((img_array - bg_color) ** 2, axis=2))
    mask = diff > 40  # color distance threshold

    # Find rows and columns with foreground pixels
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)

    if not rows.any() or not cols.any():
        return image, False

    row_indices = np.where(rows)[0]
    col_indices = np.where(cols)[0]

    min_row, max_row = int(row_indices[0]), int(row_indices[-1])
    min_col, max_col = int(col_indices[0]), int(col_indices[-1])

    # Add 5% padding
    pad_h = int((max_row - min_row) * 0.05)
    pad_w = int((max_col - min_col) * 0.05)

    min_row = max(0, min_row - pad_h)
    max_row = min(h, max_row + pad_h)
    min_col = max(0, min_col - pad_w)
    max_col = min(w, max_col + pad_w)

    # Only crop if the bounding box is meaningfully smaller than the original
    crop_area = (max_row - min_row) * (max_col - min_col)
    total_area = h * w
    if crop_area >= total_area * 0.85:
        return image, False

    # Scale coordinates back to original image dimensions
    min_col = int(min_col / scale)
    min_row = int(min_row / scale)
    max_col = int(max_col / scale)
    max_row = int(max_row / scale)

    cropped = image.crop((min_col, min_row, max_col, max_row))
    return cropped, True


def preprocess_image(image_bytes, crop=True):
    """Preprocess uploaded image for prediction"""
    try:
        # Open image
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')

        # Auto-crop apple from background if requested
        was_cropped = False
        if crop:
            image, was_cropped = auto_crop_apple(image)

        # Resize to model input size
        image = image.resize((224, 224))

        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        return image_array, was_cropped
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    """API info"""
    available_models = list(models.keys())
    return {
        "name": "Apple Oxidation Days Prediction API - Variety Specific",
        "version": "4.0",
        "model_type": "regression",
        "description": "Upload an apple photo to predict how many days since it was cut",
        "available_models": available_models,
        "supported_varieties": ["combined", "gala", "smith", "red_delicious"],
        "usage": "Add ?variety=gala, ?variety=smith, or ?variety=red_delicious to use variety-specific models"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if len(models) > 0 else "no_models_loaded",
        "models_loaded": list(models.keys()),
        "metadata": {k: v for k, v in metadata_store.items()}
    }

# Valid variety options
VALID_VARIETIES = ['combined', 'gala', 'smith', 'red_delicious']

@app.post("/analyze")
async def analyze_apple(
    file: UploadFile = File(...),
    variety: Optional[str] = Query('combined', description="Apple variety: 'combined', 'gala', 'smith', or 'red_delicious'"),
    crop: Optional[bool] = Query(True, description="Auto-crop apple from background before analysis")
):
    """
    Analyze apple photo and predict days since cut

    Args:
        file: Image file of the apple
        variety: Which model to use - 'combined' (default), 'gala', 'smith', or 'red_delicious'
        crop: Auto-crop apple from background (default True). Improves accuracy for phone photos.

    Returns:
    - days: Predicted days since apple was cut
    - confidence_interval: Estimated range based on validation MAE
    - interpretation: Human-readable interpretation
    - model_used: Which variety model was used
    """

    # Validate variety
    variety = variety.lower()
    if variety not in VALID_VARIETIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid variety. Must be one of {VALID_VARIETIES}. Got: {variety}"
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
        image_array, was_cropped = preprocess_image(image_bytes, crop=crop)

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
            },
            "preprocessing": {
                "auto_crop_requested": crop,
                "was_cropped": was_cropped
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@app.post("/batch_analyze")
async def batch_analyze(
    files: list[UploadFile] = File(...),
    variety: Optional[str] = Query('combined', description="Apple variety: 'combined', 'gala', 'smith', or 'red_delicious'"),
    crop: Optional[bool] = Query(True, description="Auto-crop apple from background before analysis")
):
    """
    Analyze multiple apple photos at once

    Useful for comparing oxidation progression
    """

    # Validate variety
    variety = variety.lower()
    if variety not in VALID_VARIETIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid variety. Must be one of {VALID_VARIETIES}"
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
            image_array, was_cropped = preprocess_image(image_bytes, crop=crop)

            prediction = model.predict(image_array, verbose=0)
            predicted_days = float(prediction[0][0])

            results.append({
                "filename": file.filename,
                "days_since_cut": round(predicted_days, 2),
                "was_cropped": was_cropped,
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
