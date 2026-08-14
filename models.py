from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='patient') # 'patient' or 'admin'
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to predictions
    predictions = db.relationship('PredictionRecord', backref='patient', lazy=True)

class PredictionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Input Features
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    cp = db.Column(db.Integer)
    trestbps = db.Column(db.Integer)
    chol = db.Column(db.Integer)
    fbs = db.Column(db.Integer)
    restecg = db.Column(db.Integer)
    thalach = db.Column(db.Integer)
    exang = db.Column(db.Integer)
    oldpeak = db.Column(db.Float)
    slope = db.Column(db.Integer)
    ca = db.Column(db.Integer)
    thal = db.Column(db.Integer)
    
    # Prediction Results
    prediction_label = db.Column(db.String(50)) # "Heart Disease Warning" / "No Heart Disease"
    disease_probability = db.Column(db.Float)
    risk_level = db.Column(db.String(50)) # "Low Risk", "Moderate Risk", "Higher Risk"
    
    # Storing recommendations as JSON string
    recommendations_json = db.Column(db.Text)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_recommendations(self):
        if self.recommendations_json:
            return json.loads(self.recommendations_json)
        return {}
