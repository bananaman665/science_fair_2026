# Apple Oxidation Detection - Deployment Plan

## Overview

This document outlines the deployment strategy:
1. **Local Development** - Web app + Capacitor for mobile
2. **Cloud Deployment** - Google Cloud Run (pay-per-use, scales to zero)

---

## Part 1: Local Development Setup

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | **React + Vite** | Fast, modern web framework |
| Mobile Wrapper | **Capacitor** | Wrap web app as iOS/Android |
| Styling | **Tailwind CSS** | Rapid UI development |
| API Client | **Fetch/Axios** | HTTP requests to backend |
| Camera | **Capacitor Camera** | Native camera access |
| Backend | **FastAPI** | Python ML API (already built) |

### Project Structure

```
science_fair_2026/
├── backend/                    # Python API + Models
│   ├── apple_api_regression.py
│   ├── *.h5                   # ML models (4 files, ~270MB)
│   ├── *.json                 # Model metadata
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # React + Capacitor App
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── capacitor.config.ts
│   └── package.json
├── data_repository/            # Training data (not in git)
└── docs/                       # Documentation
```

### Local Development Workflow

```
┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │     │  Mobile Device  │
│  localhost:5173 │     │  (Capacitor)    │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   FastAPI Backend     │
         │   localhost:8000      │
         │   (4 ML Models)       │
         └───────────────────────┘
```

### Frontend Setup Commands

```bash
# 1. Create frontend
cd frontend
npm create vite@latest . -- --template react
npm install

# 2. Add dependencies
npm install @capacitor/core @capacitor/cli
npm install @capacitor/camera @capacitor/filesystem
npm install -D tailwindcss postcss autoprefixer

# 3. Initialize Capacitor
npx cap init "Apple Freshness" "com.sciencefair.applefreshness"

# 4. Add mobile platforms
npm install @capacitor/android @capacitor/ios
npx cap add android
npx cap add ios

# 5. Development
npm run dev              # Start web dev server (localhost:5173)
npx cap sync             # Sync to mobile platforms
npx cap open android     # Open in Android Studio
npx cap open ios         # Open in Xcode
```

### Backend Setup Commands

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Ensure models are present
ls *.h5  # Should show 4 model files

# 3. Start API
python apple_api_regression.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

---

## Part 2: Cloud Deployment - Google Cloud Run

### Why Google Cloud Run?

| Feature | Benefit |
|---------|---------|
| **Scales to zero** | No cost when idle |
| **Pay-per-request** | ~$0.00002 per request |
| **First 2M requests FREE** | Perfect for science fair |
| **Auto-scaling** | Handles traffic spikes |
| **Container-based** | Easy deployment |
| **HTTPS included** | Secure by default |

### Cost Estimate

| Usage | Monthly Cost |
|-------|--------------|
| 100 requests | ~$0.00 (free tier) |
| 1,000 requests | ~$0.02 |
| 10,000 requests | ~$0.20 |

**For a science fair demo: Essentially FREE**

### Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        USER DEVICES                          │
├──────────────────┬──────────────────┬───────────────────────┤
│   iOS App        │   Android App    │   Web Browser         │
│   (Capacitor)    │   (Capacitor)    │   (React PWA)         │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                    │
         └──────────────────┼────────────────────┘
                            │ HTTPS
                            ▼
              ┌─────────────────────────┐
              │   Google Cloud Run      │
              │                         │
              │  ┌───────────────────┐  │
              │  │   FastAPI Server  │  │
              │  │   (Container)     │  │
              │  │                   │  │
              │  │  ┌─────────────┐  │  │
              │  │  │ ML Models   │  │  │
              │  │  │ (4 x 67MB)  │  │  │
              │  │  └─────────────┘  │  │
              │  └───────────────────┘  │
              └─────────────────────────┘
                            │
                            ▼
              URL: https://apple-api-xxxxx.run.app
```

### Deployment Files

#### backend/Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and models
COPY apple_api_regression.py .
COPY *.h5 .
COPY *.json .

# Cloud Run uses PORT env variable
ENV PORT=8080
EXPOSE 8080

# Start server
CMD ["sh", "-c", "uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}"]
```

#### backend/requirements.txt (for Cloud Run)

```
tensorflow-cpu==2.15.0
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pillow>=10.0.0
numpy>=1.24.0
```

#### backend/.dockerignore

```
__pycache__/
*.pyc
*.pyo
.git/
.gitignore
README.md
*.md
ml_training/
```

### Deployment Steps

#### Prerequisites
1. Google Cloud account (free tier available)
2. Google Cloud CLI installed (`gcloud`)
3. Docker installed (for local testing)

#### Step-by-Step Deployment

