# Usage Guide

This guide explains how to use the Autism Emotion Detection web application.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Camera Functionality](#camera-functionality)
- [Image Upload](#image-upload)
- [Understanding Results](#understanding-results)
- [Emotion Categories](#emotion-categories)
- [Best Practices](#best-practices)
- [Tips for Better Accuracy](#tips-for-better-accuracy)

## 🚀 Getting Started

### Starting the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python app.py
   ```
   Wait for: `Running on http://0.0.0.0:5000`

2. **Start the Frontend**
   ```bash
   cd frontend
   npm start
   ```
   Browser will open to `http://localhost:3000`

3. **Access the Application**
   - Open your browser
   - Navigate to `http://localhost:3000`
   - You should see the Emotion Detection interface

## 🎥 Camera Functionality

### Starting Camera Detection

1. **Click "Start Camera" Button**
   - The button is located in the video section
   - Your browser will request camera permissions

2. **Allow Camera Access**
   - Click "Allow" when prompted
   - The camera feed will appear in the video section

3. **Real-time Detection**
   - Detection starts automatically
   - Emotions are analyzed every ~300ms (3-4 FPS)
   - Results appear in real-time on the right side

### Using Camera Detection

**Best Practices:**
- Ensure good lighting
- Face the camera directly
- Keep face centered in frame
- Maintain appropriate distance (2-3 feet)
- Remove glasses if they cause reflections

**What You'll See:**
- Live video feed in the left panel
- Dominant emotion displayed prominently
- All emotion scores with confidence percentages
- FPS counter showing processing speed

### Stopping Camera

- Click **"Stop Camera"** button
- Camera feed stops
- Detection loop terminates
- Results are cleared

## 📸 Image Upload

### Uploading an Image

1. **Click "Upload Image" Button**
   - Located next to the camera controls
   - Opens file selection dialog

2. **Select Image File**
   - Supported formats: JPG, PNG, JPEG
   - Any image size (will be resized automatically)

3. **View Results**
   - Image is processed immediately
   - Results appear in the results panel
   - Emotion breakdown is displayed

### Image Requirements

**Supported Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)

**Image Quality:**
- Clear, well-lit images work best
- Face should be clearly visible
- Avoid blurry or dark images
- Cropped face images work well

## 📊 Understanding Results

### Dominant Emotion Display

The dominant emotion is shown prominently with:
- **Emoji**: Visual representation of the emotion
- **Label**: Emotion name (capitalized)
- **Confidence**: Percentage confidence score

Example:
```
😊
Happy
87.5% confidence
```

### All Emotions Breakdown

Below the dominant emotion, you'll see all 7 emotions with:
- **Emotion Name**: Label for each emotion
- **Confidence Score**: Percentage (0-100%)
- **Progress Bar**: Visual representation of confidence
- **Emoji**: Icon for each emotion

Emotions are sorted by confidence (highest first).

### Reading the Results

**High Confidence (>70%):**
- Strong prediction
- Emotion is likely accurate
- Clear facial expression

**Medium Confidence (40-70%):**
- Moderate prediction
- May be ambiguous
- Check other emotion scores

**Low Confidence (<40%):**
- Weak prediction
- Expression may be unclear
- Try better lighting or angle

## 😊 Emotion Categories

The system detects 7 basic emotions:

### 1. Happy 😊
- **Characteristics**: Smiling, raised cheeks, crinkled eyes
- **Color**: Green
- **Common triggers**: Positive events, joy, contentment

### 2. Sad 😢
- **Characteristics**: Downturned mouth, drooping eyes
- **Color**: Blue
- **Common triggers**: Disappointment, loss, melancholy

### 3. Angry 😠
- **Characteristics**: Frowning, narrowed eyes, tense features
- **Color**: Red
- **Common triggers**: Frustration, irritation, rage

### 4. Surprised 😲
- **Characteristics**: Wide eyes, raised eyebrows, open mouth
- **Color**: Yellow
- **Common triggers**: Unexpected events, shock

### 5. Fearful 😨
- **Characteristics**: Wide eyes, raised eyebrows, tense mouth
- **Color**: Purple
- **Common triggers**: Anxiety, worry, fear

### 6. Disgusted 🤢
- **Characteristics**: Wrinkled nose, downturned mouth
- **Color**: Orange
- **Common triggers**: Revulsion, distaste

### 7. Neutral 😐
- **Characteristics**: Relaxed features, minimal expression
- **Color**: Gray
- **Common triggers**: Resting state, calm

## ✅ Best Practices

### For Best Results

1. **Lighting**
   - Use natural or bright, even lighting
   - Avoid harsh shadows
   - Face should be well-lit

2. **Positioning**
   - Face the camera directly
   - Keep face centered
   - Maintain 2-3 feet distance

3. **Expression**
   - Make clear, natural expressions
   - Avoid exaggerated expressions
   - Keep face still during detection

4. **Environment**
   - Minimize background distractions
   - Use plain backgrounds when possible
   - Ensure stable internet connection

### Camera Settings

- **Resolution**: 640x480 (automatic)
- **Frame Rate**: 3-4 FPS (optimized for API calls)
- **Format**: JPEG compression for transmission

### Image Quality Tips

- Use high-resolution images when possible
- Ensure face is clearly visible
- Avoid filters or heavy editing
- Use images with good contrast

## 🎯 Tips for Better Accuracy

### Improving Detection Accuracy

1. **Face Detection**
   - Ensure face is clearly visible
   - Avoid partial face occlusion
   - Remove masks or face coverings

2. **Expression Clarity**
   - Make distinct expressions
   - Hold expression for a moment
   - Avoid rapid expression changes

3. **Technical Settings**
   - Use stable internet connection
   - Close unnecessary browser tabs
   - Ensure sufficient system resources

4. **Model Performance**
   - Use custom-trained models for better accuracy
   - Train models on similar data to your use case
   - Fine-tune models for specific scenarios

### Common Issues and Solutions

**Issue**: "No face detected"
- **Solution**: Ensure face is clearly visible, improve lighting

**Issue**: Low confidence scores
- **Solution**: Better lighting, clearer expression, closer to camera

**Issue**: Wrong emotion detected
- **Solution**: Expression may be ambiguous, check other emotion scores

**Issue**: Camera not starting
- **Solution**: Check browser permissions, ensure camera is not in use by another app

## 🔄 Real-time Detection Loop

The camera detection works in a continuous loop:

1. Capture frame from video stream
2. Draw frame to canvas
3. Convert to base64 JPEG
4. Send to backend API
5. Receive emotion predictions
6. Update UI with results
7. Wait 300ms
8. Repeat

This loop continues until you click "Stop Camera".

## 📱 Browser Compatibility

### Supported Browsers

- **Chrome**: Full support (recommended)
- **Firefox**: Full support
- **Edge**: Full support
- **Safari**: Full support (macOS/iOS)

### Browser Requirements

- Modern browser (last 2 versions)
- WebRTC support (for camera)
- JavaScript enabled
- Local storage enabled

## 🎨 Interface Overview

### Main Layout

```
┌─────────────────────────────────────────┐
│         Emotion Detection AI             │
│  Real-time facial emotion recognition   │
└─────────────────────────────────────────┘

┌──────────────────┬──────────────────────┐
│                  │                      │
│   Video/Canvas   │   Detection Results  │
│                  │                      │
│   [Controls]     │   - Dominant Emotion │
│                  │   - All Emotions    │
│                  │   - Confidence Bars │
│                  │                      │
└──────────────────┴──────────────────────┘
```

### Control Buttons

- **Start Camera**: Begin real-time detection
- **Stop Camera**: End detection and stop camera
- **Upload Image**: Select and analyze image file

## 🔗 Related Documentation

- [Installation Guide](02-installation.md) - Setup instructions
- [API Reference](06-api-reference.md) - Backend API details
- [Troubleshooting](09-troubleshooting.md) - Common issues
- [FAQ](11-faq.md) - Frequently asked questions

---

**Next**: Learn about training custom models in the [Training Guide](05-training-guide.md)

