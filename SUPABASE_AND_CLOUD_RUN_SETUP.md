# Complete Setup Guide: Supabase + Google Cloud Run

This guide walks you through setting up both **Supabase** (for authentication and database) and **Google Cloud Run** (for your ML API backend) for the Apple Oxidation App.

---

## Table of Contents

1. [Part 1: Supabase Setup](#part-1-supabase-setup)
2. [Part 2: Google Cloud Run Setup](#part-2-google-cloud-run-setup)
3. [Part 3: Connect Everything](#part-3-connect-everything)
4. [Part 4: Testing & Verification](#part-4-testing--verification)
5. [Troubleshooting](#troubleshooting)

---

# Part 1: Supabase Setup

Supabase provides:
- **User Authentication** (email/password, Google, Apple Sign-In)
- **Database** (PostgreSQL for storing scan history)
- **Row Level Security** (users can only see their own data)

## Step 1: Create a Supabase Account

1. Go to **https://supabase.com**
2. Click **"Start your project"** or **"Sign Up"**
3. Sign up with:
   - GitHub account (recommended), OR
   - Email and password
4. Verify your email if required

## Step 2: Create a New Project

1. Click **"New Project"**
2. Fill in:
   - **Name:** `apple-oxidation-app`
   - **Database Password:** Create a strong password (save this!)
   - **Region:** Choose closest to your users (e.g., `West US` or `East US`)
3. Click **"Create new project"**
4. Wait 1-2 minutes for setup to complete

## Step 3: Get Your API Keys

Once the project is ready:

1. Go to **Settings** (gear icon in sidebar)
2. Click **API** in the left menu
3. Copy these values (you'll need them later):

```
Project URL: https://xxxxxxxxxx.supabase.co
anon public key: eyJhbGci... (long string)
```

> ⚠️ **Keep these safe!** The anon key is safe to use in your frontend, but don't share your service_role key publicly.

## Step 4: Set Up the Database Table

You need a table to store user scan history.

### Option A: Using the SQL Editor (Recommended)

1. Go to **SQL Editor** in the sidebar
2. Click **"New query"**
3. Paste this SQL and click **"Run"**:

```sql
-- Create the user_scans table
CREATE TABLE IF NOT EXISTS user_scans (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  image_uri TEXT,
  variety TEXT,
  days_since_cut DECIMAL(5,2),
  oxidation_level TEXT,
  confidence_lower DECIMAL(5,2),
  confidence_upper DECIMAL(5,2),
  interpretation TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries by user
CREATE INDEX IF NOT EXISTS idx_user_scans_user_id ON user_scans(user_id);

-- Create index for ordering by date
CREATE INDEX IF NOT EXISTS idx_user_scans_created_at ON user_scans(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE user_scans ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own scans
CREATE POLICY "Users can view own scans" 
  ON user_scans FOR SELECT 
  USING (auth.uid() = user_id);

-- Policy: Users can insert their own scans
CREATE POLICY "Users can insert own scans" 
  ON user_scans FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own scans
CREATE POLICY "Users can update own scans" 
  ON user_scans FOR UPDATE 
  USING (auth.uid() = user_id);

-- Policy: Users can delete their own scans
CREATE POLICY "Users can delete own scans" 
  ON user_scans FOR DELETE 
  USING (auth.uid() = user_id);
```

4. You should see "Success. No rows returned" - this is correct!

### Option B: Using the Table Editor

1. Go to **Table Editor** in the sidebar
2. Click **"Create a new table"**
3. Create the table manually (more tedious)

## Step 5: Set Up Authentication

### Enable Email Authentication

1. Go to **Authentication** in the sidebar
2. Click **Providers** tab
3. **Email** should be enabled by default
4. Configure options:
   - ✅ Enable Email Confirmations (recommended for production)
   - ✅ Enable email change confirmations

### Enable Google OAuth (Optional)

1. In **Authentication > Providers**, find **Google**
2. Toggle it **ON**
3. You'll need:
   - **Client ID** from Google Cloud Console
   - **Client Secret** from Google Cloud Console

To get Google OAuth credentials:

1. Go to https://console.cloud.google.com/apis/credentials
2. Create **OAuth 2.0 Client ID**
3. Set **Authorized redirect URI** to:
   ```
   https://YOUR_PROJECT_REF.supabase.co/auth/v1/callback
   ```
4. Copy the Client ID and Secret to Supabase

### Enable Apple Sign-In (Optional - for iOS)

1. In **Authentication > Providers**, find **Apple**
2. Toggle it **ON**
3. You'll need an Apple Developer account ($99/year)
4. Follow Apple's [Sign in with Apple setup guide](https://developer.apple.com/sign-in-with-apple/get-started/)

## Step 6: Configure Site URL

1. Go to **Authentication > URL Configuration**
2. Set **Site URL** to:
   - For development: `http://localhost:5173`
   - For production: `https://your-app-domain.com`
3. Add **Redirect URLs**:
   ```
   http://localhost:5173/**
   https://your-app-domain.com/**
   capacitor://localhost/**
   http://localhost/**
   ```

---

# Part 2: Google Cloud Run Setup

Google Cloud Run hosts your ML prediction API.

## Step 1: Create Google Cloud Account

1. Go to **https://console.cloud.google.com**
2. Sign in with your Google account
3. Accept Terms of Service
4. Click **"Activate"** to start free trial
   - Get **$300 free credits** for 90 days!
   - Credit card required (won't be charged during trial)

## Step 2: Create a New Project

1. Click the project dropdown in the top bar
2. Click **"NEW PROJECT"**
3. Enter:
   - **Project name:** `apple-oxidation-app`
   - **Location:** Leave as "No organization"
4. Click **"CREATE"**
5. Click **"SELECT PROJECT"** when ready

## Step 3: Install Google Cloud CLI

### macOS:
```bash
brew install google-cloud-sdk
```

### Windows:
Download from: https://cloud.google.com/sdk/docs/install

### Linux:
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Verify Installation:
```bash
gcloud --version
```

## Step 4: Authenticate and Configure

```bash
# Login to Google Cloud (opens browser)
gcloud auth login

# List your projects
gcloud projects list

# Set your project (replace with your project ID)
gcloud config set project apple-oxidation-app

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 5: Prepare Backend Files

Your backend should already have these files. Verify they exist:

### `backend/Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files and code
COPY models/ ./models/
COPY *.h5 ./
COPY *.json ./
COPY apple_api_regression.py .

# Cloud Run uses PORT env variable
ENV PORT=8080
EXPOSE 8080

# Run the app
CMD uvicorn apple_api_regression:app --host 0.0.0.0 --port ${PORT}
```

### `backend/.dockerignore`

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
ml_training/
```

## Step 6: Deploy to Cloud Run

```bash
# Navigate to backend directory
cd /Users/andrew/projects/science_fair_2026/backend

# Deploy (first time takes 5-10 minutes)
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

**What each flag does:**
| Flag | Purpose |
|------|---------|
| `--source .` | Build from current directory |
| `--region us-central1` | Deploy to US Central (cheapest) |
| `--allow-unauthenticated` | Public API access |
| `--memory 2Gi` | 2GB RAM for TensorFlow |
| `--cpu 2` | 2 CPU cores |
| `--timeout 300` | 5 minute request timeout |
| `--max-instances 10` | Limit scaling to control costs |

## Step 7: Get Your API URL

After deployment completes, get your URL:

```bash
gcloud run services describe apple-oxidation-api \
  --region us-central1 \
  --format 'value(status.url)'
```

You'll get something like:
```
https://apple-oxidation-api-abc123xyz-uc.a.run.app
```

**Save this URL!** You'll need it for the frontend.

## Step 8: Test the Deployment

```bash
# Test root endpoint
curl https://YOUR-URL.run.app

# Test health endpoint
curl https://YOUR-URL.run.app/health

# Test with an image
curl -X POST "https://YOUR-URL.run.app/analyze?variety=combined" \
  -F "file=@/path/to/test-apple.jpg"
```

---

# Part 3: Connect Everything

Now connect your frontend to both services.

## Step 1: Update Frontend Environment Variables

Edit `frontend/.env`:

```bash
# Supabase Configuration
VITE_SUPABASE_URL=https://YOUR-PROJECT-ID.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your-key-here

# Google Cloud Run API
VITE_API_URL=https://apple-oxidation-api-abc123xyz-uc.a.run.app
```

Replace the placeholder values with your actual credentials from:
- **Supabase:** Settings > API
- **Cloud Run:** The URL from Step 7 above

## Step 2: Update CORS in Backend

Edit `backend/apple_api_regression.py` and add your frontend URLs to the origins list:

```python
origins = [
    # Local development
    "http://localhost:5173",
    "http://localhost:4173",
    
    # Mobile apps
    "capacitor://localhost",
    "http://localhost",
    
    # Production (add your deployed frontend URL)
    "https://your-app.vercel.app",
    "https://your-app.netlify.app",
    # Add any other domains where your frontend is hosted
]
```

Then redeploy:

```bash
cd /Users/andrew/projects/science_fair_2026/backend
gcloud run deploy apple-oxidation-api --source . --region us-central1
```

## Step 3: Test the Full Flow

1. Start the frontend:
```bash
cd /Users/andrew/projects/science_fair_2026/frontend
npm run dev
```

2. Open http://localhost:5173
3. Create an account / sign in
4. Take a photo and analyze
5. Check that history is saved (refresh page to verify)

---

# Part 4: Testing & Verification

## Test Supabase Connection

```bash
# From frontend directory
cd /Users/andrew/projects/science_fair_2026/frontend
npm run dev
```

Open browser console (F12) and check for errors. You should NOT see:
- "Missing Supabase environment variables"
- CORS errors

## Test Cloud Run API

```bash
# Health check
curl https://YOUR-CLOUD-RUN-URL/health

# Expected response:
{
  "status": "healthy",
  "models_loaded": ["combined", "gala", "smith"],
  ...
}
```

## Verify Database Table

In Supabase Dashboard:
1. Go to **Table Editor**
2. Select **user_scans**
3. After doing a scan in the app, you should see rows appear here

## Check Authentication

1. Go to **Authentication > Users** in Supabase
2. Create an account in your app
3. Verify the user appears in the dashboard

---

# Troubleshooting

## Supabase Issues

### "Missing Supabase environment variables"
- Check that `.env` file exists in `frontend/`
- Verify `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` are set
- Restart the dev server after editing `.env`

### "User not found" / Auth errors
- Check **Authentication > URL Configuration** in Supabase
- Make sure Site URL and Redirect URLs are correct
- Clear browser cache/localStorage

### "permission denied for table user_scans"
- Row Level Security is blocking the request
- Run the SQL from Step 4 again to ensure policies exist
- Check that the user is authenticated before querying

### History not saving
- Check browser console for errors
- Verify the user_scans table was created correctly
- Test with Supabase Table Editor to ensure RLS policies work

## Cloud Run Issues

### Build fails
```bash
# Check logs for errors
gcloud builds list --limit=1
gcloud builds log BUILD_ID
```

Common fixes:
- Verify Dockerfile syntax
- Ensure all model files (*.h5) are present
- Check requirements.txt has all dependencies

### Container crashes on start
```bash
# Check logs
gcloud run logs read apple-oxidation-api --region us-central1 --limit=50
```

Common causes:
- Missing model files
- Incorrect PORT usage
- Out of memory (increase `--memory`)

### CORS errors in browser
- Add your frontend URL to the `origins` list
- Redeploy the backend
- Clear browser cache

### "Container exceeded memory limit"
```bash
# Increase memory
gcloud run deploy apple-oxidation-api \
  --source . \
  --region us-central1 \
  --memory 4Gi
```

### Slow cold starts
- This is normal for TensorFlow models
- First request after idle takes 10-30 seconds
- Set `--min-instances 1` to keep one instance warm (costs more)

---

# Cost Summary

## Supabase Free Tier
- ✅ 500 MB database
- ✅ 1 GB file storage
- ✅ 50,000 monthly active users
- ✅ Unlimited API requests

**You'll likely stay free forever for a science fair project!**

## Google Cloud Run Free Tier
- ✅ 2 million requests/month
- ✅ 360,000 GB-seconds of memory
- ✅ 180,000 vCPU-seconds

**Estimated cost:** $0-5/month for typical science fair usage

---

# Quick Reference

## Supabase Dashboard
```
https://supabase.com/dashboard/project/YOUR-PROJECT-ID
```

## Cloud Run Console
```
https://console.cloud.google.com/run
```

## Deploy Commands

```bash
# Deploy backend to Cloud Run
cd backend
gcloud run deploy apple-oxidation-api --source . --region us-central1

# Get Cloud Run URL
gcloud run services describe apple-oxidation-api \
  --region us-central1 --format 'value(status.url)'

# View Cloud Run logs
gcloud run logs tail apple-oxidation-api --region us-central1

# Delete Cloud Run service (stops all charges)
gcloud run services delete apple-oxidation-api --region us-central1
```

## Environment Variables Checklist

| Variable | Where to Get It |
|----------|-----------------|
| `VITE_SUPABASE_URL` | Supabase > Settings > API > Project URL |
| `VITE_SUPABASE_ANON_KEY` | Supabase > Settings > API > anon public |
| `VITE_API_URL` | Cloud Run deployment URL |

---

**🎉 Congratulations!** You now have a fully deployed app with:
- User authentication via Supabase
- Secure database with row-level security
- ML API running on Google Cloud Run
- Auto-scaling and HTTPS built-in
