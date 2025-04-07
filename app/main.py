# Flask app with routing + RBAC logic

from flask import Flask, render_template, request, redirect, session, url_for
from data import sensor_data

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a real key in production

# Simulated users and roles stored in-memory
users = {
    'admin': {'password': 'admin123', 'role': 'Admin'},
    'analyst': {'password': 'analyst123', 'role': 'Analyst'},
    'guest': {'password': 'guest123', 'role': 'Guest'}
}

def save_user(username, password, role):
    users[username] = {'password': password, 'role': role}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    if user and user['password'] == password:
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if username in users:
            return render_template('register.html', error='Username already exists')
        save_user(username, password, role)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
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
