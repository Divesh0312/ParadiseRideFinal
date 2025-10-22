"""
Database initialization script for AI Travel Chatbot
This script creates all necessary database tables
"""

from app import app, db
from models import User, SearchHistory, Itinerary

def init_database():
    """Initialize the database with all tables"""
    print("Initializing database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print table information
            print("\nCreated tables:")
            print("- users: Store user account information")
            print("- search_history: Store mood-based search queries")
            print("- itineraries: Store detailed travel itineraries")
            
            # Check if tables exist by counting
            user_count = User.query.count()
            search_count = SearchHistory.query.count()
            itinerary_count = Itinerary.query.count()
            
            print(f"\nCurrent database status:")
            print(f"- Users: {user_count}")
            print(f"- Search History: {search_count}")
            print(f"- Itineraries: {itinerary_count}")
            
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False
    
    return True

def create_sample_data():
    """Create some sample data for testing (optional)"""
    print("\nCreating sample data for testing...")
    
    with app.app_context():
        try:
            # Check if sample user already exists
            sample_user = User.query.filter_by(email='demo@paradiseride.com').first()
            if not sample_user:
                # Create sample user
                from models import create_user
                sample_user = create_user(
                    name="Demo User",
                    email="demo@paradiseride.com",
                    password="demo123"
                )
                print("✅ Sample user created: demo@paradiseride.com (password: demo123)")
            else:
                print("ℹ️  Sample user already exists")
                
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("AI Travel Chatbot - Database Initialization")
    print("=" * 50)
    
    if init_database():
        # Ask if user wants to create sample data
        create_sample = input("\nWould you like to create sample data for testing? (y/n): ").lower().strip()
        if create_sample in ['y', 'yes']:
            create_sample_data()
        
        print("\n" + "=" * 50)
        print("Database initialization complete!")
        print("You can now run the application with: python app.py")
        print("=" * 50)
    else:
        print("❌ Database initialization failed!")