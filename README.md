# 🍎 Apple Oxidation Detection - Science Fair 2025

**AI-Powered Assessment of Apple Freshness Using Computer Vision**

[![Project Status](https://img.shields.io/badge/Status-In%20Development-yellow)](https://github.com/your-username/science-fair-2025)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Flutter](https://img.shields.io/badge/Flutter-3.0%2B-blue)](https://flutter.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Project Overview

This project develops an AI-powered mobile application that analyzes photographs of apples to determine their oxidation level and freshness. Using transfer learning with EfficientNet-B0, our system classifies apple oxidation into four categories: Fresh, Light, Moderate, and Heavy oxidation.

**Key Innovation**: Real-time freshness assessment through smartphone photography, making food quality evaluation accessible to consumers and reducing food waste.

## 🏗️ Repository Structure

This is a **monorepo** containing all components of our science fair project:

```
science_fair_2025/
├── 📖 docs/                          # Project documentation
│   ├── Science_Fair_2025_Tech_Development_Plan.md
│   └── data_collection_guidelines/   # Team protocols & training
├── 🔬 backend/                       # Python ML/API server
│   ├── ml_models/                    # TensorFlow/Keras models
│   ├── api/                          # FastAPI endpoints
│   └── image_processing/             # OpenCV utilities
├── 📱 frontend/                      # Flutter mobile app
│   ├── lib/                          # Dart source code
│   └── assets/                       # UI resources
├── 📊 data_repository/               # Data collection & training
│   ├── 01_raw_images/               # Original photos
│   ├── 02_processed_images/         # Curated datasets
│   ├── 03_data_tracking/            # Collection logs
│   ├── 04_scripts/                  # Automation tools
│   └── 05_archive/                  # Historical data
└── 🔧 scripts/                      # Cross-project utilities
```

## 🧪 Scientific Approach

### Transfer Learning Strategy
- **Base Model**: EfficientNet-B0 (pre-trained on ImageNet)
- **Custom Classification**: 4-class oxidation assessment
- **Training Data**: 200-500 images per apple variety
- **Apple Varieties**: Red Delicious, Granny Smith, Gala

### Data Collection Protocol
- **Timeline**: 7-day oxidation progression per apple
- **Collection Rounds**: 4 rounds × 3 varieties × 7 days = 84 photo sessions
- **Standardization**: Controlled lighting, consistent angles, standardized backgrounds
- **Team Coordination**: Digital workflow with Google Drive synchronization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ with pip
- Flutter SDK 3.0+
- Git
- Google Drive API access (for data sync)

### 1. Clone and Setup
```bash
git clone https://github.com/your-username/science-fair-2025.git
cd science-fair-2025

# Setup data repository
./data_repository/04_scripts/setup_repository.sh

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Install Flutter dependencies
cd ../frontend
flutter pub get
```

### 2. Data Collection
```bash
# Create sample data structure
./data_repository/04_scripts/simple_sync.sh sample

# Check repository status
./data_repository/04_scripts/simple_sync.sh status

# Setup Google Drive sync (requires API credentials)
./data_repository/04_scripts/simple_sync.sh setup
```

### 3. Development

**Backend Development:**
```bash
cd backend
python -m uvicorn main:app --reload  # Start API server
```

**Frontend Development:**
```bash
cd frontend
flutter run                          # Launch mobile app
```

**Model Training:**
```bash
cd backend/ml_models
python train_model.py               # Train oxidation classifier
```

## 📋 Data Collection Workflow

Our team follows a rigorous data collection protocol:

1. **Apple Procurement**: 3 varieties, multiple specimens per variety
2. **Daily Photography**: Standardized photos at 24-hour intervals
3. **Digital Logging**: Automated tracking via Google Sheets integration
4. **Quality Control**: Team training and validation protocols
5. **Data Sync**: Automatic Google Drive backup and team collaboration

**Key Documents:**
- [Data Collection Guidelines](docs/data_collection_guidelines/Apple_Oxidation_Data_Collection_Guidelines.md)
- [Daily Checklist](docs/data_collection_guidelines/Daily_Collection_Checklist.md)
- [Team Training](docs/data_collection_guidelines/Team_Training_Presentation.md)

## 🔧 Technology Stack

### Machine Learning
- **Framework**: TensorFlow 2.x / Keras
- **Architecture**: EfficientNet-B0 with custom classification head
- **Training**: Transfer learning with fine-tuning
- **Deployment**: TensorFlow Lite for mobile inference

### Backend
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