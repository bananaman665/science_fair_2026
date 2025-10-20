#!/bin/bash
# Start the Apple Oxidation Days Prediction API

echo "🍎 Starting Apple Oxidation Days Prediction API..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 Interactive docs at: http://localhost:8000/docs"
echo ""

cd backend
source .venv/bin/activate
python apple_api_regression.py
