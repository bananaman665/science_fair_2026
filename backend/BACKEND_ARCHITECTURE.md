# 🍎 Backend Architecture - Apple Oxidation Detection API

**Project:** Science Fair 2025 - Apple Oxidation Detection System  
**Date:** September 28, 2025  
**Version:** 1.0  

---

## 🎯 Architecture Overview

The backend serves as the core AI-powered engine for apple oxidation detection, built as a modern REST API that processes images and returns oxidation analysis results. This Python-based system integrates our trained EfficientNet-B0 transfer learning model with a robust web service architecture.

**Core Purpose:** Receive apple photographs from Flutter mobile app, analyze oxidation state using ML model, return structured oxidation assessment data.

---

## 🏗️ Technology Stack

### **Core Framework**
- **FastAPI** - Modern, high-performance Python web framework
  - Automatic API documentation (OpenAPI/Swagger)
  - Built-in data validation with Pydantic
  - Async support for high performance
  - Excellent for ML model serving

### **Machine Learning Stack**
- **TensorFlow 2.x/Keras** - ML model serving and inference
- **EfficientNet-B0** - Pre-trained CNN with custom classification head
- **OpenCV** - Image preprocessing and computer vision operations
- **PIL (Pillow)** - Image manipulation and format handling
- **NumPy** - Numerical operations for image arrays
- **TensorFlow Lite** - Optional mobile-optimized model format

### **Data & Storage**
- **PostgreSQL** - Relational database for metadata storage
- **SQLAlchemy** - Object-Relational Mapping (ORM)
- **File System** - Local image storage (with S3 migration path)
- **Alembic** - Database migrations

### **Additional Libraries**
- **Pydantic** - Data models and input validation
- **python-multipart** - File upload handling
- **python-dotenv** - Environment configuration management
- **Uvicorn** - ASGI server for FastAPI
- **Pytest** - Unit testing framework

---

## 🛠️ API Design

### **Core Endpoints**

```
POST /api/v1/analyze-apple     # Primary image analysis endpoint
GET  /api/v1/analysis/{id}     # Retrieve specific analysis results
GET  /api/v1/history           # Get analysis history
GET  /api/v1/health            # System health check
POST /api/v1/feedback          # User feedback for model improvement
GET  /api/v1/docs              # Auto-generated API documentation
```

### **Primary Endpoint Details**

#### `POST /api/v1/analyze-apple`
**Request:**
```json
{
  "content-type": "multipart/form-data",
  "body": {
    "image": "binary_image_data",
    "apple_variety": "Red Delicious|Granny Smith|Gala",  // optional
    "user_id": "string",  // optional
    "metadata": {  // optional
      "timestamp": "ISO_datetime",
      "location": "string"
    }
  }
}
```

**Response:**
```json
{
  "analysis_id": "uuid4",
  "oxidation_score": 45,  // 0-100 scale
  "oxidation_category": "Light",  // Fresh|Light|Medium|Heavy
  "confidence": 0.89,  // 0.0-1.0
  "processing_time_ms": 234,
  "timestamp": "2025-09-28T10:30:00Z",
  "model_version": "v1.0.0",
  "image_metadata": {
    "width": 224,
    "height": 224,
    "format": "JPEG"
  }
}
```

#### `GET /api/v1/history`
**Query Parameters:**
```
?limit=20&offset=0&user_id=optional&date_from=ISO_date&date_to=ISO_date
```

**Response:**
```json
{
  "total_count": 156,
  "results": [
    {
      "analysis_id": "uuid4",
      "oxidation_score": 45,
      "oxidation_category": "Light",
      "timestamp": "2025-09-28T10:30:00Z",
      "apple_variety": "Red Delicious"
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "has_next": true
  }
}
```

---

## 🔄 Processing Pipeline

### **Image Analysis Workflow**

```
1. 📥 Image Reception & Validation
   ├── File format validation (JPEG/PNG/WEBP)
   ├── File size check (max 10MB)
   ├── Image dimensions validation
   ├── Basic corruption detection
   └── Security scan (malicious content)

2. 🔧 Image Preprocessing
   ├── Resize to 224x224 pixels (EfficientNet input)
   ├── ImageNet normalization (mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
   ├── Color space conversion (RGB consistency)
   ├── Optional: Brightness/contrast enhancement
   └── Array conversion for TensorFlow

3. 🧠 ML Model Inference
   ├── Load EfficientNet-B0 model (cached in memory)
   ├── Forward pass through network
   ├── Extract softmax probabilities
   ├── Confidence threshold validation
   └── Category classification

4. 📊 Post-processing & Response
   ├── Convert probabilities to 0-100 oxidation score
   ├── Map to categorical labels (Fresh/Light/Medium/Heavy)
   ├── Store results in PostgreSQL
   ├── Generate unique analysis ID
   ├── Log performance metrics
   └── Format JSON response
```

