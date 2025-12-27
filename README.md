# Apple Oxidation Detection - Science Fair 2026

**AI-Powered Assessment of Apple Freshness Using Computer Vision**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Project Overview

This project uses machine learning to analyze photographs of cut apples and predict how many days since they were cut (oxidation level). The system uses regression models trained on variety-specific data to provide accurate freshness predictions.

### Key Features

- **4 Trained Models**: Combined, Gala, Granny Smith, Red Delicious
- **REST API**: FastAPI server for image analysis
- **Mobile Ready**: Designed for React + Capacitor mobile app
- **Cloud Deployable**: Configured for Google Cloud Run

## Results Summary

| Model | Validation MAE | Training Samples |
|-------|----------------|------------------|
| Red Delicious | **0.75 days** | 83 |
| Granny Smith | **0.86 days** | 83 |
| Gala | **1.18 days** | 83 |
| Combined | **1.20 days** | 249 |

*MAE = Mean Absolute Error (lower is better)*

## Repository Structure

```
science_fair_2026/
├── backend/                    # Python ML API
│   ├── apple_api_regression.py # FastAPI server
│   ├── *.h5                    # Trained models (4 files, ~270MB)
│   ├── *.json                  # Model metadata
│   ├── Dockerfile              # For cloud deployment
│   └── requirements.txt
├── frontend/                   # React + Capacitor app (TBD)
├── data_repository/            # Training data
│   └── 01_raw_images/
│       └── second_collection_nov2024/  # 312 images
├── docs/                       # Documentation
│   ├── DEPLOYMENT_PLAN.md      # Local & cloud deployment guide
│   └── IMAGE_NAMING_CONVENTIONS.md
├── train_regression_model.py   # Model training script
├── organize_new_images.py      # Image organization tool
└── README.md
```

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/science_fair_2026.git
cd science_fair_2026
```

### 2. Install Dependencies

```bash
pip install tensorflow fastapi uvicorn pillow python-multipart scikit-learn
```

### 3. Get Model Files

Model files (*.h5) are not stored in git due to size (~270MB total).

**Option A**: Download from release/shared archive
```bash
# Extract models archive to backend/
tar -xzvf models_archive.tar.gz -C backend/
```

**Option B**: Train models from data
```bash
python train_regression_model.py  # Trains all 4 models
```

### 4. Start API Server

```bash
cd backend
python apple_api_regression.py
# Server runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 5. Test the API

```bash
# Check health
curl http://localhost:8000/health

# Analyze an apple image
curl -X POST "http://localhost:8000/analyze?variety=smith" \
  -F "file=@apple_photo.jpg"
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available models |
| GET | `/health` | Health check with model status |
| POST | `/analyze?variety=X` | Analyze single image |
| POST | `/batch_analyze?variety=X` | Analyze multiple images |

**Variety options**: `combined`, `gala`, `smith`, `red_delicious`

## Training Data

- **Total Images**: 312
- **Apple Varieties**: 3 (Gala, Granny Smith, Red Delicious)
- **Apples per Variety**: 4
- **Time Range**: 0-6.5 days (13 sessions over 1 week)
- **Collection Period**: November 2024

## Technology Stack

- **ML Framework**: TensorFlow/Keras
- **API**: FastAPI + Uvicorn
- **Image Processing**: PIL/Pillow
- **Deployment**: Docker + Google Cloud Run
- **Frontend**: React + Vite + Capacitor (planned)

## Deployment

See [docs/DEPLOYMENT_PLAN.md](docs/DEPLOYMENT_PLAN.md) for detailed instructions on:
- Local development setup
- Google Cloud Run deployment
- Mobile app development with Capacitor

## Documentation

- [DEPLOYMENT_PLAN.md](docs/DEPLOYMENT_PLAN.md) - Local & cloud deployment
- [IMAGE_NAMING_CONVENTIONS.md](docs/IMAGE_NAMING_CONVENTIONS.md) - Data organization
- [MODEL_RESULTS.md](MODEL_RESULTS.md) - Training results and analysis

## License

MIT License - see [LICENSE](LICENSE) for details.

---

*Predicting apple freshness through computer vision*
