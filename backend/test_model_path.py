"""Test script to verify model path resolution"""
import os
import sys

# Get the project root directory (parent of backend directory)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FINAL_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'final_model.h5')
BEST_MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'best_model.h5')

print("="*60)
print("MODEL PATH TEST")
print("="*60)
print(f"Backend directory: {BACKEND_DIR}")
print(f"Project root: {PROJECT_ROOT}")
print(f"\nFinal model path: {FINAL_MODEL_PATH}")
print(f"  Exists: {os.path.exists(FINAL_MODEL_PATH)}")
print(f"\nBest model path: {BEST_MODEL_PATH}")
print(f"  Exists: {os.path.exists(BEST_MODEL_PATH)}")

if os.path.exists(BEST_MODEL_PATH):
    size = os.path.getsize(BEST_MODEL_PATH) / (1024*1024)
    print(f"  Size: {size:.2f} MB")
    print("\n✅ Model file found! Path resolution is correct.")
else:
    print("\n❌ Model file not found. Checking alternative paths...")
    # Try relative path
    alt_path = os.path.join('..', 'models', 'best_model.h5')
    print(f"Alternative path: {alt_path}")
    print(f"  Exists: {os.path.exists(alt_path)}")
    if os.path.exists(alt_path):
        abs_alt = os.path.abspath(alt_path)
        print(f"  Absolute: {abs_alt}")

