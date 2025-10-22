from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import json
import re
import random

# Import local modules
from config import Config, MOOD_DESTINATIONS
from models import db, User, SearchHistory, Itinerary, create_user, get_user_by_email, save_search_history, create_itinerary

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# AI Chatbot Logic
class TravelChatbot:
    """Simple AI Travel Chatbot with mood-based recommendations"""
    
    def __init__(self):
        self.mood_keywords = {
            'calm': ['calm', 'peaceful', 'serene', 'quiet', 'tranquil', 'relaxed', 'zen', 'meditate', 
                    'peace', 'still', 'silence', 'soothing', 'gentle', 'soft', 'restful', 'mindful'],
            'excited': ['excited', 'energetic', 'party', 'fun', 'adventure', 'wild', 'crazy', 'lively',
                       'thrilled', 'enthusiastic', 'pumped', 'hyper', 'upbeat', 'dynamic', 'spirited'],
            'romantic': ['romantic', 'love', 'couple', 'honeymoon', 'intimate', 'cozy', 'date',
                        'partner', 'relationship', 'valentine', 'anniversary', 'together', 'romantic getaway'],
            'adventurous': ['adventurous', 'thrill', 'extreme', 'hiking', 'trekking', 'adrenaline', 'challenge',
                           'daring', 'bold', 'brave', 'explore', 'discover', 'expedition', 'wilderness'],
            'stressed': ['stressed', 'tired', 'exhausted', 'overwhelmed', 'need break', 'burnout', 'pressure',
                        'anxiety', 'tension', 'worried', 'hectic', 'busy', 'overworked', 'mental health'],
            'happy': ['happy', 'joyful', 'cheerful', 'celebrate', 'vibrant', 'colorful', 'festive',
                     'elated', 'delighted', 'content', 'pleased', 'optimistic', 'positive', 'good mood']
        }
    
    def detect_mood(self, text):
        """Detect mood from user input text"""
        text = text.lower()
        mood_scores = {}
        
        # Enhanced keyword matching with weights
        for mood, keywords in self.mood_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Give higher weight to exact matches
                    if keyword == text.strip():
                        score += 3
                    elif text.startswith(keyword) or text.endswith(keyword):
                        score += 2
                    else:
                        score += 1
            mood_scores[mood] = score
        
        # Also check for common phrases
        mood_phrases = {
            'stressed': ['need a break', 'feeling overwhelmed', 'work stress', 'too much pressure'],
            'calm': ['want peace', 'need quiet', 'seek tranquility', 'peaceful place'],
            'excited': ['want fun', 'party time', 'full of energy', 'ready to explore'],
            'romantic': ['with partner', 'date night', 'romantic getaway', 'couple trip'],
            'adventurous': ['want adventure', 'thrill seeking', 'extreme sports', 'mountain climbing'],
            'happy': ['feeling good', 'want to celebrate', 'in good mood', 'cheerful']
        }
        
        for mood, phrases in mood_phrases.items():
            for phrase in phrases:
                if phrase in text:
                    mood_scores[mood] = mood_scores.get(mood, 0) + 2
        
        # Return the mood with highest score, or 'happy' as default
        detected_mood = max(mood_scores, key=mood_scores.get) if max(mood_scores.values()) > 0 else 'happy'
        return detected_mood
    
    def get_recommendations(self, mood, user_query):
        """Get travel recommendations based on mood"""
        if mood not in MOOD_DESTINATIONS:
            mood = 'happy'  # Default fallback
        
        destinations = MOOD_DESTINATIONS[mood]['destinations']
        
        # Add some randomization to make responses feel more dynamic
        selected_destinations = random.sample(destinations, min(3, len(destinations)))
        
        response = {
            'mood': mood,
            'query': user_query,
            'destinations': selected_destinations,
            'message': self.generate_response_message(mood, selected_destinations)
        }
        
        return response
    
    def generate_response_message(self, mood, destinations):
        """Generate a friendly response message"""
        mood_messages = {
            'calm': f"I sense you're looking for some tranquility! Here are {len(destinations)} peaceful destinations perfect for your current mood:",
            'excited': f"You sound full of energy! Here are {len(destinations)} exciting places that match your adventurous spirit:",
            'romantic': f"Planning something special? Here are {len(destinations)} romantic destinations perfect for you and your loved one:",
            'adventurous': f"Ready for an adrenaline rush? Here are {len(destinations)} thrilling destinations for the adventurer in you:",
            'stressed': f"You need some relaxation! Here are {len(destinations)} stress-free destinations to help you unwind:",
            'happy': f"I love your positive energy! Here are {len(destinations)} vibrant destinations to keep those good vibes going:"
        }
        
        return mood_messages.get(mood, f"Here are {len(destinations)} amazing destinations in India for you:")
    
    def get_accommodation_and_dining_recommendations(self, destination_name):
        """Get hotel and restaurant recommendations for a destination"""
        
        # Hotel recommendations by destination
        hotel_recommendations = {
            'Goa': {
                'luxury': ['Taj Exotica Resort & Spa', 'The Leela Goa', 'Grand Hyatt Goa'],
                'mid_range': ['Novotel Goa Resort & Spa', 'Holiday Inn Resort Goa', 'Radisson Blu Resort Goa'],
                'budget': ['OYO Hotels Goa', 'Zostel Goa', 'Backpacker Panda Goa']
            },
            'Kerala': {
                'luxury': ['Kumarakom Lake Resort', 'Taj Green Cove Resort & Spa', 'The Leela Kovalam'],
                'mid_range': ['Fragrant Nature Backwater Resort', 'Spice Village CGH Earth', 'Casino Hotel Kochi'],
                'budget': ['Kochi Backpackers', 'Zostel Vashisht', 'Green Woods Bethlehem']
            },
            'Rajasthan': {
                'luxury': ['Taj Lake Palace Udaipur', 'The Oberoi Udaivilas', 'Rambagh Palace Jaipur'],
                'mid_range': ['Hotel Haveli Inn Pal', 'Umaid Bhawan Palace', 'Tree of Life Resort & Spa'],
                'budget': ['Zostel Jaipur', 'Moustache Hostel Jaipur', 'Backpacker Panda Jaipur']
            },
            'Himachal Pradesh': {
                'luxury': ['The Oberoi Cecil Shimla', 'Wildflower Hall Shimla', 'Fortune Park Dalhousie'],
                'mid_range': ['Hotel Snow Valley Resorts', 'Apple Country Resort Manali', 'Hotel Hilltop Shimla'],
                'budget': ['Zostel Manali', 'Backpacker Panda Kasol', 'The Hosteller Manali']
            },
            'Karnataka': {
                'luxury': ['Taj West End Bangalore', 'The Serai Bandipur', 'Evolve Back Coorg'],
                'mid_range': ['Club Mahindra Coorg', 'Hotel Mayura Hoysala', 'The Gateway Hotel KR Road'],
                'budget': ['Zostel Bangalore', 'Backpacker Panda Hampi', 'Gokarna International Beach Resort']
            },
            'Maharashtra': {
                'luxury': ['The Taj Mahal Palace Mumbai', 'JW Marriott Mumbai', 'The St. Regis Mumbai'],
                'mid_range': ['Hotel Sahyadri Pune', 'Lemon Tree Hotel Mumbai', 'The Pride Hotel Pune'],
                'budget': ['Zostel Mumbai', 'Backpacker Panda Lonavala', 'YMCA Mumbai']
            },
            'Tamil Nadu': {
                'luxury': ['Taj Fisherman\'s Cove Chennai', 'The Leela Palace Chennai', 'Fortune Resort Bay Island'],
                'mid_range': ['Hotel Sangam Thanjavur', 'GRT Grand Chennai', 'Sterling Yelagiri'],
                'budget': ['Zostel Pondicherry', 'Backpacker Panda Kodaikanal', 'Hotel Saravana Bhavan Lodge']
            }
        }
        
        # Restaurant recommendations by destination
        restaurant_recommendations = {
            'Goa': {
                'fine_dining': ['Thalassa', 'La Plage', 'Bomra\'s'],
                'local_cuisine': ['Vinayak Family Restaurant', 'Mum\'s Kitchen', 'Fish Curry Rice'],
                'street_food': ['Goa Bhel', 'Bebinca Cafe', 'Cafe Chocolatti'],
                'beach_shacks': ['Curlies Beach Shack', 'Shiva Valley', 'Anjuna Beach Restaurant']
            },
            'Kerala': {
                'fine_dining': ['Dhe Puttu', 'Casino Hotel Restaurant', 'The Rice Boat'],
                'local_cuisine': ['Saravana Bhavan', 'Aryaas Restaurant', 'Hotel Rahmath'],
                'street_food': ['Kozhikode Biryani Stall', 'Ernakulam Food Street', 'Kochi Spice Market'],
                'backwater_dining': ['Backwater Ripples', 'Lake Palace Restaurant', 'Coconut Lagoon']
            },
            'Rajasthan': {
                'fine_dining': ['1135 AD Restaurant', 'Ambrai Restaurant', 'Handi Restaurant'],
                'local_cuisine': ['Chokhi Dhani', 'Laxmi Misthan Bhandar', 'Rawat Mishtan Bhandar'],
                'street_food': ['Johri Bazaar Food Street', 'Bapu Bazaar', 'Clock Tower Market'],
                'rooftop_dining': ['Upre Restaurant', 'Sky Deck Lounge', 'Sunset Terrace']
            },
            'Himachal Pradesh': {
                'fine_dining': ['The Restaurant at Wildflower Hall', 'Eighteen71 Cookhouse & Bar', 'Wake & Bake Cafe'],
                'local_cuisine': ['Sher-e-Punjab', 'Johnson Cafe', 'Cafe 1947'],
                'mountain_cafes': ['Moon Dance Cafe', 'German Bakery Kasol', 'Evergreen Cafe'],
                'street_food': ['Mall Road Food Stalls', 'Manali Market', 'Old Manali Cafes']
            },
            'Karnataka': {
                'fine_dining': ['Karavalli', 'Toit Brewpub', 'The Only Place'],
                'local_cuisine': ['MTR Restaurant', 'Vidyarthi Bhavan', 'Brahmin\'s Coffee Bar'],
                'street_food': ['VV Puram Food Street', 'Commercial Street Eateries', 'Russell Market'],
                'coastal_cuisine': ['Gokarna Beach Restaurants', 'Udupi Krishna Bhavan', 'Fisherman\'s Wharf']
            },
            'Maharashtra': {
                'fine_dining': ['Trishna', 'The Table', 'Indigo Delicatessen'],
                'local_cuisine': ['Britannia & Co.', 'Cafe Madras', 'Hotel Goodluck'],
                'street_food': ['Mohammed Ali Road', 'Juhu Beach Chaat', 'Crawford Market'],
                'hill_station': ['Hotel Chandralok Lonavala', 'Rama Krishna Restaurant', 'German Bakery Pune']
            },
            'Tamil Nadu': {
                'fine_dining': ['Dakshin Restaurant', 'Benjarong', 'Peshawri'],
                'local_cuisine': ['Murugan Idli Shop', 'Saravana Bhavan', 'Hotel Junior Kuppanna'],
                'street_food': ['Marina Beach Food Stalls', 'T Nagar Food Street', 'Pondy Bazaar'],
                'temple_food': ['Annapoorna Restaurant', 'Amma Unavagam', 'Krishna Sweets']
            }
        }
        
        # Default recommendations if destination not found
        default_hotels = {
            'luxury': ['Premium Heritage Hotel', 'Luxury Resort & Spa', 'Grand Palace Hotel'],
            'mid_range': ['Comfort Inn Hotel', 'Best Western Hotel', 'Holiday Resort'],
            'budget': ['OYO Hotels', 'Budget Backpacker Hostel', 'Economy Lodge']
        }
        
        default_restaurants = {
            'fine_dining': ['Premium Fine Dining Restaurant', 'Luxury Multi-Cuisine Restaurant'],
            'local_cuisine': ['Local Traditional Restaurant', 'Authentic Regional Cuisine'],
            'street_food': ['Local Food Street', 'Traditional Market Eateries'],
            'cafes': ['Local Coffee House', 'Traditional Tea Stall']
        }
        
        # Find matching destination (partial match)
        hotels = default_hotels
        restaurants = default_restaurants
        
        for dest_key in hotel_recommendations.keys():
            if dest_key.lower() in destination_name.lower() or destination_name.lower() in dest_key.lower():
                hotels = hotel_recommendations[dest_key]
                restaurants = restaurant_recommendations[dest_key]
                break
        
        return hotels, restaurants
    
    def create_itinerary(self, destination_data, trip_duration=3):
        """Create a detailed itinerary for a destination"""
        destination = destination_data
        days = []
        
        attractions = destination['attractions']
        food_spots = destination['food']
        
        # Get hotel and restaurant recommendations based on destination
        hotels, restaurants = self.get_accommodation_and_dining_recommendations(destination['name'])
        
        # Calculate estimated budget per day
        try:
            budget_str = destination['budget'].replace('₹', '').replace(',', '').replace(' per day', '')
            # Extract numeric budget (take middle value if range)
            if '-' in budget_str:
                budget_parts = budget_str.split('-')
                min_budget = int(''.join(filter(str.isdigit, budget_parts[0].strip())))
                max_budget = int(''.join(filter(str.isdigit, budget_parts[1].strip())))
                daily_budget = (min_budget + max_budget) // 2
            else:
                # Single budget value
                daily_budget = int(''.join(filter(str.isdigit, budget_str)))
        except (ValueError, IndexError):
            # Default budget if parsing fails
            daily_budget = 5000  # Default ₹5,000 per day
        
        # Select hotels and restaurants for the itinerary
        selected_hotel = random.choice(hotels['mid_range']) if 'mid_range' in hotels else "Comfort Hotel"
        budget_hotel = random.choice(hotels['budget']) if 'budget' in hotels else "Budget Lodge"
        luxury_hotel = random.choice(hotels['luxury']) if 'luxury' in hotels else "Premium Resort"
        
        selected_restaurants = []
        for category in restaurants.keys():
            if restaurants[category]:
                selected_restaurants.extend(random.sample(restaurants[category], min(2, len(restaurants[category]))))
        
        if not selected_restaurants:
            selected_restaurants = ["Local Restaurant", "Traditional Eatery", "Regional Cuisine Restaurant"]
        
        for day in range(1, trip_duration + 1):
            if day == 1:
                recommended_hotel = selected_hotel
                lunch_restaurant = selected_restaurants[0] if len(selected_restaurants) > 0 else "Local Restaurant"
                dinner_restaurant = selected_restaurants[1] if len(selected_restaurants) > 1 else "Traditional Eatery"
                
                activities = [
                    {'time': '10:00 AM', 'title': 'Arrival & Check-in', 'description': f'Arrive at destination, check into {recommended_hotel}, freshen up and get oriented', 'tags': ['Travel', 'Accommodation'], 'hotel': recommended_hotel},
                    {'time': '12:00 PM', 'title': f'Lunch at {lunch_restaurant}', 'description': f'Welcome lunch at {lunch_restaurant} - try {food_spots[0] if food_spots else "local specialties"} and authentic regional flavors', 'tags': ['Food', 'Culture'], 'restaurant': lunch_restaurant},
                    {'time': '2:00 PM', 'title': f'Visit {attractions[0] if attractions else "City Center"}', 'description': f'Explore the famous {attractions[0] if attractions else "main attractions"}, take photos, learn about local history and culture', 'tags': ['Sightseeing', 'Photography']},
                    {'time': '5:00 PM', 'title': 'Evening Walk & Local Shopping', 'description': 'Leisurely walk around the area, interact with locals, shop for souvenirs and local handicrafts', 'tags': ['Walking', 'Shopping']},
                    {'time': '7:30 PM', 'title': f'Dinner at {dinner_restaurant}', 'description': f'Evening dinner at {dinner_restaurant} featuring {food_spots[1] if len(food_spots) > 1 else "regional specialties"}, experience authentic local dining culture', 'tags': ['Food', 'Culture'], 'restaurant': dinner_restaurant}
                ]
                day_plan = {
                    'day': day,
                    'title': f'Arrival Day - Welcome to {destination["name"]}',
                    'activities': activities,
                    'accommodation': {'name': recommended_hotel, 'type': 'Mid-range Hotel'}
                }
            elif day == trip_duration:
                checkout_restaurant = selected_restaurants[(day-1) % len(selected_restaurants)] if selected_restaurants else "Local Farewell Restaurant"
                
                activities = [
                    {'time': '8:00 AM', 'title': 'Early Morning Leisure', 'description': f'Final peaceful moments at {recommended_hotel}, pack essentials, prepare for departure', 'tags': ['Relaxation', 'Travel'], 'hotel': recommended_hotel},
                    {'time': '10:00 AM', 'title': f'Final Visit - {attractions[-1] if len(attractions) > 1 else "Local Market"}', 'description': f'Last exploration of {attractions[-1] if len(attractions) > 1 else "nearby attractions"}, capture final memorable photos', 'tags': ['Sightseeing', 'Photography']},
                    {'time': '12:00 PM', 'title': f'Check-out & Farewell Lunch at {checkout_restaurant}', 'description': f'Hotel check-out from {recommended_hotel}, final local meal at {checkout_restaurant}, gather belongings and memories', 'tags': ['Travel', 'Food'], 'hotel': recommended_hotel, 'restaurant': checkout_restaurant},
                    {'time': '2:00 PM', 'title': 'Last-minute Shopping & Souvenirs', 'description': 'Buy souvenirs, local handicrafts, gifts for family and friends, final local market exploration', 'tags': ['Shopping', 'Souvenirs']},
                    {'time': '4:00 PM', 'title': 'Departure Journey', 'description': 'Head to airport/station, bid farewell to this beautiful destination with wonderful memories', 'tags': ['Travel', 'Departure']}
                ]
                day_plan = {
                    'day': day,
                    'title': f'Departure Day - Farewell {destination["name"]}',
                    'activities': activities,
                    'accommodation': {'name': recommended_hotel, 'type': 'Mid-range Hotel', 'checkout': True}
                }
            else:
                attraction_index = (day - 1) % len(attractions) if attractions else 0
                food_index = (day - 1) % len(food_spots) if food_spots else 0
                current_attraction = attractions[attraction_index] if attractions else "Local Attractions"
                current_food = food_spots[food_index] if food_spots else "local cuisine"
                
                # Select restaurants for lunch and dinner
                lunch_restaurant = selected_restaurants[(day-1) * 2 % len(selected_restaurants)] if selected_restaurants else f"Local {current_food} Restaurant"
                dinner_restaurant = selected_restaurants[(day-1) * 2 + 1 % len(selected_restaurants)] if selected_restaurants else "Traditional Evening Restaurant"
                
                activities = [
                    {'time': '9:00 AM', 'title': f'Morning at {current_attraction}', 'description': f'Explore {current_attraction}, learn about its fascinating history and cultural significance', 'tags': ['Sightseeing', 'Culture']},
                    {'time': '11:30 AM', 'title': 'Photography & Hidden Gems', 'description': f'Capture beautiful moments at {current_attraction}, explore hidden gems and secret spots around the area', 'tags': ['Photography', 'Exploration']},
                    {'time': '1:00 PM', 'title': f'Lunch at {lunch_restaurant}', 'description': f'Enjoy delicious {current_food} at {lunch_restaurant}, experience authentic local flavors and traditional cooking styles', 'tags': ['Food', 'Culture'], 'restaurant': lunch_restaurant},
                    {'time': '3:00 PM', 'title': 'Afternoon Adventure & Personal Time', 'description': 'Free time for personal exploration, shopping for local crafts, or relaxation as per your preference', 'tags': ['Free Time', 'Flexible']},
                    {'time': '6:00 PM', 'title': 'Evening Relaxation & Sunset Views', 'description': 'Unwind at scenic spots, enjoy beautiful sunset views, interact with friendly locals, cultural immersion experience', 'tags': ['Relaxation', 'Culture']},
                    {'time': '8:00 PM', 'title': f'Dinner at {dinner_restaurant} & Night Experience', 'description': f'Traditional dinner at {dinner_restaurant}, experience local nightlife, cultural performances and entertainment if available', 'tags': ['Food', 'Entertainment'], 'restaurant': dinner_restaurant}
                ]
                day_plan = {
                    'day': day,
                    'title': f'Day {day} - Exploring {current_attraction}',
                    'activities': activities,
                    'accommodation': {'name': recommended_hotel, 'type': 'Mid-range Hotel'}
                }
            
            days.append(day_plan)
        
        # Calculate detailed budget breakdown
        total_budget = daily_budget * trip_duration
        budget_breakdown = {
            'accommodation': int(total_budget * 0.4),
            'food': int(total_budget * 0.3),
            'transportation': int(total_budget * 0.2),
            'activities': int(total_budget * 0.1),
            'total': total_budget
        }
        
        return {
            'destination': destination['name'],
            'duration': trip_duration,
            'budget_range': destination['budget'],
            'estimated_budget': f"₹{total_budget:,}",
            'budget_breakdown': budget_breakdown,
            'best_time': destination['best_time'],
            'days': days,
            'accommodation_recommendations': {
                'primary_hotel': selected_hotel,
                'budget_options': hotels.get('budget', [])[:3],
                'mid_range_options': hotels.get('mid_range', [])[:3],
                'luxury_options': hotels.get('luxury', [])[:3]
            },
            'dining_recommendations': {
                'featured_restaurants': selected_restaurants[:6],
                'fine_dining': restaurants.get('fine_dining', [])[:3] if 'fine_dining' in restaurants else restaurants.get('local_cuisine', [])[:3],
                'local_cuisine': restaurants.get('local_cuisine', [])[:3] if 'local_cuisine' in restaurants else [],
                'street_food': restaurants.get('street_food', [])[:3] if 'street_food' in restaurants else []
            },
            'travel_tips': [
                f'Best time to visit: {destination["best_time"]}',
                f'Estimated budget: ₹{total_budget:,} for {trip_duration} days',
                f'Recommended accommodation: {selected_hotel} (Mid-range option)',
                'Book accommodations in advance during peak season',
                'Try local transportation for authentic experience',
                'Keep some cash handy for local vendors and street food',
                'Respect local customs and traditions',
                'Don\'t forget to try the recommended local restaurants!',
                'Ask hotel staff for additional local restaurant recommendations'
            ]
        }

