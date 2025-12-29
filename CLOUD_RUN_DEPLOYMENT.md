# Google Cloud Run Deployment Guide

This guide explains how to deploy your FastAPI backend to Google Cloud Run and configure CORS for the frontend.

## Prerequisites

1. Google Cloud account with billing enabled
2. Google Cloud CLI (`gcloud`) installed
3. Docker installed locally (for testing)

## Backend CORS Configuration

✅ **CORS is already configured** in `backend/apple_api_regression.py`!

The backend is set up to accept requests from:
- `http://localhost:5173` - Vite dev server
- `http://localhost:4173` - Vite preview
- `capacitor://localhost` - iOS mobile app
- `http://localhost` - Android mobile app

### Adding Production Frontend URL

When you deploy your frontend, add the production URL to the CORS origins list in `backend/apple_api_regression.py`:

```python
origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "capacitor://localhost",
    "http://localhost",
    "https://your-app.vercel.app",      # Add your production URL here
    "https://your-app.netlify.app",     # Or wherever you deploy
]
```

## Dockerfile for Cloud Run

Create a `Dockerfile` in your backend directory:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files and application code
COPY models/ ./models/
COPY apple_api_regression.py .

# Expose port (Cloud Run uses PORT env variable)
ENV PORT=8080
EXPOSE 8080

# Run the application with uvicorn
CMD uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}
```

## Create `requirements.txt`

In your backend directory:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
tensorflow==2.15.0
pillow==10.1.0
numpy==1.24.3
opencv-python-headless==4.8.1.78
python-multipart==0.0.6
```

## Deployment Steps

### 1. Initialize Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Build and Deploy to Cloud Run

From your backend directory:

```bash
# Build and deploy in one command
gcloud run deploy apple-oxidation-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 60 \
  --max-instances 10

# This will:
# - Build a Docker image from your code
# - Push it to Google Container Registry
# - Deploy it to Cloud Run
# - Give you a URL like: https://apple-oxidation-api-xxxxx.run.app
```

### 3. Test Your Deployment

```bash
# Get your Cloud Run URL
CLOUD_RUN_URL=$(gcloud run services describe apple-oxidation-api \
  --region us-central1 \
  --format 'value(status.url)')

echo "Your API is deployed at: $CLOUD_RUN_URL"

# Test the health endpoint
curl $CLOUD_RUN_URL/health
```

### 4. Update Frontend Environment Variables

Update `frontend/.env` with your Cloud Run URL:

```env
VITE_API_URL=https://apple-oxidation-api-xxxxx.run.app
```

For production deployments (Vercel, Netlify, etc.), set this environment variable in your hosting platform's settings.

## Production Considerations

### Authentication (Optional)

If you want to require authentication for API calls:

1. **Update Cloud Run deployment:**
```bash
gcloud run deploy apple-oxidation-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated  # Remove public access
```

2. **Add authentication to FastAPI:**
```python
from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization")

    token = authorization.split(" ")[1]
    # Verify Supabase JWT token here
    # Use supabase-py library to validate the token

@app.post("/analyze")
async def analyze_apple(
    file: UploadFile,
    variety: str = "combined",
    auth: str = Depends(verify_token)
):
    # Your existing code...
```

### Cost Optimization

**Cloud Run Pricing:**
- Only pay when requests are being processed
- Free tier: 2 million requests/month
- Billing based on CPU, memory, and request duration

**Tips to reduce costs:**
1. Set `--min-instances 0` (default) to scale to zero when not in use
2. Use `--max-instances 10` to prevent runaway costs
3. Optimize model loading (cache in memory)
4. Use smaller Docker images

### Monitoring

View logs and metrics:

```bash
# View logs
gcloud run logs read apple-oxidation-api --region us-central1

# View in Cloud Console
https://console.cloud.google.com/run
```

### CI/CD Deployment

For automatic deployments on code changes, use GitHub Actions:

Create `.github/workflows/deploy-cloud-run.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy apple-oxidation-api \
            --source ./backend \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated \
            --memory 2Gi \
            --cpu 2
```

## Troubleshooting

### Container fails to start
- Check logs: `gcloud run logs read apple-oxidation-api --region us-central1`
- Verify PORT environment variable is used correctly
- Ensure all model files are included in the container

### CORS errors
- Add your frontend domain to the `origins` list in CORS middleware
- Check that credentials are allowed: `allow_credentials=True`

### Timeout errors
- Increase timeout: `--timeout 300` (max 1 hour for 2nd gen)
- Optimize model loading (load once at startup, not per request)

### Out of memory
- Increase memory: `--memory 4Gi` (max 32Gi)
- Check model size and optimize if needed

## Next Steps

1. Set up custom domain for your API
2. Enable Cloud CDN for faster global access
3. Set up Cloud Monitoring alerts
4. Implement request logging and analytics
