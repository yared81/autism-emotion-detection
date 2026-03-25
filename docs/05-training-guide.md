# Training Guide

This guide explains how to train custom emotion detection models for the Autism Emotion Detection project.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Requirements](#dataset-requirements)
- [Training Scripts](#training-scripts)
- [Training Parameters](#training-parameters)
- [Model Evaluation](#model-evaluation)
- [Improving Accuracy](#improving-accuracy)
- [Transfer Learning](#transfer-learning)
- [Output Files](#output-files)
- [Troubleshooting Training](#troubleshooting-training)

## 🎯 Overview

The project includes multiple training scripts for different use cases:

1. **train_advanced_model.py** - Full-featured training with comprehensive evaluation
2. **train_fast_model.py** - Optimized for faster training (20-30 minutes)
3. **train_baseline.py** - Simple baseline model for quick testing

## 📁 Dataset Requirements

### Dataset Structure

Your dataset must be organized as follows:

```
archive (1)/
├── train/
│   ├── angry/
│   │   ├── image1.png
│   │   ├── image2.jpg
│   │   └── ...
│   ├── disgusted/
│   ├── fearful/
│   ├── happy/
│   ├── neutral/
│   ├── sad/
│   └── surprised/
└── test/
    ├── angry/
    ├── disgusted/
    ├── fearful/
    ├── happy/
    ├── neutral/
    ├── sad/
    └── surprised/
```

### Dataset Path Configuration

Update the dataset path in the training script:

```python
DATASET_PATH = r'C:\Users\Meron  Yenie\Downloads\archive (1)'
TRAIN_DIR = os.path.join(DATASET_PATH, 'train')
TEST_DIR = os.path.join(DATASET_PATH, 'test')
```

### Dataset Requirements

- **Format**: PNG, JPG, or JPEG images
- **Size**: Any size (will be resized to 48x48)
- **Color**: Grayscale (converted automatically)
- **Labels**: 7 emotion categories (angry, disgusted, fearful, happy, neutral, sad, surprised)
- **Balance**: Ideally balanced across classes (see class distribution analysis)

## 🚀 Training Scripts

### 1. Advanced Model Training

**File**: `scripts/train_advanced_model.py`

**Features**:
- Deep CNN architecture (4 convolutional blocks)
- Comprehensive data augmentation
- Full dataset usage (no sampling)
- Detailed evaluation metrics
- Training history visualization

**Usage**:
```bash
cd scripts
python train_advanced_model.py
```

**Or use batch file**:
```bash
run_training.bat
```

**Model Architecture**:
- 4 Conv blocks: 64→128→256→512 filters
- Batch normalization after each layer
- Dropout for regularization (0.25-0.5)
- Dense layers: 512→256→7
- Total parameters: ~15-20M

**Training Time**: 30-60 minutes (CPU), 10-20 minutes (GPU)

### 2. Fast Model Training

**File**: `scripts/train_fast_model.py`

**Features**:
- Optimized for speed (20-30 minutes)
- Data sampling (2000 samples per class)
- Smaller model architecture
- Faster convergence

**Usage**:
```bash
cd scripts
python train_fast_model.py
```

**Or use batch file**:
```bash
run_fast_training.bat
```

**Model Architecture**:
- 3 Conv blocks: 32→64→128 filters
- Reduced dense layers: 256→128→7
- Total parameters: ~5-8M

**Training Time**: 20-30 minutes (CPU)

### 3. Baseline Model

**File**: `scripts/train_baseline.py`

**Features**:
- Simple CNN architecture
- Quick testing and prototyping
- Minimal dependencies

**Usage**:
```bash
cd scripts
python train_baseline.py
```

## ⚙️ Training Parameters

### Common Parameters

| Parameter | Advanced Model | Fast Model | Description |
|-----------|---------------|------------|-------------|
| Epochs | 100 | 25 | Maximum training epochs |
| Batch Size | 64 | 128 | Samples per batch |
| Learning Rate | 0.001 | 0.002 | Initial learning rate |
| Validation Split | 10% | 15% | Validation data percentage |
| Early Stopping Patience | 15 | 8 | Epochs to wait before stopping |
| Image Size | 48x48 | 48x48 | Input image dimensions |

### Data Augmentation

**Advanced Model**:
```python
ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)
```

**Fast Model**:
```python
ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    zoom_range=0.1
)
```

### Callbacks

All training scripts include:

1. **EarlyStopping**: Stops training if validation accuracy doesn't improve
2. **ReduceLROnPlateau**: Reduces learning rate when loss plateaus
3. **ModelCheckpoint**: Saves best model during training

## 📊 Model Evaluation

### Evaluation Metrics

After training, the script generates:

1. **Test Accuracy**: Overall accuracy on test set
2. **Test Loss**: Categorical cross-entropy loss
3. **Classification Report**: Per-class precision, recall, F1-score
4. **Confusion Matrix**: Visual confusion matrix
5. **Training History**: Accuracy and loss curves

### Output Files

After training completes:

```
models/
├── best_model.h5          # Best model during training
└── final_model.h5        # Final trained model

# Analysis files
class_distribution.png    # Class distribution visualization
confusion_matrix.png      # Confusion matrix heatmap
training_history.png      # Training curves
training_results.txt      # Detailed text report
```

### Reading Results

**Training Results File** (`training_results.txt`):
- Test accuracy percentage
- Test loss value
- Classification report with per-class metrics
- Class distribution statistics

**Confusion Matrix**:
- Shows true vs predicted labels
- Diagonal = correct predictions
- Off-diagonal = misclassifications

**Training History**:
- Accuracy curve (train vs validation)
- Loss curve (train vs validation)
- Check for overfitting (large gap between train/val)

## 🎯 Improving Accuracy (85-95% Target)

### Strategy 1: Use All Training Data

Remove data sampling in fast training:

```python
# In train_fast_model.py, change:
X_train, y_train = load_images_labels(TRAIN_DIR, max_samples_per_class=None)
```

### Strategy 2: Enhanced Data Augmentation

Add more augmentation techniques:

```python
ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    horizontal_flip=True,
    zoom_range=0.15,
    brightness_range=[0.8, 1.2],
    shear_range=0.1,
    fill_mode='nearest'
)
```

### Strategy 3: Class Balancing

Handle imbalanced classes:

```python
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight(
    'balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = dict(enumerate(class_weights))

# Use in model.fit()
model.fit(..., class_weight=class_weight_dict)
```

### Strategy 4: Transfer Learning

Use pre-trained models (see Transfer Learning section below)

### Strategy 5: Learning Rate Scheduling

Implement learning rate decay:

```python
from tensorflow.keras.callbacks import LearningRateScheduler

def step_decay(epoch):
    if epoch < 30:
        return 0.001
    elif epoch < 60:
        return 0.0005
    else:
        return 0.0001

lr_scheduler = LearningRateScheduler(step_decay)
```

### Strategy 6: More Epochs with Patience

Increase training time:

```python
epochs=150  # More epochs
patience=25  # More patience for early stopping
```

## 🔄 Transfer Learning

### Using Pre-trained Models

Transfer learning can significantly improve accuracy. Use models like:

- **EfficientNetB0**: Lightweight and efficient
- **ResNet50**: Deep residual network
- **VGG16**: Classic architecture

### Transfer Learning Steps

1. **Load Pre-trained Base Model**
   ```python
   from tensorflow.keras.applications import EfficientNetB0
   
   base_model = EfficientNetB0(
       weights='imagenet',
       include_top=False,
       input_shape=(224, 224, 3)
   )
   ```

2. **Freeze Base Layers**
   ```python
   base_model.trainable = False
   ```

3. **Add Custom Head**
   ```python
   x = GlobalAveragePooling2D()(base_model.output)
   x = Dense(512, activation='relu')(x)
   x = Dropout(0.5)(x)
   outputs = Dense(7, activation='softmax')(x)
   ```

4. **Train in Two Phases**
   - Phase 1: Train only the head (frozen base)
   - Phase 2: Fine-tune entire model (unfreeze top layers)

### Transfer Learning Example

See the high-accuracy training script provided in the project discussion for a complete transfer learning implementation.

## 📁 Output Files

### Model Files

- **best_model.h5**: Best model during training (based on validation accuracy)
- **final_model.h5**: Final model after training completes

### Analysis Files

- **class_distribution.png**: Bar chart showing class distribution
- **confusion_matrix.png**: Heatmap of confusion matrix
- **training_history.png**: Training accuracy and loss curves
- **training_results.txt**: Detailed text report

### Using Trained Models

After training, models are automatically saved. The backend will load them:

1. Check for `models/final_model.h5`
2. Fallback to `models/best_model.h5`
3. Use DeepFace if no custom model found

## 🐛 Troubleshooting Training

### Out of Memory

**Problem**: `ResourceExhaustedError` or system crashes

**Solutions**:
- Reduce batch size: `batch_size=32` or `batch_size=16`
- Use data sampling: `max_samples_per_class=1000`
- Reduce model size (fewer filters/layers)

### Slow Training

**Problem**: Training takes too long

**Solutions**:
- Use GPU (TensorFlow will detect automatically)
- Use fast training script
- Reduce epochs or use early stopping
- Reduce dataset size (sampling)

### Low Accuracy

**Problem**: Model accuracy is low (<60%)

**Solutions**:
- Check class distribution (may be imbalanced)
- Increase training epochs
- Adjust learning rate
- Use more data augmentation
- Try transfer learning
- Check dataset quality

### Overfitting

**Problem**: Large gap between train and validation accuracy

**Solutions**:
- Increase dropout rates
- Add more data augmentation
- Reduce model complexity
- Use early stopping
- Add regularization

### Model Not Saving

**Problem**: Model files not created

**Solutions**:
- Check `models/` directory exists
- Verify write permissions
- Check disk space
- Review error messages in console

## 📈 Expected Results

### Advanced Model

- **Accuracy**: 65-75% (depending on dataset)
- **Training Time**: 30-60 minutes (CPU)
- **Model Size**: ~15-20M parameters

### Fast Model

- **Accuracy**: 60-70% (depending on dataset)
- **Training Time**: 20-30 minutes (CPU)
- **Model Size**: ~5-8M parameters

### High-Accuracy Model (Transfer Learning)

- **Accuracy**: 85-95% (with proper setup)
- **Training Time**: 1-3 hours (GPU recommended)
- **Model Size**: Varies by base model

## 🔗 Related Documentation

- [Model Information](08-model-information.md) - Model architecture details
- [Installation Guide](02-installation.md) - Setup instructions
- [Troubleshooting](09-troubleshooting.md) - Common issues
- [Development Guide](10-development.md) - Development setup

---

**Next**: Learn about the API in the [API Reference](06-api-reference.md)

