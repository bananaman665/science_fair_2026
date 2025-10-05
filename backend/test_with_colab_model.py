#!/usr/bin/env python3
"""
Test FastAPI Backend with Colab-Trained Model
Science Fair 2025 - Integration Testing

This script helps you test your FastAPI backend with the model
you trained in Google Colab.
"""

import os
import sys
import subprocess
import requests
import json
from pathlib import Path

def setup_instructions():
    """Print setup instructions for the user."""
    print("🎯 How to Test Your Colab Model with FastAPI Backend")
    print("=" * 60)
    print()
    print("📦 STEP 1: Download Your Model from Colab")
    print("   - In Colab, look for the downloadable .zip file")
    print("   - Download it (e.g., 'flower_efficientnet_colab_20251004_123456.zip')")
    print("   - Extract it to your backend/ml_training/models/ folder")
    print()
    print("📁 STEP 2: Set Up Model Directory")
    print("   Your folder structure should look like:")
    print("   backend/ml_training/models/")
    print("   └── your_model_folder/")
    print("       ├── saved_model.pb")
    print("       ├── variables/")
    print("       └── metadata.json")
    print()
    print("🚀 STEP 3: Start the API Server")
    print("   Run this script with the model path:")
    print("   python test_with_colab_model.py path/to/your/model")
    print()
    print("🧪 STEP 4: Test the API")
    print("   The script will:")
    print("   - Start your FastAPI server")
    print("   - Test all endpoints")
    print("   - Show you how it works")
    print()
    
def test_api_endpoints(base_url="http://localhost:8000"):
    """Test all API endpoints."""
    print("🧪 Testing API Endpoints...")
    print("-" * 40)
    
    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
        
        # Test health check
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        health_data = response.json()
        print(f"   Model loaded: {health_data.get('model_loaded')}")
        print()
        
        # Test model info
        response = requests.get(f"{base_url}/api/v1/model-info")
        if response.status_code == 200:
            print(f"✅ Model info: {response.status_code}")
            model_info = response.json()
            print(f"   Classes: {model_info.get('classes')}")
            print(f"   Input size: {model_info.get('input_size')}")
        else:
            print(f"❌ Model info: {response.status_code} - {response.text}")
        print()
        
        # Test demo endpoint
        response = requests.get(f"{base_url}/api/v1/demo")
        print(f"✅ Demo endpoint: {response.status_code}")
        print("   This shows how your Flutter app will interact with the API")
        print()
        
        # Test interactive docs
        print("📚 Interactive API Documentation:")
        print(f"   Open in browser: {base_url}/docs")
        print("   This is where you can test image uploads!")
        print()
        
        return True
        
    except requests.ConnectionError:
        print("❌ Cannot connect to API server")
        print("   Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def start_api_server(model_path):
    """Start the FastAPI server with the model."""
    print(f"🚀 Starting API server with model: {model_path}")
    
    # Set environment variable
    env = os.environ.copy()
    env["MODEL_PATH"] = model_path
    
    # Start server
    cmd = [sys.executable, "main.py"]
    print(f"   Command: MODEL_PATH={model_path} python main.py")
    print("   Server will start on: http://localhost:8000")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run(cmd, env=env, cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")

def main():
    """Main function."""
    print("🍎 Apple Oxidation Detection - Backend Testing")
    print("=" * 50)
    print()
    
    if len(sys.argv) < 2:
        setup_instructions()
        
        # Check if there are any model directories
        models_dir = Path(__file__).parent / "ml_training" / "models"
        if models_dir.exists():
            model_folders = [f for f in models_dir.iterdir() if f.is_dir()]
            if model_folders:
                print("🔍 Found existing model folders:")
                for i, folder in enumerate(model_folders, 1):
                    print(f"   {i}. {folder.name}")
                print()
                print("💡 To use one of these, run:")
                print(f"   python {sys.argv[0]} ml_training/models/FOLDER_NAME")
        
        return
    
    model_path = sys.argv[1]
    
    # Validate model path
    if not os.path.exists(model_path):
        print(f"❌ Model path does not exist: {model_path}")
        print()
        print("💡 Make sure you:")
        print("   1. Downloaded your model from Colab")
        print("   2. Extracted it to the correct location")
        print("   3. Provided the correct path")
        return
    
    # Check for required files
    required_files = ["saved_model.pb", "variables"]
    missing_files = []
    
    for file_name in required_files:
        file_path = os.path.join(model_path, file_name)
        if not os.path.exists(file_path):
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Missing required model files: {missing_files}")
        print("   Your model folder should contain:")
        for file_name in required_files:
            print(f"   - {file_name}")
        return
    
    print(f"✅ Model path validated: {model_path}")
    print()
    
    # Start the server
    start_api_server(model_path)

if __name__ == "__main__":
    main()