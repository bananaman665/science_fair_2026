# 🍎 Backend Training Setup - Science Fair 2025

Welcome to the backend training environment! This setup will help you understand exactly how EfficientNet-B0 transfer learning works before applying it to your apple oxidation images.

## 📚 Learning Objectives

By working through this code, you'll understand:
1. **Transfer Learning**: How to adapt pre-trained models for new tasks
2. **EfficientNet-B0**: Modern CNN architecture and why it's perfect for mobile AI
3. **Training Pipeline**: Complete process from data loading to model saving
4. **API Integration**: How trained models serve predictions through REST APIs
5. **Production Ready**: Real-world ML deployment patterns

## 🏗️ Project Structure

```
backend/
├── main.py                          # FastAPI backend (minimal)
├── requirements.txt                 # Python dependencies
├── ml_training/                     # Training code and experiments
│   ├── train_efficientnet.py       # Main training script
│   ├── test_model.py               # Model testing and inference
│   ├── data/                       # Training data (auto-downloaded)
│   └── models/                     # Saved trained models
└── README.md                       # This file
```

## 🚀 Quick Start Guide

### Step 1: Environment Setup
```bash
# Your virtual environment should already be activated
# If not: source .venv/bin/activate

# Verify installation
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
python -c "import fastapi; print('FastAPI installed!')"
```

### Step 2: Train Your First Model
```bash
# Run the complete training demonstration
python ml_training/train_efficientnet.py
```

**What this does:**
- Downloads TensorFlow flowers dataset (5 classes, similar to your 4 oxidation levels)
- Creates EfficientNet-B0 model with transfer learning
- Trains in 2 phases: frozen base → fine-tuning
- Generates visualizations and saves trained model
- **Takes ~10-15 minutes on modern CPU, ~3-5 minutes with GPU**

### Step 3: Test the Trained Model
```bash
# After training completes, note the saved model path
# Example: ./ml_training/models/flower_classification_efficientnet_20250928_183045

# Test the model (update path as needed)
python -c "
from ml_training.test_model import demo_inference
model_path = './ml_training/models/flower_classification_efficientnet_XXXXXX_XXXXXX'  # Update this
tester = demo_inference(model_path)
print('Model testing demo complete!')
"
```

### Step 4: Start the API Server
```bash
# Set the model path (update with your actual path)
export MODEL_PATH="./ml_training/models/flower_classification_efficientnet_XXXXXX_XXXXXX"

# Start the FastAPI server
python main.py
```

Then visit: http://localhost:8000/docs to see the interactive API documentation!

## 🎯 Key Learning Points

### 1. Transfer Learning Process
The `train_efficientnet.py` script shows the exact 2-phase process:

**Phase 1 - Classification Head Training:**
```python
# Freeze the pre-trained EfficientNet-B0 base
base_model.trainable = False

# Train only the new classification layers
model.fit(train_data, epochs=10)
```

**Phase 2 - Fine-tuning:**
```python
# Unfreeze top layers for domain-specific learning
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Fine-tune with lower learning rate
model.compile(optimizer=Adam(lr=0.0001))
model.fit(train_data, epochs=10)
```

### 2. EfficientNet-B0 Architecture
```python
# Pre-trained feature extractor
base_model = tf.keras.applications.EfficientNetB0(
    weights='imagenet',      # Powerful pre-trained features
    include_top=False,       # Remove original classifier
    input_shape=(224, 224, 3)  # Standard input size
)

# Custom classification head for your task
model = tf.keras.Sequential([
    base_model,                              # Feature extraction
    tf.keras.layers.GlobalAveragePooling2D(), # Spatial pooling
    tf.keras.layers.Dropout(0.3),           # Regularization
    tf.keras.layers.Dense(128, activation='relu'), # Feature transformation
    tf.keras.layers.Dense(4, activation='softmax')  # 4 oxidation classes
])
```

### 3. Data Preprocessing
```python
def preprocess_image(image, label):
    # Resize to EfficientNet input size
    image = tf.image.resize(image, [224, 224])
    
    # Normalize to [0,1] range
    image = tf.cast(image, tf.float32) / 255.0
    
    # EfficientNet preprocessing (ImageNet normalization)
    image = tf.keras.applications.efficientnet.preprocess_input(image * 255.0)
    
    return image, label
```

