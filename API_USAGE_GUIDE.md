# Apple Oxidation API - Usage Guide

## 🚀 Quick Start

### Start the API Server
```bash
cd /Users/andrew/projects/science_fair_2026/backend
python apple_api_regression.py
```

Server will be available at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

## 📋 Available Models

The API loads three models at startup:

1. **Combined Model** (default) - Trained on all varieties
2. **Gala Model** - Optimized for Gala apples (0.750 days MAE)
3. **Smith Model** - Optimized for Granny Smith apples (0.568 days MAE)

## 🔧 API Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "models_loaded": ["combined", "gala", "smith"],
  "metadata": {
    "combined": { "validation_mae": 1.395, ... },
    "gala": { "validation_mae": 0.750, ... },
    "smith": { "validation_mae": 0.568, ... }
  }
}
```

### 2. Analyze Single Apple

#### Using Combined Model (Default)
```bash
curl -X POST "http://localhost:8000/analyze" \
     -F "file=@path/to/apple_photo.jpg"
```

#### Using Gala-Specific Model
```bash
curl -X POST "http://localhost:8000/analyze?variety=gala" \
     -F "file=@path/to/apple_photo.jpg"
```

#### Using Granny Smith-Specific Model
```bash
curl -X POST "http://localhost:8000/analyze?variety=smith" \
     -F "file=@path/to/apple_photo.jpg"
```

Response:
```json
{
  "success": true,
  "prediction": {
    "days_since_cut": 2.34,
    "confidence_interval": {
      "lower": 1.77,
      "upper": 2.91
    },
    "interpretation": "Light oxidation - about 2 days old",
    "oxidation_level": "light"
  },
  "model_info": {
    "variety_used": "smith",
    "validation_mae": 0.568,
    "training_samples": 35
  }
}
```

### 3. Batch Analysis

Analyze multiple photos at once:

```bash
curl -X POST "http://localhost:8000/batch_analyze?variety=smith" \
     -F "files=@photo1.jpg" \
     -F "files=@photo2.jpg" \
     -F "files=@photo3.jpg"
```

Response:
```json
{
  "total_files": 3,
  "successful": 3,
  "variety_used": "smith",
  "results": [
    {
      "filename": "photo1.jpg",
      "days_since_cut": 1.23,
      "success": true
    },
    {
      "filename": "photo2.jpg",
      "days_since_cut": 2.45,
      "success": true
    },
    {
      "filename": "photo3.jpg",
      "days_since_cut": 3.67,
      "success": true
    }
  ]
}
```

## 🎯 Model Selection Guide

### When to use each model:

| Apple Variety | Recommended Model | Expected MAE |
|--------------|-------------------|--------------|
| Gala | `variety=gala` | 0.75 days |
| Granny Smith | `variety=smith` | 0.57 days |
| Unknown variety | `variety=combined` | 1.40 days |
| Mixed varieties | `variety=combined` | 1.40 days |

### Performance Comparison

Testing on 8 Granny Smith photos:

| Model Used | MAE (days) | MAE (hours) | Performance |
|------------|------------|-------------|-------------|
| Smith-specific | **1.47** | 35.2 | ✅ Best |
| Combined | 2.02 | 48.4 | ⚠️ Fair |
| Gala-specific | 2.29 | 54.9 | ❌ Poor |

**Key Insight**: Using the wrong variety model makes predictions 36% worse!

## 🐍 Python Example

```python
import requests

# Analyze a Granny Smith apple
url = "http://localhost:8000/analyze"
params = {"variety": "smith"}
files = {"file": open("granny_smith_photo.jpg", "rb")}

response = requests.post(url, params=params, files=files)
result = response.json()

print(f"Days since cut: {result['prediction']['days_since_cut']}")
print(f"Confidence: {result['prediction']['confidence_interval']}")
print(f"Model used: {result['model_info']['variety_used']}")
```

## 🌐 JavaScript Example

```javascript
async function analyzeApple(imageFile, variety = 'combined') {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(
    `http://localhost:8000/analyze?variety=${variety}`,
    {
      method: 'POST',
      body: formData
    }
  );
  
  const result = await response.json();
  
  console.log(`Days since cut: ${result.prediction.days_since_cut}`);
  console.log(`Model used: ${result.model_info.variety_used}`);
  
  return result;
}

