# Frontend Guide

Complete guide to the React frontend of the Autism Emotion Detection application.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Component Structure](#component-structure)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Styling with Tailwind CSS](#styling-with-tailwind-css)
- [Building and Deployment](#building-and-deployment)
- [Environment Variables](#environment-variables)
- [Customization](#customization)

## 🎯 Overview

The frontend is built with React 18 and Tailwind CSS, providing a modern, responsive interface for emotion detection.

### Technology Stack

- **React 18.2.0** - UI framework
- **Tailwind CSS 3.3.6** - Utility-first CSS framework
- **Axios 1.6.0** - HTTP client for API calls
- **React Scripts 5.0.1** - Build tools and development server

## 🏗️ Architecture

### Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── index.js            # React entry point
│   ├── index.css           # Global styles
│   ├── App.js              # Main app component
│   ├── App.css             # App-specific styles
│   └── components/
│       └── EmotionDetector.js  # Main detection component
├── package.json             # Dependencies
├── tailwind.config.js       # Tailwind configuration
└── postcss.config.js        # PostCSS configuration
```

### Component Hierarchy

```
App
└── EmotionDetector
    ├── Video Element
    ├── Canvas Element
    ├── Controls (Start/Stop Camera, Upload)
    ├── Results Display
    └── Error Display
```

## 🧩 Component Structure

### App.js

Main application component that renders the EmotionDetector.

**Location**: `src/App.js`

**Key Features**:
- Sets up API URL from environment
- Provides app layout and header
- Renders EmotionDetector component

**Code Structure**:
```javascript
function App() {
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <header>...</header>
      <EmotionDetector apiUrl={API_URL} />
      <footer>...</footer>
    </div>
  );
}
```

### EmotionDetector Component

Main component handling all emotion detection functionality.

**Location**: `src/components/EmotionDetector.js`

**Key Responsibilities**:
- Camera management
- Image capture and processing
- API communication
- Results display
- Error handling

## 📊 State Management

### State Variables

```javascript
const [isDetecting, setIsDetecting] = useState(false);
const [emotion, setEmotion] = useState(null);
const [emotions, setEmotions] = useState({});
const [error, setError] = useState(null);
const [fps, setFps] = useState(0);
```

**State Descriptions**:
- `isDetecting`: Boolean indicating if camera detection is active
- `emotion`: String with dominant emotion name
- `emotions`: Object with all emotion scores
- `error`: String with error message (if any)
- `fps`: Number showing frames per second

### Refs

```javascript
const videoRef = useRef(null);        // Video element reference
const canvasRef = useRef(null);       // Canvas element reference
const streamRef = useRef(null);       // Media stream reference
const animationFrameRef = useRef(null); // Animation frame ID
const isDetectingRef = useRef(false);  // Detection state ref (for closures)
```

**Ref Usage**:
- `videoRef`: Access video element for camera feed
- `canvasRef`: Hidden canvas for frame capture
- `streamRef`: Media stream for cleanup
- `animationFrameRef`: Cancel animation frames
- `isDetectingRef`: Track detection state in closures

## 🔌 API Integration

### API Client Setup

```javascript
import axios from 'axios';

const apiUrl = 'http://localhost:5000';
```

### Camera Detection Endpoint

**Endpoint**: `POST /api/detect-emotion`

**Implementation**:
```javascript
const detectEmotion = async () => {
  // Capture frame to canvas
  const canvas = canvasRef.current;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(videoRef.current, 0, 0);
  
  // Convert to base64
  const imageData = canvas.toDataURL('image/jpeg', 0.8);
  
  // Send to API
  const response = await axios.post(`${apiUrl}/api/detect-emotion`, {
    image: imageData
  });
  
  // Update state
  setEmotion(response.data.dominant_emotion);
  setEmotions(response.data.emotions);
};
```

### File Upload Endpoint

**Endpoint**: `POST /api/detect-emotion-file`

**Implementation**:
```javascript
const handleFileUpload = async (e) => {
  const file = e.target.files[0];
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(
    `${apiUrl}/api/detect-emotion-file`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  
  setEmotion(response.data.dominant_emotion);
  setEmotions(response.data.emotions);
};
```

### Error Handling

```javascript
try {
  const response = await axios.post(...);
  if (response.data.error) {
    setError(response.data.error);
  } else {
    setEmotion(response.data.dominant_emotion);
    setEmotions(response.data.emotions);
  }
} catch (err) {
  if (err.response?.data?.error) {
    setError(err.response.data.error);
  } else {
    setError('Failed to detect emotion');
  }
}
```

## 🎨 Styling with Tailwind CSS

### Configuration

**File**: `tailwind.config.js`

```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Utility Classes

The frontend uses Tailwind utility classes extensively:

**Layout**:
```javascript
<div className="max-w-6xl mx-auto">
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
```

**Colors**:
```javascript
className="bg-gradient-to-r from-blue-600 to-purple-600"
className="bg-green-500"
```

**Spacing**:
```javascript
className="p-6 mt-4 mb-6"
```

### Custom Styles

**Global Styles**: `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Component Styles**: `src/App.css`

Additional component-specific styles if needed.

## 🚀 Building and Deployment

### Development

```bash
cd frontend
npm start
```

Starts development server at `http://localhost:3000`

### Production Build

```bash
npm run build
```

Creates optimized production build in `build/` directory.

### Deploying Build

**Static Hosting** (Netlify, Vercel, etc.):
1. Run `npm run build`
2. Upload `build/` directory
3. Configure redirects for React Router (if used)

**Server Deployment**:
```bash
# Serve with serve package
npm install -g serve
serve -s build -l 3000
```

## 🔧 Environment Variables

### Configuration

Create `.env` file in `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

### Usage

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

**Note**: Environment variables must start with `REACT_APP_` to be accessible in React.

### Production Environment

For production, set environment variables:
- Build-time: Set in `.env.production`
- Runtime: Configure in hosting platform

## 🎨 Customization

### Changing Colors

Update emotion colors in `EmotionDetector.js`:

```javascript
const emotionColors = {
  'happy': 'bg-green-500',
  'sad': 'bg-blue-500',
  // ... customize colors
};
```

### Modifying Layout

Update component structure in `EmotionDetector.js`:

```javascript
return (
  <div className="max-w-6xl mx-auto">
    {/* Customize layout here */}
  </div>
);
```

### Adding Features

**New Emotion Categories**:
1. Update `emotionColors` and `emotionEmojis` objects
2. Ensure backend supports new emotions
3. Update UI display logic

**Additional Controls**:
```javascript
<button onClick={handleNewFeature}>
  New Feature
</button>
```

### Styling Customization

**Theme Colors**:
Update `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      'custom-blue': '#1e40af',
    }
  }
}
```

**Custom Components**:
Create reusable components in `src/components/`:

```javascript
// src/components/EmotionCard.js
export default function EmotionCard({ emotion, confidence }) {
  return (
    <div className="bg-white rounded-lg p-4">
      {/* Custom card design */}
    </div>
  );
}
```

## 🔄 Detection Loop

### Camera Detection Flow

```javascript
const detectEmotion = async () => {
  // 1. Check if ready
  if (!videoRef.current || !isDetectingRef.current) return;
  
  // 2. Capture frame
  ctx.drawImage(video, 0, 0);
  const imageData = canvas.toDataURL('image/jpeg', 0.8);
  
  // 3. Send to API
  const response = await axios.post(...);
  
  // 4. Update state
  setEmotion(response.data.dominant_emotion);
  
  // 5. Continue loop
  if (isDetectingRef.current) {
    setTimeout(detectEmotion, 300);
  }
};
```

### Performance Optimization

- **Frame Rate**: Limited to ~3-4 FPS (300ms delay)
- **Image Quality**: JPEG compression (0.8 quality)
- **Canvas Reuse**: Single canvas element reused
- **State Updates**: Batched React updates

## 🐛 Debugging

### Console Logging

```javascript
console.log('Detection response:', response.data);
console.error('Detection error:', err);
```

### React DevTools

Install React Developer Tools browser extension for:
- Component inspection
- State debugging
- Performance profiling

### Network Inspection

Use browser DevTools Network tab to:
- Inspect API requests
- Check response times
- Debug CORS issues

## 📚 Related Documentation

- [API Reference](06-api-reference.md) - Backend API details
- [Usage Guide](04-usage-guide.md) - Application usage
- [Architecture](03-architecture.md) - System architecture
- [Troubleshooting](09-troubleshooting.md) - Common issues

---

**Next**: Learn about the model in [Model Information](08-model-information.md)

