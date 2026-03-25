from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'final_model.h5')
MODEL = None

# Emotion labels (matching training)
EMOTION_LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

def load_custom_model():
    """Load the custom trained model"""
    global MODEL
    try:
        if os.path.exists(MODEL_PATH):
            MODEL = load_model(MODEL_PATH)
            print(f"✅ Custom model loaded successfully from {MODEL_PATH}")
            return True
        else:
            print(f"⚠️  Model not found at {MODEL_PATH}")
            print("   Using fallback to DeepFace...")
            return False
    except Exception as e:
        print(f"❌ Error loading custom model: {e}")
        return False

# Try to load custom model on startup
use_custom_model = load_custom_model()

@app.route('/api/health', methods=['GET'])
def health():
    model_status = "custom trained model" if use_custom_model and MODEL else "DeepFace (fallback)"
    return jsonify({
        "status": "ok",
        "message": "Emotion Detection API is running",
        "model": model_status
    })

def preprocess_image(img, target_size=(48, 48)):
    """Preprocess image for the custom model"""
    # Convert to grayscale if needed
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

def predict_with_custom_model(img):
    """Predict emotions using custom trained model"""
    preprocessed = preprocess_image(img)
    predictions = MODEL.predict(preprocessed, verbose=0)[0]
    
    # Get emotion scores
    emotion_scores = {}
    for i, emotion in enumerate(EMOTION_LABELS):
        emotion_scores[emotion] = float(predictions[i] * 100)  # Convert to percentage
    
    # Get dominant emotion
    dominant_idx = np.argmax(predictions)
    dominant_emotion = EMOTION_LABELS[dominant_idx]
    confidence = float(predictions[dominant_idx] * 100)
    
    return {
        "dominant_emotion": dominant_emotion,
        "emotions": emotion_scores,
        "confidence": confidence
    }

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
            return jsonify({"error": "Invalid image data"}), 400
        
        # Use custom model if available, otherwise fallback to DeepFace
        if use_custom_model and MODEL is not None:
            result = predict_with_custom_model(img)
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
            result = predict_with_custom_model(img)
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

