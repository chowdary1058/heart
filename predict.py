"""
Heart Disease Prediction Function
===================================
Load the trained Random Forest model and make predictions on patient data.
"""
import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check primary location first, then saved_models fallback
PRIMARY_MODEL_PATH = os.path.join(BASE_DIR, "heart_model.pkl")
FALLBACK_MODEL_PATH = os.path.join(BASE_DIR, "saved_models", "heart_model.pkl")

# Expected feature order
FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

_cached_model = None


def load_model():
    """Load the trained Random Forest model from portable project path."""
    global _cached_model
    if _cached_model is not None:
        return _cached_model

    if os.path.exists(PRIMARY_MODEL_PATH):
        model_path = PRIMARY_MODEL_PATH
    elif os.path.exists(FALLBACK_MODEL_PATH):
        model_path = FALLBACK_MODEL_PATH
    else:
        raise FileNotFoundError(
            f"Heart model not found. Expected at '{PRIMARY_MODEL_PATH}' or '{FALLBACK_MODEL_PATH}'. "
            "Please run train.py first to generate the model."
        )

    _cached_model = joblib.load(model_path)
    return _cached_model


def predict_heart_disease(patient_info: dict) -> dict:
    """
    Predict heart disease risk for a given patient.

    Parameters
    ----------
    patient_info : dict
        Dictionary with patient features:
        {
            'age': int, 'sex': int (1=male, 0=female),
            'cp': int (0-3), 'trestbps': int, 'chol': int,
            'fbs': int (0/1), 'restecg': int (0-2),
            'thalach': int, 'exang': int (0/1), 'oldpeak': float,
            'slope': int (0-2), 'ca': int (0-4), 'thal': int (0-3)
        }

    Returns
    -------
    dict with keys:
        - prediction: int (0 = Heart Disease, 1 = No Heart Disease)
        - probability: float (probability of being class 1 - No Disease)
        - risk_label: str ("Heart Disease Detected" / "No Heart Disease")
        - model_used: str ("Random Forest")
    """
    model = load_model()

    # Build feature vector in exact feature order
    feature_values = [[float(patient_info[f]) for f in FEATURE_NAMES]]
    features_df = pd.DataFrame(feature_values, columns=FEATURE_NAMES)

    pred = int(model.predict(features_df)[0])
    
    # Calculate probability of class 1 (No Disease)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features_df)[0]
        # In case the model has classes [0, 1]
        if len(model.classes_) > 1:
            idx_class_1 = list(model.classes_).index(1) if 1 in model.classes_ else 1
            prob = float(probs[idx_class_1])
        else:
            prob = float(probs[0])
    else:
        prob = 1.0 if pred == 1 else 0.0

    return {
        'prediction': pred,
        'probability': prob,
        'risk_label': "No Heart Disease" if pred == 1 else "Heart Disease Detected",
        'model_used': "Random Forest"
    }


if __name__ == "__main__":
    sample_patient = {
        'age': 55, 'sex': 1, 'cp': 0, 'trestbps': 140,
        'chol': 260, 'fbs': 0, 'restecg': 1, 'thalach': 145,
        'exang': 1, 'oldpeak': 2.0, 'slope': 1, 'ca': 1, 'thal': 3
    }

    print("Heart Disease Prediction (Random Forest)")
    print("=" * 40)
    print(f"Patient Info: {sample_patient}\n")

    result = predict_heart_disease(sample_patient)

    print(f"Prediction:  {result['prediction']}")
    print(f"Probability: {result['probability']:.4f}")
    print(f"Result:      {result['risk_label']}")
    print(f"Model Used:  {result['model_used']}")
