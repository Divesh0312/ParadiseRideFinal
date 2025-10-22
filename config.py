import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # SQLAlchemy Database Configuration
    # For local development with SQLite - use current directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///travel_chatbot.db'
    
    # For MySQL (uncomment and configure as needed)
    # MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    # MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    # MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    # MYSQL_DB = os.environ.get('MYSQL_DB') or 'travel_chatbot'
    # SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for debugging SQL queries
    
    # Supabase Configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or 'https://your-project.supabase.co'
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or 'your-supabase-anon-key'
    
    # AI/OpenAI Configuration (optional)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or None
    
    # Flask-Login settings
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Pagination settings
    POSTS_PER_PAGE = 10
    
    # Email settings (for future use)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # App settings
    APP_NAME = "ParadiseRide - AI Travel Chatbot"
    APP_VERSION = "1.0.0"

# Mood to destination mapping
MOOD_DESTINATIONS = {
    'calm': {
        'destinations': [
            {
                'name': 'Kerala Backwaters',
                'description': 'Serene houseboat experiences in Alleppey',
                'best_time': 'October to March',
                'budget': '₹8,000-15,000 per day',
                'attractions': ['Houseboat cruise', 'Kumarakom Bird Sanctuary', 'Vembanad Lake'],
                'food': ['Fish curry', 'Appam', 'Karimeen fry']
            },
            {
                'name': 'Coorg, Karnataka',
                'description': 'Coffee plantations and misty hills',
                'best_time': 'October to March',
                'budget': '₹5,000-10,000 per day',
                'attractions': ['Coffee plantations', 'Abbey Falls', 'Raja\'s Seat'],
                'food': ['Pandi curry', 'Bamboo shoot curry', 'Coorg coffee']
            },
            {
                'name': 'Rishikesh, Uttarakhand',
                'description': 'Yoga capital with Ganges views',
                'best_time': 'September to November, March to April',
                'budget': '₹3,000-8,000 per day',
                'attractions': ['Laxman Jhula', 'Beatles Ashram', 'Ganges Aarti'],
                'food': ['Chole bhature', 'Aloo puri', 'Lassi']
            }
        ]
    },
    'excited': {
        'destinations': [
            {
                'name': 'Goa',
                'description': 'Beaches, nightlife, and Portuguese heritage',
                'best_time': 'November to February',
                'budget': '₹4,000-12,000 per day',
                'attractions': ['Baga Beach', 'Dudhsagar Falls', 'Old Goa Churches'],
                'food': ['Fish curry rice', 'Bebinca', 'Feni']
            },
            {
                'name': 'Manali, Himachal Pradesh',
                'description': 'Adventure sports and mountain views',
                'best_time': 'May to October',
                'budget': '₹5,000-10,000 per day',
                'attractions': ['Rohtang Pass', 'Solang Valley', 'Hadimba Temple'],
                'food': ['Dham', 'Trout fish', 'Apple-based dishes']
            },
            {
                'name': 'Rann of Kutch, Gujarat',
                'description': 'White salt desert and cultural festivals',
                'best_time': 'November to February',
                'budget': '₹6,000-15,000 per day',
                'attractions': ['White Rann', 'Kutch Festival', 'Wild Ass Sanctuary'],
                'food': ['Gujarati thali', 'Kutchi dabeli', 'Khaman']
            }
        ]
    },
    'romantic': {
        'destinations': [
            {
                'name': 'Udaipur, Rajasthan',
                'description': 'City of lakes and royal palaces',
                'best_time': 'September to March',
                'budget': '₹8,000-20,000 per day',
                'attractions': ['Lake Pichola', 'City Palace', 'Jag Mandir'],
                'food': ['Dal baati churma', 'Laal maas', 'Ghewar']
            },
            {
                'name': 'Ooty, Tamil Nadu',
                'description': 'Hill station with tea gardens',
                'best_time': 'April to June, September to November',
                'budget': '₹4,000-10,000 per day',
                'attractions': ['Botanical Gardens', 'Ooty Lake', 'Tea Museum'],
                'food': ['South Indian breakfast', 'Ooty chocolate', 'Nilgiri tea']
            },
            {
                'name': 'Alleppey, Kerala',
                'description': 'Venice of the East with backwaters',
                'best_time': 'October to March',
                'budget': '₹10,000-25,000 per day',
                'attractions': ['Backwater cruise', 'Alappuzha Beach', 'Marari Beach'],
                'food': ['Karimeen curry', 'Appam', 'Coconut-based dishes']
            }
        ]
    },
    'adventurous': {
        'destinations': [
            {
                'name': 'Leh-Ladakh, Jammu & Kashmir',
                'description': 'High-altitude desert with stunning landscapes',
                'best_time': 'June to September',
                'budget': '₹8,000-18,000 per day',
                'attractions': ['Pangong Lake', 'Nubra Valley', 'Magnetic Hill'],
                'food': ['Thukpa', 'Momos', 'Butter tea']
            },
            {
                'name': 'Spiti Valley, Himachal Pradesh',
                'description': 'Cold desert mountain valley',
                'best_time': 'May to October',
                'budget': '₹6,000-12,000 per day',
                'attractions': ['Key Monastery', 'Chandratal Lake', 'Pin Valley'],
                'food': ['Tibetan cuisine', 'Yak cheese', 'Local barley dishes']
            },
            {
                'name': 'Rishikesh, Uttarakhand',
                'description': 'Adventure sports and river rafting',
                'best_time': 'September to November, March to May',
                'budget': '₹4,000-10,000 per day',
                'attractions': ['River rafting', 'Bungee jumping', 'Trekking trails'],
                'food': ['North Indian vegetarian', 'Street food', 'Organic cafe food']
            }
        ]
    },
    'stressed': {
        'destinations': [
            {
                'name': 'Munnar, Kerala',
                'description': 'Tea plantations and cool climate',
                'best_time': 'September to March',
                'budget': '₹5,000-12,000 per day',
                'attractions': ['Tea gardens', 'Mattupetty Dam', 'Eravikulam National Park'],
                'food': ['Kerala cuisine', 'Tea', 'Spice-based dishes']
            },
            {
                'name': 'Dharamshala, Himachal Pradesh',
                'description': 'Peaceful hill station with Tibetan culture',
                'best_time': 'March to June, September to December',
                'budget': '₹3,000-8,000 per day',
                'attractions': ['McLeod Ganj', 'Bhagsu Waterfall', 'Norbulingka Institute'],
                'food': ['Tibetan cuisine', 'Momos', 'Thukpa']
            },
            {
                'name': 'Pushkar, Rajasthan',
                'description': 'Sacred town with serene lake',
                'best_time': 'October to March',
                'budget': '₹3,000-7,000 per day',
                'attractions': ['Pushkar Lake', 'Brahma Temple', 'Camel safari'],
                'food': ['Rajasthani vegetarian', 'Malpua', 'Lassi']
            }
        ]
    },
    'happy': {
        'destinations': [
            {
                'name': 'Mumbai, Maharashtra',
                'description': 'City of dreams with vibrant culture',
                'best_time': 'November to February',
                'budget': '₹5,000-15,000 per day',
                'attractions': ['Marine Drive', 'Gateway of India', 'Bollywood studios'],
                'food': ['Vada pav', 'Pav bhaji', 'Street food']
            },
            {
                'name': 'Jaipur, Rajasthan',
                'description': 'Pink City with royal heritage',
                'best_time': 'October to March',
                'budget': '₹4,000-12,000 per day',
                'attractions': ['Hawa Mahal', 'Amber Fort', 'City Palace'],
                'food': ['Dal baati churma', 'Ghewar', 'Rajasthani thali']
            },
            {
                'name': 'Hampi, Karnataka',
                'description': 'Ancient ruins and historical significance',
                'best_time': 'October to February',
                'budget': '₹2,500-6,000 per day',
                'attractions': ['Virupaksha Temple', 'Stone Chariot', 'Hippie Island'],
                'food': ['South Indian meals', 'Coconut-based dishes', 'Local Karnataka cuisine']
            }
        ]
    }
}