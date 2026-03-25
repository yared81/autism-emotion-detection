from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load the trained model (try final_model.h5 first, then best_model.h5)
# Get the project root directory (parent of backend directory)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FINAL_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'final_model.h5')
BEST_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'best_model.h5')
MODEL = None

# Emotion labels (matching training - lowercase)
EMOTION_LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

def load_custom_model():
    """Load the custom trained model"""
    global MODEL
    try:
        # List of possible paths to check
        possible_paths = [
            FINAL_MODEL_PATH,
            BEST_MODEL_PATH,
            # Fallback: relative path from backend directory
            os.path.join('..', 'models', 'final_model.h5'),
            os.path.join('..', 'models', 'best_model.h5'),
            # Fallback: absolute path from current working directory
            os.path.join(os.getcwd(), 'models', 'final_model.h5'),
            os.path.join(os.getcwd(), 'models', 'best_model.h5'),
            # Fallback: from project root if running from different location
            os.path.join(PROJECT_ROOT, 'models', 'final_model.h5'),
            os.path.join(PROJECT_ROOT, 'models', 'best_model.h5'),
        ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_paths = []
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if abs_path not in seen:
                seen.add(abs_path)
                unique_paths.append(abs_path)
        
        # Try each path
        for model_path in unique_paths:
            if os.path.exists(model_path):
                MODEL = load_model(model_path)
                print(f"✅ Custom model loaded successfully from {model_path}")
                return True
        
        # If we get here, no model was found
        print(f"⚠️  Model not found. Checked paths:")
        for path in unique_paths[:4]:  # Show first 4 paths
            print(f"   - {path} (exists: {os.path.exists(path)})")
        print("   Using fallback to DeepFace...")
        return False
    except Exception as e:
        print(f"❌ Error loading custom model: {e}")
        import traceback
        traceback.print_exc()
        return False

# Try to load custom model on startup
use_custom_model = load_custom_model()

def detect_face(img):
    """Detect face in image using Haar Cascade"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        # Return the largest face
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = largest_face
        return gray[y:y+h, x:x+w], (x, y, w, h)
    return None, None

def preprocess_image(img, target_size=(48, 48), detect_face_first=True):
    """Preprocess image for the custom model"""
    # Try to detect face first (for camera/webcam feeds)
    if detect_face_first:
        face_roi, face_coords = detect_face(img)
        if face_roi is not None:
            # Use detected face region
            gray = face_roi
        else:
            # No face detected, use entire image (for uploaded images that are already cropped)
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
    else:
        # Direct processing without face detection
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
    
    # Resize to model input size
    resized = cv2.resize(gray, target_size)
    
    # Normalize
    normalized = resized.astype('float32') / 255.0
    
    # Reshape for model (add batch and channel dimensions)
    reshaped = np.expand_dims(normalized, axis=0)  # Add batch dimension
    reshaped = np.expand_dims(reshaped, axis=-1)   # Add channel dimension
    
    return reshaped

def predict_with_custom_model(img, detect_face_first=True):
    """Predict emotions using custom trained model"""
    # Detect face first for better accuracy (especially for camera feeds)
    face_roi, face_coords = detect_face(img) if detect_face_first else (None, None)
    
    if face_roi is None and detect_face_first:
        # No face detected - return error
        print("⚠️  No face detected in image")
        return {
            "error": "No face detected in image. Please ensure a face is visible.",
            "dominant_emotion": None,
            "emotions": {},
            "confidence": 0
        }
    
    print(f"✅ Face detected: {face_coords}")
    
    # Preprocess the image (or face region)
    preprocessed = preprocess_image(img, detect_face_first=detect_face_first)
    predictions = MODEL.predict(preprocessed, verbose=0)[0]
    print(f"✅ Predictions made: {predictions.shape}")
    
    # Get emotion scores
    emotion_scores = {}
    for i, emotion in enumerate(EMOTION_LABELS):
        emotion_scores[emotion] = float(predictions[i] * 100)  # Convert to percentage
    
    # Get dominant emotion
    dominant_idx = np.argmax(predictions)
    dominant_emotion = EMOTION_LABELS[dominant_idx]
    confidence = float(predictions[dominant_idx] * 100)
    
    result = {
        "dominant_emotion": dominant_emotion,
        "emotions": emotion_scores,
        "confidence": confidence
    }
    
    # Add face coordinates if detected (for frontend visualization)
    if face_coords:
        result["face_coordinates"] = {
            "x": int(face_coords[0]),
            "y": int(face_coords[1]),
            "width": int(face_coords[2]),
            "height": int(face_coords[3])
        }
    
    return result

@app.route('/api/health', methods=['GET'])
def health():
    model_status = "custom trained model" if use_custom_model and MODEL else "DeepFace (fallback)"
    return jsonify({
        "status": "ok",
        "message": "Emotion Detection API is running",
        "model": model_status
    })

@app.route('/api/detect-emotion', methods=['POST'])
def detect_emotion():
    try:
        data = request.json
        
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("❌ Failed to decode image")
            return jsonify({"error": "Invalid image data"}), 400
        
        print(f"✅ Image decoded successfully: {img.shape}")
        
        # Use custom model if available, otherwise fallback to DeepFace
        if use_custom_model and MODEL is not None:
            # For camera/webcam feeds, detect face first
            result = predict_with_custom_model(img, detect_face_first=True)
            
            # Check if there was an error (no face detected)
            if result.get("error"):
                # Return error but don't fail completely - let frontend handle it
                return jsonify(result), 200  # Return 200 so frontend can display the error message
            
            # Success - return the result
            return jsonify(result)
        else:
            # Fallback to DeepFace
            from deepface import DeepFace
            result_deepface = DeepFace.analyze(
                img,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            if isinstance(result_deepface, list):
                result_deepface = result_deepface[0]
            
            emotion_scores = result_deepface.get('emotion', {})
            dominant_emotion = result_deepface.get('dominant_emotion', 'Unknown')
            
            result = {
                "dominant_emotion": dominant_emotion,
                "emotions": emotion_scores,
                "confidence": emotion_scores.get(dominant_emotion, 0) if emotion_scores else 0
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/detect-emotion-file', methods=['POST'])
def detect_emotion_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Read image file
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({"error": "Invalid image file"}), 400
        
        # Use custom model if available
        if use_custom_model and MODEL is not None:
            # For file uploads, try with face detection first, fallback to full image
            result = predict_with_custom_model(img, detect_face_first=True)
            
            # If no face detected, try processing entire image (for pre-cropped images)
            if result.get("error"):
                result = predict_with_custom_model(img, detect_face_first=False)
        else:
            # Fallback to DeepFace
            from deepface import DeepFace
            result_deepface = DeepFace.analyze(
                img,
                actions=['emotion'],
                enforce_detection=False,
                silent=True
            )
            
            if isinstance(result_deepface, list):
                result_deepface = result_deepface[0]
            
            emotion_scores = result_deepface.get('emotion', {})
            dominant_emotion = result_deepface.get('dominant_emotion', 'Unknown')
            
            result = {
                "dominant_emotion": dominant_emotion,
                "emotions": emotion_scores,
                "confidence": emotion_scores.get(dominant_emotion, 0) if emotion_scores else 0
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

