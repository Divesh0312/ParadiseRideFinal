"""
Super Simple Working Flask App with Database Auto-Creation
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables and demo user on first run
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(email='demo@paradiseride.com').first():
        demo_user = User(
            name="Demo User",
            email="demo@paradiseride.com",
            password_hash=generate_password_hash("demo123")
        )
        db.session.add(demo_user)
        db.session.commit()
        print("✅ Demo user created!")

# Routes
@app.route('/')
def index():
    return '''
    <html>
    <head><title>ParadiseRide - Working!</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>🛫 ParadiseRide - AI Travel Chatbot</h1>
        <h2>✅ App is Working!</h2>
        <p>The database and authentication are set up correctly.</p>
        <div style="margin: 30px;">
            <a href="/login" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px;">
                🔑 Login
            </a>
        </div>
        <div style="margin: 20px; background: #f0f9ff; padding: 20px; border-radius: 10px; display: inline-block;">
            <h3>Demo Account:</h3>
            <p>📧 Email: demo@paradiseride.com</p>
            <p>🔑 Password: demo123</p>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return '''
    <html>
    <head><title>Login - ParadiseRide</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>🛫 ParadiseRide Login</h1>
        <div style="max-width: 400px; margin: 0 auto;">
            <form method="POST">
                <div style="margin: 20px 0;">
                    <input type="email" name="email" placeholder="Email" required 
                           style="width: 100%; padding: 15px; border: 2px solid #ddd; border-radius: 10px;"
                           value="demo@paradiseride.com">
                </div>
                <div style="margin: 20px 0;">
                    <input type="password" name="password" placeholder="Password" required 
                           style="width: 100%; padding: 15px; border: 2px solid #ddd; border-radius: 10px;"
                           value="demo123">
                </div>
                <button type="submit" style="background: #667eea; color: white; padding: 15px 30px; border: none; border-radius: 10px; cursor: pointer;">
                    🔑 Sign In
                </button>
            </form>
            <div style="margin: 20px; background: #f0f9ff; padding: 15px; border-radius: 10px;">
                <p><strong>Demo Account (pre-filled):</strong></p>
                <p>📧 demo@paradiseride.com</p>
                <p>🔑 demo123</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard')
@login_required
def dashboard():
    return f'''
    <html>
    <head><title>Dashboard - ParadiseRide</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>🎉 Welcome, {current_user.name}!</h1>
        <h2>✅ Login Successful!</h2>
        <p>You are now logged into ParadiseRide.</p>
        <div style="margin: 30px;">
            <p>🛫 Your AI Travel Chatbot is ready!</p>
            <a href="/logout" style="background: #ef4444; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px;">
                🚪 Logout
            </a>
        </div>
        <div style="margin: 20px; background: #f0fdf4; padding: 20px; border-radius: 10px; display: inline-block;">
            <h3>✅ Everything is working:</h3>
            <p>✓ Database connected</p>
            <p>✓ User authentication</p>
            <p>✓ Session management</p>
            <p>✓ Ready for full chatbot features!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("🚀 Starting Simple ParadiseRide App...")
    print("🌐 Visit: http://127.0.0.1:5000")
    print("📧 Demo: demo@paradiseride.com")
    print("🔑 Pass: demo123")
    app.run(debug=True)