# Model Information

Complete documentation about the emotion detection models used in this project.

## 📋 Table of Contents

- [Overview](#overview)
- [Model Architecture](#model-architecture)
- [Model Versions](#model-versions)
- [Input/Output Specifications](#inputoutput-specifications)
- [Emotion Labels](#emotion-labels)
- [Performance Metrics](#performance-metrics)
- [Model Files](#model-files)
- [Loading and Using Models](#loading-and-using-models)

## 🎯 Overview

The project supports two model types:

1. **Custom Trained CNN** - Custom convolutional neural network trained on your dataset
2. **DeepFace** - Pre-trained emotion detection library (fallback)

The backend automatically uses the custom model if available, otherwise falls back to DeepFace.

## 🏗️ Model Architecture

### Custom CNN Model

The custom model uses a deep convolutional neural network architecture.

#### Advanced Model Architecture

```
Input: 48x48x1 (grayscale)

Conv Block 1:
  Conv2D(64, 3x3) + ReLU
  BatchNormalization
  Conv2D(64, 3x3) + ReLU
  MaxPooling2D(2x2)
  Dropout(0.25)

Conv Block 2:
  Conv2D(128, 3x3) + ReLU
  BatchNormalization
  Conv2D(128, 3x3) + ReLU
  MaxPooling2D(2x2)
  Dropout(0.25)

Conv Block 3:
  Conv2D(256, 3x3) + ReLU
  BatchNormalization
  Conv2D(256, 3x3) + ReLU
  MaxPooling2D(2x2)
  Dropout(0.25)

Conv Block 4:
  Conv2D(512, 3x3) + ReLU
  BatchNormalization
  Conv2D(512, 3x3) + ReLU
  MaxPooling2D(2x2)
  Dropout(0.25)

Dense Layers:
  Flatten
  Dense(512) + ReLU
  BatchNormalization
  Dropout(0.5)
  Dense(256) + ReLU
  BatchNormalization
  Dropout(0.5)
  Dense(7) + Softmax

Output: 7 emotion probabilities
```

#### Fast Model Architecture

Similar structure but with reduced complexity:
- 3 Conv blocks (32→64→128 filters)
- Smaller dense layers (256→128)
- ~5-8M parameters vs ~15-20M

### Model Parameters

**Advanced Model**:
- Total Parameters: ~15-20 million
- Trainable Parameters: ~15-20 million
- Model Size: ~60-80 MB (H5 format)

**Fast Model**:
- Total Parameters: ~5-8 million
- Trainable Parameters: ~5-8 million
- Model Size: ~20-30 MB (H5 format)

## 📦 Model Versions

### Model File Naming

- `best_model.h5` - Best model during training (based on validation accuracy)
- `final_model.h5` - Final model after training completes

### Loading Priority

The backend loads models in this order:

1. `models/final_model.h5` (primary)
2. `models/best_model.h5` (fallback)
3. DeepFace library (if no custom model found)

## 📥 Input/Output Specifications

### Input Requirements

**Format**: Grayscale image
**Size**: 48x48 pixels
**Normalization**: Pixel values 0.0 to 1.0 (float32)
**Shape**: (1, 48, 48, 1) - (batch, height, width, channels)

**Preprocessing Pipeline**:
1. Face detection (Haar Cascade)
2. Crop face region
3. Convert to grayscale
4. Resize to 48x48
5. Normalize to [0, 1]
6. Add batch and channel dimensions

### Output Format

**Format**: Softmax probabilities
**Shape**: (7,) - 7 emotion probabilities
**Range**: 0.0 to 1.0 (sum = 1.0)

**Output Structure**:
```python
[
  angry_prob,      # Index 0
  disgusted_prob,  # Index 1
  fearful_prob,    # Index 2
  happy_prob,      # Index 3
  neutral_prob,    # Index 4
  sad_prob,        # Index 5
  surprised_prob   # Index 6
]
```

## 😊 Emotion Labels

### Label Mapping

| Index | Label | Description |
|-------|-------|-------------|
| 0 | `angry` | Anger, frustration, irritation |
| 1 | `disgusted` | Disgust, revulsion, distaste |
| 2 | `fearful` | Fear, anxiety, worry |
| 3 | `happy` | Happiness, joy, contentment |
| 4 | `neutral` | Neutral expression, resting face |
| 5 | `sad` | Sadness, melancholy, disappointment |
| 6 | `surprised` | Surprise, shock, astonishment |

### Label Consistency

Labels are lowercase and match between:
- Training scripts
- Backend API
- Frontend display

## 📊 Performance Metrics

### Expected Accuracy

**Advanced Model**:
- Test Accuracy: 65-75% (depending on dataset)
- Per-class accuracy varies by emotion

**Fast Model**:
- Test Accuracy: 60-70% (depending on dataset)
- Faster inference, slightly lower accuracy

**High-Accuracy Model** (Transfer Learning):
- Test Accuracy: 85-95% (with proper setup)
- Requires transfer learning implementation

### Performance Characteristics

**Inference Speed**:
- CPU: ~50-100ms per image
- GPU: ~10-20ms per image

**Memory Usage**:
- Model loading: ~200-300 MB RAM
- Inference: ~50-100 MB additional

## 📁 Model Files

### File Locations

```
models/
├── best_model.h5      # Best model from training
└── final_model.h5    # Final trained model
```

### File Format

- **Format**: HDF5 (H5)
- **Framework**: TensorFlow/Keras
- **Compatibility**: TensorFlow 2.10+

### Model Loading

Models are loaded using TensorFlow/Keras:

```python
from tensorflow.keras.models import load_model

model = load_model('models/final_model.h5')
```

## 🔄 Loading and Using Models

### Backend Loading

The backend automatically loads models on startup:

```python
def load_custom_model():
    # Try multiple paths
    possible_paths = [
        'models/final_model.h5',
        'models/best_model.h5',
        # ... fallback paths
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            MODEL = load_model(path)
            return True
    
    return False  # Fallback to DeepFace
```

### Manual Model Loading

**Python**:
```python
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Load model
model = load_model('models/final_model.h5')

# Preprocess image
img = Image.open('image.jpg').convert('L')
img = img.resize((48, 48))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)
img_array = np.expand_dims(img_array, axis=-1)

# Predict
predictions = model.predict(img_array)
emotion_idx = np.argmax(predictions[0])
emotion_labels = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']
emotion = emotion_labels[emotion_idx]
confidence = predictions[0][emotion_idx] * 100

print(f"Emotion: {emotion}, Confidence: {confidence:.2f}%")
```

### Model Inference

**Preprocessing**:
1. Face detection (optional but recommended)
2. Grayscale conversion
3. Resize to 48x48
4. Normalize to [0, 1]
5. Reshape to (1, 48, 48, 1)

**Prediction**:
```python
predictions = model.predict(preprocessed_image, verbose=0)
dominant_emotion_idx = np.argmax(predictions[0])
confidence = predictions[0][dominant_emotion_idx] * 100
```

## 🔧 Model Customization

### Retraining Models

See [Training Guide](05-training-guide.md) for:
- Training custom models
- Improving accuracy
- Transfer learning

### Model Architecture Changes

To modify architecture, edit training scripts:

```python
# In train_advanced_model.py or train_fast_model.py
def create_model():
    model = Sequential([
        # Modify layers here
        Conv2D(64, (3, 3), ...),
        # ...
    ])
    return model
```

### Fine-tuning

For fine-tuning existing models:

```python
# Load pre-trained model
model = load_model('models/final_model.h5')

# Unfreeze some layers
for layer in model.layers[:-10]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Fine-tune on new data
model.fit(...)
```

## 📈 Model Evaluation

### Evaluation Metrics

After training, models are evaluated using:

- **Accuracy**: Overall classification accuracy
- **Per-class Accuracy**: Accuracy for each emotion
- **Confusion Matrix**: Detailed error analysis
- **Classification Report**: Precision, recall, F1-score

### Interpreting Results

**High Accuracy (>70%)**:
- Model performs well
- Good generalization
- Reliable predictions

**Medium Accuracy (50-70%)**:
- Acceptable performance
- May need improvement
- Check confusion matrix for patterns

**Low Accuracy (<50%)**:
- Model needs improvement
- Check dataset quality
- Consider transfer learning

## 🔗 Related Documentation

- [Training Guide](05-training-guide.md) - How to train models
- [Architecture](03-architecture.md) - System architecture
- [API Reference](06-api-reference.md) - API usage
- [Troubleshooting](09-troubleshooting.md) - Common issues

---

**Next**: Troubleshooting guide in [Troubleshooting](09-troubleshooting.md)

