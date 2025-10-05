# ML Models Directory

This directory contains your trained EfficientNet-B0 models.

## 📁 Directory Structure:
```
models/
├── colab_flower_demo/          # Model trained in Colab (flowers dataset)
│   ├── saved_model.pb         # TensorFlow SavedModel format
│   ├── variables/             # Model weights and variables
│   └── metadata.json          # Model info (classes, accuracy, etc.)
├── apple_oxidation_v1/         # Your first apple oxidation model
└── apple_oxidation_v2/         # Improved apple model (future)
```

## 🚀 How to Add Your Colab Model:

1. **Download from Colab**: Look for the `.zip` file created by the notebook
2. **Extract Here**: Unzip the model folder into this directory
3. **Test Integration**: Use `../test_with_colab_model.py` to test with FastAPI
4. **Deploy**: Your model is ready for production!

## 🍎 Model Progression:

- **Phase 1**: Colab flower demo (learning transfer learning)
- **Phase 2**: Apple oxidation model (your science fair project)
- **Phase 3**: Optimized model (mobile deployment)

Each model follows the same structure and can be loaded by your FastAPI backend!