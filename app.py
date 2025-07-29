from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Fake user DB and study data
USERS_FILE = 'users.json'

def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    users = load_users()
    user_data = users[username]
    return render_template('dashboard.html', user=user_data)

@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = load_users()
    username = session['username']
    if request.method == 'POST':
        subject = request.form['subject']
        duration = request.form['duration']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        users[username]['sessions'].append({
            "subject": subject,
            "duration": duration,
            "timestamp": timestamp
        })
        save_users(users)
        flash('Session logged!')
    return render_template('sessions.html', sessions=users[username]['sessions'])

@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = load_users()
    username = session['username']
    if request.method == 'POST':
        action = request.form['action']
        subject = request.form['subject']
        if action == 'add' and subject not in users[username]['subjects']:
            users[username]['subjects'].append(subject)
        elif action == 'remove' and subject in users[username]['subjects']:
            users[username]['subjects'].remove(subject)
        save_users(users)
    return render_template('subjects.html', subjects=users[username]['subjects'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

print("Starting Flask app...")

if __name__ == '__main__':
    app.run(debug=True)