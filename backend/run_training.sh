#!/bin/bash
# Training runner script that ensures virtual environment is activated

echo "🔄 Activating virtual environment..."
source .venv/bin/activate

echo "🐍 Python environment:"
which python
python --version

echo "📦 TensorFlow check:"
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')" 2>/dev/null || echo "TensorFlow not found - check installation"

echo "🚀 Starting conceptual demo (avoids macOS TensorFlow issues)..."
python ml_training/concept_demo.py