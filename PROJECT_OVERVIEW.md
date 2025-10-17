# 🌍 GoTravel AI Backend - Project Overview

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Request                            │
│                 "Show me hotels in Dhaka"                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Server                             │
│                    (main.py, routes.py)                         │
│  • CORS middleware                                              │
│  • Request validation                                           │
│  • Error handling                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangChain AI Agent                           │
│                       (agent.py)                                │
│  • Google Gemini 2.0 Flash                                      │
│  • Conversation history management                              │
│  • Tool calling & orchestration                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Tool Selection                             │
│                       (tools.py)                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ search_hotels│  │search_packages│  │search_places │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ get_weather  │  │create_booking│  │get_hotel_rooms│         │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Layer                                    │
│              (database.py, Supabase)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Hotels  │  │ Packages │  │  Places  │  │ Bookings │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 External APIs                                   │
│  • OpenWeatherMap (weather data)                                │
│  • Google Gemini (AI responses)                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🗂️ Project Structure

```
gotravel-server/
│
├── 📄 main.py                  # FastAPI application entry point
│   ├── App initialization with lifespan
│   ├── CORS middleware
│   ├── Global error handlers
│   ├── Request logging
│   └── Route registration
│
├── 📄 config.py                # Configuration management
│   ├── Environment variables loading
│   ├── Settings validation
│   └── Pydantic Settings model
│
├── 📄 database.py              # Supabase database client
│   ├── SupabaseClient class
│   ├── Hotel operations (search, get by ID, rooms)
│   ├── Package operations (search, cheapest, by ID)
│   ├── Place operations (search, popular, by ID)
│   └── Booking operations (create, get, list)
│
├── 📄 agent.py                 # LangChain AI agent
│   ├── TravelAgent class
│   ├── Google Gemini integration
│   ├── Tool calling agent setup
│   ├── Conversation history management
│   └── Message processing logic
│
├── 📄 tools.py                 # LangChain tools
│   ├── @tool search_hotels
│   ├── @tool get_hotel_rooms
│   ├── @tool search_packages
│   ├── @tool get_cheapest_packages
│   ├── @tool search_places
│   ├── @tool get_popular_places
│   ├── @tool get_weather
│   └── @tool create_booking
│
├── 📄 routes.py                # FastAPI route handlers
│   ├── POST /api/chat - Main chat endpoint
│   ├── GET /api/health - Health check
│   ├── POST /api/session/info - Session info
│   ├── POST /api/session/clear - Clear history
│   ├── POST /api/booking - Direct booking
│   └── GET /api/ - Root info
│
├── 📄 models.py                # Pydantic models
│   ├── ChatRequest/Response
│   ├── SessionInfo/Clear models
│   ├── BookingRequest/Response
│   ├── HealthCheckResponse
│   └── Error response models
│
├── 📄 utils.py                 # Utility functions
│   ├── Date parsing & formatting
│   ├── Price formatting
│   ├── Location extraction
│   ├── Validation functions
│   └── Intent classification
│
├── 📄 test.py                  # Test suite
│   ├── Configuration tests
│   ├── Database connectivity tests
│   ├── Agent functionality tests
│   └── Sample query tests
│
├── 📄 requirements.txt         # Python dependencies
│   ├── FastAPI & Uvicorn
│   ├── LangChain & Google GenAI
│   ├── Supabase client
│   └── Other utilities
│
├── 📄 .env.example             # Environment template
├── 📄 .gitignore               # Git ignore rules
│
├── 📄 Dockerfile               # Docker configuration
├── 📄 docker-compose.yml       # Docker Compose config
│
├── 📄 start.bat                # Windows startup script
├── 📄 start.sh                 # Linux/Mac startup script
│
├── 📄 README.md                # Main documentation
├── 📄 SETUP_GUIDE.md           # Detailed setup guide
├── 📄 API_USAGE.md             # API usage examples
│
└── 📁 supabase/                # Database migrations
    └── migrations/
        ├── users.sql
        ├── hotels.sql
        ├── rooms.sql
        ├── packages.sql
        ├── places.sql
        ├── bookings.sql
        └── ...
```

## 🎯 Key Features

### 1. **Intelligent Query Processing**
```python
User: "Show me luxury hotels in Dhaka"
↓
Agent classifies intent → "hotel_search"
↓
Calls search_hotels tool with parameters
↓
Fetches data from Supabase
↓
LLM formats response naturally
↓
Returns: "I found 5 luxury hotels in Dhaka..."
```

### 2. **Context-Aware Conversations**
```python
User: "Show me hotels in Dhaka"
Assistant: "I found 10 hotels..."

User: "What about the prices?"  # No need to repeat "Dhaka"
Assistant: "The prices range from..."  # Remembers context
```

