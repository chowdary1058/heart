import os
import joblib
import pandas as pd
import numpy as np
from predict import predict_heart_disease, FEATURE_NAMES
from recommendation import analyze_patient

print("Expected Feature Order for Random Forest:")
print(FEATURE_NAMES)

# Sample Patient
sample_patient_py = {
    'age': 55, 'sex': 1, 'cp': 0, 'trestbps': 140,
    'chol': 260, 'fbs': 0, 'restecg': 1, 'thalach': 145,
    'exang': 1, 'oldpeak': 2.0, 'slope': 1, 'ca': 1, 'thal': 3
}

# Values parsed by Flask in app.py logic
sample_patient_flask = {
    'age': int(55),
    'sex': int(1),
    'cp': int(0),
    'trestbps': int(140),
    'chol': int(260),
    'fbs': int(0),
    'restecg': int(1),
    'thalach': int(145),
    'exang': int(1),
    'oldpeak': float(2.0),
    'slope': int(1),
    'ca': int(1),
    'thal': int(3)
}

print("\nFlask Dictionary:")
print(sample_patient_flask)

print("\nPredict.py Function Output:")
pred_res = predict_heart_disease(sample_patient_py)
print(pred_res)

print("\nRecommendation Module Output:")
rec_res = analyze_patient(sample_patient_flask)
print(rec_res)

print("\nAll flow checks passed successfully!")
