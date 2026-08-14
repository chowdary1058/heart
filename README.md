# Heart Disease Prediction & Health Recommendation System 🫀

An intelligent end-to-end web application for predicting cardiovascular disease risk and generating personalized health & lifestyle recommendations using Deep Learning and Machine Learning models.

---

## 🌟 Key Features

- **Multi-Model Deep Learning Architecture**:
  - Deep Neural Network (DNN) with PyTorch
  - Multi-Layer Perceptron (MLP)
  - TabNet (Attentive Interpretable Tabular Learning)
  - Random Forest / Ensemble Benchmark
- **Risk Assessment & Confidence Scoring**: Real-time heart disease likelihood prediction with confidence metrics and risk-level categorization (Low, Moderate, High, Severe).
- **Personalized Recommendations Engine**: Rule-based lifestyle, dietary, exercise, and clinical follow-up advice tailored to individual patient biomarkers (Cholesterol, Blood Pressure, Heart Rate, Blood Sugar, ST-segment analysis).
- **Interactive Web Interface**: Built with Flask, featuring:
  - Patient self-service portal & history tracking
  - Doctor / Admin analytics dashboard with patient records and distribution plots
  - Visual charts for model metrics (Confusion Matrix, ROC Curve, Loss/Accuracy Curves)
- **Role-Based Authentication**: Secure authentication system for Patients and Doctors/Admins with SQLite database storage.

---

## 📁 Project Structure

```text
├── app.py                     # Flask web application & API routing
├── models.py                  # Database models (User, PredictionRecord)
├── train.py                   # Model training script (DNN, MLP, TabNet, Random Forest)
├── predict.py                 # Prediction utility & model loading functions
├── recommendation.py          # Personalized health recommendation engine
├── heart.csv                  # Dataset used for training and evaluation
├── requirements.txt           # Python dependencies
├── saved_models/              # Serialized trained weights, encoders, and scalers
├── plots/                     # Evaluation metrics and exploratory data analysis charts
└── templates/                 # HTML templates (Dashboard, Prediction, Analytics, Auth)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PyTorch & CUDA (optional for GPU acceleration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chowdary1058/heart.git
   cd heart
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux / macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the models (optional, pre-trained models are included):**
   ```bash
   python train.py
   ```

5. **Run the Flask application:**
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📊 Dataset & Features

The model evaluates key cardiovascular risk factors including:
- **Age**: Patient's age in years
- **Sex**: Patient's biological sex (1 = male, 0 = female)
- **Chest Pain Type (cp)**: 0: Typical Angina, 1: Atypical Angina, 2: Non-anginal Pain, 3: Asymptomatic
- **Resting Blood Pressure (trestbps)**: mm Hg on admission to the hospital
- **Serum Cholesterol (chol)**: mg/dl
- **Fasting Blood Sugar (fbs)**: > 120 mg/dl (1 = true; 0 = false)
- **Resting ECG (restecg)**: 0: Normal, 1: ST-T wave abnormality, 2: Left ventricular hypertrophy
- **Max Heart Rate Achieved (thalach)**: Maximum heart rate reached during exercise test
- **Exercise Induced Angina (exang)**: 1 = yes, 0 = no
- **ST Depression (oldpeak)**: ST depression induced by exercise relative to rest
- **Slope of the Peak Exercise ST Segment (slope)**: 0: Upsloping, 1: Flat, 2: Downsloping
- **Number of Major Vessels (ca)**: 0-3 colored by fluoroscopy
- **Thalassemia (thal)**: 1 = Normal, 2 = Fixed Defect, 3 = Reversible Defect

---

## 🛡️ License

This project is licensed under the MIT License.
