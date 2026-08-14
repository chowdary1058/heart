"""
AI Agent for Heart Disease Risk Prediction
==========================================
Machine Learning Training Pipeline
Model: Random Forest Classifier
"""
import os
import sys
import io
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

# Configuration
SEED = 42
TEST_SIZE = 0.20

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "heart.csv")
MODEL_PATH = os.path.join(BASE_DIR, "heart_model.pkl")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)

# 1. Load and Inspect Dataset
print("=" * 60)
print("1. LOADING AND INSPECTING DATASET")
print("=" * 60)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print(f"Initial Dataset Shape: {df.shape}")
print(f"\nMissing values per column:\n{df.isnull().sum()}")
duplicates_count = df.duplicated().sum()
print(f"\nDuplicate rows detected: {duplicates_count}")

# 2. Preprocessing: Remove duplicates
df_clean = df.drop_duplicates().reset_index(drop=True)
print(f"\nCleaned Dataset Shape (after removing duplicates): {df_clean.shape}")

# Exact feature list & target
FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]
TARGET_COL = 'target'

X = df_clean[FEATURE_NAMES]
y = df_clean[TARGET_COL]

# 3. Train-Test Split (80/20 Stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=SEED, stratify=y
)
print(f"\nTraining set shape: {X_train.shape}")
print(f"Testing set shape:  {X_test.shape}")

# 4. Train Random Forest Classifier
print("\n" + "=" * 60)
print("2. TRAINING RANDOM FOREST CLASSIFIER")
print("=" * 60)

rf_model = RandomForestClassifier(random_state=SEED, n_estimators=100)
rf_model.fit(X_train, y_train)
print("Random Forest model training completed.")

# 5. Evaluate on Held-out Test Set
print("\n" + "=" * 60)
print("3. MODEL EVALUATION ON TEST SET")
print("=" * 60)

y_pred = rf_model.predict(X_test)
y_prob = rf_model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
cm = confusion_matrix(y_test, y_pred)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1-Score:  {f1:.4f}")
print("\nConfusion Matrix:")
print(cm)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Disease', 'No Disease']))

# 6. Save Model and Metadata
# Save primary model file as heart_model.pkl
joblib.dump(rf_model, MODEL_PATH)
# Also save to saved_models/ for redundancy
joblib.dump(rf_model, os.path.join(SAVED_MODELS_DIR, "heart_model.pkl"))

# Save metadata including feature names order
metadata = {
    'feature_names': FEATURE_NAMES,
    'target_names': ['Disease', 'No Disease'],
    'accuracy': float(acc),
    'precision': float(prec),
    'recall': float(rec),
    'f1': float(f1)
}
joblib.dump(metadata, os.path.join(SAVED_MODELS_DIR, "model_metadata.joblib"))

print(f"\nTrained model successfully saved as: {MODEL_PATH}")
print("Training complete!")
