# Apple Oxidation API - Usage Guide

## Quick Start

### 1. Set up the Python environment (first time only)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Requirements**: Python 3.12+, TensorFlow 2.16+ (requirements.txt handles this).

### 2. Start the API server
```bash
# Option A: From project root
./start_regression_api.sh

# Option B: Manual
cd backend
source .venv/bin/activate
python apple_api_regression.py
```

- Server: **http://localhost:8000**
- Interactive Swagger docs: **http://localhost:8000/docs**

### 3. Verify models loaded
```bash
curl http://localhost:8000/health
```

You should see `"status": "healthy"` and all 4 models in `models_loaded`.

**Note on paths**: The API resolves model paths relative to the script location
(`backend/`), so it works regardless of which directory you launch from.

## Available Models

4 variety-specific CNN regression models (MobileNetV2, 224x224 input):

| Model | Variety Param | Samples | Validation MAE | Best For |
|-------|---------------|---------|----------------|----------|
| Red Delicious | `red_delicious` | 83 | 0.75 days | Red apples |
| Granny Smith | `smith` | 83 | 0.86 days | Green apples |
| Gala | `gala` | 83 | 1.18 days | Red/yellow apples |
| Combined | `combined` | 249 | 1.20 days | Unknown variety (fallback) |

Always use the variety-specific model when you know the apple type. The wrong
variety model can degrade accuracy by 30%+.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info & available models |
| GET | `/health` | Health check with model status |
| POST | `/analyze?variety=X` | Analyze single image |
| POST | `/batch_analyze?variety=X` | Analyze multiple images |

## Testing with curl

### Health check
```bash
curl http://localhost:8000/health
```

### Analyze a single apple
```bash
# Granny Smith model
curl -X POST "http://localhost:8000/analyze?variety=smith" \
  -F "file=@path/to/apple_photo.jpg"

# Combined model (default if no variety param)
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@path/to/apple_photo.jpg"
```

### Test with training images (known ground truth)

Fresh apple (day 0, should predict ~0 days):
```bash
curl -X POST "http://localhost:8000/analyze?variety=smith" \
  -F "file=@data_repository/01_raw_images/second_collection_nov2024/granny_smith/fruit_1/granny_smith_fruit1_day0_000h_top_down_20241101-am.JPG"
```

Oxidized apple (day 6, 158h, should predict ~6.5 days):
```bash
curl -X POST "http://localhost:8000/analyze?variety=smith" \
  -F "file=@data_repository/01_raw_images/second_collection_nov2024/granny_smith/fruit_1/granny_smith_fruit1_day6_158h_top_down_20241107-pm.JPG"
```

Gala with gala model (~1.5 days):
```bash
curl -X POST "http://localhost:8000/analyze?variety=gala" \
  -F "file=@data_repository/01_raw_images/second_collection_nov2024/gala/fruit_1/gala_fruit1_day1_035h_top_down_20241102-pm.JPG"
```

### Batch analysis
```bash
curl -X POST "http://localhost:8000/batch_analyze?variety=smith" \
  -F "file=@image1.jpg" -F "file=@image2.jpg" -F "file=@image3.jpg"
```

### Compare all models on the same photo
```bash
PHOTO="data_repository/01_raw_images/second_collection_nov2024/granny_smith/fruit_1/granny_smith_fruit1_day1_035h_top_down_20241102-pm.JPG"

echo "Combined:" && curl -s -X POST "http://localhost:8000/analyze?variety=combined" -F "file=@$PHOTO" | python3 -m json.tool
echo "Smith:" && curl -s -X POST "http://localhost:8000/analyze?variety=smith" -F "file=@$PHOTO" | python3 -m json.tool
echo "Gala:" && curl -s -X POST "http://localhost:8000/analyze?variety=gala" -F "file=@$PHOTO" | python3 -m json.tool
```

## Response Format

### Single analysis (`/analyze`)
```json
{
  "success": true,
  "prediction": {
    "days_since_cut": 2.34,
    "confidence_interval": {
      "lower": 1.48,
      "upper": 3.20
    },
    "interpretation": "Light oxidation - about 2 days old",
    "oxidation_level": "light"
  },
  "model_info": {
    "variety_used": "smith",
    "validation_mae": 0.856,
    "training_samples": 83
  }
}
```

### Batch analysis (`/batch_analyze`)
```json
{
  "total_files": 3,
  "successful": 3,
  "variety_used": "smith",
  "results": [
    { "filename": "photo1.jpg", "days_since_cut": 1.23, "success": true },
    { "filename": "photo2.jpg", "days_since_cut": 2.45, "success": true },
    { "filename": "photo3.jpg", "days_since_cut": 3.67, "success": true }
  ]
}
```

## Oxidation Level Interpretations

| Days | Interpretation | Oxidation Level |
|------|---------------|-----------------|
| < 0.5 | Fresh - just cut | none |
| 0.5 - 1.5 | Very fresh | minimal |
| 1.5 - 2.5 | Light oxidation | light |
| 2.5 - 3.5 | Medium oxidation | medium |
| 3.5 - 4.5 | Significant oxidation | medium-heavy |
| > 4.5 | Heavy oxidation | heavy |

## Code Examples

### Python
```python
import requests

url = "http://localhost:8000/analyze"
params = {"variety": "smith"}
files = {"file": open("granny_smith_photo.jpg", "rb")}

response = requests.post(url, params=params, files=files)
result = response.json()

print(f"Days since cut: {result['prediction']['days_since_cut']}")
print(f"Confidence: {result['prediction']['confidence_interval']}")
```

### JavaScript (used by the frontend)
```javascript
async function analyzeApple(imageFile, variety = 'combined') {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(
    `http://localhost:8000/analyze?variety=${variety}`,
    { method: 'POST', body: formData }
  );

  return await response.json();
}
```

## Troubleshooting

### "no_models_loaded" on health check
The API can't find the `.h5` files. This was fixed by using `BASE_DIR = Path(__file__).resolve().parent`
so paths resolve relative to the script. If models are missing entirely:
```bash
# Check they exist
ls -lh backend/*.h5

# If missing, restore from archive or retrain
tar -xzvf models_archive.tar.gz -C backend/
# or
python train_regression_model.py
```

### TensorFlow version errors
The models were saved with **Keras 3** (TF 2.16+). Do NOT set `TF_USE_LEGACY_KERAS=1`
or install `tf-keras` — that forces Keras 2 which can't load these models. Just use
standard TensorFlow 2.16+.

### Wrong predictions
1. **Check variety parameter** — using the wrong variety model hurts accuracy by 30%+
2. **Crop test images** — removing phone backgrounds improves accuracy (21.2% improvement)
3. **Models trained on 0-6.5 days** — predictions outside this range may be unreliable

## Docker Deployment

```bash
cd backend
docker build -t apple-oxidation-api .
docker run -p 8080:8080 apple-oxidation-api
```

The Dockerfile uses `PORT` env var (defaults to 8080) for Google Cloud Run compatibility.

## Further Reading

- [MODEL_RESULTS.md](MODEL_RESULTS.md) — Detailed performance analysis & scientific findings
- [CLOUD_RUN_DEPLOYMENT.md](CLOUD_RUN_DEPLOYMENT.md) — Google Cloud deployment guide
- http://localhost:8000/docs — Interactive Swagger UI (when server is running)
