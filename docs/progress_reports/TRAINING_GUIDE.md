# Advanced Model Training Guide

## Overview
This script trains an advanced CNN model on your custom emotion detection dataset with comprehensive evaluation metrics.

## Features
- ✅ **Advanced CNN Architecture**: Deep convolutional network with batch normalization and dropout
- ✅ **Data Augmentation**: Improves model generalization
- ✅ **Class Distribution Analysis**: Visualizes data balance across emotions
- ✅ **Confusion Matrix**: Detailed per-class performance analysis
- ✅ **Training History**: Tracks accuracy and loss over epochs
- ✅ **Early Stopping**: Prevents overfitting
- ✅ **Learning Rate Scheduling**: Optimizes training process
- ✅ **Best Model Saving**: Automatically saves the best performing model

## Dataset Structure
Your dataset should be organized as:
```
archive (1)/
  train/
    angry/
    disgusted/
    fearful/
    happy/
    neutral/
    sad/
    surprised/
  test/
    (same structure)
```

## How to Run

### Option 1: Using Batch File (Easiest)
Double-click `run_training.bat`

### Option 2: Command Line
```bash
cd "C:\Users\Meron  Yenie\Desktop\Autism-Emotion-Detection"
python scripts/train_advanced_model.py
```

## Output Files

After training completes, you'll get:

1. **models/best_model.h5** - Best model during training
2. **models/final_model.h5** - Final trained model
3. **class_distribution.png** - Visual class distribution
4. **confusion_matrix.png** - Confusion matrix visualization
5. **training_history.png** - Accuracy and loss curves
6. **training_results.txt** - Detailed text report

## Model Architecture

The model uses:
- 4 convolutional blocks with increasing filters (64→128→256→512)
- Batch normalization after each conv layer
- Dropout for regularization (0.25-0.5)
- 2 dense layers (512→256→7)
- Total parameters: ~15-20M

## Training Parameters

- **Epochs**: Up to 100 (with early stopping)
- **Batch Size**: 64
- **Learning Rate**: 0.001 (with reduction on plateau)
- **Validation Split**: 10% of training data
- **Data Augmentation**: Rotation, shifts, flips, zoom

## Expected Results

- **Test Accuracy**: Should achieve 60-75%+ depending on dataset quality
- **Training Time**: 30-60 minutes on CPU, 10-20 minutes on GPU

## Troubleshooting

### Out of Memory
- Reduce batch size in the script (change `batch_size=64` to `batch_size=32`)

### Slow Training
- Ensure you have GPU support (TensorFlow will use it automatically if available)
- Reduce number of epochs or use smaller model

### Low Accuracy
- Check class distribution (may need data balancing)
- Increase training epochs
- Adjust learning rate

## Next Steps

After training:
1. Review the confusion matrix to see which emotions are confused
2. Check class distribution for imbalanced classes
3. Use the saved model in your web application
4. Fine-tune hyperparameters if needed

