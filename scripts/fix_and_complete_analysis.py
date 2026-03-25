"""
Fix and complete the analysis after training
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.models import load_model
from PIL import Image
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Dataset path
DATASET_PATH = r'C:\Users\Meron  Yenie\Downloads\archive (1)'
TEST_DIR = os.path.join(DATASET_PATH, 'test')
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'final_model.h5')

# Emotion labels
EMOTION_LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

def load_test_data():
    """Load test dataset"""
    print("Loading test data...")
    images = []
    labels = []
    
    for emotion_idx, emotion in enumerate(EMOTION_LABELS):
        emotion_folder = os.path.join(TEST_DIR, emotion)
        if not os.path.exists(emotion_folder):
            continue
        
        files = [f for f in os.listdir(emotion_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        print(f"  {emotion}: {len(files)} images")
        
        for file in files:
            try:
                img_path = os.path.join(emotion_folder, file)
                img = Image.open(img_path).convert('L')
                img = img.resize((48, 48))
                images.append(np.array(img))
                labels.append(emotion_idx)
            except:
                continue
    
    X_test = np.array(images).astype('float32') / 255.0
    X_test = np.expand_dims(X_test, -1)
    y_test = np.array(labels)
    
    return X_test, y_test

def plot_confusion_matrix_fixed(y_true, y_pred, save_path='confusion_matrix.png'):
    """Plot and save confusion matrix with numpy fix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=EMOTION_LABELS, yticklabels=EMOTION_LABELS,
                cbar_kws={'label': 'Count'}, mask=None)
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Confusion matrix saved to {save_path}")
    plt.close()

def main():
    print("="*60)
    print("COMPLETING ANALYSIS - FIXING NUMPY COMPATIBILITY")
    print("="*60)
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        # Try best_model.h5
        best_model = MODEL_PATH.replace('final_model.h5', 'best_model.h5')
        if os.path.exists(best_model):
            print(f"Using best_model.h5 instead...")
            model = load_model(best_model)
        else:
            print(f"❌ Model not found at {MODEL_PATH}")
            return
    else:
        print(f"✅ Loading model from {MODEL_PATH}")
        model = load_model(MODEL_PATH)
    
    # Load test data
    X_test, y_test = load_test_data()
    print(f"\n✅ Test dataset loaded: {len(X_test)} samples")
    
    # Make predictions
    print("\n🔮 Making predictions...")
    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"\n🎯 Test Accuracy: {accuracy*100:.2f}%")
    
    # Generate confusion matrix
    print("\n📊 Generating confusion matrix...")
    plot_confusion_matrix_fixed(y_test, y_pred)
    
    # Classification report
    print("\n📋 Generating classification report...")
    report = classification_report(y_test, y_pred, target_names=EMOTION_LABELS)
    print(report)
    
    # Save results
    with open('training_results.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("EMOTION DETECTION - TRAINING RESULTS\n")
        f.write("="*60 + "\n\n")
        f.write(f"Test Accuracy: {accuracy*100:.2f}%\n\n")
        f.write("Classification Report:\n")
        f.write(report)
    
    print("\n✅ Results saved to training_results.txt")
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

