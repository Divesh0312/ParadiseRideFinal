"""
Ultra-simple database setup - guaranteed to work!
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)

# Simple database in current directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Current directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'temp-key'

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    query = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)
    is_favorite = db.Column(db.Boolean, default=False)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.String(50))
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    detailed_plan = db.Column(db.Text)
    mood_tag = db.Column(db.String(50))
    is_completed = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# Setup function
def setup():
    print("🚀 Setting up database...")
    
    with app.app_context():
        # Create tables
        db.create_all()
        print("✅ Tables created!")
        
        # Create demo user
        if not User.query.filter_by(email='demo@paradiseride.com').first():
            demo_user = User(
                name="Demo User",
                email="demo@paradiseride.com",
                password_hash=generate_password_hash("demo123")
            )
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Demo user created!")
        else:
            print("✅ Demo user already exists!")
    
    print("🎉 Setup complete!")
    print("📧 Login: demo@paradiseride.com")
    print("🔑 Password: demo123")

if __name__ == '__main__':
    setup()