# 🛫 ParadiseRide - AI Travel Chatbot

**Let your mood decide your next adventure across India!**

ParadiseRide is an intelligent travel planning web application that uses AI to recommend destinations across India based on your current emotional state and mood. Whether you're feeling calm, excited, romantic, adventurous, stressed, or happy - our AI chatbot will suggest the perfect destinations and create personalized itineraries just for you.

## ✨ Features

### 🤖 AI-Powered Recommendations
- Emotion-based destination suggestions
- Natural language processing for mood detection
- Personalized travel recommendations for India

### 🗺️ Comprehensive Travel Planning
- Detailed day-by-day itineraries
- Budget estimates and best travel times
- Local attractions and food recommendations
- Travel tips and insights

### 💬 Interactive Chatbot Interface
- ChatGPT-style conversational UI
- Real-time mood-based suggestions
- Quick mood selector buttons
- Conversation history

### 👤 User Management
- Secure user authentication (signup/login)
- Personal dashboard with trip statistics
- Search history and saved itineraries
- Trip management and tracking

### 🎨 Modern Design
- Responsive design (mobile & desktop)
- Smooth animations and transitions
- India-themed visual elements
- Glass morphism and gradient effects

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Git (optional)

### Installation

1. **Clone or Download the Project**
   ```bash
   # If using Git
   git clone <repository-url>
   cd AI_Travel_Chatbot
   
   # Or download and extract the ZIP file
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```
   - Choose 'y' when prompted to create sample data
   - This creates a demo account for testing

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Open Your Browser**
   ```
   http://127.0.0.1:5000
   ```

## 🎯 Demo Account

For quick testing, use the demo account:
- **Email:** `demo@paradiseride.com`
- **Password:** `demo123`

## 🏗️ Project Structure

```
AI_Travel_Chatbot/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, SearchHistory, Itinerary)
├── config.py              # Configuration and mood mappings
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── signup.html        # Registration page
│   ├── chatbot.html       # Main chatbot interface
│   ├── dashboard.html     # User dashboard
│   ├── itinerary.html     # Detailed itinerary view
│   ├── about.html         # About us page
│   └── team.html          # Team page
├── static/                # Static assets
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/            # Image assets
└── instance/              # Database and instance files
    └── database.db        # SQLite database (auto-created)
```

## 🎨 Key Pages

### 🏠 Landing Page (`/`)
- Hero section with India-themed background
- Feature showcase
- Popular destinations by mood
- Call-to-action sections

### 💬 Chatbot Interface (`/chatbot`)
- ChatGPT-style conversation UI
- Mood selector buttons
- Real-time destination suggestions
- Itinerary creation functionality

### 📊 Dashboard (`/dashboard`)
- User statistics and metrics
- Recent searches and itineraries
- Quick access to saved trips

### 🗺️ Itinerary View (`/itinerary/<id>`)
- Detailed day-by-day travel plans
- Budget breakdowns
- Local recommendations

## 🤖 AI Logic

The application uses a sophisticated mood detection system:

### Mood Categories
- **Calm:** Kerala backwaters, Coorg, Rishikesh
- **Excited:** Goa, Manali, Rann of Kutch
- **Romantic:** Udaipur, Ooty, Alleppey
- **Adventurous:** Leh-Ladakh, Spiti Valley, Rishikesh
- **Stressed:** Munnar, Dharamshala, Pushkar
- **Happy:** Mumbai, Jaipur, Hampi

### Recommendation Process
1. **Text Analysis:** Analyzes user input for mood keywords
2. **Mood Detection:** Determines primary emotional state
3. **Destination Matching:** Maps mood to suitable locations
4. **Personalization:** Considers user preferences and history
5. **Itinerary Generation:** Creates detailed travel plans

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///instance/database.db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
OPENAI_API_KEY=your-openai-api-key-if-needed
```

### Database Options

#### SQLite (Default)
- Perfect for development and small deployments
- No additional setup required
- Database file created automatically

#### MySQL
Uncomment MySQL settings in `config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'your_username'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'travel_chatbot'
```

#### Supabase (Cloud)
Configure Supabase settings for cloud deployment:
```python
SUPABASE_URL = 'https://your-project.supabase.co'
SUPABASE_KEY = 'your-supabase-anon-key'
```

## 📱 API Endpoints

### Public Routes
- `GET /` - Landing page
- `GET /about` - About page
- `GET /team` - Team page
- `GET /login` - Login page
- `POST /login` - User authentication
- `GET /signup` - Registration page
- `POST /signup` - User registration

### Protected Routes (Login Required)
- `GET /chatbot` - Main chatbot interface
- `GET /dashboard` - User dashboard
- `GET /itinerary/<id>` - View specific itinerary
- `POST /api/chat` - Chatbot conversation API
- `POST /api/create_itinerary` - Create new itinerary
- `GET /api/itineraries` - Get user itineraries
- `GET /api/search_history` - Get search history

## 🎨 Styling Features

- **CSS Variables:** Consistent color scheme and spacing
- **Responsive Design:** Works on all device sizes
- **Animations:** Smooth transitions and micro-interactions
- **Modern UI:** Glass morphism, gradients, and shadows
- **Typography:** Poppins font family for modern look

## 🔒 Security Features

- **Password Hashing:** Using Werkzeug security
- **Session Management:** Flask-Login integration
- **CSRF Protection:** Flask-WTF forms
- **Input Sanitization:** XSS prevention
- **Authentication:** Protected routes and user verification

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Visit: http://127.0.0.1:5000
```

### Production Deployment
1. **Set Environment Variables**
2. **Configure Production Database**
3. **Set DEBUG=False in config**
4. **Use WSGI Server (Gunicorn, uWSGI)**
5. **Configure Reverse Proxy (Nginx)**

### Platform Deployment
- **Heroku:** Add `Procfile` and `runtime.txt`
- **Vercel:** Configure `vercel.json`
- **Railway:** Direct deployment support
- **DigitalOcean App Platform:** Compatible

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Flask Community** - For the amazing web framework
- **Unsplash** - For beautiful travel photography
- **Font Awesome** - For comprehensive icon library
- **Google Fonts** - For the Poppins font family

## 📞 Support

For support and questions:
- Create an issue in the repository
- Email: support@paradiseride.com
- Website: [ParadiseRide](http://your-domain.com)

---

**Made with ❤️ for travel enthusiasts across India**

*ParadiseRide - Where emotions meet destinations!*