### **Error Handling Strategy**
- **Image Validation Errors**: Clear error messages with correction suggestions
- **Model Inference Failures**: Graceful degradation with retry logic
- **Database Errors**: Transaction rollback and user notification
- **Performance Monitoring**: Request timing and resource usage tracking

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connection & session management
│   │
│   ├── models/                    # Pydantic data models
│   │   ├── __init__.py
│   │   ├── analysis.py            # Analysis request/response models
│   │   ├── database_models.py     # SQLAlchemy ORM models
│   │   └── responses.py           # API response schemas
│   │
│   ├── api/                       # API route handlers
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── apple.py           # Apple analysis endpoints
│   │       ├── history.py         # Analysis history endpoints
│   │       └── health.py          # Health check endpoints
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── image_processor.py     # Image preprocessing pipeline
│   │   ├── ml_predictor.py        # ML model inference service
│   │   ├── database_service.py    # Database operations
│   │   └── analysis_service.py    # Core analysis workflow
│   │
│   ├── ml_models/                 # Machine learning components
│   │   ├── __init__.py
│   │   ├── model_loader.py        # Model loading and caching
│   │   ├── predictor.py           # Prediction interface
│   │   └── saved_models/          # TensorFlow SavedModel files
│   │       ├── efficientnet_v1.0.0/
│   │       └── metadata.json
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── image_utils.py         # Image manipulation helpers
│       ├── logging_config.py      # Structured logging setup
│       ├── exceptions.py          # Custom exception classes
│       └── validators.py          # Input validation functions
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest configuration
│   ├── test_api/                 # API endpoint tests
│   ├── test_services/            # Business logic tests
│   ├── test_ml_models/           # Model inference tests
│   └── test_utils/               # Utility function tests
│
├── migrations/                    # Database migrations (Alembic)
│   ├── versions/
│   └── alembic.ini
│
├── scripts/                       # Development and deployment scripts
│   ├── setup_database.py
│   ├── load_test_data.py
│   └── model_performance_test.py
│
├── requirements/                  # Dependency management
│   ├── base.txt                  # Core dependencies
│   ├── development.txt           # Dev-only dependencies
│   └── production.txt            # Production dependencies
│
├── docker/                       # Container configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── README.md                     # Backend-specific documentation
└── BACKEND_ARCHITECTURE.md      # This document
```

---

## 🗄️ Database Design

### **Analysis Results Table**
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_path VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255),
    
    -- ML Results
    oxidation_score INTEGER NOT NULL CHECK (oxidation_score >= 0 AND oxidation_score <= 100),
    oxidation_category VARCHAR(20) NOT NULL CHECK (oxidation_category IN ('Fresh', 'Light', 'Medium', 'Heavy')),
    confidence FLOAT NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    model_version VARCHAR(20) NOT NULL,
    
    -- Apple Information
    apple_variety VARCHAR(50),  -- Red Delicious, Granny Smith, Gala
    
    -- Technical Metadata
    processing_time_ms INTEGER NOT NULL,
    image_width INTEGER,
    image_height INTEGER,
    image_format VARCHAR(10),
    
    -- User & Session
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_oxidation_category ON analyses(oxidation_category);
```

### **Model Performance Tracking**
```sql
CREATE TABLE model_performance (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(20) NOT NULL,
    accuracy_score FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    test_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    notes TEXT
);
```

---

## 🔧 Key Implementation Components

### **ML Model Service**
```python
class AppleOxidationPredictor:
    """Core ML prediction service for apple oxidation detection."""
    
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = ['Fresh', 'Light', 'Medium', 'Heavy']
        self.input_size = (224, 224, 3)
    
    def preprocess_image(self, image: PIL.Image) -> np.ndarray:
        """Preprocess image for EfficientNet inference."""
        # Resize to model input size
        image = image.resize((224, 224))
        
        # Convert to array and normalize
        image_array = np.array(image) / 255.0
        
        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image_array = (image_array - mean) / std
        
        # Add batch dimension
        return np.expand_dims(image_array, axis=0)
    
    def predict(self, image: PIL.Image) -> dict:
        """Run prediction on preprocessed image."""
        processed_image = self.preprocess_image(image)
        
        # Model inference
        predictions = self.model.predict(processed_image)
        
        # Extract results
        confidence = float(np.max(predictions))
        predicted_class = int(np.argmax(predictions))
        category = self.class_names[predicted_class]
        
        # Convert to 0-100 oxidation score
        oxidation_score = self._calculate_oxidation_score(predictions)
        
        return {
            'oxidation_score': oxidation_score,
            'oxidation_category': category,
            'confidence': confidence,
            'raw_predictions': predictions.tolist()
        }
    
    def _calculate_oxidation_score(self, predictions: np.ndarray) -> int:
        """Convert categorical predictions to 0-100 oxidation score."""
        # Weight categories: Fresh=0, Light=33, Medium=66, Heavy=100
        weights = np.array([0, 33, 66, 100])
        score = np.sum(predictions[0] * weights)
        return int(np.round(score))
```

