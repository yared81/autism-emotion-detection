import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from PIL import Image
import pandas as pd

# Dataset path
DATASET_PATH = r'C:\Users\Meron  Yenie\Downloads\archive (1)'
TRAIN_DIR = os.path.join(DATASET_PATH, 'train')
TEST_DIR = os.path.join(DATASET_PATH, 'test')

# Emotion labels (matching folder names)
EMOTION_LABELS = ['angry', 'disgusted', 'fearful', 'happy', 'neutral', 'sad', 'surprised']

def load_images_labels(folder, img_size=(48, 48), max_samples_per_class=None):
    """Load images and labels from folder structure with optional sampling"""
    images = []
    labels = []
    
    print(f"\nLoading images from {folder}...")
    
    for emotion_idx, emotion in enumerate(EMOTION_LABELS):
        emotion_folder = os.path.join(folder, emotion)
        if not os.path.exists(emotion_folder):
            print(f"Warning: {emotion_folder} not found, skipping...")
            continue
            
        files = [f for f in os.listdir(emotion_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        # Limit samples per class for faster training
        if max_samples_per_class and len(files) > max_samples_per_class:
            import random
            files = random.sample(files, max_samples_per_class)
        
        print(f"  {emotion}: {len(files)} images")
        
        for file in files:
            try:
                img_path = os.path.join(emotion_folder, file)
                img = Image.open(img_path).convert('L')  # Convert to grayscale
                img = img.resize(img_size)
                images.append(np.array(img))
                labels.append(emotion_idx)
            except Exception as e:
                continue
    
    return np.array(images), np.array(labels)

def plot_class_distribution(y_train, y_test, save_path='class_distribution.png'):
    """Plot class distribution for train and test sets"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Train distribution
    train_counts = pd.Series(y_train).value_counts().sort_index()
    axes[0].bar(range(len(EMOTION_LABELS)), [train_counts.get(i, 0) for i in range(len(EMOTION_LABELS))])
    axes[0].set_title('Training Set Class Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Emotion Class', fontsize=12)
    axes[0].set_ylabel('Number of Images', fontsize=12)
    axes[0].set_xticks(range(len(EMOTION_LABELS)))
    axes[0].set_xticklabels(EMOTION_LABELS, rotation=45, ha='right')
    axes[0].grid(axis='y', alpha=0.3)
    
    for i, count in enumerate([train_counts.get(i, 0) for i in range(len(EMOTION_LABELS))]):
        axes[0].text(i, count, str(count), ha='center', va='bottom', fontsize=9)
    
    # Test distribution
    test_counts = pd.Series(y_test).value_counts().sort_index()
    axes[1].bar(range(len(EMOTION_LABELS)), [test_counts.get(i, 0) for i in range(len(EMOTION_LABELS))])
    axes[1].set_title('Test Set Class Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Emotion Class', fontsize=12)
    axes[1].set_ylabel('Number of Images', fontsize=12)
    axes[1].set_xticks(range(len(EMOTION_LABELS)))
    axes[1].set_xticklabels(EMOTION_LABELS, rotation=45, ha='right')
    axes[1].grid(axis='y', alpha=0.3)
    
    for i, count in enumerate([test_counts.get(i, 0) for i in range(len(EMOTION_LABELS))]):
        axes[1].text(i, count, str(count), ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nClass distribution saved to {save_path}")
    plt.close()

def create_fast_model(input_shape=(48, 48, 1), num_classes=7):
    """Create a faster, optimized CNN model for emotion recognition"""
    model = Sequential([
        # First Conv Block - Reduced filters
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape, padding='same'),
        BatchNormalization(),
        Conv2D(32, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Second Conv Block
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Third Conv Block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        
        # Dense Layers - Reduced size
        Flatten(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def plot_confusion_matrix(y_true, y_pred, save_path='confusion_matrix.png'):
    """Plot and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(12, 10))
    # Fix numpy compatibility issue
    import warnings
    warnings.filterwarnings('ignore')
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
    print(f"\nConfusion matrix saved to {save_path}")
    plt.close()

def plot_training_history(history, save_path='training_history.png'):
    """Plot training history"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Accuracy
    axes[0].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
    axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Accuracy', fontsize=12)
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Loss
    axes[1].plot(history.history['loss'], label='Train Loss', linewidth=2)
    axes[1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Loss', fontsize=12)
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nTraining history saved to {save_path}")
    plt.close()

def main():
    print("="*60)
    print("EMOTION DETECTION - FAST TRAINING SCRIPT")
    print("Optimized for 20-30 minute training time")
    print("="*60)
    
    # Load data with sampling for faster training
    print("\n[1/6] Loading training data (sampling for speed)...")
    # Limit to 2000 samples per class for faster training
    X_train, y_train = load_images_labels(TRAIN_DIR, max_samples_per_class=2000)
    
    print("\n[2/6] Loading test data...")
    # Use all test data for accurate evaluation
    X_test, y_test = load_images_labels(TEST_DIR)
    
    print(f"\nDataset Summary:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Test samples: {len(X_test)}")
    print(f"  Image shape: {X_train[0].shape}")
    
    # Normalize images
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    
    # Reshape for CNN (add channel dimension)
    X_train = np.expand_dims(X_train, -1)
    X_test = np.expand_dims(X_test, -1)
    
    # One-hot encode labels
    y_train_cat = to_categorical(y_train, num_classes=len(EMOTION_LABELS))
    y_test_cat = to_categorical(y_test, num_classes=len(EMOTION_LABELS))
    
    # Split training data for validation (smaller validation set for speed)
    X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
        X_train, y_train_cat, test_size=0.15, random_state=42, stratify=y_train_cat
    )
    
    print(f"\n  Training: {len(X_train_split)}")
    print(f"  Validation: {len(X_val_split)}")
    print(f"  Test: {len(X_test)}")
    
    # Plot class distribution
    print("\n[3/6] Analyzing class distribution...")
    plot_class_distribution(y_train, y_test)
    
    # Create model
    print("\n[4/6] Creating optimized CNN model...")
    model = create_fast_model(input_shape=(48, 48, 1), num_classes=len(EMOTION_LABELS))
    
    # Compile model with higher learning rate for faster convergence
    model.compile(
        optimizer=Adam(learning_rate=0.002),  # Higher LR for faster training
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("\nModel Architecture:")
    model.summary()
    
    # Light data augmentation (less overhead)
    datagen = ImageDataGenerator(
        rotation_range=10,  # Reduced from 15
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1
    )
    datagen.fit(X_train_split)
    
    # Callbacks - More aggressive early stopping
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=8,  # Reduced from 15 for faster stopping
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,  # Reduced from 5
            min_lr=0.0001,
            verbose=1
        ),
        ModelCheckpoint(
            'models/best_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train model - REDUCED EPOCHS
    print("\n[5/6] Training model...")
    print("Target: 20-30 minutes")
    print("Max epochs: 25 (with early stopping)")
    
    history = model.fit(
        datagen.flow(X_train_split, y_train_split, batch_size=128),  # Larger batch for speed
        steps_per_epoch=len(X_train_split) // 128,
        epochs=25,  # Reduced from 100
        validation_data=(X_val_split, y_val_split),
        callbacks=callbacks,
        verbose=1
    )
    
    # Load best model
    print("\nLoading best model...")
    model.load_weights('models/best_model.h5')
    
    # Evaluate on test set
    print("\n[6/6] Evaluating on test set...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test_cat, verbose=0)
    
    print(f"\n{'='*60}")
    print(f"TEST SET RESULTS")
    print(f"{'='*60}")
    print(f"Test Accuracy: {test_accuracy*100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Predictions
    y_pred = model.predict(X_test, verbose=0)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # Classification report
    print(f"\n{'='*60}")
    print("CLASSIFICATION REPORT")
    print(f"{'='*60}")
    report = classification_report(y_test, y_pred_classes, target_names=EMOTION_LABELS)
    print(report)
    
    # Confusion matrix
    print("\nGenerating confusion matrix...")
    plot_confusion_matrix(y_test, y_pred_classes)
    
    # Training history
    plot_training_history(history)
    
    # Save final model
    model.save('models/final_model.h5')
    print("\nFinal model saved to models/final_model.h5")
    
    # Save results to text file
    with open('training_results.txt', 'w') as f:
        f.write("="*60 + "\n")
        f.write("EMOTION DETECTION - TRAINING RESULTS (FAST TRAINING)\n")
        f.write("="*60 + "\n\n")
        f.write(f"Test Accuracy: {test_accuracy*100:.2f}%\n")
        f.write(f"Test Loss: {test_loss:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
        f.write("\n\nClass Distribution:\n")
        f.write(f"Training samples: {len(X_train)}\n")
        f.write(f"Test samples: {len(X_test)}\n")
        for i, emotion in enumerate(EMOTION_LABELS):
            train_count = np.sum(y_train == i)
            test_count = np.sum(y_test == i)
            f.write(f"  {emotion}: Train={train_count}, Test={test_count}\n")
    
    print("\nResults saved to training_results.txt")
    print(f"\n{'='*60}")
    print("TRAINING COMPLETE!")
    print(f"{'='*60}")

if __name__ == '__main__':
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    main()

