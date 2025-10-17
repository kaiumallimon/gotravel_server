# GoTravel AI Backend# GoTravel AI Backend - Complete Documentation# GoTravel AI Backend



🌍 **Intelligent Travel Booking Assistant powered by AI**



A conversational AI system for the travel industry using FastAPI, LangChain, Google Gemini, and Supabase.🌍 **Production-Grade AI Travel Booking Assistant**🌍 **Production-Grade AI Travel Booking Assistant**



---



## 🏗️ System ArchitectureAn intelligent backend system that powers a conversational AI travel assistant using FastAPI, LangChain, Google Gemini, and Supabase.An intelligent backend system that powers a conversational AI travel assistant using FastAPI, LangChain, Google Gemini, and Supabase.



```mermaid

graph TD

    A[User Request] --> B[FastAPI Server]---## 🚀 Features

    B --> C[Request Validation & CORS]

    C --> D[LangChain AI Agent]

    D --> E[Google Gemini 2.0 Flash]

    E --> F[Tool Selection]## Table of Contents- 🤖 **Intelligent Conversational AI** - Natural language processing using Google Gemini 2.0 Flash

    F --> G{Which Tool?}

    - 🏨 **Hotel Search & Booking** - Find and reserve accommodations

    G -->|Hotel Search| H1[search_hotels]

    G -->|Package Search| H2[search_packages]1. [Overview](#overview)- ✈️ **Travel Package Discovery** - Explore packages by destination, category, and price

    G -->|Place Search| H3[search_places]

    G -->|Weather| H4[get_weather]2. [Features](#features)- 🗺️ **Tourist Place Recommendations** - Discover attractions and destinations

    G -->|Booking| H5[create_booking]

    G -->|Favorites| H6[get_user_favorites]3. [Architecture](#architecture)- 🌤️ **Real-time Weather Information** - Get current weather for any location

    G -->|Price Sorting| H7[get_*_by_price]

    4. [Technology Stack](#technology-stack)- 📝 **Smart Booking System** - Create bookings through natural conversation

    H1 --> I[Supabase Database]

    H2 --> I5. [Project Structure](#project-structure)- 🔄 **Session Management** - Maintain conversation context across interactions

    H3 --> I

    H4 --> J[OpenWeatherMap API]6. [Setup & Installation](#setup--installation)- 🛠️ **Tool-Based Architecture** - Flexible LangChain tools for data fetching

    H5 --> I

    H6 --> I7. [Configuration](#configuration)

    H7 --> I

    8. [API Documentation](#api-documentation)## 🏗️ Architecture

    I --> K[Data Processing]

    J --> K9. [Usage Examples](#usage-examples)

    K --> L[LLM Response Formatting]

    L --> M[JSON Response]10. [Available Tools](#available-tools)```

    M --> N[User]

    11. [Database Schema](#database-schema)User Query → FastAPI → LangChain Agent → Tool Selection → Data Fetching → LLM Response Formatting → User

    style A fill:#e1f5ff

    style E fill:#fff3e012. [Deployment](#deployment)                         ↓

    style I fill:#f3e5f5

    style J fill:#e8f5e913. [Troubleshooting](#troubleshooting)                    Google Gemini 2.0 Flash

    style N fill:#e1f5ff

```14. [Quick Reference](#quick-reference)                         ↓



### Architecture Layers15. [Contributing](#contributing)                    Tools (LangChain)



**1. API Layer (FastAPI)**                    ├── search_hotels

- Handles HTTP requests/responses

- CORS middleware for cross-origin requests---                    ├── search_packages

- Request validation using Pydantic models

- Session management                    ├── search_places

- Error handling and logging

## Overview                    ├── get_weather

**2. AI Agent Layer (LangChain)**

- Conversation context management                    └── create_booking

- Intent classification

- Tool selection and orchestrationGoTravel AI Backend is a sophisticated conversational AI system designed specifically for the travel industry. It combines the power of Large Language Models with structured database queries to provide intelligent travel recommendations, hotel searches, package bookings, and weather information through natural language interactions.                         ↓

- Response generation using Google Gemini

- Multi-turn conversation support                    Supabase Database



**3. Tool Layer (LangChain Tools)**### Key Capabilities```

- Modular functions for specific tasks

- Database query execution

- External API integration

- Data formatting and validation- 🤖 Natural language understanding using Google Gemini 2.0 Flash## 📦 Technology Stack



**4. Data Layer (Supabase)**- 🏨 Intelligent hotel search with location filtering

- PostgreSQL database

- RESTful API auto-generated- ✈️ Travel package discovery by destination, category, and budget- **Framework**: FastAPI 0.109.0

- Real-time subscriptions

- Authentication ready- 🗺️ Tourist place recommendations with rich details- **AI/ML**: LangChain + Google Gemini 2.0 Flash



**5. External Services**- 🌤️ Real-time weather information integration- **Database**: Supabase (PostgreSQL)

- Google Gemini AI for natural language processing

- OpenWeatherMap for weather data- 📝 Conversational booking system- **External APIs**: OpenWeatherMap



---- 🔄 Session-based conversation memory- **Python**: 3.9+



## 🤖 What the Chatbot Can Do- 🛠️ Extensible tool-based architecture



### 🏨 Hotel Operations## 📁 Project Structure



- **Search hotels by location**---

  - Example: *"Show me hotels in Dhaka"*

  - Example: *"Find hotels in Cox's Bazar"*```



- **Sort hotels by price**## Featuresgotravel-server/

  - Example: *"Show me hotels in Dhaka sorted by price"*

  - Example: *"Cheapest to most expensive hotels in Sylhet"*├── main.py              # FastAPI application entry point



- **Get hotel room details**### Core Features├── config.py            # Configuration and environment variables

  - Example: *"What rooms are available at Radisson Blu?"*

  - Example: *"Show me room types and prices"*├── database.py          # Supabase client and database operations



### ✈️ Travel Package Operations- **Intelligent Conversational AI** - Natural language processing using Google Gemini 2.0 Flash├── agent.py             # LangChain AI agent implementation



- **Search packages by destination**- **Hotel Search & Booking** - Find and reserve accommodations by location and amenities├── tools.py             # LangChain tools for data fetching

  - Example: *"Show me packages to Sylhet"*

  - Example: *"Find travel packages in Bangladesh"*- **Travel Package Discovery** - Explore packages filtered by destination, category, price, and duration├── routes.py            # FastAPI route definitions



- **Search packages by category**- **Tourist Place Recommendations** - Discover attractions, landmarks, and destinations├── models.py            # Pydantic models for requests/responses

  - Example: *"Show me beach packages"*

  - Example: *"Find adventure tours"*- **Real-time Weather Information** - Get current weather conditions for any location├── utils.py             # Utility functions



- **Search packages by price**- **Smart Booking System** - Create bookings through natural conversation├── requirements.txt     # Python dependencies

  - Example: *"Packages under 10000 BDT"*

  - Example: *"Luxury packages between 15000 and 25000"*- **Session Management** - Maintain conversation context across multiple interactions├── .env.example         # Environment variables template



- **Search packages by duration**- **Tool-Based Architecture** - Flexible LangChain tools for modular data fetching├── .gitignore          # Git ignore rules

  - Example: *"Show me 3-day packages"*

  - Example: *"Weekend tour packages"*└── supabase/           # Database migrations



- **Get cheapest packages**### Advanced Features    └── migrations/

  - Example: *"What are the cheapest packages?"*

  - Example: *"Show me budget-friendly tours"*        ├── users.sql



- **Sort packages by price**- Context-aware conversations with memory        ├── hotels.sql

  - Example: *"Show all packages sorted by price"*

  - Example: *"List packages from cheapest to most expensive"*- Multi-tool orchestration for complex queries        ├── packages.sql



- **Get all packages in a country**- Structured output with JSON formatting        ├── places.sql

  - Example: *"Show me all tour packages in Bangladesh"*

  - Example: *"What travel packages do you have?"*- Error handling and graceful fallbacks        ├── bookings.sql



### 🗺️ Tourist Places Operations- Request logging and monitoring        └── ...



- **Search places by location**- CORS support for web applications```

  - Example: *"Tourist places in Bangladesh"*

  - Example: *"Show me places to visit in Dhaka"*- Interactive API documentation (Swagger/ReDoc)



- **Search places by category**## 🛠️ Setup & Installation

  - Example: *"Show me beaches in Bangladesh"*

  - Example: *"Historical places near Dhaka"*---



- **Search places near a city**### Prerequisites

  - Example: *"Places to visit near Dhaka"*

  - Example: *"Tourist spots around Sylhet"*## Architecture



- **Get popular places**- Python 3.9 or higher

  - Example: *"What are the most popular tourist destinations?"*

  - Example: *"Show me top attractions"*### System Architecture- Supabase account and project



### 🌤️ Weather Information- Google AI API key (for Gemini)



- **Get current weather**```- OpenWeatherMap API key (optional, for weather features)

  - Example: *"What's the weather in Dhaka?"*

  - Example: *"Current temperature in Cox's Bazar"*User Request → FastAPI → LangChain Agent → Tool Selection → Data Fetching → LLM Response Formatting → User

  - Example: *"Is it raining in Sylhet?"*

                         ↓### Installation Steps

### 📝 Booking Operations

                    Google Gemini 2.0 Flash

- **Create bookings**

  - Example: *"Book package ID abc123 for 2 people, John Doe, john@email.com, +8801712345678"*                         ↓1. **Clone the repository**

  - Example: *"Reserve this package for 4 guests"*

                    Tools (LangChain)   ```bash

### ⭐ User Favorites

                    ├── search_hotels   cd gotravel-server

- **View saved items**

  - Example: *"What are my favorites?"*                    ├── search_packages   ```

  - Example: *"Show my saved packages"*

  - Example: *"What hotels have I bookmarked?"*                    ├── search_places



### 💬 Conversational Features                    ├── get_weather2. **Create virtual environment**



- **Context-aware conversations**                    └── create_booking   ```bash

  - User: *"Show me hotels in Dhaka"*

  - Bot: *"I found 10 hotels..."*                         ↓   python -m venv venv

  - User: *"What about the prices?"* ← Remembers we're talking about Dhaka hotels

                      Supabase Database   

- **Multi-step queries**

  - Example: *"What's the weather in Cox's Bazar and show me hotels there"*```   # Windows

  - Example: *"Find beach packages under 15000 and check the weather"*

   .\venv\Scripts\activate

- **Follow-up questions**

  - User: *"Show me packages to Sylhet"*### Request Flow   

  - Bot: *"I found 5 packages..."*

  - User: *"Which one is cheapest?"* ← Understands context   # Linux/Mac



---**Simple Query:**   source venv/bin/activate



## 🛠️ Available Tools```   ```



### Hotel Tools1. User sends: "Show me hotels in Dhaka"



| Tool | Description |2. FastAPI receives POST /api/chat3. **Install dependencies**

|------|-------------|

| `search_hotels` | Search for hotels by city and country |3. Request validated via Pydantic models   ```bash

| `get_hotel_rooms` | Get available rooms for a specific hotel with pricing |

| `get_hotels_by_price` | Get hotels sorted by price (low to high or high to low) |4. Passed to TravelAgent.process_message()   pip install -r requirements.txt



### Package Tools5. LangChain agent analyzes query   ```



| Tool | Description |6. Agent selects search_hotels tool

|------|-------------|

| `search_packages` | Search packages by destination, category, price range, and duration |7. Tool calls database.search_hotels(city="Dhaka")4. **Configure environment variables**

| `get_cheapest_packages` | Get the 5 most affordable travel packages |

| `get_packages_by_price` | Get all packages sorted by price |8. Supabase returns hotel records   ```bash



### Place Tools9. Tool formats results as JSON   # Copy the example file



| Tool | Description |10. LLM generates natural language response   cp .env.example .env

|------|-------------|

| `search_places` | Search tourist places by location, category, or proximity |11. Response sent back through FastAPI   

| `get_popular_places` | Get the most popular tourist destinations |

12. User receives: "I found 10 hotels in Dhaka..."   # Edit .env with your actual credentials

### User Tools

```   ```

| Tool | Description |

|------|-------------|

| `get_user_favorites` | Retrieve user's saved hotels, packages, and places |

---5. **Configure your .env file**

### Utility Tools

   ```env

| Tool | Description |

|------|-------------|## Technology Stack   # Supabase Configuration

| `get_weather` | Get current weather information for any city |

| `create_booking` | Create bookings for packages or hotels |   SUPABASE_URL=https://your-project.supabase.co



---### Core Technologies   SUPABASE_KEY=your-supabase-anon-key



## 📊 Technology Stack   



- **Backend Framework**: FastAPI 0.115.0- **Framework**: FastAPI 0.115.0 (High-performance async web framework)   # Google AI Configuration

- **AI/LLM**: LangChain + Google Gemini 2.0 Flash

- **Database**: Supabase (PostgreSQL)- **AI/ML**: LangChain + Google Gemini 2.0 Flash   GOOGLE_API_KEY=your-google-gemini-api-key

- **Weather API**: OpenWeatherMap

- **Language**: Python 3.13- **Database**: Supabase (PostgreSQL with real-time features)   



---- **External APIs**: OpenWeatherMap (Weather data)   # OpenWeatherMap API (optional)



## 🚀 Quick Start- **Python**: 3.9+ with async/await support   OPENWEATHER_API_KEY=your-openweather-api-key



```bash   

# Install dependencies

pip install -r requirements.txt### Key Dependencies   # Server Configuration



# Configure environment variables   HOST=0.0.0.0

cp .env.example .env

# Edit .env with your API keys```   PORT=8000



# Seed database with sample datafastapi==0.115.0   DEBUG=True

python seed_data.py

uvicorn[standard]==0.32.0   

# Start server

python main.pylangchain>=0.3.13   # CORS Settings

```

langchain-google-genai>=2.0.5   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

**API Documentation**: http://localhost:8000/docs

google-generativeai==0.8.3   ```

---

supabase==2.10.0

## 📡 API Endpoints

pydantic==2.9.26. **Set up Supabase database**

| Endpoint | Method | Purpose |

|----------|--------|---------|```   - Run all SQL migrations in the `supabase/migrations/` directory

| `/api/chat` | POST | Main conversational interface |

| `/api/health` | GET | System health check |   - Ensure all tables are created properly

| `/api/booking` | POST | Direct booking creation |

| `/api/session/info` | POST | Get session information |---

| `/api/session/clear` | POST | Clear conversation history |

| `/docs` | GET | Interactive API documentation (Swagger) |7. **Run the server**

| `/redoc` | GET | Alternative API documentation (ReDoc) |

## Project Structure   ```bash

---

   python main.py

## 🔗 Example Chat Request

```   ```

```bash

curl -X POST "http://localhost:8000/api/chat" \gotravel-server/

  -H "Content-Type: application/json" \

  -d '{├── main.py              # FastAPI application entry point   Or using uvicorn directly:

    "message": "Show me hotels in Dhaka sorted by price",

    "session_id": "user123"├── config.py            # Configuration and environment variables   ```bash

  }'