### **Image Processing Service**
```python
class ImageProcessor:
    """Image validation and preprocessing utilities."""
    
    ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_DIMENSION = 224
    
    @classmethod
    def validate_image(cls, image_file) -> tuple[bool, str]:
        """Validate uploaded image file."""
        try:
            # Check file size
            if len(image_file.read()) > cls.MAX_FILE_SIZE:
                return False, "Image file too large (max 10MB)"
            
            image_file.seek(0)  # Reset file pointer
            
            # Open and validate image
            image = PIL.Image.open(image_file)
            
            # Check format
            if image.format not in cls.ALLOWED_FORMATS:
                return False, f"Unsupported format. Use: {', '.join(cls.ALLOWED_FORMATS)}"
            
            # Check dimensions
            if min(image.size) < cls.MIN_DIMENSION:
                return False, f"Image too small. Minimum {cls.MIN_DIMENSION}x{cls.MIN_DIMENSION}"
            
            return True, "Valid image"
            
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    @classmethod
    def enhance_image(cls, image: PIL.Image) -> PIL.Image:
        """Apply basic image enhancement for better model performance."""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Optional: Apply subtle contrast enhancement
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)  # Slight contrast boost
        
        return image
```

---

## 🚀 Development Phases

### **Phase 1: Foundation Setup (Week 8)**
**Goals:** Establish core API structure and basic functionality

**Tasks:**
- [ ] Initialize FastAPI project with proper structure
- [ ] Set up PostgreSQL database and SQLAlchemy models
- [ ] Implement basic image upload endpoint
- [ ] Create health check and API documentation
- [ ] Set up development environment with Docker
- [ ] Configure logging and error handling

**Deliverables:**
- Working FastAPI server with `/health` endpoint
- Database schema and connection
- Basic image upload validation
- Project documentation

### **Phase 2: ML Model Integration (Week 9)**
**Goals:** Integrate trained EfficientNet model and implement prediction pipeline

**Tasks:**
- [ ] Load and cache EfficientNet-B0 model
- [ ] Implement image preprocessing pipeline
- [ ] Create ML prediction service
- [ ] Integrate model with API endpoints
- [ ] Add confidence thresholding and error handling
- [ ] Implement oxidation score calculation

**Deliverables:**
- Working `/analyze-apple` endpoint
- ML model serving infrastructure
- Image preprocessing pipeline
- Prediction result storage

### **Phase 3: API Enhancement (Week 10)**
**Goals:** Complete API functionality and add production features

**Tasks:**
- [ ] Implement analysis history endpoints
- [ ] Add user session management
- [ ] Create feedback collection system
- [ ] Add comprehensive error handling
- [ ] Implement API rate limiting
- [ ] Add performance monitoring

**Deliverables:**
- Complete API with all endpoints
- User session management
- Performance monitoring
- Comprehensive error handling

### **Phase 4: Production Readiness (Week 11)**
**Goals:** Prepare for deployment and testing

**Tasks:**
- [ ] Create Docker production configuration
- [ ] Add comprehensive unit and integration tests
- [ ] Implement logging and monitoring
- [ ] Performance optimization and caching
- [ ] Security enhancements
- [ ] API documentation finalization

**Deliverables:**
- Production-ready Docker containers
- Comprehensive test suite
- Performance benchmarks
- Security validation

---

## 📊 Performance Targets

### **Response Time Goals**
- **Image Analysis**: < 1 second end-to-end
- **History Retrieval**: < 200ms
- **Health Check**: < 50ms

### **Throughput Targets**
- **Concurrent Users**: 50+ simultaneous requests
- **Daily Analyses**: 10,000+ image analyses
- **Uptime**: 99.9% availability

