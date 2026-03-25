from deepface import DeepFace
import cv2

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Analyze the frame for emotions using DeepFace
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']

        # Display the emotion on the video feed
        cv2.putText(frame, f'Emotion: {dominant_emotion}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    except Exception as e:
        print("Error:", e)

    cv2.imshow('Real-Time Emotion Detection (DeepFace)', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
