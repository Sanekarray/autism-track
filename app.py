import joblib
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pandas as pd
import os
import traceback
from flask import jsonify
from sklearn.preprocessing import LabelEncoder, StandardScaler

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')

# Load models and preprocessors
autism_model = joblib.load("C:/Users/cyrin/PycharmProjects/autismproject/templates/autism_svm_model.pkl")
label_encoders = joblib.load("C:/Users/cyrin/PycharmProjects/autismproject/templates/label_encoders.pkl")
scaler = joblib.load("C:/Users/cyrin/PycharmProjects/autismproject/templates/scaler.pkl")
training_columns = joblib.load("C:/Users/cyrin/PycharmProjects/autismproject/templates/training_columns.pkl")

# Load data to get patient IDs
data = pd.read_csv('C:/Users/cyrin/PycharmProjects/autismproject/data_autism.csv')

# Use the correct column name: CASE_NO_PATIENT'S
patient_ids = data["CASE_NO_PATIENT'S"].unique()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Simulate a database of users
users = {'user@example.com': {'password': 'password', 'id': 1}}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user['id'] == int(user_id):
            return User(user_id)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/autism')
def autism():
    return render_template('autism.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            if email in users and users[email]['password'] == password:
                user = User(users[email]['id'])
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('autism'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        else:
            flash('Please provide both email and password.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email not in users:
            users[email] = {'password': password, 'id': len(users) + 1}
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already registered. Please log in or use a different email.', 'danger')
    return render_template('signup.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')  # Create forgot_password.html template

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    autism_result = None
    error = None
    if request.method == 'POST':
        try:
            patient_id = request.form['patient_id']
            print(f"Received patient_id: {patient_id}")

            patient_data = data[data["CASE_NO_PATIENT'S"] == int(patient_id)]
            print("Patient data before preprocessing:\n", patient_data)

            patient_data = preprocess_data(patient_data)
            print("Patient data after preprocessing:\n", patient_data)

            # Predict Autism probability
            autism_probabilities = autism_model.predict_proba(patient_data)
            autism_result = {
                'id': patient_id,
                'probability': autism_probabilities[0][1],  # Probability of class 1 (autism)
                'prediction': 'High Risk' if autism_probabilities[0][1] > 0.5 else 'Low Risk'
            }
        except Exception as e:
            print(f"Error during prediction: {e}")
            print(traceback.format_exc())  # Print the full traceback
            error = str(e)

    return render_template('Prediction.html', patient_ids=patient_ids, autism_result=autism_result, error=error)

def preprocess_data(patient_data):
    # Keep only training columns
    patient_data = patient_data[training_columns].copy()

    # Encode categorical variables and scale numerical variables
    for col in patient_data.columns:
        if col in label_encoders:
            patient_data.loc[:, col] = label_encoders[col].transform(patient_data[col])
    patient_data.loc[:, patient_data.select_dtypes(include=['int64', 'float64']).columns] = scaler.transform(patient_data[patient_data.select_dtypes(include=['int64', 'float64']).columns])
    return patient_data

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    if email in users:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