### 3. **Multi-Tool Orchestration**
```python
User: "What's the weather in Cox's Bazar and show me hotels there"
↓
Agent calls:
  1. get_weather("Cox's Bazar")
  2. search_hotels(city="Cox's Bazar")
↓
Combines results in single response
```

### 4. **Flexible Data Fetching**
```python
# Hotels by location
search_hotels(city="Dhaka")

# Hotels by rating
search_hotels(min_rating=4.0)

# Packages by budget
search_packages(max_price=25000)

# Packages by category
search_packages(category="luxury")

# Places near location
search_places(near_city="Dhaka")
```

## 🔄 Request Flow Examples

### Example 1: Simple Hotel Search

```
1. User sends: "Show me hotels in Dhaka"
2. FastAPI receives POST /api/chat
3. Request validated via Pydantic models
4. Passed to TravelAgent.process_message()
5. LangChain agent analyzes query
6. Agent selects search_hotels tool
7. Tool calls database.search_hotels(city="Dhaka")
8. Supabase returns hotel records
9. Tool formats results as JSON
10. LLM generates natural language response
11. Response sent back through FastAPI
12. User receives: "I found 10 hotels in Dhaka..."
```

### Example 2: Complex Multi-Step Query

```
1. User: "What's the weather in Cox's Bazar? Also show me packages there"
2. Agent analyzes: Need 2 tools
3. Calls get_weather("Cox's Bazar")
4. Calls search_packages(destination="Cox's Bazar")
5. Both results passed to LLM
6. LLM combines: "The weather is 28°C and sunny. I found 5 packages..."
```

### Example 3: Booking Creation

```
1. User: "Book package ABC for 2 people, John Doe, john@email.com"
2. Agent extracts:
   - Package ID: ABC
   - Participants: 2
   - Name: John Doe
   - Email: john@email.com
3. Calls create_booking tool
4. Tool validates and creates booking in database
5. Returns booking reference
6. LLM formats: "✅ Booking confirmed! Reference: BK12345678"
```

## 🚦 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Main conversational interface |
| `/api/health` | GET | System health check |
| `/api/session/info` | POST | Get session information |
| `/api/session/clear` | POST | Clear chat history |
| `/api/booking` | POST | Direct booking creation |
| `/api/` | GET | API information |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |

## 🛠️ Technology Choices

### Why FastAPI?
- ⚡ High performance (async support)
- 📝 Automatic API documentation
- ✅ Built-in validation with Pydantic
- 🔧 Easy to develop and maintain

### Why LangChain?
- 🤖 Powerful agent framework
- 🔌 Easy tool integration
- 💬 Conversation memory management
- 🔄 Flexible orchestration

### Why Google Gemini?
- 🚀 Fast response times
- 💡 Strong reasoning capabilities
- 🛠️ Native tool calling support
- 💰 Cost-effective

### Why Supabase?
- 🗄️ PostgreSQL with real-time features
- 🔐 Built-in authentication
- 🌐 RESTful API auto-generated
- 🆓 Generous free tier

## 🔐 Security Considerations

1. **Environment Variables**: All sensitive data in .env
2. **Input Validation**: Pydantic models validate all inputs
3. **Error Handling**: Generic error messages in production
4. **CORS**: Configurable allowed origins
5. **Rate Limiting**: Should be implemented for production
6. **Authentication**: Should be added for production use

## 📈 Performance Optimization

1. **Async Operations**: FastAPI + async/await for concurrency
2. **Database Indexing**: Indexes on frequently queried columns
3. **Connection Pooling**: Supabase client handles this
4. **Response Caching**: Can be added with Redis
5. **Request Batching**: Tools can fetch multiple items

## 🧪 Testing Strategy

```bash
# Unit tests for individual functions
pytest tests/test_database.py

# Integration tests for API endpoints
pytest tests/test_routes.py

# Agent behavior tests
pytest tests/test_agent.py

# Full system test
python test.py
```

## 📦 Deployment Options

1. **Local Development**: `python main.py`
2. **Docker**: `docker-compose up`
3. **Cloud Platforms**:
   - Heroku
   - Railway
   - AWS ECS/Fargate
   - Google Cloud Run
   - Azure App Service

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Supabase Documentation](https://supabase.com/docs)

## 🚀 Future Enhancements

- [ ] Add user authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add caching layer (Redis)
- [ ] Implement webhooks for bookings
- [ ] Add email notifications
- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Advanced analytics dashboard
- [ ] Payment gateway integration
- [ ] Real-time chat with WebSockets

---

**Built with ❤️ for the travel industry**
