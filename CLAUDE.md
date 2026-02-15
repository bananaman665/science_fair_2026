# Apple Oxidation Detection - Science Fair 2026

## What This Project Is

A science fair project that uses CNN regression models (TensorFlow/Keras) to predict
how many days since an apple was cut, based on a photo. The system has a FastAPI backend,
trained models for 3 apple varieties, and a React + Capacitor mobile frontend.

## Project Structure

```
science_fair_2026/
├── backend/                           # FastAPI server + trained models
│   ├── apple_api_regression.py        # Main API (FastAPI, runs on port 8000)
│   ├── requirements.txt               # Python deps (fastapi, tensorflow 2.16+)
│   ├── Dockerfile                     # For Google Cloud Run deployment
│   ├── *.h5                           # 4 trained models (~270MB total, gitignored)
│   ├── *.json                         # Model metadata files (gitignored)
│   └── ml_training/                   # Training experiments & alternative scripts
├── frontend/                          # React + Vite + Capacitor mobile app
│   ├── src/                           # React source (pages, components, services)
│   ├── android/                       # Capacitor Android native project
│   └── ios/                           # Capacitor iOS native project
├── data_repository/                   # All training data
│   ├── 01_raw_images/
│   │   └── second_collection_nov2024/ # Main dataset: 312 images (3 varieties)
│   ├── 02_processed_images/           # Curated/cropped sets
│   ├── 03_data_tracking/              # Collection metadata & logs
│   └── 04_scripts/                    # Google Drive sync, automation
├── docs/                              # Guides, collection procedures
├── train_regression_model.py          # Main training script (trains all 4 models)
├── test_optimal_strategy.py           # Validates preprocessing approach
├── test_both_varieties.py             # Compares variety-specific models
├── manual_crop_apples.py              # Interactive GUI for cropping test images
├── organize_new_images.py             # Auto-organize images into training structure
└── MODEL_RESULTS.md                   # Final results & scientific findings
```

## Trained Models

4 CNN regression models (MobileNetV2 transfer learning, 224x224 input, predicts days 0-6.5):

| Model | File | Samples | Validation MAE |
|-------|------|---------|----------------|
| Red Delicious | `apple_oxidation_days_model_red_delicious.h5` | 83 | 0.75 days |
| Granny Smith | `apple_oxidation_days_model_smith.h5` | 83 | 0.86 days |
| Gala | `apple_oxidation_days_model_gala.h5` | 83 | 1.18 days |
| Combined | `apple_oxidation_days_model_combined.h5` | 249 | 1.20 days |

Models are stored in `backend/` but gitignored due to size. Restore from archive:

```bash
tar -xzvf models_archive.tar.gz -C backend/
```

Or retrain:

```bash
python train_regression_model.py
```

## Training Data

- 312 images from November 2024 collection
- 3 varieties: Gala, Granny Smith, Red Delicious
- 4 apples per variety, 2 angles (top-down + 45-degree), 13 time sessions over 6.5 days
- File naming: `[variety]_fruit[N]_day[N]_[hours]h_[angle]_[date]-[am|pm].JPG`
- Hours in filename map to days since cut (e.g., 158h = 6.58 days)

## Running the API & Testing

See **[API_USAGE_GUIDE.md](API_USAGE_GUIDE.md)** for full setup, all curl commands,
test examples with training images, response format, troubleshooting, and code examples.

Quick start:

```bash
cd backend
source .venv/bin/activate       # First time: python3 -m venv .venv && pip install -r requirements.txt
python apple_api_regression.py  # Runs at http://localhost:8000, docs at /docs
```

## Important Technical Notes

- **Python 3.12+** required. TensorFlow 2.15 does NOT work with 3.12; use 2.16+.
- **Models saved with Keras 3**. Do NOT set `TF_USE_LEGACY_KERAS=1` or install `tf-keras`.
- **Model paths** use `Path(__file__).resolve().parent` so the API works from any directory.
- **CORS** is configured for Vite dev server, Capacitor iOS/Android, and custom URL schemes.

## Key Scientific Achievement

**21.2% accuracy improvement** by solving domain shift:

- Train on ORIGINAL images (full context with backgrounds)
- Test on CROPPED images (removes messy phone backgrounds)
- Use variety-specific models (wrong variety hurts accuracy by 30%+)

## Frontend

React + Vite app with Capacitor for iOS/Android. Uses Supabase for auth (social login only).
The backend CORS config already allows requests from Vite dev server, Capacitor, and iOS/Android.

```bash
cd frontend
npm install
npm run dev          # Vite dev server at localhost:5173
npx cap sync         # Sync web assets to native projects
npx cap open ios     # Open in Xcode
npx cap open android # Open in Android Studio
```

## Where We Left Off

- All 4 variety-specific regression models trained and verified working
- FastAPI backend running locally with all models loading correctly
- API tested via curl with training images (day 0 fresh, day 6 oxidized, etc.)
- Docker deployment config in place for Google Cloud Run
- Frontend mobile app exists with auth, scanning UI, and history
- Git repo cleaned up (removed node_modules, Capacitor build artifacts from tracking)
