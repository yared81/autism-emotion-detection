# Getting Started

Welcome to the Autism Emotion Detection project! This guide will help you get up and running quickly.

## 🎯 Project Overview

The Autism Emotion Detection project is a web-based application that uses deep learning to detect and classify human emotions from facial expressions. It provides real-time emotion detection through webcam feeds and supports image upload for analysis.

### What This Project Does

- **Real-time Emotion Detection**: Analyze emotions from live webcam feed
- **Image Analysis**: Upload images for emotion detection
- **Custom Models**: Train your own emotion detection models
- **Web Interface**: Modern, responsive UI built with React and Tailwind CSS
- **RESTful API**: Backend API for emotion detection services

## ✨ Key Features

- 🎥 **Real-time Webcam Detection** - Live emotion analysis from camera feed
- 📸 **Image Upload** - Analyze emotions from uploaded images
- 🎨 **Modern UI** - Beautiful, responsive interface with Tailwind CSS
- 🤖 **AI-Powered** - Custom-trained CNN models or DeepFace integration
- 📊 **Detailed Results** - Emotion breakdown with confidence scores
- 🔧 **Customizable** - Train your own models with your dataset

## 🚀 Quick Start (5 Minutes)

### Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Node.js 14+ and npm installed
- [ ] Webcam (for real-time detection)
- [ ] Modern web browser (Chrome, Firefox, Edge, Safari)
- [ ] 2GB+ free disk space

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd Autism-Emotion-Detection

# Or download and extract the project folder
```

### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up Frontend

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### Step 4: Start the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python app.py
```
Backend will run on `http://localhost:5000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```
Frontend will open at `http://localhost:3000`

### Step 5: Use the Application

1. Open your browser to `http://localhost:3000`
2. Click **"Start Camera"** to begin real-time detection
3. Or click **"Upload Image"** to analyze a photo
4. View the emotion results and confidence scores

## 📋 What You'll Need

### Software Requirements

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Python | 3.8 | 3.10+ |
| Node.js | 14.0 | 18.0+ |
| npm | 6.0 | 9.0+ |
| pip | 20.0 | 23.0+ |

### Hardware Requirements

- **CPU**: Multi-core processor (2+ cores recommended)
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB free space for dependencies and models
- **Webcam**: For real-time detection (optional)
- **GPU**: Optional but recommended for training (CUDA-compatible)

### Operating System

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 10+, etc.)

## 🎓 Next Steps

Now that you have the application running:

1. **Learn to Use It**: Read the [Usage Guide](04-usage-guide.md)
2. **Understand the Architecture**: Check [System Architecture](03-architecture.md)
3. **Train Your Own Model**: Follow the [Training Guide](05-training-guide.md)
4. **Explore the API**: Review [API Reference](06-api-reference.md)

## 🆘 Need Help?

- **Installation Issues?** → See [Installation Guide](02-installation.md)
- **Something Not Working?** → Check [Troubleshooting](09-troubleshooting.md)
- **Have Questions?** → Read [FAQ](11-faq.md)

## 📚 Documentation Navigation

- **Previous**: [Documentation Index](README.md)
- **Next**: [Installation Guide](02-installation.md)

---

**Ready to dive deeper?** Continue to the [Installation Guide](02-installation.md) for detailed setup instructions.

