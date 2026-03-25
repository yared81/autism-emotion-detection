# Frequently Asked Questions

Common questions and answers about the Autism Emotion Detection project.

## 📋 Table of Contents

- [General Questions](#general-questions)
- [Installation Questions](#installation-questions)
- [Usage Questions](#usage-questions)
- [Training Questions](#training-questions)
- [Technical Questions](#technical-questions)
- [Troubleshooting Questions](#troubleshooting-questions)

## ❓ General Questions

### What is this project?

The Autism Emotion Detection project is a web-based application that uses deep learning to detect and classify human emotions from facial expressions in real-time or from uploaded images.

### What emotions can it detect?

The system detects 7 basic emotions:
- Happy 😊
- Sad 😢
- Angry 😠
- Surprised 😲
- Fearful 😨
- Disgusted 🤢
- Neutral 😐

### Is this project free to use?

Yes, this project is open-source and free to use for educational and research purposes.

### What technologies does it use?

- **Frontend**: React, Tailwind CSS
- **Backend**: Flask (Python)
- **ML Framework**: TensorFlow/Keras
- **Computer Vision**: OpenCV
- **Models**: Custom CNN or DeepFace

### Can I use this commercially?

Check the license file in the repository. Generally, open-source projects allow commercial use, but verify the specific license terms.

## 🔧 Installation Questions

### What are the system requirements?

- Python 3.8+
- Node.js 14+
- 4GB+ RAM
- 2GB+ free disk space
- Webcam (for real-time detection)

### Do I need a GPU?

A GPU is optional but recommended for:
- Training models (faster training)
- Real-time inference (better performance)

For basic usage, CPU is sufficient.

### How long does installation take?

- Backend setup: 5-10 minutes
- Frontend setup: 5-10 minutes
- Total: ~15-20 minutes

### Can I install on Windows/Mac/Linux?

Yes, the project supports:
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 10+, etc.)

### Do I need to train a model?

No, the system can use DeepFace as a fallback. However, training a custom model on your dataset will provide better accuracy for your specific use case.

## 💻 Usage Questions

### How do I start the application?

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && npm start`
3. Open browser to `http://localhost:3000`

### Why isn't my camera working?

- Check browser permissions (click "Allow" when prompted)
- Ensure camera is not in use by another app
- Try a different browser
- Check camera in system settings

### Can I use it without a camera?

Yes, you can upload images instead of using the camera.

### What image formats are supported?

- JPEG (.jpg, .jpeg)
- PNG (.png)

### How accurate is the detection?

- Custom models: 60-75% (depending on training)
- DeepFace: ~70-80%
- High-accuracy models (transfer learning): 85-95%

### Why are some emotions confused?

Some emotions have similar facial expressions:
- Fear and Surprise (both have wide eyes)
- Sad and Neutral (similar mouth positions)
- Angry and Disgusted (similar brow positions)

This is normal and can be improved with better training data.

## 🎓 Training Questions

### How long does training take?

- **Fast model**: 20-30 minutes
- **Advanced model**: 30-60 minutes (CPU), 10-20 minutes (GPU)
- **Transfer learning**: 1-3 hours (GPU recommended)

### How much data do I need?

Minimum recommendations:
- 500+ images per emotion class
- Balanced distribution across classes
- More data = better accuracy

### Can I use my own dataset?

Yes! Organize your dataset in the required folder structure (see [Training Guide](05-training-guide.md)).

### How do I improve accuracy?

1. Use more training data
2. Ensure balanced classes
3. Use data augmentation
4. Try transfer learning
5. Fine-tune hyperparameters

### What if my dataset is imbalanced?

Use class weights in training:
```python
from sklearn.utils.class_weight import compute_class_weight
class_weights = compute_class_weight('balanced', classes, y_train)
```

### Can I use pre-trained models?

Yes, the project supports transfer learning with models like:
- EfficientNetB0
- ResNet50
- VGG16

See the [Training Guide](05-training-guide.md) for details.

## 🔬 Technical Questions

### How does the model work?

The custom CNN model:
1. Detects face using Haar Cascade
2. Preprocesses image (grayscale, resize, normalize)
3. Passes through convolutional layers
4. Outputs 7 emotion probabilities

### What is the model input size?

- Input: 48x48 pixels, grayscale
- Normalized: 0.0 to 1.0
- Shape: (1, 48, 48, 1)

### How fast is inference?

- CPU: ~50-100ms per image
- GPU: ~10-20ms per image

### Can I use a different model?

Yes, you can:
1. Train a custom model
2. Replace model file in `models/` directory
3. Modify backend to load different model

### How does face detection work?

Uses OpenCV Haar Cascade classifier:
- Detects face in image
- Returns bounding box coordinates
- Crops face region for emotion analysis

### What happens if no face is detected?

The API returns an error message:
```json
{
  "error": "No face detected in image. Please ensure a face is visible."
}
```

The frontend displays this message to the user.

## 🐛 Troubleshooting Questions

### Backend won't start

**Check**:
- Python version: `python --version`
- Dependencies installed: `pip list`
- Port 5000 available
- Virtual environment activated

### Frontend won't start

**Check**:
- Node.js version: `node --version`
- Dependencies installed: `npm list`
- Port 3000 available
- No syntax errors in code

### Model not loading

**Check**:
- Model file exists: `ls models/`
- File permissions
- TensorFlow version compatibility
- Check backend console for errors

### Camera not working

**Check**:
- Browser permissions
- Camera not in use by another app
- Try different browser
- Check system camera settings

### Low accuracy

**Solutions**:
- Use more training data
- Improve data quality
- Try transfer learning
- Adjust hyperparameters
- Check class distribution

### API errors

**Check**:
- Backend is running
- Correct API URL
- CORS enabled
- Request format correct
- Check browser console

### Out of memory during training

**Solutions**:
- Reduce batch size
- Use data sampling
- Reduce model size
- Use GPU if available
- Close other applications

## 📚 Additional Resources

### Documentation

- [Getting Started](01-getting-started.md) - Quick start
- [Installation Guide](02-installation.md) - Setup
- [Usage Guide](04-usage-guide.md) - How to use
- [Training Guide](05-training-guide.md) - Model training
- [API Reference](06-api-reference.md) - API docs
- [Troubleshooting](09-troubleshooting.md) - Common issues

### Still Have Questions?

- Check [Troubleshooting Guide](09-troubleshooting.md)
- Review [Development Guide](10-development.md)
- Open an issue on GitHub
- Check project documentation

---

**Back to**: [Documentation Index](README.md)

