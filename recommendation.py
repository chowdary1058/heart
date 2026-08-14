"""
Heart Disease AI Agent - Recommendation Module
==============================================
Generates lifestyle recommendations based on patient input and AI model predictions.
"""

from predict import predict_heart_disease

def get_risk_level(disease_probability: float) -> str:
    """Determine a simple risk level based on the probability of heart disease."""
    if disease_probability < 0.35:
        return "Low Risk"
    elif disease_probability < 0.70:
        return "Moderate Risk"
    else:
        return "Higher Risk"


def generate_recommendations(patient_info: dict, risk_level: str) -> dict:
    """Generate user-friendly lifestyle recommendations relevant to patient input."""
    recs = {
        "diet": [],
        "physical_activity": [],
        "sleep": ["Aim for 7-9 hours of quality sleep per night to support proper cardiovascular recovery.",
                  "Try to maintain a consistent sleep schedule, even on weekends."],
        "smoking_alcohol": [],
        "healthy_habits": ["Manage stress through relaxation techniques like meditation, deep breathing, or yoga."]
    }

    # Diet based on cholesterol and blood pressure
    chol = patient_info.get("chol", 200)
    trestbps = patient_info.get("trestbps", 120)

    if chol > 240:
        recs["diet"].append("Your cholesterol is elevated. Focus on reducing saturated fats and eliminating trans fats.")
        recs["diet"].append("Increase intake of soluble fiber (e.g., oats, beans, fruits) to help lower LDL cholesterol.")
    elif chol > 200:
        recs["diet"].append("Your cholesterol is borderline high. Maintain a balanced diet rich in fruits, vegetables, and whole grains.")
    else:
        recs["diet"].append("Your cholesterol is in a healthy range. Continue eating a heart-healthy, balanced diet.")

    if trestbps > 130:
        recs["diet"].append("Your blood pressure is elevated. Consider the DASH diet and reduce your salt/sodium intake.")
    
    # Physical activity based on age and exercise-induced angina (exang)
    exang = patient_info.get("exang", 0)
    
    if exang == 1:
        recs["physical_activity"].append("Since you experience exercise-induced angina, please consult your physician before starting any new exercise routine.")
        recs["physical_activity"].append("Start with light, low-impact activities such as gentle walking.")
    else:
        if risk_level == "Higher Risk":
            recs["physical_activity"].append("Consult your doctor for a tailored exercise plan.")
            recs["physical_activity"].append("Gradually incorporate moderate aerobic exercise as recommended by your healthcare provider.")
        else:
            recs["physical_activity"].append("Aim for at least 150 minutes of moderate-intensity aerobic activity per week (e.g., brisk walking, cycling).")
            recs["physical_activity"].append("Include strength training exercises at least two days a week.")

    # Smoking / Alcohol (general advice since dataset doesn't have direct smoking feature)
    recs["smoking_alcohol"].append("If you smoke, quitting is the best thing you can do for your heart. Seek support if needed.")
    recs["smoking_alcohol"].append("Limit alcohol intake to moderate levels (up to one drink a day for women, two for men).")

    # Additional habit based on fasting blood sugar
    fbs = patient_info.get("fbs", 0)
    if fbs == 1:
        recs["healthy_habits"].append("Your fasting blood sugar is elevated. Monitor your sugar intake and follow up with your doctor for diabetes screening.")

    return recs


def analyze_patient(patient_info: dict) -> dict:
    """
    Main agent function to process patient info, get prediction, and return report.
    """
    # 1. Get prediction from ML model
    pred_result = predict_heart_disease(patient_info)
    
    # The dataset target: 0 = Disease, 1 = No Disease
    # `pred_result['probability']` is the probability of class 1 (No Disease).
    # We calculate the probability of DISEASE for easier user understanding.
    prob_no_disease = pred_result['probability']
    prob_disease = 1.0 - prob_no_disease
    
    # 2. Determine Risk Level
    risk_level = get_risk_level(prob_disease)
    
    # 3. Generate Recommendations
    recommendations = generate_recommendations(patient_info, risk_level)
    
    # 4. Compile final report
    report = {
        "prediction": "Heart Disease Warning" if pred_result['prediction'] == 0 else "No Heart Disease Detected",
        "disease_probability": round(prob_disease * 100, 2),
        "risk_level": risk_level,
        "recommendations": recommendations,
        "disclaimer": (
            "DISCLAIMER: This system is an educational AI risk-prediction tool, "
            "not a medical diagnosis. The predictions and recommendations are generated "
            "by artificial intelligence based on statistical patterns and should NOT "
            "be used as a substitute for professional medical advice, diagnosis, or treatment. "
            "Always consult a qualified healthcare provider for medical concerns."
        )
    }
    
    return report


if __name__ == "__main__":
    # Test cases
    print("AI AGENT FOR HEART DISEASE RISK PREDICTION")
    print("=" * 50)
    
    patients = [
        {
            "name": "Patient A (Healthy Profile)",
            "data": {
                'age': 40, 'sex': 0, 'cp': 2, 'trestbps': 110,
                'chol': 180, 'fbs': 0, 'restecg': 0, 'thalach': 160,
                'exang': 0, 'oldpeak': 0.0, 'slope': 2, 'ca': 0, 'thal': 2
            }
        },
        {
            "name": "Patient B (Moderate Risk Profile)",
            "data": {
                'age': 55, 'sex': 1, 'cp': 1, 'trestbps': 135,
                'chol': 230, 'fbs': 0, 'restecg': 1, 'thalach': 140,
                'exang': 0, 'oldpeak': 1.2, 'slope': 1, 'ca': 1, 'thal': 2
            }
        },
        {
            "name": "Patient C (High Risk Profile)",
            "data": {
                'age': 65, 'sex': 1, 'cp': 0, 'trestbps': 160,
                'chol': 280, 'fbs': 1, 'restecg': 2, 'thalach': 110,
                'exang': 1, 'oldpeak': 2.5, 'slope': 0, 'ca': 3, 'thal': 3
            }
        }
    ]
    
    for p in patients:
        print(f"\n--- Analyzing: {p['name']} ---")
        print(f"Inputs: Age: {p['data']['age']}, BP: {p['data']['trestbps']}, Chol: {p['data']['chol']}, "
              f"FBS: {p['data']['fbs']}, ExAng: {p['data']['exang']}")
        
        result = analyze_patient(p['data'])
        
        print("\n[AI PREDICTION]")
        print(f"Prediction:   {result['prediction']}")
        print(f"Probability:  {result['disease_probability']}% chance of heart disease")
        print(f"Risk Level:   {result['risk_level']}")
        
        print("\n[LIFESTYLE RECOMMENDATIONS]")
        print(" Diet:")
        for r in result['recommendations']['diet']: print(f"   - {r}")
        print(" Physical Activity:")
        for r in result['recommendations']['physical_activity']: print(f"   - {r}")
        print(" Sleep:")
        for r in result['recommendations']['sleep']: print(f"   - {r}")
        print(" Smoking & Alcohol:")
        for r in result['recommendations']['smoking_alcohol']: print(f"   - {r}")
        print(" General Habits:")
        for r in result['recommendations']['healthy_habits']: print(f"   - {r}")
        
        print(f"\n{result['disclaimer']}")
        print("-" * 50)
