# 🍎 Apple Oxidation Detection - Science Fair 2026# 🍎 Apple Oxidation Detection - Science Fair 2025



**AI-Powered Assessment of Apple Freshness Using Computer Vision****AI-Powered Assessment of Apple Freshness Using Computer Vision**



[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)[![Project Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/your-username/science-fair-2025)

[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://tensorflow.org)[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)[![Flutter](https://img.shields.io/badge/Flutter-3.0%2B-blue)](https://flutter.dev)

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Project Overview

## 🎯 Project Overview

This project develops an AI-powered system that analyzes photographs of apples to predict how many days since they were cut (oxidation level). Using transfer learning with MobileNetV2, our regression model predicts continuous days with **1.158 days Mean Absolute Error** on real-world test photos.

This project develops an AI-powered mobile application that analyzes photographs of apples to determine their oxidation level and freshness. Using transfer learning with EfficientNet-B0, our system classifies apple oxidation into four categories: Fresh, Light, Moderate, and Heavy oxidation.

**Key Achievement**: 21.2% accuracy improvement through solving domain shift problem.

**Key Innovation**: Real-time freshness assessment through smartphone photography, making food quality evaluation accessible to consumers and reducing food waste.

## 🏆 Results Summary

## 🏗️ Repository Structure

| Metric | Value |

|--------|-------|This is a **monorepo** containing all components of our science fair project:

| **Best MAE** | 1.158 days (~28 hours) |

| **Improvement** | 21.2% better than baseline |```

| **Strategy** | Train on original images, test on cropped |science_fair_2025/

| **Apple Variety** | Granny Smith model |├── 📖 docs/                          # Project documentation

│   ├── Science_Fair_2025_Tech_Development_Plan.md

## 🔬 Scientific Findings│   └── data_collection_guidelines/   # Team protocols & training

├── 🔬 backend/                       # Python ML/API server

### Domain Shift Solution│   ├── ml_models/                    # TensorFlow/Keras models

We discovered that background differences between training and test images caused accuracy problems:│   ├── api/                          # FastAPI endpoints

- **Training images**: Clean white backgrounds (controlled environment)│   └── image_processing/             # OpenCV utilities

- **Test images**: Cluttered phone backgrounds (real-world)├── 📱 frontend/                      # Flutter mobile app

│   ├── lib/                          # Dart source code

**Solution**: Keep training images original (rich context), but crop test images to remove backgrounds.│   └── assets/                       # UI resources

├── 📊 data_repository/               # Data collection & training

### Variety-Specific Models│   ├── 01_raw_images/               # Original photos

Different apple varieties oxidize at different rates:│   ├── 02_processed_images/         # Curated datasets

- **Granny Smith**: Slower oxidation, green color masks browning│   ├── 03_data_tracking/            # Collection logs

- **Gala**: Faster oxidation, more visible browning│   ├── 04_scripts/                  # Automation tools

│   └── 05_archive/                  # Historical data

Using variety-specific models improved accuracy significantly.└── 🔧 scripts/                      # Cross-project utilities

```

## 🏗️ Repository Structure

## 🧪 Scientific Approach

```

science_fair_2026/### Transfer Learning Strategy

├── 📖 docs/                          # Project documentation- **Base Model**: EfficientNet-B0 (pre-trained on ImageNet)

├── 🔬 backend/                       # Python ML/API server- **Custom Classification**: 4-class oxidation assessment

│   ├── apple_api_regression.py       # FastAPI server- **Training Data**: 200-500 images per apple variety

│   └── *.h5                          # Trained models (gitignored)- **Apple Varieties**: Red Delicious, Granny Smith, Gala

├── 📊 data_repository/               # Data collection

│   ├── 01_raw_images/               # Training photos (88 images)### Data Collection Protocol

│   ├── compare_images/              # Test photos (8 images)- **Timeline**: 7-day oxidation progression per apple

│   └── compare_images_cropped_manual/ # Cropped test photos- **Collection Rounds**: 4 rounds × 3 varieties × 7 days = 84 photo sessions

├── train_regression_model.py         # Model training script- **Standardization**: Controlled lighting, consistent angles, standardized backgrounds

├── test_both_varieties.py            # Variety testing script- **Team Coordination**: Digital workflow with Google Drive synchronization

├── manual_crop_apples.py             # Interactive cropping tool

└── MODEL_RESULTS.md                  # Detailed results## 🚀 Quick Start

```

### Prerequisites

## 🚀 Quick Start- Python 3.8+ with pip

- Flutter SDK 3.0+

### 1. Setup- Git

```bash- Google Drive API access (for data sync)

git clone https://github.com/bananaman665/science_fair_2026.git

cd science_fair_2026### 1. Clone and Setup

```bash

# Install dependenciesgit clone https://github.com/your-username/science-fair-2025.git

cd backendcd science-fair-2025

pip install -r requirements.txt

```# Setup data repository

./data_repository/04_scripts/setup_repository.sh

### 2. Train Model

```bash# Install Python dependencies

cd ..cd backend

python train_regression_model.py smith  # Train Granny Smith modelpip install -r requirements.txt

python train_regression_model.py gala   # Train Gala model

```# Install Flutter dependencies

cd ../frontend

### 3. Test Modelflutter pub get

```bash```

python test_both_varieties.py  # Compare both variety models

```### 2. Data Collection

```bash

### 4. Start API# Create sample data structure

```bash./data_repository/04_scripts/simple_sync.sh sample

cd backend

python apple_api_regression.py# Check repository status

# Server at http://localhost:8000./data_repository/04_scripts/simple_sync.sh status

```

# Setup Google Drive sync (requires API credentials)

### 5. Analyze Apple./data_repository/04_scripts/simple_sync.sh setup

```bash```

# Crop test image first (interactive tool)

python manual_crop_apples.py### 3. Development



# Then analyze**Backend Development:**

curl -X POST "http://localhost:8000/analyze?variety=smith" \```bash

     -F "file=@cropped_apple.jpg"cd backend

```python -m uvicorn main:app --reload  # Start API server

```

## 📊 Training Data

**Frontend Development:**

- **Total Photos**: 88 images```bash

- **Apple Varieties**: Gala (44), Granny Smith (44)  cd frontend

- **Time Range**: Days 0-5 of oxidationflutter run                          # Launch mobile app

- **Collection**: October 2025, standardized setup```



## 🔧 Technology Stack**Model Training:**

```bash

- **ML Framework**: TensorFlow/Kerascd backend/ml_models

- **Base Model**: MobileNetV2 (transfer learning)python train_model.py               # Train oxidation classifier

- **API**: FastAPI```

- **Image Processing**: OpenCV, PIL

- **Cropping**: Interactive manual tool## 📋 Data Collection Workflow



## 📈 Key ScriptsOur team follows a rigorous data collection protocol:



| Script | Purpose |1. **Apple Procurement**: 3 varieties, multiple specimens per variety

|--------|---------|2. **Daily Photography**: Standardized photos at 24-hour intervals

| `train_regression_model.py` | Train variety-specific models |3. **Digital Logging**: Automated tracking via Google Sheets integration

| `test_both_varieties.py` | Compare Smith vs Gala models |4. **Quality Control**: Team training and validation protocols

| `manual_crop_apples.py` | Interactive cropping for test images |5. **Data Sync**: Automatic Google Drive backup and team collaboration

| `backend/apple_api_regression.py` | REST API server |

**Key Documents:**

## 📝 Documentation- [Data Collection Guidelines](docs/data_collection_guidelines/Apple_Oxidation_Data_Collection_Guidelines.md)

- [Daily Checklist](docs/data_collection_guidelines/Daily_Collection_Checklist.md)

- **[MODEL_RESULTS.md](MODEL_RESULTS.md)** - Detailed results and findings- [Team Training](docs/data_collection_guidelines/Team_Training_Presentation.md)

- **[API_USAGE_GUIDE.md](API_USAGE_GUIDE.md)** - API documentation

- **[docs/](docs/)** - Additional documentation## 🔧 Technology Stack



## 📝 License### Machine Learning

- **Framework**: TensorFlow 2.x / Keras

MIT License - see [LICENSE](LICENSE)- **Architecture**: EfficientNet-B0 with custom classification head

- **Training**: Transfer learning with fine-tuning

---- **Deployment**: TensorFlow Lite for mobile inference



*Predicting apple freshness through computer vision* 🍎✨### Backend

- **API**: FastAPI (Python)
- **Image Processing**: OpenCV, PIL
- **Database**: PostgreSQL (metadata), filesystem (images)
- **Deployment**: Docker containers

### Frontend
- **Framework**: Flutter (Dart)
- **Camera**: camera plugin for image capture
- **HTTP**: dio for API communication
- **State Management**: Provider pattern

### DevOps & Collaboration
- **Version Control**: Git (monorepo structure)
- **Data Sync**: Google Drive API with automated backup
- **Documentation**: Markdown with comprehensive guides
- **Testing**: Unit tests for ML pipeline, widget tests for UI

## 📈 Project Timeline

**Phase 1 - Data Collection (Weeks 1-4)**
- [ ] Apple procurement and initial setup
- [ ] Daily data collection (4 rounds)
- [ ] Quality validation and team training

**Phase 2 - Model Development (Weeks 5-8)**
- [ ] Dataset curation and preprocessing
- [ ] Transfer learning implementation
- [ ] Model training and validation
- [ ] Performance optimization

**Phase 3 - Application Development (Weeks 9-11)**
- [ ] Backend API development
- [ ] Flutter mobile app implementation
- [ ] Integration testing
- [ ] User interface refinement

**Phase 4 - Science Fair Preparation (Week 12)**
- [ ] Final testing and bug fixes
- [ ] Presentation materials
- [ ] Demonstration preparation
- [ ] Documentation finalization

## 🧑‍🤝‍🧑 Team Collaboration

### Git Workflow
- **Main Branch**: Stable, deployable code
- **Feature Branches**: Individual development work
- **Pull Requests**: Code review and testing

### Data Management
- **Local Repository**: Individual team member workspaces
- **Google Drive**: Centralized data backup and sharing
- **Automated Sync**: Scripts handle bidirectional synchronization

### Communication
- **Documentation**: All protocols and procedures documented
- **Training Materials**: Comprehensive team onboarding
- **Progress Tracking**: Regular milestone reviews

## 🏆 Expected Outcomes

### Scientific Contributions
- **Novel Dataset**: Comprehensive apple oxidation image dataset
- **Practical Application**: Accessible food quality assessment tool
- **Reproducible Research**: Open-source methodology and code

### Technical Achievements
- **Mobile AI**: Real-time inference on consumer devices
- **Transfer Learning**: Effective domain adaptation for food science
- **User Experience**: Intuitive interface for non-technical users

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a science fair project, but we welcome feedback and suggestions:

1. Review our [documentation](docs/)
2. Check our [data collection protocols](docs/data_collection_guidelines/)
3. Examine our [technical approach](docs/Science_Fair_2025_Tech_Development_Plan.md)

## 📞 Contact

**Project Team**: [Your School Name] Science Fair 2025
**Project Advisor**: [Advisor Name]
**Contact**: [your-email@example.com]

---

*Building the future of food quality assessment, one apple at a time.* 🍎✨