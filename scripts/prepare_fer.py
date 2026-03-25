import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from PIL import Image

# Paths
data_dir = 'data'
train_dir = os.path.join(data_dir, 'train')
test_dir = os.path.join(data_dir, 'test')

# Load images and labels from folders
def load_images_labels(folder):
    images = []
    labels = []
    label_map = {name: idx for idx, name in enumerate(os.listdir(folder))}
    for emotion, idx in label_map.items():
        emotion_folder = os.path.join(folder, emotion)
        for file in os.listdir(emotion_folder):
            img_path = os.path.join(emotion_folder, file)
            img = Image.open(img_path).convert('L')  # grayscale
            img = img.resize((48,48))
            images.append(np.array(img))
            labels.append(idx)
    return np.array(images), np.array(labels)

X_train, y_train = load_images_labels(train_dir)
X_test, y_test = load_images_labels(test_dir)

# Normalize images
X_train = X_train / 255.0
X_test = X_test / 255.0

# One-hot encode labels
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Split train into train + validation
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

# Save arrays
np.save('data/X_train.npy', X_train)
np.save('data/y_train.npy', y_train)
np.save('data/X_val.npy', X_val)
np.save('data/y_val.npy', y_val)
np.save('data/X_test.npy', X_test)
np.save('data/y_test.npy', y_test)

print("Data prepared and saved!")
