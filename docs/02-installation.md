# Installation Guide

This guide provides detailed installation instructions for all components of the Autism Emotion Detection project.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Backend Installation](#backend-installation)
- [Frontend Installation](#frontend-installation)
- [Verification](#verification)
- [Platform-Specific Notes](#platform-specific-notes)

## 🔧 System Requirements

### Minimum Requirements

- **OS**: Windows 10, macOS 10.15, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **Node.js**: 14.0 or higher
- **RAM**: 4GB minimum
- **Storage**: 2GB free space
- **Internet**: Required for downloading dependencies

### Recommended Requirements

- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **RAM**: 8GB or more
- **GPU**: CUDA-compatible GPU for training (optional)
- **Storage**: 5GB+ for models and dependencies

## 🐍 Backend Installation

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip 20.0 or higher
```

### Step 2: Navigate to Backend Directory

```bash
cd backend
```

### Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Backend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Verify Backend Installation

```bash
python -c "import flask, cv2, numpy, tensorflow; print('All dependencies installed!')"
```

If you see "All dependencies installed!", the backend is ready.

### Step 6: Install Model Dependencies (Optional)

If you plan to train models, install additional dependencies:

```bash
cd ../scripts
pip install -r requirements_training.txt
```

## ⚛️ Frontend Installation

### Step 1: Verify Node.js Installation

```bash
node --version
# Should show v14.0 or higher

npm --version
# Should show 6.0 or higher
```

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Frontend Dependencies

```bash
npm install
```

This will install:
- React and React DOM
- Tailwind CSS
- Axios for API calls
- Other development dependencies

### Step 4: Verify Frontend Installation

```bash
npm list --depth=0
```

You should see all packages listed without errors.

## ✅ Verification

### Test Backend

1. Start the backend server:
```bash
cd backend
python app.py
```

2. You should see:
```
✅ Custom model loaded successfully from ...
 * Running on http://0.0.0.0:5000
```

3. Test the health endpoint:
```bash
# In another terminal
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "message": "Emotion Detection API is running",
  "model": "custom trained model"
}
```

### Test Frontend

1. Start the frontend:
```bash
cd frontend
npm start
```

2. Browser should automatically open to `http://localhost:3000`

3. You should see the Emotion Detection interface

## 🔐 Environment Setup

### Backend Environment Variables

Create a `.env` file in the `backend/` directory (optional):

```env
PORT=5000
FLASK_ENV=development
MODEL_PATH=models/final_model.h5
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory (optional):

```env
REACT_APP_API_URL=http://localhost:5000
```

## 🪟 Platform-Specific Notes

### Windows

**Common Issues:**
- Use `python` instead of `python3`
- Use backslashes in paths: `venv\Scripts\activate`
- May need to install Visual C++ Build Tools for some packages

**PowerShell:**
```powershell
# If you get execution policy errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS

**Common Issues:**
- May need to install Xcode Command Line Tools:
```bash
xcode-select --install
```

- If using Homebrew Python:
```bash
brew install python3
```

### Linux

**Ubuntu/Debian:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv nodejs npm

# May need to install additional packages for OpenCV
sudo apt-get install libopencv-dev python3-opencv
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-pip python3-virtualenv nodejs npm
```

## 🐛 Troubleshooting Installation

### Python Issues

**Problem**: `python` command not found
- **Solution**: Use `python3` instead, or add Python to PATH

**Problem**: `pip` command not found
- **Solution**: Install pip: `python -m ensurepip --upgrade`

### Node.js Issues

**Problem**: `npm` command not found
- **Solution**: Reinstall Node.js from [nodejs.org](https://nodejs.org/)

**Problem**: Permission errors on npm install
- **Solution**: Use `npm install --legacy-peer-deps` or fix npm permissions

### Dependency Installation Issues

**Problem**: OpenCV installation fails
- **Solution**: 
  ```bash
  pip install opencv-python-headless
  ```

**Problem**: TensorFlow installation fails
- **Solution**: 
  ```bash
  pip install tensorflow --upgrade
  ```

**Problem**: Watchdog compatibility issues
- **Solution**: 
  ```bash
  pip install --upgrade werkzeug watchdog
  ```

### Virtual Environment Issues

**Problem**: Virtual environment not activating
- **Solution**: Use full path or check activation script exists

**Problem**: Packages not found after activation
- **Solution**: Ensure virtual environment is activated (check prompt)

## 📦 Dependency Management

### Backend Dependencies

Core dependencies are listed in `backend/requirements.txt`:
- Flask (web framework)
- Flask-CORS (CORS support)
- OpenCV (image processing)
- NumPy (numerical operations)
- TensorFlow (ML framework)
- DeepFace (fallback emotion detection)

### Frontend Dependencies

Core dependencies are in `frontend/package.json`:
- React (UI framework)
- Tailwind CSS (styling)
- Axios (HTTP client)

### Updating Dependencies

**Backend:**
```bash
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
npm update
```

## 🎯 Quick Installation Scripts

### Windows (Batch File)

Use the provided batch files:
- `start_backend.bat` - Starts backend server
- `start_frontend.bat` - Starts frontend server

### Linux/Mac (Shell Script)

Create startup scripts:
```bash
# start_backend.sh
#!/bin/bash
cd backend
source venv/bin/activate
python app.py
```

## 📚 Next Steps

After successful installation:

1. **Verify Installation**: Run the verification steps above
2. **Read Usage Guide**: [Usage Guide](04-usage-guide.md)
3. **Check Architecture**: [System Architecture](03-architecture.md)

## 🔗 Related Documentation

- [Getting Started](01-getting-started.md) - Quick start guide
- [Troubleshooting](09-troubleshooting.md) - Common issues and solutions
- [Development Guide](10-development.md) - Development setup

---

**Installation complete?** Move on to the [Usage Guide](04-usage-guide.md) to learn how to use the application!

