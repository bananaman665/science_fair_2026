#!/bin/bash
# Startup script for Apple Analysis API

echo "🍎 Starting Apple Analysis API..."
echo "📁 Working directory: $(pwd)"

# Activate virtual environment
echo "🔄 Activating virtual environment..."
cd /Users/andrew/projects/science_fair_2026/backend
source .venv/bin/activate

# Change to ml_training directory
cd ml_training

# Check if model files exist
if [ ! -f "apple_model_local_1808.h5" ]; then
    echo "❌ Model file not found!"
    exit 1
fi

if [ ! -f "model_metadata.json" ]; then
    echo "❌ Metadata file not found!"
    exit 1
fi

echo "✅ Model files found"
echo "🚀 Starting FastAPI server..."
echo "📡 Server will be available at: http://localhost:8000"
echo "📋 API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python production_apple_api.py