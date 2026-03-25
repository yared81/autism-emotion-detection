# Troubleshooting

Common issues and solutions for the Autism Emotion Detection project.

## 📋 Table of Contents

- [Installation Issues](#installation-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Model Loading Problems](#model-loading-problems)
- [Camera Access Issues](#camera-access-issues)
- [Performance Optimization](#performance-optimization)
- [Error Messages](#error-messages)
- [Debugging Tips](#debugging-tips)

## 🔧 Installation Issues

### Python Not Found

**Problem**: `python: command not found` or `python3: command not found`

**Solutions**:
- **Windows**: Use `py` command: `py --version`
- **Linux/Mac**: Install Python: `sudo apt-get install python3` or `brew install python3`
- Add Python to PATH environment variable
- Use full path: `C:\Python39\python.exe`

### pip Not Found

**Problem**: `pip: command not found`

**Solutions**:
```bash
# Install pip
python -m ensurepip --upgrade

# Or use python -m pip instead
python -m pip install -r requirements.txt
```

### Node.js/npm Not Found

**Problem**: `node: command not found` or `npm: command not found`

**Solutions**:
- Download and install from [nodejs.org](https://nodejs.org/)
- Verify installation: `node --version` and `npm --version`
- Add to PATH if needed

### Virtual Environment Issues

**Problem**: Virtual environment not activating

**Windows**:
```bash
# Use full path
.\venv\Scripts\activate

# Or use python -m venv
python -m venv venv
```

**Linux/Mac**:
```bash
source venv/bin/activate
```

**Problem**: Packages not found after activation

**Solution**: Ensure virtual environment is activated (check for `(venv)` in prompt)

## 🐍 Backend Issues

### Flask Server Won't Start

**Problem**: `Address already in use`

**Solution**:
```bash
# Find and kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill
```

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Model Not Loading

**Problem**: `Model not found at models\final_model.h5`

**Solutions**:
1. Check model file exists: `ls models/` or `dir models\`
2. Verify file path in `backend/app.py`
3. Train a model first (see [Training Guide](05-training-guide.md))
4. Check file permissions

**Problem**: `Error loading custom model`

**Solution**:
- Check TensorFlow version: `pip install tensorflow>=2.10.0`
- Verify model file is not corrupted
- Check console for detailed error messages

### Watchdog Compatibility Error

**Problem**: `ImportError: cannot import name 'EVENT_TYPE_CLOSED'`

**Solution**:
```bash
pip install --upgrade werkzeug watchdog
```

Or disable reloader in `backend/app.py`:
```python
app.run(..., use_reloader=False)
```

### OpenCV Issues

**Problem**: `ImportError: No module named 'cv2'`

**Solution**:
```bash
pip install opencv-python
# Or for headless version:
pip install opencv-python-headless
```

**Problem**: OpenCV installation fails

**Solution**:
- Install system dependencies first
- Use pre-built wheels: `pip install --upgrade pip` then retry

## ⚛️ Frontend Issues

### npm Install Fails

**Problem**: `npm ERR!` errors during installation

**Solutions**:
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use legacy peer deps
npm install --legacy-peer-deps
```

### React App Won't Start

**Problem**: `EADDRINUSE: address already in use :::3000`

**Solution**:
```bash
# Kill process on port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill
```

**Problem**: Browser doesn't open automatically

**Solution**: Manually navigate to `http://localhost:3000`

### Build Errors

**Problem**: Build fails with errors

**Solutions**:
```bash
# Clear build cache
rm -rf build node_modules/.cache

# Reinstall dependencies
npm install

# Try building again
npm run build
```

## 🤖 Model Loading Problems

### Model File Not Found

**Problem**: Backend reports "Model not found"

**Solutions**:
1. Train a model first (see [Training Guide](05-training-guide.md))
2. Check model file location: `models/final_model.h5` or `models/best_model.h5`
3. Verify file exists: `ls models/` or `dir models\`
4. Check file permissions

### Model Loading Errors

**Problem**: `ValueError: Unknown layer` or similar errors

**Solution**:
- Ensure TensorFlow version matches training version
- Re-train model with current TensorFlow version
- Check model file is not corrupted

### DeepFace Fallback Issues

**Problem**: DeepFace not working as fallback

**Solution**:
```bash
pip install deepface
# May need to download models on first use
```

## 📷 Camera Access Issues

### Camera Permission Denied

**Problem**: Browser blocks camera access

**Solutions**:
1. Click "Allow" when browser prompts
2. Check browser settings:
   - Chrome: Settings → Privacy → Site Settings → Camera
   - Firefox: Preferences → Privacy → Permissions → Camera
3. Use HTTPS in production (required for camera access)
4. Check camera is not in use by another application

### Camera Not Detected

**Problem**: "Unable to access camera"

**Solutions**:
1. Check camera is connected and working
2. Test camera in another application
3. Check device manager (Windows) or system settings
4. Restart browser
5. Try different browser

### Camera Feed Not Showing

**Problem**: Camera starts but no video appears

**Solutions**:
1. Check browser console for errors
2. Verify camera permissions
3. Try refreshing the page
4. Check if other apps are using camera
5. Test in different browser

### Detection Not Working

**Problem**: Camera works but no detection

**Solutions**:
1. Check backend is running: `http://localhost:5000/api/health`
2. Check browser console for API errors
3. Verify API URL in frontend: `REACT_APP_API_URL`
4. Check network tab in browser DevTools
5. Ensure face is clearly visible

## ⚡ Performance Optimization

### Slow Detection

**Problem**: Detection is slow or laggy

**Solutions**:
1. Reduce frame rate (increase delay in detection loop)
2. Lower image quality (reduce JPEG compression)
3. Use GPU for model inference
4. Close unnecessary browser tabs
5. Check system resources (CPU/RAM usage)

### High Memory Usage

**Problem**: Application uses too much memory

**Solutions**:
1. Reduce batch size in training
2. Limit concurrent API requests
3. Clear browser cache
4. Restart application periodically
5. Use smaller model (fast model instead of advanced)

### Slow Training

**Problem**: Model training takes too long

**Solutions**:
1. Use GPU (TensorFlow will detect automatically)
2. Use fast training script
3. Reduce dataset size (sampling)
4. Reduce epochs or use early stopping
5. Increase batch size (if memory allows)

## ❌ Error Messages

### "No face detected in image"

**Cause**: Face detection failed

**Solutions**:
- Ensure face is clearly visible
- Improve lighting
- Face camera directly
- Remove face coverings
- Try different image

### "Invalid image data"

**Cause**: Image decoding failed

**Solutions**:
- Check image format (JPEG/PNG)
- Verify image is not corrupted
- Check base64 encoding
- Try different image

### "No image provided"

**Cause**: Missing image in request

**Solutions**:
- Check request format
- Verify image field in JSON
- Check file upload form data

### "Failed to detect emotion"

**Cause**: General API error

**Solutions**:
- Check backend logs
- Verify model is loaded
- Check image format
- Try again with different image

## 🐛 Debugging Tips

### Backend Debugging

**Enable Debug Mode**:
```python
# In backend/app.py
app.run(debug=True, use_reloader=False)
```

**Check Logs**:
- Console output shows model loading status
- API requests logged to console
- Error tracebacks printed

**Test Endpoints**:
```bash
# Health check
curl http://localhost:5000/api/health

# Test detection (with base64 image)
curl -X POST http://localhost:5000/api/detect-emotion \
  -H "Content-Type: application/json" \
  -d '{"image": "..."}'
```

### Frontend Debugging

**Browser Console**:
- Open DevTools (F12)
- Check Console tab for errors
- Check Network tab for API calls

**React DevTools**:
- Install React Developer Tools extension
- Inspect component state
- Check props and hooks

**Console Logging**:
```javascript
console.log('Detection response:', response.data);
console.error('Error:', err);
```

### Model Debugging

**Check Model Loading**:
```python
# In backend/app.py, add logging
print(f"Model loaded: {MODEL is not None}")
print(f"Model summary:")
MODEL.summary()
```

**Test Model Directly**:
```python
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('models/final_model.h5')
test_input = np.random.rand(1, 48, 48, 1)
prediction = model.predict(test_input)
print(prediction)
```

### Network Debugging

**Check API Connection**:
```bash
# Test backend is accessible
curl http://localhost:5000/api/health

# Check CORS headers
curl -I http://localhost:5000/api/health
```

**Browser Network Tab**:
- Check request/response headers
- Verify status codes
- Inspect response data
- Check for CORS errors

## 📚 Getting More Help

### Check Documentation

1. [Installation Guide](02-installation.md) - Setup issues
2. [API Reference](06-api-reference.md) - API problems
3. [Training Guide](05-training-guide.md) - Model training issues
4. [FAQ](11-faq.md) - Common questions

### Common Solutions Checklist

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Model file exists
- [ ] Camera permissions granted
- [ ] Browser console checked
- [ ] Network tab checked
- [ ] Logs reviewed

## 🔗 Related Documentation

- [Installation Guide](02-installation.md) - Setup instructions
- [API Reference](06-api-reference.md) - API details
- [Training Guide](05-training-guide.md) - Model training
- [Development Guide](10-development.md) - Development setup

---

**Next**: Development guide in [Development Guide](10-development.md)

