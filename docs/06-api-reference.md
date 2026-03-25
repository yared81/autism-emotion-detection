# API Reference

Complete documentation for the Autism Emotion Detection REST API.

## 📋 Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Request/Response Formats](#requestresponse-formats)
- [Error Handling](#error-handling)
- [Example Requests](#example-requests)

## 🌐 Overview

The Emotion Detection API is a RESTful service built with Flask that provides emotion detection capabilities. It supports both real-time camera feeds and image file uploads.

### API Features

- Real-time emotion detection from base64-encoded images
- File upload support for image analysis
- Custom model integration with DeepFace fallback
- Face detection and preprocessing
- JSON response format

## 🔗 Base URL

```
http://localhost:5000
```

For production, replace with your server URL.

## 🔐 Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

For production deployments, consider adding:
- API key authentication
- JWT tokens
- Rate limiting

## 📡 Endpoints

### 1. Health Check

Check API status and model information.

**Endpoint**: `GET /api/health`

**Request**:
```http
GET /api/health HTTP/1.1
Host: localhost:5000
```

**Response** (200 OK):
```json
{
  "status": "ok",
  "message": "Emotion Detection API is running",
  "model": "custom trained model"
}
```

**Response Fields**:
- `status` (string): API status ("ok")
- `message` (string): Status message
- `model` (string): Active model type ("custom trained model" or "DeepFace (fallback)")

**Example**:
```bash
curl http://localhost:5000/api/health
```

---

### 2. Detect Emotion (Base64 Image)

Detect emotions from a base64-encoded image. Used for real-time camera feeds.

**Endpoint**: `POST /api/detect-emotion`

**Request Headers**:
```http
Content-Type: application/json
```

**Request Body**:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Request Fields**:
- `image` (string, required): Base64-encoded image with optional data URI prefix

**Response** (200 OK):
```json
{
  "dominant_emotion": "happy",
  "emotions": {
    "angry": 2.5,
    "disgusted": 1.2,
    "fearful": 0.8,
    "happy": 87.5,
    "neutral": 5.3,
    "sad": 1.5,
    "surprised": 0.2
  },
  "confidence": 87.5,
  "face_coordinates": {
    "x": 120,
    "y": 80,
    "width": 200,
    "height": 200
  }
}
```

**Response Fields**:
- `dominant_emotion` (string): Emotion with highest confidence
- `emotions` (object): All emotion scores (0-100%)
- `confidence` (float): Confidence of dominant emotion (0-100%)
- `face_coordinates` (object, optional): Detected face bounding box
  - `x` (int): X coordinate
  - `y` (int): Y coordinate
  - `width` (int): Face width
  - `height` (int): Face height

**Error Response** (200 OK with error):
```json
{
  "error": "No face detected in image. Please ensure a face is visible.",
  "dominant_emotion": null,
  "emotions": {},
  "confidence": 0
}
```

**Example** (cURL):
```bash
curl -X POST http://localhost:5000/api/detect-emotion \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,..."}'
```

**Example** (Python):
```python
import requests
import base64

# Read image and encode
with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Send request
response = requests.post(
    'http://localhost:5000/api/detect-emotion',
    json={'image': f'data:image/jpeg;base64,{image_data}'}
)

result = response.json()
print(f"Dominant emotion: {result['dominant_emotion']}")
print(f"Confidence: {result['confidence']}%")
```

**Example** (JavaScript):
```javascript
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
// ... draw image to canvas ...

const imageData = canvas.toDataURL('image/jpeg', 0.8);

fetch('http://localhost:5000/api/detect-emotion', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ image: imageData })
})
.then(response => response.json())
.then(data => {
  console.log('Dominant emotion:', data.dominant_emotion);
  console.log('Confidence:', data.confidence);
});
```

---

### 3. Detect Emotion (File Upload)

Detect emotions from an uploaded image file.

**Endpoint**: `POST /api/detect-emotion-file`

**Request Headers**:
```http
Content-Type: multipart/form-data
```

**Request Body** (Form Data):
- `file` (file, required): Image file (JPEG, PNG)

**Response** (200 OK):
```json
{
  "dominant_emotion": "sad",
  "emotions": {
    "angry": 5.2,
    "disgusted": 2.1,
    "fearful": 3.4,
    "happy": 8.7,
    "neutral": 12.3,
    "sad": 65.8,
    "surprised": 2.5
  },
  "confidence": 65.8
}
```

**Response Fields**: Same as `/api/detect-emotion`

**Error Response** (400 Bad Request):
```json
{
  "error": "No file provided"
}
```

**Example** (cURL):
```bash
curl -X POST http://localhost:5000/api/detect-emotion-file \
  -F "file=@image.jpg"
```

**Example** (Python):
```python
import requests

with open('image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:5000/api/detect-emotion-file',
        files=files
    )

result = response.json()
print(f"Emotion: {result['dominant_emotion']}")
```

**Example** (JavaScript):
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/api/detect-emotion-file', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Emotion:', data.dominant_emotion);
});
```

---

## 📝 Request/Response Formats

### Image Formats

**Supported Formats**:
- JPEG (.jpg, .jpeg)
- PNG (.png)

**Image Processing**:
- Images are automatically resized to 48x48 for custom models
- Face detection is performed before emotion analysis
- Images are converted to grayscale for custom models

### Emotion Labels

The API returns 7 emotion categories:

1. `angry` - Anger
2. `disgusted` - Disgust
3. `fearful` - Fear
4. `happy` - Happiness
5. `neutral` - Neutral expression
6. `sad` - Sadness
7. `surprised` - Surprise

### Confidence Scores

- Range: 0.0 to 100.0 (percentage)
- Sum of all emotions: ~100%
- Higher scores indicate stronger predictions

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful (may include error in response body) |
| 400 | Bad Request | Invalid request (missing image/file) |
| 500 | Internal Server Error | Server error during processing |

### Error Response Format

```json
{
  "error": "Error message description"
}
```

### Common Errors

**No Image Provided**:
```json
{
  "error": "No image provided"
}
```
**Solution**: Include `image` field in JSON body

**No File Provided**:
```json
{
  "error": "No file provided"
}
```
**Solution**: Include `file` in form data

**Invalid Image Data**:
```json
{
  "error": "Invalid image data"
}
```
**Solution**: Check image format and encoding

**No Face Detected**:
```json
{
  "error": "No face detected in image. Please ensure a face is visible.",
  "dominant_emotion": null,
  "emotions": {},
  "confidence": 0
}
```
**Solution**: Ensure face is clearly visible in image

## 🔄 Rate Limiting

Currently, the API does not implement rate limiting. For production:

- Implement rate limiting (e.g., 100 requests/minute)
- Add API key authentication
- Monitor usage and set quotas

## 📊 Example Workflows

### Real-time Camera Detection

```javascript
// Capture frame from video
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
ctx.drawImage(videoElement, 0, 0);
const imageData = canvas.toDataURL('image/jpeg', 0.8);

// Send to API
fetch('/api/detect-emotion', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({image: imageData})
})
.then(res => res.json())
.then(data => {
  if (data.error) {
    console.error(data.error);
  } else {
    updateUI(data);
  }
});
```

### Batch Image Processing

```python
import requests
import os

def process_images(image_dir):
    results = []
    for filename in os.listdir(image_dir):
        if filename.endswith(('.jpg', '.png')):
            with open(os.path.join(image_dir, filename), 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    'http://localhost:5000/api/detect-emotion-file',
                    files=files
                )
                results.append({
                    'file': filename,
                    'emotion': response.json()['dominant_emotion'],
                    'confidence': response.json()['confidence']
                })
    return results
```

## 🔗 Related Documentation

- [Architecture](03-architecture.md) - System architecture
- [Usage Guide](04-usage-guide.md) - Application usage
- [Frontend Guide](07-frontend-guide.md) - Frontend integration
- [Troubleshooting](09-troubleshooting.md) - Common issues

---

**Next**: Learn about frontend development in the [Frontend Guide](07-frontend-guide.md)