// Usage
const fileInput = document.getElementById('apple-photo');
analyzeApple(fileInput.files[0], 'smith');
```

## 🧪 Testing Your API

### Test with existing validation photos:

```bash
# Day 1 Granny Smith (should predict ~1 day)
curl -X POST "http://localhost:8000/analyze?variety=smith" \
     -F "file=@data_repository/compare_images/smith1-day1.jpg"

# Day 4 Granny Smith (should predict ~1.5-2 days)
curl -X POST "http://localhost:8000/analyze?variety=smith" \
     -F "file=@data_repository/compare_images/smith1-day4.jpg"
```

### Compare all three models:

```bash
# Test same photo with all models
PHOTO="data_repository/compare_images/smith1-day1.jpg"

echo "Combined model:"
curl -X POST "http://localhost:8000/analyze?variety=combined" -F "file=@$PHOTO" | jq '.prediction.days_since_cut'

echo "Gala model:"
curl -X POST "http://localhost:8000/analyze?variety=gala" -F "file=@$PHOTO" | jq '.prediction.days_since_cut'

echo "Smith model:"
curl -X POST "http://localhost:8000/analyze?variety=smith" -F "file=@$PHOTO" | jq '.prediction.days_since_cut'
```

## 📊 Interpreting Results

### Oxidation Levels

| Days | Interpretation | Oxidation Level |
|------|---------------|-----------------|
| < 0.5 | Fresh - just cut | none |
| 0.5 - 1.5 | Very fresh | minimal |
| 1.5 - 2.5 | Light oxidation | light |
| 2.5 - 3.5 | Medium oxidation | medium |
| 3.5 - 4.5 | Significant oxidation | medium-heavy |
| > 4.5 | Heavy oxidation | heavy |

### Confidence Intervals

The API returns confidence intervals based on validation MAE:
- **Smith model**: ±0.57 days
- **Gala model**: ±0.75 days
- **Combined model**: ±1.40 days

Example:
```json
{
  "days_since_cut": 2.34,
  "confidence_interval": {
    "lower": 1.77,  // 2.34 - 0.57
    "upper": 2.91   // 2.34 + 0.57
  }
}
```

## 🔍 Troubleshooting

### API won't start
```bash
# Check if models exist
ls -lh backend/*.h5

# Should see:
# apple_oxidation_days_model_combined.h5
# apple_oxidation_days_model_gala.h5
# apple_oxidation_days_model_smith.h5
```

If models missing, train them:
```bash
python train_regression_model.py
```

### Wrong predictions
1. **Check variety parameter**: Using Gala model on Granny Smith = 36% worse!
2. **Check image quality**: Blurry or poorly lit photos reduce accuracy
3. **Check apple age**: Models trained on 0-5 days, extrapolation may fail
4. **Check variety**: Models optimized for Gala and Granny Smith only

### Model not found error
```json
{
  "detail": "Model 'gala' not loaded. Available models: ['combined', 'smith']"
}
```

Solution: Check which models loaded at startup. May need to retrain missing model.

## 🎓 Best Practices

1. **Always specify variety when known**
   - Don't rely on combined model if you know the variety
   - 27-36% improvement with correct variety model

2. **Use batch endpoint for multiple photos**
   - More efficient than individual requests
   - Maintains consistency with same model

3. **Consider confidence intervals**
   - Smith model most precise (±0.57 days)
   - Combined model least precise (±1.40 days)

4. **Validate on your own data**
   - Test with known samples first
   - Our validation shows Day 1 is excellent, Days 2-4 need work

## 📚 Further Reading

- `VARIETY_SPECIFIC_MODELS.md` - Detailed performance analysis
- `VALIDATION_RESULTS_ANALYSIS.md` - Original validation findings
- `/docs` endpoint - Interactive API documentation

---

**Questions?** Check the Science Fair 2026 documentation or run the validation tests to see expected performance.
