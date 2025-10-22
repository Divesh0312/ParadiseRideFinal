"""
Simple Database initialization script for AI Travel Chatbot
This version works without importing the main app
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Create a simple Flask app just for database initialization
app = Flask(__name__)

# Use absolute path for database
import os
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'temp-key-for-init'

db = SQLAlchemy(app)

# Simple User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    query = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Itinerary(db.Model):
    __tablename__ = 'itineraries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.String(50))
    description = db.Column(db.Text)
    detailed_plan = db.Column(db.Text)
    mood_tag = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_database():
    """Initialize the database with all tables"""
    print("🚀 Quick Database Setup Starting...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create demo user
            demo_user = User.query.filter_by(email='demo@paradiseride.com').first()
            if not demo_user:
                demo_user = User(
                    name="Demo User",
                    email="demo@paradiseride.com",
                    password_hash=generate_password_hash("demo123")
                )
                db.session.add(demo_user)
                db.session.commit()
                print("✅ Demo user created: demo@paradiseride.com (password: demo123)")
            else:
                print("ℹ️  Demo user already exists")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("🛫 ParadiseRide - Quick Database Setup")
    print("=" * 50)
    
    if init_database():
        print("\n✅ Setup complete! You can now run: python app.py")
        print("🎯 Demo login: demo@paradiseride.com / demo123")
    else:
        print("❌ Setup failed!")