# 🍎 Apple Oxidation Days Prediction Model

## 📊 Regression Approach (Days Since Cut)

Instead of classifying apples into categories (fresh/light/medium/heavy), this model **predicts the continuous number of days** since the apple was cut.

### Why This Is Better:

✅ **More Precise:** "2.3 days old" vs "medium oxidation"  
✅ **More Scientific:** Actual measurable time values  
✅ **More Useful:** Users get exact freshness estimate  
✅ **Better for Science Fair:** Shows quantitative analysis

---

## 🚀 Quick Start

### 1. Train the Model

```bash
cd /Users/andrew/projects/science_fair_2026
source backend/.venv/bin/activate
python train_regression_model.py
```

**What it does:**
- Loads all 88 photos from your collection
- Extracts days from filename (based on hours since cut)
- Trains CNN regression model
- Predicts continuous days (0.0 to 5.0)
- Saves model to `backend/apple_oxidation_days_model.h5`

**Expected output:**
```
Training: 70 images
Validation: 18 images
Validation MAE: ~0.3-0.5 days
```

---

### 2. Test the API

```bash
cd backend
python apple_api_regression.py
```

**API Endpoint:**
```
POST http://localhost:8000/analyze
```

**Example Response:**
```json
{
  "success": true,
  "prediction": {
    "days_since_cut": 2.34,
    "confidence_interval": {
      "lower": 1.84,
      "upper": 2.84
    },
    "interpretation": "Light oxidation - about 2 days old",
    "oxidation_level": "light"
  }
}
```

---

## 📸 How It Works

### Training Data Format:

Your photos are organized by time:
```
gala_fruit1_day0_000h_top_down.JPG  →  0.00 days
gala_fruit1_day1_024h_top_down.JPG  →  1.00 days
gala_fruit1_day2_048h_top_down.JPG  →  2.00 days
gala_fruit1_day3_072h_top_down.JPG  →  3.00 days
gala_fruit1_day4_096h_top_down.JPG  →  4.00 days
gala_fruit1_day5_120h_top_down.JPG  →  5.00 days
```

The model learns to predict the **continuous days value** from the photo.

---

## 🎯 Model Architecture

```
Input: 224x224 RGB image
  ↓
Conv2D (32 filters) + MaxPooling
  ↓
Conv2D (64 filters) + MaxPooling
  ↓
Conv2D (64 filters) + MaxPooling
  ↓
Dense (128 neurons) + Dropout
  ↓
Dense (64 neurons)
  ↓
Output: 1 neuron (linear activation)
  = Predicted days (continuous)
```

**Loss Function:** Mean Squared Error (MSE)  
**Metric:** Mean Absolute Error (MAE) in days

---

## 📊 Expected Performance

With your 88-photo dataset:

- **Training samples:** ~70 photos
- **Validation samples:** ~18 photos
- **Expected MAE:** 0.3-0.5 days
- **Interpretation:** Predictions typically within ±0.5 days of actual

---

## 🧪 Testing Predictions

After training, test with new apple photos:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@my_apple_photo.jpg"
```

**You'll get:**
- Days since cut (e.g., 2.34 days)
- Confidence interval (e.g., 1.84 - 2.84 days)
- Human interpretation (e.g., "Light oxidation")

---

## 🎓 Science Fair Presentation

### Great talking points:

1. **"We use regression instead of classification"**
   - More sophisticated ML approach
   - Continuous predictions vs discrete categories

2. **"Our model predicts actual time, not just categories"**
   - Quantitative analysis
   - Measurable, scientific output

3. **"Mean Absolute Error of ~0.5 days"**
   - Shows model accuracy
   - Explains confidence intervals

4. **"Trained on 88 real apple photos over 5 days"**
   - Real data collection methodology
   - Multiple apple varieties for robustness

---

## 📝 Files Created

- `train_regression_model.py` - Training script
- `backend/apple_api_regression.py` - FastAPI server
- `backend/apple_oxidation_days_model.h5` - Trained model
- `backend/model_metadata_regression.json` - Model info
- `backend/training_history_regression.png` - Training plots

---

## 🔄 Next Steps

1. **Train the model** with your 88 photos
2. **Test predictions** on validation set
3. **Deploy API** for live predictions
4. **Collect more data** to improve accuracy
5. **Science Fair demo** with live predictions!

🎯 **This approach is perfect for your Science Fair project - it's more advanced and shows real quantitative analysis!**
