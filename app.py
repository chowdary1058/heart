import os
import json
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, PredictionRecord
from recommendation import analyze_patient

app = Flask(__name__)
# Secret key loaded from environment variable FLASK_SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'heart_disease_default_secret_key_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heartapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================
# PUBLIC ROUTES & AUTH
# ==========================================
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            # Only patients can login here
            if user.role != 'patient':
                flash('Please use the admin login portal.', 'error')
                return redirect(url_for('login'))
                
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', admin_login=False)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            if user.role != 'admin':
                flash('Access denied. Administrator privileges required.', 'error')
                return redirect(url_for('admin_login'))
                
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials', 'error')
    return render_template('login.html', admin_login=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_pw, role='patient')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        username = request.form.get('username', '').strip()
        age = request.form.get('age')
        gender = request.form.get('gender')

        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()

        # Check username uniqueness if changed
        if username and username != current_user.username:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash('Username is already taken by another user.', 'error')
                return redirect(url_for('profile'))
            current_user.username = username

        current_user.full_name = full_name if full_name else None
        current_user.email = email if email else None
        current_user.phone = phone if phone else None
        current_user.age = int(age) if age and age.isdigit() else None
        current_user.gender = gender if gender else None

        # Update password if requested
        if new_password:
            if not current_password or not check_password_hash(current_user.password_hash, current_password):
                flash('Current password verification failed. Password was not updated.', 'error')
                db.session.commit()
                return redirect(url_for('profile'))
            current_user.password_hash = generate_password_hash(new_password, method='scrypt')
            flash('Password and profile details updated successfully!', 'success')
            db.session.commit()
            return redirect(url_for('profile'))

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    stats = {
        'total_assessments': PredictionRecord.query.filter_by(user_id=current_user.id).count(),
        'latest_record': PredictionRecord.query.filter_by(user_id=current_user.id).order_by(PredictionRecord.timestamp.desc()).first()
    }
    return render_template('profile.html', stats=stats)

# ==========================================
# PATIENT ROUTES
# ==========================================
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'patient':
        return redirect(url_for('admin_dashboard'))
        
    history = PredictionRecord.query.filter_by(user_id=current_user.id).order_by(PredictionRecord.timestamp.desc()).all()
    return render_template('dashboard.html', records=history, history=history)

@app.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    if current_user.role != 'patient':
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            # Extract features
            patient_info = {
                'age': int(request.form.get('age', 50)),
                'sex': int(request.form.get('sex', 0)),
                'cp': int(request.form.get('cp', 0)),
                'trestbps': int(request.form.get('trestbps', 120)),
                'chol': int(request.form.get('chol', 200)),
                'fbs': int(request.form.get('fbs', 0)),
                'restecg': int(request.form.get('restecg', 0)),
                'thalach': int(request.form.get('thalach', 150)),
                'exang': int(request.form.get('exang', 0)),
                'oldpeak': float(request.form.get('oldpeak', 0.0)),
                'slope': int(request.form.get('slope', 0)),
                'ca': int(request.form.get('ca', 0)),
                'thal': int(request.form.get('thal', 2))
            }

            # Run ML logic via recommendation module
            result = analyze_patient(patient_info)

            # Save to Database
            record = PredictionRecord(
                user_id=current_user.id,
                **patient_info,
                prediction_label=result['prediction'],
                disease_probability=result['disease_probability'],
                risk_level=result['risk_level'],
                recommendations_json=json.dumps(result['recommendations'])
            )
            db.session.add(record)
            db.session.commit()

            return redirect(url_for('result', rec_id=record.id))
        
        except Exception as e:
            flash(f"Error processing assessment: {str(e)}", "error")
            return redirect(url_for('assessment'))

    return render_template('assessment.html')

