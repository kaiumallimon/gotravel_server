# API Usage Guide

## Quick Start Examples

### 1. Basic Chat Interaction

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me hotels in Dhaka",
    "session_id": "user123_session"
  }'
```

**Response:**
```json
{
  "success": true,
  "response": "I found 10 hotels in Dhaka. Here are the top options:\n\n1. **Radisson Blu Dhaka**\n   📍 Dhaka, Bangladesh\n   ⭐ Rating: 4.5/5.0\n\n2. **Pan Pacific Sonargaon**\n   📍 Dhaka, Bangladesh\n   ⭐ Rating: 4.3/5.0\n\nWould you like more details about any specific hotel?",
  "session_id": "user123_session",
  "tools_used": [
    {
      "tool": "search_hotels",
      "input": {
        "city": "Dhaka"
      }
    }
  ],
  "message_count": 1,
  "timestamp": "2025-10-18T10:30:00"
}
```

### 2. Package Search

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find me luxury travel packages to Sylhet under 25000 BDT",
    "session_id": "user123_session"
  }'
```

### 3. Weather Information

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the weather in Cox'\''s Bazar?",
    "session_id": "user123_session"
  }'
```

### 4. Tourist Places

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me popular tourist places near Dhaka",
    "session_id": "user123_session"
  }'
```

### 5. Create Booking via Chat

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Book package ID abc-123 for 2 people. Name: John Doe, Email: john@example.com, Phone: +8801712345678",
    "session_id": "user123_session"
  }'
```

### 6. Direct Booking API

**Request:**
```bash
curl -X POST "http://localhost:8000/api/booking" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_type": "package",
    "item_id": "550e8400-e29b-41d4-a716-446655440000",
    "guest_name": "John Doe",
    "guest_email": "john@example.com",
    "guest_phone": "+8801712345678",
    "total_participants": 2,
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Booking created successfully",
  "booking_reference": "BK12345678",
  "booking_type": "package",
  "total_amount": 50000.0,
  "currency": "BDT"
}
```

### 7. Health Check

**Request:**
```bash
curl -X GET "http://localhost:8000/api/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-18T10:30:00",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "ai_model": "ready",
    "weather_api": "configured"
  }
}
```

### 8. Session Management

**Get Session Info:**
```bash
curl -X POST "http://localhost:8000/api/session/info" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123_session"
  }'
```

**Clear Session:**
```bash
curl -X POST "http://localhost:8000/api/session/clear" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123_session"
  }'
```

## Python Client Example

```python
import requests
import json

class GoTravelClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def chat(self, message):
        """Send a message to the AI assistant"""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "message": message,
                "session_id": self.session_id
            }
        )
        data = response.json()
        
        # Save session ID for continuity
        if not self.session_id:
            self.session_id = data.get("session_id")
        
        return data.get("response")
    
    def create_booking(self, booking_type, item_id, guest_info):
        """Create a booking"""
        response = requests.post(
            f"{self.base_url}/api/booking",
            json={
                "booking_type": booking_type,
                "item_id": item_id,
                **guest_info
            }
        )
        return response.json()

# Usage
client = GoTravelClient()

# Chat
response = client.chat("Show me hotels in Dhaka")
print(response)

# Follow-up (uses same session)
response = client.chat("What about the prices?")
print(response)

# Create booking
booking = client.create_booking(
    booking_type="package",
    item_id="package-uuid",
    guest_info={
        "guest_name": "John Doe",
        "guest_email": "john@example.com",
        "guest_phone": "+8801712345678",
        "total_participants": 2
    }
)
print(booking)
```

## JavaScript/TypeScript Client Example

```typescript
class GoTravelClient {
  private baseUrl: string;
  private sessionId: string | null;

  constructor(baseUrl: string = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.sessionId = null;
  }

  async chat(message: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: this.sessionId,
      }),
    });

    const data = await response.json();
    
    // Save session ID
    if (!this.sessionId) {
      this.sessionId = data.session_id;
    }

    return data.response;
  }

  async createBooking(bookingData: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/booking`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });

    return response.json();
  }
}

// Usage
const client = new GoTravelClient();

// Chat
const response = await client.chat('Show me hotels in Dhaka');
console.log(response);

// Create booking
const booking = await client.createBooking({
  booking_type: 'package',
  item_id: 'package-uuid',
  guest_name: 'John Doe',
  guest_email: 'john@example.com',
  guest_phone: '+8801712345678',
  total_participants: 2,
});
console.log(booking);
```

## React Hook Example

```typescript
import { useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function useGoTravelChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message: string) => {
    setLoading(true);
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
        }),
      });

      const data = await response.json();
      
      if (!sessionId) {
        setSessionId(data.session_id);
      }

      // Add assistant message
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: data.response },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        { role: 'assistant', content: 'Sorry, an error occurred.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading };
}
```

## Common Query Examples

### Hotels
- "Show me hotels in Dhaka"
- "Find luxury hotels in Cox's Bazar with rating above 4"
- "What are the cheapest hotels in Chittagong?"
- "Hotels near the airport in Dhaka"

### Packages
- "Show me travel packages to Sylhet"
- "Find adventure packages in Bangladesh"
- "What are the cheapest packages in December?"
- "3-day packages to Cox's Bazar"

### Places
- "Popular tourist places in Bangladesh"
- "Show me beaches near Dhaka"
- "Historical places in Dhaka"
- "Places to visit near Sylhet"

### Weather
- "What's the weather in Dhaka?"
- "Current temperature in Cox's Bazar"
- "Weather forecast for Sylhet"

### Bookings
- "Book package [ID] for 2 people, name John Doe, email john@example.com, phone +8801712345678"
- "Reserve this hotel for 3 nights"

## Error Handling

The API uses standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid input)
- **404**: Not Found (resource doesn't exist)
- **422**: Validation Error (incorrect data format)
- **500**: Internal Server Error

Example error response:
```json
{
  "success": false,
  "error": "Validation error",
  "detail": [
    {
      "loc": ["body", "guest_email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing rate limiting using middleware.

## Authentication

The current version doesn't require authentication. For production, implement JWT-based authentication:

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.post("/chat")
async def chat(request: ChatRequest, token: str = Depends(security)):
    # Verify token
    # ...
```