```├── database.py          # Supabase client and database operations   uvicorn main:app --reload --host 0.0.0.0 --port 8000



**Response:**├── agent.py             # LangChain AI agent implementation   ```

```json

{├── tools.py             # LangChain tools for data fetching

  "success": true,

  "response": "I found 10 hotels in Dhaka sorted by price...",├── routes.py            # FastAPI route definitions## 📚 API Documentation

  "session_id": "user123",

  "tools_used": [├── models.py            # Pydantic models for requests/responses

    {

      "tool": "get_hotels_by_price",├── utils.py             # Utility functionsOnce the server is running, access the interactive API documentation:

      "input": {"city": "Dhaka", "sort_order": "low_to_high"}

    }├── test.py              # Test suite

  ],

  "message_count": 1,├── seed_data.py         # Database seeding script- **Swagger UI**: http://localhost:8000/docs

  "timestamp": "2025-10-18T10:30:00"

}├── requirements.txt     # Python dependencies- **ReDoc**: http://localhost:8000/redoc

```

├── .env.example         # Environment variables template- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

├── .gitignore          # Git ignore rules

## 📝 License

├── Dockerfile          # Docker configuration## 🔌 API Endpoints

MIT License

├── docker-compose.yml  # Docker Compose config

---

├── start.bat           # Windows startup script### Chat Endpoint

