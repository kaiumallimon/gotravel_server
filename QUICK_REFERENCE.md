# 🎯 Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env      # Then edit .env

# Run
python main.py
# OR
uvicorn main:app --reload

# Test
python test.py
python config.py  # Validate config
```

## 🔑 Environment Variables

```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
GOOGLE_API_KEY=AIza...
OPENWEATHER_API_KEY=xxx  # Optional
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

## 📡 Essential Endpoints

```bash
# Chat
POST /api/chat
{
  "message": "Show me hotels in Dhaka",
  "session_id": "optional_session_id"
}

# Health Check
GET /api/health

# Clear Session
POST /api/session/clear
{"session_id": "session_123"}

# Documentation
GET /docs        # Swagger UI
GET /redoc       # ReDoc
```

## 🛠️ Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `search_hotels` | Find hotels | city, country, min_rating |
| `get_hotel_rooms` | Get room info | hotel_id |
| `search_packages` | Find packages | destination, category, max_price |
| `get_cheapest_packages` | Budget packages | - |
| `search_places` | Find places | country, city, category, near_city |
| `get_popular_places` | Popular places | - |
| `get_weather` | Weather info | city |
| `create_booking` | Book item | booking_type, item_id, guest_info |

## 💬 Sample Queries

```
"Show me hotels in Dhaka"
"Find luxury hotels in Cox's Bazar with rating above 4"
"What are the cheapest packages?"
"Show me 3-day packages to Sylhet"
"What's the weather in Dhaka?"
"Popular tourist places in Bangladesh"
"Places to visit near Dhaka"
"Book package XYZ for 2 people, John Doe, john@email.com, +8801712345678"
```

## 🗄️ Database Tables

```
users           → User accounts
hotels          → Hotel listings
rooms           → Hotel rooms
packages        → Travel packages
places          → Tourist destinations
bookings        → Booking records
reviews         → User reviews
conversations   → Chat history
search_history  → Search logs
user_favorites  → Saved items
```

## 🔧 Common Tasks

### Add a New Tool

```python
# In tools.py
@tool
def my_new_tool(param: str) -> str:
    """Tool description for the AI"""
    try:
        # Your logic here
        result = database.some_operation(param)
        return json.dumps({"success": True, "data": result})
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

# Add to tools list
tools = [..., my_new_tool]
```

### Modify System Prompt

```python
# In agent.py
SYSTEM_PROMPT = """
Your customized prompt here...
"""
```

### Add New Route

```python
# In routes.py
@router.post("/api/my-endpoint")
async def my_endpoint(request: MyRequest):
    # Your logic
    return {"result": "data"}
```

## 🐛 Troubleshooting

```bash
# Import errors
pip install -r requirements.txt --force-reinstall

# Database errors
python -c "from database import supabase_client; print(supabase_client.client)"

# Config errors
python config.py

# Port in use
# Windows: taskkill /PID <PID> /F
# Linux: lsof -ti:8000 | xargs kill -9

# Check logs
tail -f gotravel_backend.log
```

## 📊 Response Format

```json
{
  "success": true,
  "response": "AI response here...",
  "session_id": "abc123",
  "tools_used": [
    {
      "tool": "search_hotels",
      "input": {"city": "Dhaka"}
    }
  ],
  "message_count": 5,
  "timestamp": "2025-10-18T10:30:00"
}
```

## 🔒 Security Checklist

- [ ] Configure .env with real credentials
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Validate all inputs
- [ ] Configure proper CORS
- [ ] Use environment variables
- [ ] Enable request logging
- [ ] Set up monitoring

## 🚢 Docker Commands

```bash
# Build
docker build -t gotravel-backend .

# Run
docker run -p 8000:8000 --env-file .env gotravel-backend

# Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 📈 Monitoring

```python
# Check health
curl http://localhost:8000/api/health

# View logs
tail -f gotravel_backend.log

# Check sessions
# In Python console:
from agent import travel_agent
print(travel_agent.chat_histories.keys())
```

## 🎨 Customize AI Behavior

```python
# In config.py
temperature: float = 0.7  # 0.0-1.0 (higher = more creative)
max_tokens: int = 2048    # Max response length

# In agent.py
max_iterations=5          # Max tool calls per query
```

## 📚 Useful Links

- FastAPI Docs: https://fastapi.tiangolo.com/
- LangChain Docs: https://python.langchain.com/
- Gemini API: https://ai.google.dev/
- Supabase Docs: https://supabase.com/docs

## ⚡ Performance Tips

1. Use async/await for I/O operations
2. Add database indexes on common queries
3. Implement response caching
4. Use connection pooling
5. Optimize LLM token usage
6. Batch database queries when possible
7. Add request timeout limits
8. Use CDN for static assets

## 🎯 Best Practices

- ✅ Always validate user inputs
- ✅ Use type hints everywhere
- ✅ Handle errors gracefully
- ✅ Log important events
- ✅ Write descriptive docstrings
- ✅ Keep tools focused and simple
- ✅ Test each component independently
- ✅ Use environment variables
- ✅ Version your API
- ✅ Document your code

---

**Need help?** Check README.md, SETUP_GUIDE.md, or API_USAGE.md
