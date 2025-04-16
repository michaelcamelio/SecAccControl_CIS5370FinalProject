from flask import Flask, render_template, request, redirect, session, url_for, flash
from data import sensor_data
from datetime import datetime, timedelta
import re
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey' 

# Simulated users
users = {
    'Michael': {'password': 'admin123', 'role': 'Admin'},
    'Ann': {'password': 'analyst123', 'role': 'Analyst'},
    'Robert': {'password': 'guest123', 'role': 'Guest'}
}

login_attempts = {}

# Utility functions
def validate_password(password):
    return (
        len(password) >= 16 and
        re.search(r'[A-Z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )

def is_account_locked(username):
    now = datetime.now()
    attempts = login_attempts.get(username, [])
    attempts = [t for t in attempts if now - t < timedelta(minutes=15)]
    login_attempts[username] = attempts
    return len(attempts) >= 5

def record_failed_login(username):
    now = datetime.now()
    login_attempts.setdefault(username, []).append(now)

def send_mock_mfa_code(email, code):
    print(f"[DEBUG] MFA code for {email}: {code}")  # Future email/SMS API Implementation

def save_user(username, password, role):
    users[username] = {'password': password, 'role': role}

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)

    if is_account_locked(username):
        return render_template('login.html', error="Too many failed attempts. Try again later.")

    if user and user['password'] == password:
        session['username'] = username
        session['role'] = user['role']
        session['mfa_code'] = str(random.randint(100000, 999999))
        login_attempts.pop(username, None)
        send_mock_mfa_code('user@example.com', session['mfa_code']) # Mock email sending
        return redirect(url_for('verify_mfa'))
    else:
        record_failed_login(username)
        return render_template('login.html', error="Invalid credentials")

@app.route('/verify-mfa', methods=['GET', 'POST'])
def verify_mfa():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        code = request.form['code']
        if code == session.get('mfa_code'):
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect MFA code.")
            return redirect(url_for('verify_mfa'))
    
    return render_template('verify_mfa.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if username in users:
            return render_template('register.html', error='Username already exists')
        if not validate_password(password):
            return render_template('register.html', error='Password must be 16+ characters, include uppercase, number, and special char.')
        
        save_user(username, password, role)
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session or not session.get('authenticated'):
        return redirect(url_for('home'))

    role = session['role']
    if role == 'Admin':
        data = sensor_data
    elif role == 'Analyst':
        data = sensor_data[-5:]
    elif role == 'Guest':
        data = [sensor_data[-1]]
    else:
        return redirect(url_for('unauthorized'))
    
    return render_template('dashboard.html', username=session['username'], role=role, data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/unauthorized')
def unauthorized():
    return render_template('access_denied.html')

if __name__ == '__main__':
    app.run(debug=True)
