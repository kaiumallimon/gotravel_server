# 🚀 Complete Setup Guide

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.9 or higher installed
- [ ] Git installed (optional, for version control)
- [ ] Supabase account ([Create one here](https://supabase.com))
- [ ] Google AI Studio account ([Get API key here](https://makersuite.google.com/app/apikey))
- [ ] OpenWeatherMap account ([Get API key here](https://openweathermap.org/api)) - Optional

## Step-by-Step Setup

### 1. Prepare Your Supabase Database

#### A. Create a Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Fill in project details
4. Wait for the project to be created

#### B. Run Database Migrations
1. In Supabase dashboard, go to **SQL Editor**
2. Run each migration file in this order:
   ```
   - users.sql
   - hotels.sql
   - rooms.sql
   - places.sql
   - packages.sql
   - packages_dates.sql
   - packages_activities.sql
   - bookings.sql
   - payments.sql
   - reviews.sql
   - recommendations.sql
   - conversations.sql
   - search_history.sql
   - user_favorites.sql
   - 007_add_place_to_packages.sql
   ```

#### C. Get Your Supabase Credentials
1. Go to **Project Settings** → **API**
2. Copy:
   - **Project URL** (starts with https://xxx.supabase.co)
   - **anon/public key** (long string starting with eyJ...)

### 2. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Choose "Create API key in new project" or use existing
4. Copy the generated API key

### 3. Get OpenWeatherMap API Key (Optional)

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to **API Keys** section
4. Copy your API key

### 4. Install Python and Dependencies

#### Windows:

```powershell
# Check Python version
python --version

# If Python is not installed, download from python.org

# Navigate to project directory
cd C:\Users\YourUsername\Desktop\gotravel-server

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux/Mac:

```bash
# Check Python version
python3 --version

# Navigate to project directory
cd ~/Desktop/gotravel-server

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Configure Environment Variables

1. **Copy the example file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. **Edit .env file with your credentials:**
   ```env
   # Supabase Configuration
   SUPABASE_URL=https://yourproject.supabase.co
   SUPABASE_KEY=your_supabase_anon_key_here
   
   # Google AI Configuration
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   
   # OpenWeatherMap API (Optional)
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   
   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   
   # CORS Settings (adjust for your frontend)
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

### 6. Test the Configuration

```bash
# Test configuration validation
python config.py
```

You should see:
```
✅ Configuration validated successfully!
Supabase URL: https://xxx.supabase.co
Model: gemini-2.0-flash
```

### 7. Test Database Connection

```bash
# Run test script
python test.py
```

This will:
- Validate configuration
- Test database connectivity
- Test AI agent functionality
- Run sample queries

### 8. Start the Server

#### Option 1: Using Python directly
```bash
python main.py
```

#### Option 2: Using uvicorn with reload
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 3: Using quick start scripts
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### 9. Verify Installation

1. **Open your browser** and visit:
   - http://localhost:8000 - Root endpoint
   - http://localhost:8000/docs - Interactive API docs
   - http://localhost:8000/api/health - Health check

2. **Test the API** using curl:
   ```bash
   curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello! What can you help me with?"}'
   ```

### 10. Test Chat Functionality

Use the Swagger UI at http://localhost:8000/docs:

1. Click on **POST /api/chat**
2. Click "Try it out"
3. Enter a test message:
   ```json
   {
     "message": "Show me hotels in Dhaka",
     "session_id": "test123"
   }
   ```
4. Click "Execute"
5. Check the response

## Common Setup Issues

### Issue 1: Import Errors
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue 2: Database Connection Failed
**Error:** `Database health check failed`

**Solution:**
- Verify SUPABASE_URL and SUPABASE_KEY in .env
- Check if all migrations are applied
- Test connection in Supabase dashboard
- Ensure your IP is not blocked

### Issue 3: Google API Key Invalid
**Error:** `Invalid API key`

**Solution:**
- Verify the API key is correct
- Check if Gemini API is enabled in your Google Cloud project
- Ensure there are no extra spaces in the .env file
- Try generating a new API key

### Issue 4: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

### Issue 5: CORS Errors
**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:**
- Add your frontend URL to ALLOWED_ORIGINS in .env:
  ```env
  ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,https://yourdomain.com
  ```
- Restart the server

## Production Deployment

### Using Docker

1. **Build the image:**
   ```bash
   docker build -t gotravel-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name gotravel-backend \
     -p 8000:8000 \
     --env-file .env \
     gotravel-backend
   ```

3. **Using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

### Environment-Specific Configurations

**Production .env:**
```env
DEBUG=False
HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Development .env:**
```env
DEBUG=True
HOST=127.0.0.1
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Next Steps

After successful setup:

1. ✅ Read the [API_USAGE.md](API_USAGE.md) for detailed API documentation
2. ✅ Explore the interactive docs at `/docs`
3. ✅ Test different queries with the chat endpoint
4. ✅ Integrate with your frontend application
5. ✅ Add sample data to your database for testing
6. ✅ Configure authentication for production use
7. ✅ Set up monitoring and logging
8. ✅ Implement rate limiting for production

## Sample Data

To add sample data to your database:

```sql
-- Sample Hotel
INSERT INTO hotels (name, city, country, rating, description)
VALUES (
  'Grand Hotel Dhaka',
  'Dhaka',
  'Bangladesh',
  4.5,
  'Luxury hotel in the heart of Dhaka with modern amenities'
);

-- Sample Package
INSERT INTO packages (
  name, destination, country, category,
  duration_days, price, currency,
  max_participants, available_slots,
  description, contact_email, contact_phone,
  cover_image
)
VALUES (
  'Cox''s Bazar Beach Resort',
  'Cox''s Bazar',
  'Bangladesh',
  'beach',
  3,
  25000,
  'BDT',
  50,
  20,
  '3-day beach resort package with meals and activities',
  'info@gotravel.com',
  '+8801712345678',
  'https://example.com/image.jpg'
);

-- Sample Place
INSERT INTO places (name, country, city, category, description, cover_image)
VALUES (
  'Sundarbans',
  'Bangladesh',
  'Khulna',
  'nature',
  'World''s largest mangrove forest and UNESCO World Heritage Site',
  'https://example.com/sundarbans.jpg'
);
```

## Support

For issues and questions:
- Check the README.md
- Review API_USAGE.md
- Test with the test.py script
- Check the logs in gotravel_backend.log

## Success Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] .env file configured with valid keys
- [ ] Database migrations applied
- [ ] Configuration validated (python config.py)
- [ ] Database connection tested
- [ ] Server starts without errors
- [ ] Health check returns "healthy"
- [ ] Chat endpoint responds correctly
- [ ] Sample queries work as expected

🎉 **Congratulations!** Your GoTravel AI Backend is now ready to use!
