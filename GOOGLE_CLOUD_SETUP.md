# Google Cloud Run Setup Guide - Step by Step

This guide walks you through setting up Google Cloud and deploying your Apple Oxidation API.

## Part 1: Initial Google Cloud Setup

### Step 1: Create Google Cloud Account

1. Go to https://console.cloud.google.com
2. Sign in with your Google account
3. Accept the Terms of Service
4. You'll get **$300 in free credits** for 90 days!

### Step 2: Set Up Billing

1. Click **"Activate"** or **"Start Free Trial"** in the top banner
2. Fill in:
   - Country
   - Terms of Service agreement
   - Payment method (credit card - won't be charged during free trial)
3. Click **"Start my free trial"**

> **Note:** You won't be charged unless you manually upgrade to a paid account. The free trial gives you $300 credits.

### Step 3: Create a New Project

1. In the top bar, click the project dropdown (next to "Google Cloud")
2. Click **"NEW PROJECT"**
3. Enter project details:
   - **Project name:** `apple-oxidation-app` (or whatever you want)
   - **Location:** Leave as "No organization"
4. Click **"CREATE"**
5. Wait ~30 seconds for the project to be created
6. Click **"SELECT PROJECT"** when it appears

---

## Part 2: Install Google Cloud CLI

You need the `gcloud` command-line tool to deploy your API.

### For Mac:

```bash
# Install using Homebrew
brew install google-cloud-sdk

# Or download installer from:
# https://cloud.google.com/sdk/docs/install
```

### For Windows:

1. Download installer: https://cloud.google.com/sdk/docs/install
2. Run the installer
3. Follow the prompts (keep all defaults)
4. Restart your terminal/command prompt

### For Linux:

```bash
# Download and run installation script
curl https://sdk.cloud.google.com | bash

# Restart your shell
exec -l $SHELL
```

### Verify Installation:

```bash
gcloud --version
```

You should see something like:
```
Google Cloud SDK 456.0.0
```

---

## Part 3: Authenticate and Configure

### Step 1: Login to Google Cloud

```bash
gcloud auth login
```

This will:
1. Open your browser
2. Ask you to sign in to Google
3. Ask you to allow Google Cloud SDK access
4. Show "You are now authenticated"

### Step 2: Set Your Project

```bash
# List your projects
gcloud projects list

# Set your project (use the PROJECT_ID from the list)
gcloud config set project YOUR_PROJECT_ID
```

Example:
```bash
gcloud config set project apple-oxidation-app
```

### Step 3: Enable Required APIs

```bash
# Enable Cloud Run
gcloud services enable run.googleapis.com

# Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build
gcloud services enable cloudbuild.googleapis.com
```

This takes about 1-2 minutes. You'll see:
```
Operation "operations/..." finished successfully.
```

---

## Part 4: Prepare Your Backend for Deployment

### Step 1: Create Dockerfile

In your `backend/` directory, create a file called `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files and code
COPY models/ ./models/
COPY *.h5 ./
COPY *.json ./
COPY apple_api_regression.py .

# Cloud Run sets PORT env variable
ENV PORT=8080
EXPOSE 8080

# Run the app
CMD uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}
```

### Step 2: Create requirements.txt

In your `backend/` directory, create `requirements.txt`:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
tensorflow==2.15.0
pillow==10.1.0
numpy==1.24.3
opencv-python-headless==4.8.1.78
python-multipart==0.0.6
```

### Step 3: Create .dockerignore

In your `backend/` directory, create `.dockerignore`:

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
*.md
test_images/
```

---

## Part 5: Deploy to Cloud Run

### Navigate to Backend Directory

```bash
cd /Users/andrew/projects/science_fair_2026/backend
```

### Deploy Command

```bash
gcloud run deploy apple-oxidation-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

**What this does:**
- `apple-oxidation-api` - Your service name
- `--source .` - Build from current directory
- `--region us-central1` - Deploy to US Central (cheapest)
- `--allow-unauthenticated` - Anyone can call your API
- `--memory 2Gi` - 2GB RAM (needed for TensorFlow models)
- `--cpu 2` - 2 CPU cores for faster predictions
- `--timeout 300` - 5 minute timeout (for large images)
- `--max-instances 10` - Scale up to 10 containers max

### What Happens Next:

1. **Build starts** (takes 5-10 minutes first time):
   ```
   Building using Dockerfile and deploying container to Cloud Run service...
   ✓ Creating Container Repository...
   ✓ Uploading sources...
   ✓ Building Container... (This may take several minutes)
   ```

2. **Deployment:**
   ```
   ✓ Deploying Container...
   ✓ Creating Revision...
   ✓ Routing traffic...
   Done.
   ```

3. **You get a URL:**
   ```
   Service URL: https://apple-oxidation-api-xxxxx-uc.a.run.app
   ```

### Copy Your API URL

```bash
# Get your service URL
gcloud run services describe apple-oxidation-api \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## Part 6: Test Your Deployed API

### Test in Browser

Open your URL in a browser:
```
https://apple-oxidation-api-xxxxx-uc.a.run.app
```

You should see:
```json
{
  "name": "Apple Oxidation Days Prediction API - Variety Specific",
  "version": "4.0",
  "model_type": "regression",
  ...
}
```

### Test Health Endpoint

```bash
curl https://apple-oxidation-api-xxxxx-uc.a.run.app/health
```

### Test with an Image

```bash
# Upload a test image
curl -X POST "https://apple-oxidation-api-xxxxx-uc.a.run.app/analyze?variety=combined" \
  -F "file=@path/to/your/apple.jpg"
```

---

## Part 7: Update Frontend to Use Cloud Run

### Update .env

Edit `frontend/.env`:

```env
VITE_API_URL=https://apple-oxidation-api-xxxxx-uc.a.run.app
```

Replace `xxxxx` with your actual Cloud Run URL.

### Update CORS in Backend

Edit `backend/apple_api_regression.py` and add your frontend URL to origins:

```python
origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com",  # Add your actual frontend URL
]
```

Then redeploy:

```bash
gcloud run deploy apple-oxidation-api \
  --source . \
  --platform managed \
  --region us-central1
```

(Subsequent deploys are much faster - only ~2 minutes)

---

## Part 8: Monitor and Manage

### View Logs

```bash
# Real-time logs
gcloud run logs tail apple-oxidation-api --region us-central1

# Recent logs
gcloud run logs read apple-oxidation-api --region us-central1 --limit 50
```

### View in Console

1. Go to https://console.cloud.google.com/run
2. Click on `apple-oxidation-api`
3. See:
   - Metrics (requests, latency, errors)
   - Logs
   - Revisions
   - YAML configuration

### Update Deployment

After making code changes:

```bash
cd backend
gcloud run deploy apple-oxidation-api \
  --source . \
  --region us-central1
```

---

## Troubleshooting

### Build Fails

**Error:** `failed to build: error building image`

**Solution:** Check your Dockerfile syntax and make sure all files exist:
```bash
ls -la
# Should see: Dockerfile, requirements.txt, apple_api_regression.py, *.h5 files
```

### Container Crashes

**Error:** `Container failed to start`

**Solution:** Check logs:
```bash
gcloud run logs read apple-oxidation-api --region us-central1
```

Common issues:
- Missing model files (*.h5)
- Wrong Python version in Dockerfile
- PORT environment variable not used

### CORS Errors

**Error:** Browser shows "blocked by CORS policy"

**Solution:** Add your frontend URL to `origins` list in backend and redeploy.

### Out of Memory

**Error:** `Container instance memory limit exceeded`

**Solution:** Increase memory:
```bash
gcloud run deploy apple-oxidation-api \
  --source . \
  --memory 4Gi \
  --region us-central1
```

---

## Cost Estimates

**Cloud Run Pricing (as of 2024):**

**Free Tier (per month):**
- 2 million requests
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

**Your Configuration (2GB RAM, 2 CPU):**
- **Per request:** ~$0.00002 (if under free tier)
- **Example:** 1,000 requests/month = FREE (well under 2M limit)
- **Example:** 100,000 requests/month = FREE or ~$2-5/month

**Cold starts:** Free (first request after idle)

**You'll likely stay in the free tier unless you get thousands of users!**

---

## Next Steps

1. ✅ Deploy backend to Cloud Run
2. ✅ Update frontend .env with Cloud Run URL
3. ✅ Test the integration
4. 🚀 Deploy frontend to Vercel/Netlify
5. 📱 Build mobile apps with Capacitor

---

## Quick Reference Commands

```bash
# Deploy
gcloud run deploy apple-oxidation-api --source . --region us-central1

# Get URL
gcloud run services describe apple-oxidation-api --region us-central1 --format 'value(status.url)'

# View logs
gcloud run logs tail apple-oxidation-api --region us-central1

# Delete service (to stop charges)
gcloud run services delete apple-oxidation-api --region us-central1
```

---

**You're all set! 🎉** Your API will be running on Google Cloud Run with automatic scaling, HTTPS, and global CDN!
