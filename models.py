from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    search_history = db.relationship('SearchHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    itineraries = db.relationship('Itinerary', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return the user id as a string for Flask-Login"""
        return str(self.id)
    
    def is_authenticated(self):
        """Return True if the user is authenticated"""
        return True
    
    def is_anonymous(self):
        """Return False as this is not an anonymous user"""
        return False
    
    def get_search_count(self):
        """Get the total number of searches by this user"""
        return db.session.query(SearchHistory).filter_by(user_id=self.id).count()
    
    def get_itinerary_count(self):
        """Get the total number of itineraries created by this user"""
        return db.session.query(Itinerary).filter_by(user_id=self.id).count()
    
    def get_recent_searches(self, limit=5):
        """Get recent search history for this user"""
        return db.session.query(SearchHistory).filter_by(user_id=self.id)\
                                 .order_by(SearchHistory.timestamp.desc())\
                                 .limit(limit).all()
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'search_count': self.get_search_count(),
            'itinerary_count': self.get_itinerary_count()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class SearchHistory(db.Model):
    """Model to store user's mood-based search history"""
    
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    query = db.Column(db.Text, nullable=False)  # Original user query
    result = db.Column(db.Text, nullable=False)  # JSON string of destinations returned
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rating = db.Column(db.Integer)  # User rating of the suggestions (1-5)
    is_favorite = db.Column(db.Boolean, default=False)
    
    def __init__(self, user_id, mood, query, result):
        self.user_id = user_id
        self.mood = mood
        self.query = query
        self.result = result
    
    def get_result_dict(self):
        """Parse the JSON result string back to dictionary"""
        import json
        try:
            return json.loads(self.result)
        except:
            return {}
    
    def set_result_dict(self, result_dict):
        """Convert dictionary to JSON string for storage"""
        import json
        self.result = json.dumps(result_dict)
    
    def mark_as_favorite(self):
        """Mark this search as favorite"""
        self.is_favorite = True
        db.session.commit()
    
    def remove_from_favorites(self):
        """Remove this search from favorites"""
        self.is_favorite = False
        db.session.commit()
    
    def set_rating(self, rating):
        """Set user rating for this search (1-5)"""
        if 1 <= rating <= 5:
            self.rating = rating
            db.session.commit()
    
    def to_dict(self):
        """Convert search history object to dictionary"""
        return {
            'id': self.id,
            'mood': self.mood,
            'query': self.query,
            'result': self.get_result_dict(),
            'timestamp': self.timestamp.isoformat(),
            'rating': self.rating,
            'is_favorite': self.is_favorite
        }
    
    def __repr__(self):
        return f'<SearchHistory {self.mood} by User {self.user_id}>'


class Itinerary(db.Model):
    """Model to store detailed travel itineraries"""
    
    __tablename__ = 'itineraries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.String(50))  # Budget range as string
    duration_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    detailed_plan = db.Column(db.Text)  # JSON string of day-by-day itinerary
    mood_tag = db.Column(db.String(50))  # The mood this itinerary was created for
    is_completed = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional metadata
    difficulty_level = db.Column(db.String(20))  # easy, moderate, challenging
    travel_style = db.Column(db.String(50))  # adventure, relaxation, cultural, etc.
    group_size = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)  # User notes
    
    def __init__(self, user_id, title, destination, start_date, end_date, budget, description, detailed_plan, mood_tag):
        self.user_id = user_id
        self.title = title
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.description = description
        self.detailed_plan = detailed_plan
        self.mood_tag = mood_tag
        self.duration_days = (end_date - start_date).days + 1
    
    def get_detailed_plan_dict(self):
        """Parse the JSON detailed_plan string back to dictionary"""
        import json
        try:
            return json.loads(self.detailed_plan)
        except:
            return {}
    
    def set_detailed_plan_dict(self, plan_dict):
        """Convert dictionary to JSON string for storage"""
        import json
        self.detailed_plan = json.dumps(plan_dict)
    
    def mark_as_completed(self):
        """Mark this itinerary as completed"""
        self.is_completed = True
        db.session.commit()
    
    def mark_as_favorite(self):
        """Mark this itinerary as favorite"""
        self.is_favorite = True
        db.session.commit()
    
    def remove_from_favorites(self):
        """Remove this itinerary from favorites"""
        self.is_favorite = False
        db.session.commit()
    
    def add_notes(self, notes):
        """Add or update notes for this itinerary"""
        self.notes = notes
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def is_upcoming(self):
        """Check if this itinerary is for future dates"""
        from datetime import date
        return self.start_date > date.today()
    
    def is_current(self):
        """Check if this itinerary is currently active"""
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def is_past(self):
        """Check if this itinerary is from the past"""
        from datetime import date
        return self.end_date < date.today()
    
    def get_status(self):
        """Get the current status of the itinerary"""
        if self.is_completed:
            return 'completed'
        elif self.is_current():
            return 'active'
        elif self.is_upcoming():
            return 'upcoming'
        else:
            return 'past'
    
    @property
    def details(self):
        """Alias for detailed_plan for template compatibility"""
        return self.detailed_plan
    
    def to_dict(self):
        """Convert itinerary object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'destination': self.destination,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'budget': self.budget,
            'duration_days': self.duration_days,
            'description': self.description,
            'detailed_plan': self.get_detailed_plan_dict(),
            'mood_tag': self.mood_tag,
            'is_completed': self.is_completed,
            'is_favorite': self.is_favorite,
            'status': self.get_status(),
            'difficulty_level': self.difficulty_level,
            'travel_style': self.travel_style,
            'group_size': self.group_size,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Itinerary {self.title} to {self.destination}>'


# Helper functions for database operations
def create_user(name, email, password):
    """Create a new user"""
    if db.session.query(User).filter_by(email=email).first():
        return None  # User already exists
    
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_email(email):
    """Get user by email"""
    return db.session.query(User).filter_by(email=email).first()

def get_user_by_id(user_id):
    """Get user by ID"""
    return db.session.get(User, int(user_id))

def save_search_history(user_id, mood, query, result):
    """Save search history"""
    search = SearchHistory(user_id=user_id, mood=mood, query=query, result=result)
    db.session.add(search)
    db.session.commit()
    return search

def create_itinerary(user_id, title, destination, start_date, end_date, budget, description, detailed_plan, mood_tag):
    """Create a new itinerary"""
    itinerary = Itinerary(
        user_id=user_id,
        title=title,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        description=description,
        detailed_plan=detailed_plan,
        mood_tag=mood_tag
    )
    db.session.add(itinerary)
    db.session.commit()
    return itinerary

def get_user_itineraries(user_id, limit=None):
    """Get all itineraries for a user"""
    query = db.session.query(Itinerary).filter_by(user_id=user_id).order_by(Itinerary.created_at.desc())
    if limit:
        query = query.limit(limit)
    return query.all()

def get_user_search_history(user_id, limit=None):
    """Get search history for a user"""
    query = db.session.query(SearchHistory).filter_by(user_id=user_id).order_by(SearchHistory.timestamp.desc())
    if limit:
        query = query.limit(limit)
    return query.all()