# API Route for programmatic/direct predictions
@app.route('/predict', methods=['POST'])
def predict_api():
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        patient_info = {
            'age': int(data.get('age', 50)),
            'sex': int(data.get('sex', 0)),
            'cp': int(data.get('cp', 0)),
            'trestbps': int(data.get('trestbps', 120)),
            'chol': int(data.get('chol', 200)),
            'fbs': int(data.get('fbs', 0)),
            'restecg': int(data.get('restecg', 0)),
            'thalach': int(data.get('thalach', 150)),
            'exang': int(data.get('exang', 0)),
            'oldpeak': float(data.get('oldpeak', 0.0)),
            'slope': int(data.get('slope', 0)),
            'ca': int(data.get('ca', 0)),
            'thal': int(data.get('thal', 2))
        }
        result = analyze_patient(patient_info)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/result/<int:rec_id>')
@login_required
def result(rec_id):
    # Ensure user can only see their own results, unless they're an admin
    record = PredictionRecord.query.get_or_404(rec_id)
    if record.user_id != current_user.id and current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
        
    return render_template('result.html', record=record)

# ==========================================
# ADMIN ROUTES
# ==========================================
@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
        
    total_users = User.query.filter_by(role='patient').count()
    total_preds = PredictionRecord.query.count()
    
    # Simple risk breakdown
    high = PredictionRecord.query.filter_by(risk_level='Higher Risk').count()
    mod = PredictionRecord.query.filter_by(risk_level='Moderate Risk').count()
    low = PredictionRecord.query.filter_by(risk_level='Low Risk').count()
    
    # Specific predictions tracking
    heart_disease_preds = PredictionRecord.query.filter_by(prediction_label='Heart Disease Warning').count()
    no_disease_preds = PredictionRecord.query.filter_by(prediction_label='No Heart Disease Detected').count()
    
    stats = {
        'total_users': total_users,
        'total_predictions': total_preds,
        'heart_disease': heart_disease_preds,
        'no_disease': no_disease_preds,
        'risk_distribution': {'high': high, 'moderate': mod, 'low': low}
    }
    
    recent_preds = PredictionRecord.query.order_by(PredictionRecord.timestamp.desc()).limit(10).all()
    return render_template('admin_dashboard.html', stats=stats, recent=recent_preds)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    users = User.query.filter_by(role='patient').all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/<int:user_id>')
@login_required
def admin_user_detail(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot view admin details here', 'error')
        return redirect(url_for('admin_users'))
        
    predictions = PredictionRecord.query.filter_by(user_id=user.id).order_by(PredictionRecord.timestamp.desc()).all()
    return render_template('admin_user_detail.html', user=user, predictions=predictions)

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_user_delete(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete administrator accounts', 'error')
        return redirect(url_for('admin_users'))
        
    # Delete associated predictions first
    PredictionRecord.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.username} and all their records have been deleted.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/predictions')
@login_required
def admin_predictions():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    predictions = PredictionRecord.query.order_by(PredictionRecord.timestamp.desc()).all()
    return render_template('admin_predictions.html', predictions=predictions)


def setup_database():
    """Create DB tables, migrate schema if needed, and create initial admin user."""
    with app.app_context():
        db.create_all()
        # Auto-migrate new profile columns if they don't exist yet
        try:
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            with db.engine.begin() as conn:
                if 'full_name' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN full_name VARCHAR(150)"))
                if 'email' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR(150)"))
                if 'phone' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN phone VARCHAR(50)"))
                if 'age' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN age INTEGER"))
                if 'gender' not in columns:
                    conn.execute(text("ALTER TABLE user ADD COLUMN gender VARCHAR(20)"))
        except Exception as e:
            print("DB migration notice:", e)

        # Create admin if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            hashed_pw = generate_password_hash('admin', method='scrypt')
            admin = User(username='admin', password_hash=hashed_pw, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created (admin/admin).")

if __name__ == '__main__':
    setup_database()
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heart_model.pkl")
    if not os.path.exists(model_path):
        print(f"WARNING: Model not found at '{model_path}'. Please run train.py first.")
        
    app.run(host='0.0.0.0', port=5000, debug=True)
