# GoTravel AI Backend

🌍 **Production-Grade AI Travel Booking Assistant**

An intelligent backend system that powers a conversational AI travel assistant using FastAPI, LangChain, Google Gemini, and Supabase.

## 🚀 Features

- 🤖 **Intelligent Conversational AI** - Natural language processing using Google Gemini 2.0 Flash
- 🏨 **Hotel Search & Booking** - Find and reserve accommodations
- ✈️ **Travel Package Discovery** - Explore packages by destination, category, and price
- 🗺️ **Tourist Place Recommendations** - Discover attractions and destinations
- 🌤️ **Real-time Weather Information** - Get current weather for any location
- 📝 **Smart Booking System** - Create bookings through natural conversation
- 🔄 **Session Management** - Maintain conversation context across interactions
- 🛠️ **Tool-Based Architecture** - Flexible LangChain tools for data fetching

## 🏗️ Architecture

```
User Query → FastAPI → LangChain Agent → Tool Selection → Data Fetching → LLM Response Formatting → User
                         ↓
                    Google Gemini 2.0 Flash
                         ↓
                    Tools (LangChain)
                    ├── search_hotels
                    ├── search_packages
                    ├── search_places
                    ├── get_weather
                    └── create_booking
                         ↓
                    Supabase Database
```

## 📦 Technology Stack

- **Framework**: FastAPI 0.109.0
- **AI/ML**: LangChain + Google Gemini 2.0 Flash
- **Database**: Supabase (PostgreSQL)
- **External APIs**: OpenWeatherMap
- **Python**: 3.9+

## 📁 Project Structure

```
gotravel-server/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and environment variables
├── database.py          # Supabase client and database operations
├── agent.py             # LangChain AI agent implementation
├── tools.py             # LangChain tools for data fetching
├── routes.py            # FastAPI route definitions
├── models.py            # Pydantic models for requests/responses
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── supabase/           # Database migrations
    └── migrations/
        ├── users.sql
        ├── hotels.sql
        ├── packages.sql
        ├── places.sql
        ├── bookings.sql
        └── ...
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.9 or higher
- Supabase account and project
- Google AI API key (for Gemini)
- OpenWeatherMap API key (optional, for weather features)

### Installation Steps

1. **Clone the repository**
   ```bash
   cd gotravel-server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual credentials
   ```

5. **Configure your .env file**
   ```env
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   
   # Google AI Configuration
   GOOGLE_API_KEY=your-google-gemini-api-key
   
   # OpenWeatherMap API (optional)
   OPENWEATHER_API_KEY=your-openweather-api-key
   
   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   
   # CORS Settings
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

6. **Set up Supabase database**
   - Run all SQL migrations in the `supabase/migrations/` directory
   - Ensure all tables are created properly

7. **Run the server**
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Chat Endpoint
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Show me luxury hotels in Dhaka",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "success": true,
  "response": "I found 5 luxury hotels in Dhaka...",
  "session_id": "session_abc123",
  "tools_used": [
    {
      "tool": "search_hotels",
      "input": {"city": "Dhaka", "min_rating": 4.0}
    }
  ],
  "message_count": 2,
  "timestamp": "2025-10-18T10:30:00"
}
```

### Health Check
```http
GET /api/health
```

### Session Management
```http
POST /api/session/info
POST /api/session/clear
```

### Direct Booking
```http
POST /api/booking
Content-Type: application/json

{
  "booking_type": "package",
  "item_id": "package-uuid",
  "guest_name": "John Doe",
  "guest_email": "john@example.com",
  "guest_phone": "+8801712345678",
  "total_participants": 2
}
```

## 💬 Example Conversations

### Hotel Search
```
User: "Show me hotels in Dhaka"
AI: I found 10 hotels in Dhaka. Here are the top options:

1. **Radisson Blu**
   📍 Dhaka, Bangladesh
   ⭐ Rating: 4.5/5.0

2. **Pan Pacific Sonargaon**
   📍 Dhaka, Bangladesh
   ⭐ Rating: 4.3/5.0
...
```

### Package Discovery
```
User: "Find me luxury travel packages under 30000 BDT"
AI: I found 5 luxury packages within your budget:

1. **Cox's Bazar Beach Resort**
   📍 Cox's Bazar
   ⏱️ 3 days
   💰 ৳25,000
...
```

### Weather Query
```
User: "What's the weather in Dhaka?"
AI: The current weather in Dhaka, Bangladesh:
🌤️ Temperature: 28°C (feels like 32°C)
💧 Humidity: 75%
🌬️ Wind: 12 km/h
☁️ Conditions: Partly cloudy
```

### Booking
```
User: "Book the Cox's Bazar package for 2 people. My name is John Doe, email john@example.com, phone 01712345678"
AI: Perfect! I've created your booking:

✅ Booking Reference: BK12345678
📦 Package: Cox's Bazar Beach Resort
👥 Participants: 2
💰 Total: ৳50,000
📧 Confirmation sent to: john@example.com
```

## 🛠️ Available Tools

The AI agent has access to these tools:

1. **search_hotels** - Search hotels by location and rating
2. **get_hotel_rooms** - Get available rooms for a specific hotel
3. **search_packages** - Search travel packages by various criteria
4. **get_cheapest_packages** - Find the most affordable packages
5. **search_places** - Discover tourist attractions and destinations
6. **get_popular_places** - Get most popular tourist places
7. **get_weather** - Fetch real-time weather information
8. **create_booking** - Create bookings for packages or hotels

## 🔧 Configuration

### Model Configuration
Edit `config.py` to change AI model settings:
```python
model_name: str = "gemini-2.0-flash"
temperature: float = 0.7
max_tokens: int = 2048
```

### CORS Configuration
Update allowed origins in `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com
```

## 🧪 Testing

Test the agent directly:
```bash
python agent.py
```

Test individual tools:
```bash
python tools.py
```

## 📊 Database Schema

Key tables:
- **users** - User accounts
- **hotels** - Hotel listings with location and ratings
- **rooms** - Hotel room types and availability
- **packages** - Travel packages with pricing and itineraries
- **places** - Tourist destinations and attractions
- **bookings** - Booking records
- **reviews** - User reviews and ratings

## 🚀 Deployment

### Using Docker (Recommended)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Cloud Platforms
- **Heroku**: Use `Procfile` with `web: uvicorn main:app --host=0.0.0.0 --port=${PORT}`
- **Railway**: Automatic Python app detection
- **AWS/GCP/Azure**: Deploy as container or using platform-specific Python runtime

## 🐛 Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Connection Issues
- Verify SUPABASE_URL and SUPABASE_KEY in `.env`
- Check Supabase project status
- Ensure database migrations are applied

### AI Model Errors
- Verify GOOGLE_API_KEY is valid
- Check API quota and rate limits
- Ensure model name is correct: "gemini-2.0-flash"

## 📝 License

MIT License - Feel free to use this project for your own purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ using FastAPI, LangChain, and Google Gemini**