### **Model Performance**
- **Accuracy**: 85%+ on validation set
- **Confidence**: Average confidence > 0.8
- **Consistency**: < 5% variance in repeated predictions

---

## 🔒 Security Considerations

### **Input Validation**
- File type and size restrictions
- Image content validation
- SQL injection prevention
- XSS protection

### **Authentication & Authorization**
- Optional user authentication system
- API key management for mobile app
- Rate limiting per user/IP
- Secure session handling

### **Data Protection**
- Image data encryption at rest
- Secure database connections
- HTTPS enforcement
- User data privacy compliance

---

## 🧪 Testing Strategy

### **Unit Tests**
- Image processing functions
- ML model prediction logic
- Database operations
- Utility functions

### **Integration Tests**
- API endpoint functionality
- Database integration
- ML model integration
- Error handling scenarios

### **Performance Tests**
- Load testing with multiple concurrent requests
- Memory usage monitoring
- Response time benchmarking
- Model inference speed testing

### **End-to-End Tests**
- Complete image analysis workflow
- API contract validation
- Flutter app integration testing
- Error scenario validation

---

## 📈 Monitoring & Observability

### **Application Metrics**
- Request/response times
- Error rates and types
- ML model accuracy trends
- Database query performance

### **Infrastructure Metrics**
- CPU and memory usage
- Disk I/O and storage
- Network latency
- Database connection health

### **Business Metrics**
- Daily analysis volume
- User engagement patterns
- Apple variety distribution
- Oxidation category trends

---

## 🎓 Educational Outcomes

### **Technical Skills Developed**
- **Modern Web Development**: FastAPI, REST API design, async programming
- **Machine Learning Engineering**: Model serving, inference optimization, production ML
- **Database Design**: PostgreSQL, SQLAlchemy ORM, data modeling
- **Software Architecture**: Clean code principles, separation of concerns, scalability
- **DevOps**: Docker containerization, CI/CD concepts, monitoring

### **Computer Science Concepts**
- **API Design**: RESTful principles, HTTP methods, status codes
- **Data Structures**: Image arrays, database schemas, JSON serialization
- **Algorithms**: Image processing, neural network inference, optimization
- **Software Engineering**: Testing, documentation, version control

### **Real-World Applications**
- **Production Systems**: Scalable architecture, error handling, monitoring
- **AI/ML Deployment**: Model serving, performance optimization, validation
- **Food Technology**: Computer vision applications, quality assessment systems

---

## 🔮 Future Enhancements

### **Short-term Improvements**
- **Batch Processing**: Analyze multiple images simultaneously
- **Model Versioning**: A/B testing for model improvements
- **Advanced Preprocessing**: Automated image enhancement algorithms
- **Caching Layer**: Redis for frequently accessed data

### **Long-term Features**
- **Real-time Analysis**: WebSocket connections for live processing
- **Model Retraining**: Automated retraining pipeline with new data
- **Multi-Food Support**: Extend to other fruits and vegetables
- **Advanced Analytics**: Trend analysis and predictive insights

### **Research Opportunities**
- **Model Architecture**: Experiment with newer CNN architectures
- **Data Augmentation**: Advanced augmentation techniques
- **Explainable AI**: Visual explanations of model decisions
- **Edge Deployment**: Optimize for mobile inference

---

## 📚 Learning Resources

### **FastAPI Development**
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Python API Development Fundamentals](https://realpython.com/fastapi-python-web-apis/)

### **Machine Learning Engineering**
- [TensorFlow Model Serving Guide](https://www.tensorflow.org/tfx/guide/serving)
- [ML Engineering Best Practices](https://developers.google.com/machine-learning/guides/rules-of-ml)

### **Computer Vision**
- [OpenCV Python Tutorials](https://opencv-python-tutroals.readthedocs.io/)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)

### **Database Design**
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

---

## 📞 Implementation Support

### **Team Coordination**
- **Backend Lead**: Responsible for API development and ML integration
- **Data Engineer**: Database design and optimization
- **ML Engineer**: Model integration and performance tuning
- **DevOps**: Docker configuration and deployment setup

### **Development Workflow**
1. **Feature Planning**: Define requirements and API contracts
2. **Implementation**: Code development with unit tests
3. **Integration**: Test with database and ML components  
4. **Validation**: End-to-end testing with Flutter frontend
5. **Documentation**: Update API docs and architecture notes

---

**Document Version**: 1.0  
**Last Updated**: September 28, 2025  
**Next Review**: Week 8 of development timeline  

*This architecture document serves as the blueprint for our backend development, ensuring we build a robust, scalable, and educational system for apple oxidation detection.* 🍎✨