### 4. API Integration
The `main.py` shows how your trained model will serve predictions:

```python
@app.post("/api/v1/analyze-apple")
async def analyze_apple(file: UploadFile = File(...)):
    # Load image from mobile app
    image = Image.open(io.BytesIO(await file.read()))
    
    # Preprocess for EfficientNet
    processed = preprocess_image(image)
    
    # Run inference
    predictions = model.predict(processed)
    
    # Return structured results
    return {
        "oxidation_score": calculate_score(predictions),
        "category": get_category(predictions),
        "confidence": float(np.max(predictions))
    }
```

## 🔬 From Flowers to Apples

This demo uses flowers, but the **exact same process** will work for your apple oxidation detection:

### Dataset Mapping
```
Flowers Demo          →  Apple Oxidation
─────────────────────    ─────────────────
daisy                →  Fresh (Day 0)
dandelion            →  Light (Days 1-2)  
roses                →  Medium (Days 3-4)
sunflowers           →  Heavy (Days 5+)
tulips               →  (Extra class - you have 4)
```

### Code Changes Needed
1. **Replace dataset loader**: Use your apple images instead of flowers
2. **Update class names**: ['Fresh', 'Light', 'Medium', 'Heavy']
3. **Modify scoring**: Convert predictions to 0-100 oxidation score
4. **Same architecture**: EfficientNet-B0 transfer learning unchanged

## 🎯 Expected Results

After training, you should see:
- **Training accuracy**: 90-95% (flowers are easy to distinguish)
- **Validation accuracy**: 85-90% (good generalization)
- **Training time**: 10-15 minutes total (both phases)
- **Model size**: ~20MB (perfect for mobile deployment)

## 🔧 Troubleshooting

### Common Issues

**1. TensorFlow/GPU Issues:**
```bash
# Check TensorFlow installation
python -c "import tensorflow as tf; print(tf.config.list_physical_devices())"

# If GPU issues, training will still work on CPU (just slower)
```

**2. Memory Issues:**
```bash
# Reduce batch size in train_efficientnet.py
self.batch_size = 16  # Instead of 32
```

**3. Dataset Download Issues:**
```bash
# Clear TensorFlow datasets cache
rm -rf ~/tensorflow_datasets/
```

## 🎓 Next Steps

Once you complete this demo:

1. **✅ Understand the training process** - You'll see exactly how transfer learning works
2. **✅ See API integration** - Understand how models serve predictions
3. **✅ Ready for apple data** - Apply the same process to your oxidation images
4. **✅ Science fair ready** - You'll have professional ML knowledge

## 📊 Performance Expectations

### Training Demo (Flowers)
- **Dataset**: 3,670 flower images, 5 classes
- **Accuracy**: ~90% validation accuracy expected
- **Time**: 10-15 minutes on modern CPU

### Your Apple Project
- **Dataset**: 400-600 apple images, 4 oxidation classes  
- **Accuracy**: 85%+ expected (apples have clear oxidation progression)
- **Time**: Similar training time
- **Deployment**: Same FastAPI backend, same mobile integration

## 🏆 Success Criteria

You'll know you understand the process when you can:
- [x] Explain why we use transfer learning instead of training from scratch
- [x] Describe the 2-phase training process
- [x] Understand EfficientNet-B0 architecture benefits
- [x] See how the trained model integrates with your API
- [x] Visualize and interpret training results

## 🔍 Code Deep Dive

### Most Important Files to Understand:

1. **`ml_training/train_efficientnet.py`** - The complete training pipeline
2. **`main.py`** - How trained models serve predictions via API
3. **`ml_training/test_model.py`** - Model inference and testing

### Key Functions to Study:

- `create_model()` - EfficientNet-B0 setup and transfer learning
- `train_phase_1()` & `train_phase_2()` - Two-phase training process
- `preprocess_image()` - Image preprocessing for EfficientNet
- `predict()` - Model inference pipeline

---

**Ready to start learning?** Run `python ml_training/train_efficientnet.py` and watch the magic happen! 🚀

The training process will show you exactly how professional ML systems work, and you'll be ready to apply this knowledge to your apple oxidation detection project.