# System Architecture

This document describes the architecture and design of the Autism Emotion Detection system.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Overview](#component-overview)
- [Data Flow](#data-flow)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Model Integration](#model-integration)
- [Technology Stack](#technology-stack)

## 🏗️ Overview

The Autism Emotion Detection system is a full-stack web application that processes facial images to detect and classify emotions. The system consists of three main components:

1. **Frontend** - React-based web interface
2. **Backend** - Flask REST API server
3. **ML Model** - Custom-trained CNN or DeepFace

## 🎯 System Architecture

```mermaid
graph TB
    User[User Browser] -->|HTTP/HTTPS| Frontend[React Frontend]
    Frontend -->|REST API| Backend[Flask Backend]
    Backend -->|Load Model| Model[Custom CNN Model]
    Backend -->|Fallback| DeepFace[DeepFace Library]
    Frontend -->|Webcam Stream| Camera[User Webcam]
    Frontend -->|Image Upload| FileUpload[File System]
    Backend -->|Process Image| OpenCV[OpenCV Processing]
    OpenCV -->|Face Detection| HaarCascade[Haar Cascade]
    HaarCascade -->|Preprocess| Model
    Model -->|Predictions| Backend
    Backend -->|JSON Response| Frontend
    Frontend -->|Display Results| User
```

## 🔄 Component Overview

### Frontend Components

```mermaid
graph LR
    App[App.js] --> EmotionDetector[EmotionDetector Component]
    EmotionDetector --> VideoElement[Video Element]
    EmotionDetector --> CanvasElement[Canvas Element]
    EmotionDetector --> ResultsDisplay[Results Display]
    EmotionDetector -->|API Calls| Axios[Axios HTTP Client]
    Axios -->|POST /api/detect-emotion| BackendAPI[Backend API]
    Axios -->|POST /api/detect-emotion-file| BackendAPI
```

### Backend Components

```mermaid
graph TB
    FlaskApp[Flask Application] --> Routes[API Routes]
    Routes --> DetectEmotion[/api/detect-emotion]
    Routes --> DetectEmotionFile[/api/detect-emotion-file]
    Routes --> Health[/api/health]
    DetectEmotion --> ImageProcessor[Image Processor]
    DetectEmotionFile --> ImageProcessor
    ImageProcessor --> FaceDetector[Face Detector]
    FaceDetector --> ModelLoader[Model Loader]
    ModelLoader -->|Load| CustomModel[Custom Model]
    ModelLoader -->|Fallback| DeepFaceModel[DeepFace]
    CustomModel --> Predictor[Emotion Predictor]
    DeepFaceModel --> Predictor
    Predictor --> ResponseBuilder[Response Builder]
    ResponseBuilder --> Routes
```

## 📊 Data Flow

### Real-time Camera Detection Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Model
    participant Camera

    User->>Frontend: Click "Start Camera"
    Frontend->>Camera: Request camera access
    Camera-->>Frontend: Video stream
    Frontend->>Frontend: Capture frame to canvas
    Frontend->>Frontend: Convert to base64
    Frontend->>Backend: POST /api/detect-emotion
    Backend->>Backend: Decode base64 image
    Backend->>Backend: Detect face (Haar Cascade)
    Backend->>Backend: Preprocess image
    Backend->>Model: Predict emotions
    Model-->>Backend: Emotion predictions
    Backend->>Backend: Format response
    Backend-->>Frontend: JSON response
    Frontend->>Frontend: Update UI with results
    Frontend-->>User: Display emotions
    Note over Frontend: Loop continues every 300ms
```

### Image Upload Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Model

    User->>Frontend: Select image file
    Frontend->>Frontend: Read file as FormData
    Frontend->>Backend: POST /api/detect-emotion-file
    Backend->>Backend: Decode image file
    Backend->>Backend: Detect face (optional)
    Backend->>Backend: Preprocess image
    Backend->>Model: Predict emotions
    Model-->>Backend: Emotion predictions
    Backend->>Backend: Format response
    Backend-->>Frontend: JSON response
    Frontend->>Frontend: Display results
    Frontend-->>User: Show emotion breakdown
```

## 🔧 Backend Architecture

### Flask Application Structure

```
backend/
├── app.py                 # Main Flask application
│   ├── load_custom_model()    # Model loading logic
│   ├── detect_face()          # Face detection (Haar Cascade)
│   ├── preprocess_image()     # Image preprocessing
│   ├── predict_with_custom_model()  # Custom model prediction
│   ├── /api/health            # Health check endpoint
│   ├── /api/detect-emotion    # Camera detection endpoint
│   └── /api/detect-emotion-file  # File upload endpoint
└── requirements.txt        # Python dependencies
```

### Model Loading Strategy

The backend uses a multi-path model loading strategy:

1. **Primary**: Try loading `models/final_model.h5`
2. **Fallback**: Try loading `models/best_model.h5`
3. **DeepFace**: If no custom model found, use DeepFace library

### Image Processing Pipeline

```mermaid
graph LR
    Input[Input Image] --> Decode[Decode Base64/File]
    Decode --> ColorConvert[Convert to BGR]
    ColorConvert --> FaceDetect{Face Detected?}
    FaceDetect -->|Yes| CropFace[Crop Face Region]
    FaceDetect -->|No| FullImage[Use Full Image]
    CropFace --> Grayscale[Convert to Grayscale]
    FullImage --> Grayscale
    Grayscale --> Resize[Resize to 48x48]
    Resize --> Normalize[Normalize 0-1]
    Normalize --> Reshape[Reshape for Model]
    Reshape --> Model[CNN Model]
    Model --> Predictions[Emotion Predictions]
```

## ⚛️ Frontend Architecture

### React Component Structure

```
frontend/src/
├── App.js                    # Main application component
├── components/
│   └── EmotionDetector.js    # Main emotion detection component
│       ├── State Management
│       │   ├── isDetecting   # Camera detection state
│       │   ├── emotion       # Dominant emotion
│       │   ├── emotions      # All emotion scores
│       │   └── error         # Error messages
│       ├── Refs
│       │   ├── videoRef      # Video element reference
│       │   ├── canvasRef     # Canvas element reference
│       │   └── streamRef     # Media stream reference
│       ├── Functions
│       │   ├── startCamera()      # Initialize webcam
│       │   ├── stopCamera()       # Stop webcam
│       │   ├── detectEmotion()    # Detection loop
│       │   └── handleFileUpload() # File upload handler
│       └── UI Components
│           ├── Video Display
│           ├── Results Display
│           └── Controls
└── index.js                  # React entry point
```

### State Management Flow

```mermaid
stateDiagram-v2
    [*] --> Idle: Initial State
    Idle --> Starting: Start Camera Clicked
    Starting --> Detecting: Camera Ready
    Detecting --> Processing: Frame Captured
    Processing --> Detecting: Results Displayed
    Detecting --> Stopped: Stop Camera Clicked
    Stopped --> Idle: Reset State
    Starting --> Error: Camera Access Denied
    Processing --> Error: API Error
    Error --> Idle: Reset
```

## 🤖 Model Integration

### Custom Model Architecture

The custom CNN model follows this architecture:

```mermaid
graph TB
    Input[Input: 48x48x1] --> Conv1[Conv2D 32 filters]
    Conv1 --> BN1[BatchNorm]
    BN1 --> Conv2[Conv2D 32 filters]
    Conv2 --> Pool1[MaxPool 2x2]
    Pool1 --> Drop1[Dropout 0.25]
    Drop1 --> Conv3[Conv2D 64 filters]
    Conv3 --> BN2[BatchNorm]
    BN2 --> Conv4[Conv2D 64 filters]
    Conv4 --> Pool2[MaxPool 2x2]
    Pool2 --> Drop2[Dropout 0.25]
    Drop2 --> Conv5[Conv2D 128 filters]
    Conv5 --> BN3[BatchNorm]
    BN3 --> Conv6[Conv2D 128 filters]
    Conv6 --> Pool3[MaxPool 2x2]
    Pool3 --> Drop3[Dropout 0.25]
    Drop3 --> Flatten[Flatten]
    Flatten --> Dense1[Dense 256]
    Dense1 --> BN4[BatchNorm]
    BN4 --> Drop4[Dropout 0.5]
    Drop4 --> Dense2[Dense 128]
    Dense2 --> Drop5[Dropout 0.5]
    Drop5 --> Output[Output: 7 emotions]
```

### Model Input/Output

- **Input**: Grayscale image, 48x48 pixels, normalized (0-1)
- **Output**: 7 emotion probabilities (softmax)
- **Emotions**: angry, disgusted, fearful, happy, neutral, sad, surprised

### Model Loading and Inference

```mermaid
graph LR
    Startup[Backend Startup] --> CheckModel{Model Exists?}
    CheckModel -->|Yes| LoadModel[Load Custom Model]
    CheckModel -->|No| UseDeepFace[Use DeepFace]
    LoadModel --> Ready[Model Ready]
    UseDeepFace --> Ready
    Ready --> Request[API Request]
    Request --> Preprocess[Preprocess Image]
    Preprocess --> Inference[Model Inference]
    Inference --> Format[Format Response]
    Format --> Return[Return JSON]
```

## 🛠️ Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework |
| Tailwind CSS | 3.3.6 | Styling |
| Axios | 1.6.0 | HTTP client |
| React Scripts | 5.0.1 | Build tools |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Flask | 2.3.0+ | Web framework |
| Flask-CORS | 4.0.0+ | CORS handling |
| TensorFlow | 2.10.0+ | ML framework |
| OpenCV | 4.6.0+ | Image processing |
| NumPy | 1.21.0+ | Numerical operations |
| DeepFace | 0.0.79+ | Fallback emotion detection |

### ML/AI Technologies

| Technology | Purpose |
|------------|---------|
| TensorFlow/Keras | Model training and inference |
| OpenCV Haar Cascades | Face detection |
| Custom CNN | Emotion classification |
| DeepFace | Pre-trained emotion detection (fallback) |

## 🔐 Security Considerations

- **CORS**: Enabled for frontend-backend communication
- **Input Validation**: Image format and size validation
- **Error Handling**: Graceful error handling and fallbacks
- **Model Security**: Model files stored locally, not exposed via API

## 📈 Performance Considerations

- **Model Loading**: Models loaded once at startup
- **Image Processing**: Efficient preprocessing pipeline
- **API Response**: Optimized JSON responses
- **Frontend**: Frame rate limited to ~3-4 FPS for API calls
- **Caching**: Model predictions cached in memory

## 🔗 Related Documentation

- [Usage Guide](04-usage-guide.md) - How to use the system
- [API Reference](06-api-reference.md) - API documentation
- [Model Information](08-model-information.md) - Model details
- [Development Guide](10-development.md) - Development setup

---

**Next**: Learn how to use the system in the [Usage Guide](04-usage-guide.md)