**Built with ❤️ using FastAPI, LangChain, Google Gemini, and Supabase**

├── start.sh            # Linux/Mac startup script```http

└── supabase/           # Database migrationsPOST /api/chat

    └── migrations/Content-Type: application/json

        ├── users.sql

        ├── hotels.sql{

        ├── packages.sql  "message": "Show me luxury hotels in Dhaka",

        └── ...  "session_id": "optional_session_id",

```  "user_id": "optional_user_id"

}

---```



## Setup & Installation**Response:**

```json

### Prerequisites{

  "success": true,

- [ ] Python 3.9 or higher  "response": "I found 5 luxury hotels in Dhaka...",

- [ ] Supabase account ([Create one here](https://supabase.com))  "session_id": "session_abc123",

- [ ] Google AI API key ([Get it here](https://makersuite.google.com/app/apikey))  "tools_used": [

- [ ] OpenWeatherMap API key (Optional - [Get it here](https://openweathermap.org/api))    {

      "tool": "search_hotels",

### Step 1: Prepare Supabase Database      "input": {"city": "Dhaka", "min_rating": 4.0}

    }

1. Create a Supabase project at [supabase.com](https://supabase.com)  ],

2. Run all migration files in the `supabase/migrations/` directory  "message_count": 2,

3. Copy your Project URL and anon key from Settings → API  "timestamp": "2025-10-18T10:30:00"

}

### Step 2: Install Dependencies```



**Windows:**### Health Check

```powershell```http

python -m venv venvGET /api/health

.\venv\Scripts\activate```

pip install -r requirements.txt

```### Session Management

```http

**Linux/Mac:**POST /api/session/info

```bashPOST /api/session/clear

python3 -m venv venv```

source venv/bin/activate

pip install -r requirements.txt### Direct Booking

``````http

POST /api/booking

### Step 3: Configure EnvironmentContent-Type: application/json



```bash{

# Copy example file  "booking_type": "package",

cp .env.example .env  "item_id": "package-uuid",

  "guest_name": "John Doe",

# Edit .env with your credentials  "guest_email": "john@example.com",

```  "guest_phone": "+8801712345678",

  "total_participants": 2

**.env file:**}

```env```

# Supabase Configuration

SUPABASE_URL=https://yourproject.supabase.co## 💬 Example Conversations

SUPABASE_KEY=your_supabase_anon_key

### Hotel Search

# Google AI Configuration```

GOOGLE_API_KEY=your_google_gemini_api_keyUser: "Show me hotels in Dhaka"

AI: I found 10 hotels in Dhaka. Here are the top options:

# OpenWeatherMap API (Optional)

OPENWEATHER_API_KEY=your_openweather_api_key1. **Radisson Blu**

   📍 Dhaka, Bangladesh

# Server Configuration   ⭐ Rating: 4.5/5.0

HOST=0.0.0.0

PORT=80002. **Pan Pacific Sonargaon**

DEBUG=True   📍 Dhaka, Bangladesh

   ⭐ Rating: 4.3/5.0

# CORS Settings...

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173```

```

### Package Discovery

### Step 4: Seed Database (Optional)```

User: "Find me luxury travel packages under 30000 BDT"

Add sample data for testing:AI: I found 5 luxury packages within your budget:

```bash

python seed_data.py1. **Cox's Bazar Beach Resort**

```   📍 Cox's Bazar

   ⏱️ 3 days

### Step 5: Start the Server   💰 ৳25,000

...

```bash```

# Option 1: Direct

python main.py### Weather Query

```

# Option 2: With reloadUser: "What's the weather in Dhaka?"

uvicorn main:app --reload --host 0.0.0.0 --port 8000AI: The current weather in Dhaka, Bangladesh:

🌤️ Temperature: 28°C (feels like 32°C)

# Option 3: Quick start script💧 Humidity: 75%

./start.sh  # Linux/Mac🌬️ Wind: 12 km/h

start.bat   # Windows☁️ Conditions: Partly cloudy

``````



### Step 6: Verify Installation### Booking

```

Visit these URLs:User: "Book the Cox's Bazar package for 2 people. My name is John Doe, email john@example.com, phone 01712345678"

- http://localhost:8000 - Root endpointAI: Perfect! I've created your booking:

- http://localhost:8000/docs - Interactive API docs

- http://localhost:8000/api/health - Health check✅ Booking Reference: BK12345678

📦 Package: Cox's Bazar Beach Resort

Test with curl:👥 Participants: 2

```bash💰 Total: ৳50,000

curl -X POST "http://localhost:8000/api/chat" \📧 Confirmation sent to: john@example.com

  -H "Content-Type: application/json" \```

  -d '{"message": "Hello!"}'

```## 🛠️ Available Tools



---The AI agent has access to these tools:



## Configuration1. **search_hotels** - Search hotels by location and rating

2. **get_hotel_rooms** - Get available rooms for a specific hotel

### Environment Variables3. **search_packages** - Search travel packages by various criteria

4. **get_cheapest_packages** - Find the most affordable packages

```env5. **search_places** - Discover tourist attractions and destinations

# Supabase6. **get_popular_places** - Get most popular tourist places

SUPABASE_URL=https://your-project.supabase.co7. **get_weather** - Fetch real-time weather information

SUPABASE_KEY=your-supabase-anon-key8. **create_booking** - Create bookings for packages or hotels



# Google AI## 🔧 Configuration

GOOGLE_API_KEY=your-google-gemini-api-key

### Model Configuration

# Weather (Optional)Edit `config.py` to change AI model settings:

OPENWEATHER_API_KEY=your-openweather-key```python

model_name: str = "gemini-2.0-flash"

# Servertemperature: float = 0.7

HOST=0.0.0.0max_tokens: int = 2048

PORT=8000```

DEBUG=True

### CORS Configuration

# AI ModelUpdate allowed origins in `.env`:

MODEL_NAME=gemini-2.0-flash```env

TEMPERATURE=0.7ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com

MAX_TOKENS=2048```



# CORS## 🧪 Testing

ALLOWED_ORIGINS=http://localhost:3000

```Test the agent directly:

```bash

---python agent.py

```

## API Documentation

Test individual tools:

### Interactive Docs```bash

python tools.py

- **Swagger UI**: http://localhost:8000/docs```

- **ReDoc**: http://localhost:8000/redoc

## 📊 Database Schema

### Main Endpoints

Key tables:

| Endpoint | Method | Purpose |- **users** - User accounts

|----------|--------|---------|- **hotels** - Hotel listings with location and ratings

| `/api/chat` | POST | Main conversational interface |- **rooms** - Hotel room types and availability

| `/api/health` | GET | System health check |- **packages** - Travel packages with pricing and itineraries

| `/api/session/info` | POST | Get session information |- **places** - Tourist destinations and attractions

| `/api/session/clear` | POST | Clear chat history |- **bookings** - Booking records

| `/api/booking` | POST | Direct booking creation |- **reviews** - User reviews and ratings



### Chat Endpoint## 🚀 Deployment



**Request:**### Using Docker (Recommended)

```json```dockerfile

{FROM python:3.9-slim

  "message": "Show me hotels in Dhaka",WORKDIR /app

  "session_id": "optional_session_id"COPY requirements.txt .

}RUN pip install -r requirements.txt

```COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

**Response:**```

```json

{### Using Cloud Platforms

  "success": true,- **Heroku**: Use `Procfile` with `web: uvicorn main:app --host=0.0.0.0 --port=${PORT}`

  "response": "I found 5 hotels in Dhaka...",- **Railway**: Automatic Python app detection

  "session_id": "session_abc123",- **AWS/GCP/Azure**: Deploy as container or using platform-specific Python runtime

  "tools_used": [

    {"tool": "search_hotels", "input": {"city": "Dhaka"}}## 🐛 Troubleshooting

  ],

  "message_count": 2,### Import Errors

  "timestamp": "2025-10-18T10:30:00"```bash

}# Reinstall dependencies

```pip install -r requirements.txt --force-reinstall

```

---

### Database Connection Issues

## Usage Examples- Verify SUPABASE_URL and SUPABASE_KEY in `.env`

- Check Supabase project status

### Basic Queries- Ensure database migrations are applied



```bash### AI Model Errors

# Hotel Search- Verify GOOGLE_API_KEY is valid

curl -X POST "http://localhost:8000/api/chat" \- Check API quota and rate limits

  -H "Content-Type: application/json" \- Ensure model name is correct: "gemini-2.0-flash"

  -d '{"message": "Show me hotels in Dhaka"}'

## 📝 License

# Package Search

curl -X POST "http://localhost:8000/api/chat" \MIT License - Feel free to use this project for your own purposes.

  -H "Content-Type: application/json" \

  -d '{"message": "Find beach packages under 10000 BDT"}'## 🤝 Contributing



# WeatherContributions are welcome! Please feel free to submit a Pull Request.

curl -X POST "http://localhost:8000/api/chat" \

  -H "Content-Type: application/json" \## 📧 Support

  -d '{"message": "What is the weather in Cox'\''s Bazar?"}'

```For issues and questions, please open an issue on the repository.



### Python Client---



```python**Built with ❤️ using FastAPI, LangChain, and Google Gemini**

import requests

class GoTravelClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def chat(self, message):
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"message": message, "session_id": self.session_id}
        )
        data = response.json()
        
        if not self.session_id:
            self.session_id = data.get("session_id")
        
        return data.get("response")

# Usage
client = GoTravelClient()
print(client.chat("Show me hotels in Dhaka"))
print(client.chat("What about the prices?"))  # Maintains context
```

### JavaScript Client

```javascript
class GoTravelClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.sessionId = null;
  }

  async chat(message) {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message,
        session_id: this.sessionId
      })
    });

    const data = await response.json();
    if (!this.sessionId) this.sessionId = data.session_id;
    return data.response;
  }
}

// Usage
const client = new GoTravelClient();
const response = await client.chat('Show me hotels in Dhaka');
console.log(response);
```

---

## Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `search_hotels` | Search for hotels | city, country |
| `get_hotel_rooms` | Get room info | hotel_id |
| `search_packages` | Search packages | destination, category, max_price, duration_days |
| `get_cheapest_packages` | Get budget packages | - |
| `get_packages_by_price` | Sort packages by price | sort_order |
| `search_places` | Search tourist places | country, city, category, near_city |
| `get_popular_places` | Get popular destinations | - |
| `get_weather` | Get weather info | city |
| `create_booking` | Create a booking | booking_type, item_id, guest_info |

### Sample Queries

**Hotels:**
- "Show me hotels in Dhaka"
- "Find hotels in Cox's Bazar"

**Packages:**
- "Show me travel packages to Sylhet"
- "Find adventure packages"
- "What are the cheapest packages?"
- "Sort packages by price"

**Places:**
- "Popular tourist places in Bangladesh"
- "Show me beaches"
- "Historical places in Dhaka"

**Weather:**
- "What's the weather in Dhaka?"

**Bookings:**
- "Book package for 2 people, John Doe, john@example.com, +8801712345678"

---

## Database Schema

### Key Tables

```
users           → User accounts
hotels          → Hotel listings
rooms           → Hotel room types
packages        → Travel packages
places          → Tourist destinations
bookings        → Booking records
reviews         → User reviews
conversations   → Chat history
search_history  → Search logs
```

---

## Deployment

### Using Docker

```bash
# Build
docker build -t gotravel-backend .

# Run
docker run -p 8000:8000 --env-file .env gotravel-backend

# Docker Compose
docker-compose up -d
```

### Cloud Platforms

**Heroku:**
```bash
echo "web: uvicorn main:app --host=0.0.0.0 --port=\${PORT}" > Procfile
heroku create your-app-name
git push heroku main
```

**Railway / Render:**
- Connect GitHub repository
- Set environment variables
- Automatic deployment

---

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r requirements.txt --force-reinstall
```

**Database Connection Failed:**
- Verify SUPABASE_URL and SUPABASE_KEY
- Check if migrations are applied
- Test in Supabase dashboard

**API Key Invalid:**
- Verify Google API key is correct
- Check for extra spaces in .env
- Generate new API key if needed

**Port in Use:**
```bash
# Windows
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**CORS Errors:**
```env
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Quick Reference

### Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env

# Run
python main.py

# Test
python test.py
```

### Essential Endpoints

```bash
POST /api/chat         # Main chat
GET /api/health        # Health check
GET /docs              # API documentation
```

### Add New Tool

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description"""
    result = database.query(param)
    return json.dumps({"success": True, "data": result})

# Add to tools list
tools = [..., my_tool]
```

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

MIT License - Feel free to use for your own purposes.

---

## Support

- Open an issue on GitHub
- Check documentation
- Review troubleshooting section

---

## Credits

Built with ❤️ using:
- FastAPI
- LangChain
- Google Gemini
- Supabase

---

**🌍 Happy Travels! ✈️**
