import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

# Load the trained model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'final_model.h5')

# Emotion labels (matching training)
emotion_labels = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

# Load model
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
else:
    # Try fallback to old model name
    fallback_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'model.h5')
    if os.path.exists(fallback_path):
        model = load_model(fallback_path)
        print(f"✅ Model loaded from {fallback_path}")
    else:
        print(f"❌ Error: Model not found at {MODEL_PATH} or {fallback_path}")
        print("Please train the model first using train_advanced_model.py")
        exit(1)

# Start webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48,48))
        roi = roi/255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)
        pred = model.predict(roi, verbose=0)
        label = emotion_labels[np.argmax(pred)].capitalize()
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.putText(frame,label,(x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,255,0),2)
    cv2.imshow('Emotion Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