```bash
# 1. Authenticate with Google Cloud
gcloud auth login

# 2. Create a new project (or use existing)
gcloud projects create apple-oxidation-api --name="Apple Oxidation API"
gcloud config set project apple-oxidation-api

# 3. Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 4. Navigate to backend directory
cd backend

# 5. Build and submit container to Google Cloud
gcloud builds submit --tag gcr.io/apple-oxidation-api/apple-api

# 6. Deploy to Cloud Run
gcloud run deploy apple-api \
  --image gcr.io/apple-oxidation-api/apple-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 60 \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2

# 7. Get the service URL
gcloud run services describe apple-api --region us-central1 --format='value(status.url)'
```

#### Expected Output
```
Service [apple-api] revision [apple-api-00001] has been deployed
Service URL: https://apple-api-xxxxxx-uc.a.run.app
```

### Local Docker Testing

Before deploying, test locally:

```bash
cd backend

# Build container
docker build -t apple-api .

# Run container
docker run -p 8080:8080 apple-api

# Test
curl http://localhost:8080/health
```

---

## Part 3: Frontend Configuration

### Environment Variables

#### .env.development
```
VITE_API_URL=http://localhost:8000
```

#### .env.production
```
VITE_API_URL=https://apple-api-xxxxxx-uc.a.run.app
```

### API Service Module

**frontend/src/services/api.js**
```javascript
const API_URL = import.meta.env.VITE_API_URL;

export async function analyzeApple(imageFile, variety = 'combined') {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(
    `${API_URL}/analyze?variety=${variety}`,
    {
      method: 'POST',
      body: formData,
    }
  );

  if (!response.ok) {
    throw new Error('Analysis failed');
  }

  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_URL}/health`);
  return response.json();
}

export const VARIETIES = ['combined', 'gala', 'smith', 'red_delicious'];
```

---

## Part 4: Implementation Phases

### Phase 1: Backend Deployment
- [x] Train ML models (4 variety-specific models)
- [x] Build FastAPI server
- [x] Test locally
- [ ] Create Dockerfile
- [ ] Deploy to Google Cloud Run
- [ ] Verify cloud endpoint

### Phase 2: Frontend Development
- [ ] Set up React + Vite project
- [ ] Add Tailwind CSS
- [ ] Create camera capture component
- [ ] Create apple variety selector
- [ ] Create results display
- [ ] Connect to API (local first, then cloud)

### Phase 3: Mobile Integration
- [ ] Initialize Capacitor
- [ ] Add camera plugin
- [ ] Test on Android emulator
- [ ] Test on iOS simulator
- [ ] Build release APK/IPA

### Phase 4: Polish & Launch
- [ ] Add loading states
- [ ] Add error handling
- [ ] Offline detection
- [ ] App icons and splash screens
- [ ] Final testing

---

## Part 5: Files Needed for Deployment

### Models Archive (for other developers)

To deploy the API, you need these files from `backend/`:

```
models_archive/
├── apple_oxidation_days_model_combined.h5      (67 MB)
├── apple_oxidation_days_model_gala.h5          (67 MB)
├── apple_oxidation_days_model_smith.h5         (67 MB)
├── apple_oxidation_days_model_red_delicious.h5 (67 MB)
├── model_metadata_regression_combined.json
├── model_metadata_regression_gala.json
├── model_metadata_regression_smith.json
├── model_metadata_regression_red_delicious.json
├── apple_api_regression.py
├── requirements.txt
└── Dockerfile
```

**Total size: ~270 MB**

### Creating the Archive

```bash
cd backend
tar -czvf ../models_archive.tar.gz \
  *.h5 \
  model_metadata_regression_*.json \
  apple_api_regression.py \
  requirements.txt \
  Dockerfile
```

---

## Cost Summary

| Component | Development | Production |
|-----------|-------------|------------|
| Frontend (Vercel/Netlify) | Free | Free |
| Backend (Cloud Run) | Free | Free (2M requests) |
| Container Registry | Free | Free (first 0.5GB) |
| **Total** | **$0** | **$0** |

---

## Quick Reference

### Local Development
```bash
# Backend
cd backend && python apple_api_regression.py

# Frontend
cd frontend && npm run dev
```

### Production Deployment
```bash
# Deploy API
cd backend
gcloud builds submit --tag gcr.io/PROJECT/apple-api
gcloud run deploy apple-api --image gcr.io/PROJECT/apple-api ...

# Deploy Frontend
cd frontend
npm run build
# Upload dist/ to Vercel/Netlify
```

### API Endpoints
```
GET  /              - API info
GET  /health        - Health check with model status
POST /analyze       - Analyze single image
POST /batch_analyze - Analyze multiple images
```
