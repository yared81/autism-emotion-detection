"""
Final Analysis Script - Generates comprehensive analysis report after training
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from PIL import Image
import pandas as pd

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
        
        for file in files[:1000]:  # Limit for faster processing
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

def generate_comprehensive_report():
    """Generate comprehensive analysis report"""
    print("="*60)
    print("FINAL MODEL ANALYSIS REPORT")
    print("="*60)
    
    # Load model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        print("Please train the model first!")
        return
    
    print(f"\n✅ Loading model from {MODEL_PATH}")
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
    
    # Per-class accuracy
    print(f"\n{'='*60}")
    print("PER-CLASS ACCURACY")
    print(f"{'='*60}")
    
    cm = confusion_matrix(y_test, y_pred)
    per_class_accuracy = cm.diagonal() / cm.sum(axis=1)
    
    results_df = pd.DataFrame({
        'Emotion': EMOTION_LABELS,
        'Accuracy (%)': [acc*100 for acc in per_class_accuracy],
        'Samples': cm.sum(axis=1),
        'Correct': cm.diagonal(),
        'Incorrect': cm.sum(axis=1) - cm.diagonal()
    })
    
    print(results_df.to_string(index=False))
    
    # Classification report
    print(f"\n{'='*60}")
    print("DETAILED CLASSIFICATION REPORT")
    print(f"{'='*60}")
    report = classification_report(y_test, y_pred, target_names=EMOTION_LABELS)
    print(report)
    
    # Enhanced confusion matrix
    plt.figure(figsize=(14, 12))
    
    # Normalized confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Fix numpy compatibility
    import warnings
    warnings.filterwarnings('ignore')
    
    # Count confusion matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=EMOTION_LABELS, yticklabels=EMOTION_LABELS,
                cbar_kws={'label': 'Count'}, ax=axes[0], mask=None)
    axes[0].set_title('Confusion Matrix (Counts)', fontsize=16, fontweight='bold', pad=20)
    axes[0].set_xlabel('Predicted Label', fontsize=12)
    axes[0].set_ylabel('True Label', fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].tick_params(axis='y', rotation=0)
    
    # Normalized confusion matrix
    sns.heatmap(cm_normalized, annot=True, fmt='.2%', cmap='Greens',
                xticklabels=EMOTION_LABELS, yticklabels=EMOTION_LABELS,
                cbar_kws={'label': 'Percentage'}, ax=axes[1], mask=None)
    axes[1].set_title('Confusion Matrix (Normalized)', fontsize=16, fontweight='bold', pad=20)
    axes[1].set_xlabel('Predicted Label', fontsize=12)
    axes[1].set_ylabel('True Label', fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='y', rotation=0)
    
    plt.tight_layout()
    plt.savefig('final_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\n✅ Enhanced confusion matrix saved to final_confusion_matrix.png")
    plt.close()
    
    # Per-class performance bar chart
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Accuracy per class
    axes[0].bar(range(len(EMOTION_LABELS)), per_class_accuracy * 100, color='steelblue')
    axes[0].set_title('Per-Class Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Emotion Class', fontsize=12)
    axes[0].set_ylabel('Accuracy (%)', fontsize=12)
    axes[0].set_xticks(range(len(EMOTION_LABELS)))
    axes[0].set_xticklabels(EMOTION_LABELS, rotation=45, ha='right')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].axhline(y=accuracy*100, color='r', linestyle='--', label=f'Overall: {accuracy*100:.2f}%')
    axes[0].legend()
    
    # Add value labels
    for i, acc in enumerate(per_class_accuracy * 100):
        axes[0].text(i, acc, f'{acc:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Sample distribution
    sample_counts = cm.sum(axis=1)
    axes[1].bar(range(len(EMOTION_LABELS)), sample_counts, color='coral')
    axes[1].set_title('Test Set Class Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Emotion Class', fontsize=12)
    axes[1].set_ylabel('Number of Samples', fontsize=12)
    axes[1].set_xticks(range(len(EMOTION_LABELS)))
    axes[1].set_xticklabels(EMOTION_LABELS, rotation=45, ha='right')
    axes[1].grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, count in enumerate(sample_counts):
        axes[1].text(i, count, str(count), ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('final_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Performance analysis saved to final_performance_analysis.png")
    plt.close()
    
    # Save detailed report
    with open('FINAL_ANALYSIS_REPORT.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("FINAL MODEL ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Model: {MODEL_PATH}\n")
        f.write(f"Test Samples: {len(X_test)}\n")
        f.write(f"Test Accuracy: {accuracy*100:.2f}%\n\n")
        
        f.write("="*60 + "\n")
        f.write("PER-CLASS ACCURACY\n")
        f.write("="*60 + "\n")
        f.write(results_df.to_string(index=False))
        f.write("\n\n")
        
        f.write("="*60 + "\n")
        f.write("DETAILED CLASSIFICATION REPORT\n")
        f.write("="*60 + "\n")
        f.write(report)
        f.write("\n\n")
        
        f.write("="*60 + "\n")
        f.write("CONFUSION MATRIX\n")
        f.write("="*60 + "\n")
        f.write("Rows = True Labels, Columns = Predicted Labels\n\n")
        f.write(pd.DataFrame(cm, index=EMOTION_LABELS, columns=EMOTION_LABELS).to_string())
        f.write("\n\n")
        
        f.write("="*60 + "\n")
        f.write("NORMALIZED CONFUSION MATRIX (Percentages)\n")
        f.write("="*60 + "\n")
        f.write(pd.DataFrame(cm_normalized*100, index=EMOTION_LABELS, columns=EMOTION_LABELS).to_string())
    
    print("\n✅ Detailed report saved to FINAL_ANALYSIS_REPORT.txt")
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    print(f"\n📊 Generated Files:")
    print(f"  - final_confusion_matrix.png")
    print(f"  - final_performance_analysis.png")
    print(f"  - FINAL_ANALYSIS_REPORT.txt")
    print(f"\n🎯 Final Test Accuracy: {accuracy*100:.2f}%")

if __name__ == '__main__':
    generate_comprehensive_report()