# Initialize chatbot
chatbot = TravelChatbot()

# Auto-create database tables and demo user
def initialize_database():
    """Initialize database"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created!")
            
            # Create demo user if doesn't exist
            if not get_user_by_email('demo@paradiseride.com'):
                demo_user = create_user(
                    name="Demo User",
                    email="demo@paradiseride.com", 
                    password="demo123"
                )
                if demo_user:
                    print("✅ Demo user created: demo@paradiseride.com / demo123")
    except Exception as e:
        print(f"⚠️ Database setup error: {e}")

# Initialize database on startup
initialize_database()

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('chatbot_page'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        user = get_user_by_email(email)
        
        if user and user.check_password(password):
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page or chatbot
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('chatbot_page'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('chatbot_page'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('Please fill in all fields.', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('signup.html')
        
        # Check if email is valid
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash('Please enter a valid email address.', 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        if get_user_by_email(email):
            flash('An account with this email already exists.', 'error')
            return render_template('signup.html')
        
        # Create new user
        user = create_user(name, email, password)
        if user:
            login_user(user)
            flash(f'Welcome to ParadiseRide, {name}!', 'success')
            return redirect(url_for('chatbot_page'))
        else:
            flash('An error occurred during registration. Please try again.', 'error')
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/chatbot')
@login_required
def chatbot_page():
    """Main chatbot interface"""
    # Get recent search history for sidebar
    recent_searches = current_user.get_recent_searches(10)
    return render_template('chatbot.html', recent_searches=recent_searches)

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """API endpoint for chatbot interactions"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Detect mood and get recommendations
        detected_mood = chatbot.detect_mood(user_message)
        recommendations = chatbot.get_recommendations(detected_mood, user_message)
        
        # Save search history
        save_search_history(
            user_id=current_user.id,
            mood=detected_mood,
            query=user_message,
            result=json.dumps(recommendations)
        )
        
        return jsonify({
            'success': True,
            'response': recommendations
        })
        
    except Exception as e:
        app.logger.error(f"Chat API error: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/api/create_itinerary', methods=['POST'])
@login_required
def api_create_itinerary():
    """API endpoint to create detailed itinerary"""
    try:
        data = request.get_json()
        destination_name = data.get('destination')
        duration = data.get('duration', 3)
        start_date_str = data.get('start_date')
        mood_tag = data.get('mood', 'happy')
        
        app.logger.info(f"Creating itinerary for {destination_name}, duration: {duration}, start: {start_date_str}")
        
        if not all([destination_name, start_date_str]):
            return jsonify({'error': 'Destination and start date are required'}), 400
        
        # Validate duration
        try:
            duration = int(duration)
            if duration < 1 or duration > 30:
                return jsonify({'error': 'Duration must be between 1 and 30 days'}), 400
        except (ValueError, TypeError):
            duration = 3  # Default to 3 days
        
        # Find destination data
        destination_data = None
        for mood_destinations in MOOD_DESTINATIONS.values():
            for dest in mood_destinations['destinations']:
                if dest['name'] == destination_name:
                    destination_data = dest
                    break
            if destination_data:
                break
        
        if not destination_data:
            app.logger.error(f"Destination not found: {destination_name}")
            return jsonify({'error': f'Destination "{destination_name}" not found'}), 404
        
        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=duration-1)
        except ValueError as e:
            app.logger.error(f"Date parsing error: {e}")
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        app.logger.info(f"Creating detailed itinerary for {destination_name}")
        
        # Create detailed itinerary
        detailed_itinerary = chatbot.create_itinerary(destination_data, duration)
        
        app.logger.info(f"Detailed itinerary created successfully. Saving to database...")
        
        # Save to database
        itinerary = create_itinerary(
            user_id=current_user.id,
            title=f"{duration} Days in {destination_name}",
            destination=destination_name,
            start_date=start_date,
            end_date=end_date,
            budget=destination_data['budget'],
            description=destination_data['description'],
            detailed_plan=json.dumps(detailed_itinerary),
            mood_tag=mood_tag
        )
        
        app.logger.info(f"Itinerary saved to database with ID: {itinerary.id}")
        
        return jsonify({
            'success': True,
            'itinerary_id': itinerary.id,
            'message': 'Itinerary created successfully!',
            'itinerary': detailed_itinerary
        })
        
    except Exception as e:
        app.logger.error(f"Create itinerary error: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred creating the itinerary: {str(e)}'}), 500

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_stats = {
        'search_count': current_user.get_search_count(),
        'itinerary_count': current_user.get_itinerary_count(),
        'member_since': current_user.created_at.strftime('%B %Y')
    }
    
    recent_searches = current_user.get_recent_searches(5)
    from models import get_user_itineraries
    recent_itineraries = get_user_itineraries(current_user.id, 5)
    
    return render_template('dashboard.html', 
                         stats=user_stats, 
                         recent_searches=recent_searches,
                         recent_itineraries=recent_itineraries)

@app.route('/itinerary/<int:itinerary_id>')
@login_required
def view_itinerary(itinerary_id):
    """View detailed itinerary"""
    itinerary = db.session.query(Itinerary).filter_by(id=itinerary_id, user_id=current_user.id).first()
    if not itinerary:
        flash('Itinerary not found.', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('itinerary.html', itinerary=itinerary)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/team')
def team():
    """Team page"""
    return render_template('team.html')

@app.route('/test-images')
def test_images():
    """Test page for debugging team images"""
    return render_template('test_images.html')

@app.route('/api/itineraries')
@login_required
def api_itineraries():
    """API to get user's itineraries"""
    from models import get_user_itineraries
    itineraries = get_user_itineraries(current_user.id)
    return jsonify({
        'success': True,
        'itineraries': [itinerary.to_dict() for itinerary in itineraries]
    })

@app.route('/api/search_history')
@login_required
def api_search_history():
    """API to get user's search history"""
    from models import get_user_search_history
    searches = get_user_search_history(current_user.id)
    return jsonify({
        'success': True,
        'searches': [search.to_dict() for search in searches]
    })

@app.route('/api/optimize_budget', methods=['POST'])
@login_required
def api_optimize_budget():
    """API endpoint to optimize budget for an itinerary"""
    try:
        data = request.get_json()
        itinerary_id = data.get('itinerary_id')
        destination = data.get('destination')
        duration = data.get('duration', 3)
        current_budget = data.get('current_budget', '')
        
        app.logger.info(f"Optimizing budget for itinerary {itinerary_id}, destination: {destination}")
        
        # Verify itinerary belongs to user
        itinerary = db.session.query(Itinerary).filter_by(id=itinerary_id, user_id=current_user.id).first()
        if not itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        
        # Generate budget optimization suggestions
        optimization = generate_budget_optimization(destination, duration, current_budget)
        
        return jsonify({
            'success': True,
            'optimization': optimization
        })
        
    except Exception as e:
        app.logger.error(f"Budget optimization error: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred optimizing budget: {str(e)}'}), 500

@app.route('/api/apply_optimization', methods=['POST'])
@login_required
def api_apply_optimization():
    """API endpoint to apply budget optimization to an itinerary"""
    try:
        data = request.get_json()
        itinerary_id = data.get('itinerary_id')
        optimization_level = data.get('optimization_level', 'medium')  # 'medium' or 'high'
        destination = data.get('destination')
        duration = data.get('duration', 3)
        
        app.logger.info(f"Applying {optimization_level} optimization to itinerary {itinerary_id}")
        
        # Verify itinerary belongs to user
        itinerary = db.session.query(Itinerary).filter_by(id=itinerary_id, user_id=current_user.id).first()
        if not itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        
        # Get current itinerary data
        current_itinerary = json.loads(itinerary.detailed_plan)
        
        # Apply optimization to create updated itinerary
        optimized_itinerary = apply_budget_optimization_to_itinerary(
            current_itinerary, destination, optimization_level
        )
        
        # Update the itinerary in database
        itinerary.detailed_plan = json.dumps(optimized_itinerary)
        itinerary.budget = optimized_itinerary['estimated_budget']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{optimization_level.capitalize()} optimization applied successfully!',
            'updated_itinerary': optimized_itinerary
        })
        
    except Exception as e:
        app.logger.error(f"Apply optimization error: {str(e)}", exc_info=True)
        return jsonify({'error': f'An error occurred applying optimization: {str(e)}'}), 500

def apply_budget_optimization_to_itinerary(current_itinerary, destination, optimization_level):
    """Apply budget optimization to an existing itinerary"""
    
    # Get hotel and restaurant recommendations based on optimization level
    chatbot_instance = TravelChatbot()
    hotels, restaurants = chatbot_instance.get_accommodation_and_dining_recommendations(destination)
    
    # Update accommodation based on optimization level
    if optimization_level == 'high':
        # Use budget accommodations
        selected_hotel = random.choice(hotels['budget']) if 'budget' in hotels else "Budget Hostel"
        hotel_type = "Budget Accommodation"
        
        # Use budget restaurants (street food, local eateries)
        selected_restaurants = []
        if 'street_food' in restaurants:
            selected_restaurants.extend(restaurants['street_food'][:4])
        if 'local_cuisine' in restaurants:
            selected_restaurants.extend(restaurants['local_cuisine'][:2])
        if not selected_restaurants:
            selected_restaurants = ["Local Street Food Stall", "Budget Local Eatery", "Roadside Dhaba", "Community Kitchen"]
            
    else:  # medium optimization
        # Use budget to mid-range accommodations
        budget_hotels = hotels.get('budget', [])
        mid_range_hotels = hotels.get('mid_range', [])
        available_hotels = budget_hotels + mid_range_hotels
        selected_hotel = random.choice(available_hotels) if available_hotels else "Budget Hotel"
        hotel_type = "Budget/Mid-range Hotel"
        
        # Mix of budget and local restaurants
        selected_restaurants = []
        for category in ['local_cuisine', 'street_food']:
            if category in restaurants:
                selected_restaurants.extend(restaurants[category][:3])
        if not selected_restaurants:
            selected_restaurants = ["Local Restaurant", "Traditional Eatery", "Budget Dining", "Street Food Vendor"]
    
    # Calculate optimized budget
    original_budget_str = current_itinerary.get('estimated_budget', '₹15,000')
    original_amount = int(''.join(filter(str.isdigit, original_budget_str.replace('₹', '').replace(',', ''))))
    
    if optimization_level == 'high':
        optimized_amount = int(original_amount * 0.25)  # 75% savings
        savings_percent = 75
    else:
        optimized_amount = int(original_amount * 0.75)  # 25% savings
        savings_percent = 25
    
    savings_amount = original_amount - optimized_amount
    
    # Update accommodation recommendations
    current_itinerary['accommodation_recommendations'] = {
        'primary_hotel': selected_hotel,
        'optimization_level': optimization_level,
        'budget_options': hotels.get('budget', [])[:3],
        'selected_tier': 'budget' if optimization_level == 'high' else 'budget/mid-range'
    }
    
    # Update dining recommendations
    current_itinerary['dining_recommendations'] = {
        'featured_restaurants': selected_restaurants[:6],
        'optimization_level': optimization_level,
        'focus': 'street food & local eateries' if optimization_level == 'high' else 'local cuisine & budget dining'
    }
    
    # Update budget information
    current_itinerary['estimated_budget'] = f"₹{optimized_amount:,}"
    current_itinerary['optimization_applied'] = {
        'level': optimization_level,
        'original_budget': f"₹{original_amount:,}",
        'optimized_budget': f"₹{optimized_amount:,}",
        'savings': f"₹{savings_amount:,}",
        'savings_percentage': f"{savings_percent}%"
    }
    
    # Update daily activities with optimized hotels and restaurants
    for day_plan in current_itinerary.get('days', []):
        # Update accommodation info
        if 'accommodation' in day_plan:
            day_plan['accommodation']['name'] = selected_hotel
            day_plan['accommodation']['type'] = hotel_type
        
        # Update activities with new hotel and restaurant names
        for activity in day_plan.get('activities', []):
            # Update hotel references
            if 'hotel' in activity:
                activity['hotel'] = selected_hotel
                activity['description'] = activity['description'].replace(
                    activity.get('hotel', ''), selected_hotel
                )
            
            # Update restaurant references
            if 'restaurant' in activity:
                # Select appropriate restaurant from optimized list
                restaurant_index = hash(activity['title']) % len(selected_restaurants)
                new_restaurant = selected_restaurants[restaurant_index]
                old_restaurant = activity['restaurant']
                
                activity['restaurant'] = new_restaurant
                activity['title'] = activity['title'].replace(old_restaurant, new_restaurant)
                activity['description'] = activity['description'].replace(old_restaurant, new_restaurant)
    
    # Update travel tips
    optimization_tips = {
        'high': [
            "Stay in budget hostels, dormitories, or dharamshalas for maximum savings",
            "Eat primarily at street food stalls and local community kitchens",
            "Use only public transportation - buses and trains",
            "Visit free attractions like temples, parks, and natural viewpoints",
            "Carry your own water bottle and snacks to save money",
            "Look for free cultural events and festivals during your visit"
        ],
        'medium': [
            "Mix of budget hotels and hostels for comfortable yet affordable stays",
            "Eat at local restaurants and street food for authentic, budget-friendly meals",
            "Use public transport with occasional auto-rickshaw for convenience",
            "Focus on low-cost attractions and free cultural sites",
            "Shop at local markets for better prices on souvenirs",
            "Ask locals for hidden gems and free activity recommendations"
        ]
    }
    
    current_itinerary['travel_tips'] = [
        f"Budget optimized for {savings_percent}% savings (₹{savings_amount:,})",
        f"Accommodation: {selected_hotel} ({hotel_type})",
        f"Dining focus: {current_itinerary['dining_recommendations']['focus']}"
    ] + optimization_tips[optimization_level]
    
    return current_itinerary

def generate_budget_optimization(destination, duration, current_budget):
    """Generate budget optimization suggestions for a destination"""
    
    # Extract current budget amount
    try:
        budget_str = current_budget.replace('₹', '').replace(',', '').replace(' per day', '')
        if '-' in budget_str:
            budget_parts = budget_str.split('-')
            min_budget = int(''.join(filter(str.isdigit, budget_parts[0].strip())))
            max_budget = int(''.join(filter(str.isdigit, budget_parts[1].strip())))
            current_amount = (min_budget + max_budget) // 2 * duration
        else:
            daily_budget = int(''.join(filter(str.isdigit, budget_str)))
            current_amount = daily_budget * duration
    except:
        current_amount = 15000  # Default if parsing fails
    
    # Medium optimization (25% savings)
    medium_savings_percent = 0.25
    medium_optimized_amount = int(current_amount * (1 - medium_savings_percent))
    medium_savings_amount = current_amount - medium_optimized_amount
    
    # High optimization (75% savings)
    high_savings_percent = 0.75
    high_optimized_amount = int(current_amount * (1 - high_savings_percent))
    high_savings_amount = current_amount - high_optimized_amount
    
    # Medium optimization tips (balanced approach)
    medium_accommodation_tips = [
        "Stay in budget hotels, hostels, or homestays instead of luxury resorts",
        "Book accommodations slightly outside city center for better rates",
        "Look for properties with free breakfast included",
        "Use platforms like OYO, FabHotels for affordable verified stays",
        "Consider shared accommodations or dormitories for solo travel"
    ]
    
    medium_food_tips = [
        "Try local street food and small eateries - they're authentic and affordable",
        "Visit local markets for fresh, cheap produce and snacks",
        "Avoid hotel restaurants and tourist areas for dining",
        "Pack some snacks and water to avoid expensive tourist spot prices",
        "Look for local 'thali' restaurants for complete, affordable meals"
    ]
    
    medium_transport_tips = [
        "Use public transportation (buses, trains) instead of private taxis",
        "Book train tickets well in advance for better prices",
        "Consider shared rides or carpooling options",
        "Walk or rent bicycles for short distances",
        "Use government bus services instead of private luxury buses"
    ]
    
    medium_activity_tips = [
        "Visit free attractions like public parks, temples, and beaches",
        "Look for group discounts for paid attractions",
        "Choose nature-based activities over expensive adventure sports",
        "Visit during off-peak hours for potential discounts",
        "Explore local festivals and cultural events (usually free)"
    ]
    
    # High optimization tips (extreme budget approach)
    high_accommodation_tips = [
        "Stay in dormitories, youth hostels, or Couchsurfing (free accommodation)",
        "Camp outdoors where permitted (bring your own tent)",
        "Stay with locals through homestay networks (very affordable)",
        "Look for work-exchange programs (accommodation for work)",
        "Consider railway retiring rooms or dharamshalas (religious guesthouses)",
        "Sleep in train sleeper class for long journeys (saves hotel cost)"
    ]
    
    high_food_tips = [
        "Eat only at local street vendors and roadside dhabas (₹20-50 per meal)",
        "Buy groceries and cook your own meals when possible",
        "Drink only tap water or carry your own water bottle",
        "Skip restaurants entirely - eat where locals eat",
        "Look for community kitchens (langar) at religious places (free food)",
        "Carry dry snacks, biscuits, and instant noodles for meals"
    ]
    
    high_transport_tips = [
        "Use only government buses and local trains (cheapest option)",
        "Hitchhike when safe and legal (free transportation)",
        "Walk long distances instead of taking transport",
        "Use bicycle rentals for local travel (₹50-100 per day)",
        "Travel in general/sleeper class only",
        "Share auto-rickshaws with other passengers"
    ]
    
    high_activity_tips = [
        "Only visit free attractions - temples, parks, beaches, viewpoints",
        "Skip all paid activities and adventure sports entirely",
        "Use free walking tours or explore on your own",
        "Visit during free entry days at museums and monuments",
        "Enjoy nature-based free activities like hiking and photography",
        "Participate in local festivals and cultural events (usually free)"
    ]
    
    # Add destination-specific tips for medium optimization
    if 'Goa' in destination:
        medium_accommodation_tips.append("Stay in North Goa for budget options, avoid South Goa luxury resorts")
        medium_food_tips.append("Eat at local Goan tavernas instead of beach shacks")
        medium_activity_tips.append("Enjoy free beaches instead of paying for water sports initially")
        
        high_accommodation_tips.append("Stay in beach huts or local fisherman's houses")
        high_food_tips.append("Buy fresh fish from fishermen and cook at beach huts")
        high_activity_tips.append("Stick to free beach activities, avoid all paid water sports")
        
    elif 'Kerala' in destination:
        medium_accommodation_tips.append("Choose traditional homestays over luxury houseboats")
        medium_food_tips.append("Try local toddy shops for authentic, cheap Kerala food")
        medium_transport_tips.append("Use KSRTC buses - they're reliable and very affordable")
        
        high_accommodation_tips.append("Stay with local families or in basic dormitories")
        high_food_tips.append("Eat only at local homes or community meals")
        high_transport_tips.append("Use local buses and walk along backwaters")
        
    elif 'Rajasthan' in destination:
        medium_accommodation_tips.append("Stay in heritage havelis instead of palace hotels")
        medium_food_tips.append("Visit local dhabas for authentic Rajasthani food")
        medium_activity_tips.append("Many forts have nominal entry fees compared to private guided tours")
        
        high_accommodation_tips.append("Stay in dharamshalas near temples or basic guesthouses")
        high_food_tips.append("Eat at roadside dhabas and local households only")
        high_activity_tips.append("Visit only free viewpoints and temples, skip paid monuments")
        
    elif 'Himachal' in destination or 'Manali' in destination:
        medium_accommodation_tips.append("Book mountain homestays instead of resort properties")
        medium_food_tips.append("Try local 'dham' community meals - authentic and very affordable")
        medium_activity_tips.append("Enjoy natural hot springs and hiking trails (free activities)")
        
        high_accommodation_tips.append("Camp outdoors or stay in basic mountain huts")
        high_food_tips.append("Cook your own meals with local groceries")
        high_activity_tips.append("Only do free trekking and visit natural attractions")
    
    return {
        'original_budget': f"₹{current_amount:,}",
        'medium': {
            'optimized_budget': f"₹{medium_optimized_amount:,}",
            'savings': f"₹{medium_savings_amount:,}",
            'savings_percentage': f"{int(medium_savings_percent * 100)}%",
            'accommodation_tips': medium_accommodation_tips,
            'food_tips': medium_food_tips,
            'transport_tips': medium_transport_tips,
            'activity_tips': medium_activity_tips
        },
        'high': {
            'optimized_budget': f"₹{high_optimized_amount:,}",
            'savings': f"₹{high_savings_amount:,}",
            'savings_percentage': f"{int(high_savings_percent * 100)}%",
            'accommodation_tips': high_accommodation_tips,
            'food_tips': high_food_tips,
            'transport_tips': high_transport_tips,
            'activity_tips': high_activity_tips
        }
    }

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Context processors
@app.context_processor
def inject_user():
    """Make current user available in all templates"""
    return dict(current_user=current_user)

@app.context_processor
def inject_config():
    """Make config available in templates"""
    return dict(app_name=app.config['APP_NAME'])

# Template filters
@app.template_filter('datetime')
def datetime_filter(datetime_obj):
    """Format datetime for display"""
    return datetime_obj.strftime('%B %d, %Y at %I:%M %p')

@app.template_filter('date')
def date_filter(date_obj):
    """Format date for display"""
    return date_obj.strftime('%B %d, %Y')

@app.template_filter('from_json')
def from_json_filter(json_str):
    """Parse JSON string in templates"""
    try:
        return json.loads(json_str) if json_str else {}
    except:
        return {}

if __name__ == '__main__':
    print(f"Starting {app.config['APP_NAME']}...")
    print("Visit: http://127.0.0.1:5000")
    print("📧 Demo login: demo@paradiseride.com")
    print("🔑 Password: demo123")
    app.run(debug=True)
