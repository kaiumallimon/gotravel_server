"""
Pydantic Models for FastAPI
Request and Response models for API endpoints
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== CHAT MODELS ====================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="Optional user ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me luxury hotels in Dhaka",
                "session_id": "user123_session",
                "user_id": "user123"
            }
        }


class ToolUsed(BaseModel):
    """Information about a tool that was used"""
    tool: str = Field(..., description="Name of the tool")
    input: Dict[str, Any] = Field(..., description="Input parameters to the tool")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    success: bool = Field(..., description="Whether the request was successful")
    response: str = Field(..., description="AI assistant's response")
    session_id: str = Field(..., description="Session ID")
    tools_used: List[ToolUsed] = Field(default_factory=list, description="Tools used to generate response")
    message_count: int = Field(0, description="Number of messages in conversation")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "I found 5 luxury hotels in Dhaka. Here are the top options...",
                "session_id": "user123_session",
                "tools_used": [{"tool": "search_hotels", "input": {"city": "Dhaka", "min_rating": 4.0}}],
                "message_count": 2,
                "timestamp": "2025-10-18T10:30:00"
            }
        }


class ChatErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    session_id: Optional[str] = Field(None, description="Session ID if available")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# ==================== SESSION MODELS ====================

class SessionInfoRequest(BaseModel):
    """Request model for session info"""
    session_id: str = Field(..., description="Session ID to query")


class SessionInfoResponse(BaseModel):
    """Response model for session info"""
    exists: bool = Field(..., description="Whether the session exists")
    session_id: str = Field(..., description="Session ID")
    message_count: int = Field(0, description="Number of messages in session")


class ClearHistoryRequest(BaseModel):
    """Request model for clearing chat history"""
    session_id: str = Field(..., description="Session ID to clear")


class ClearHistoryResponse(BaseModel):
    """Response model for clearing chat history"""
    success: bool = Field(..., description="Whether the history was cleared")
    session_id: str = Field(..., description="Session ID that was cleared")
    message: str = Field(..., description="Confirmation message")


# ==================== HEALTH CHECK MODELS ====================

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field("healthy", description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    version: str = Field("1.0.0", description="API version")
    services: Dict[str, str] = Field(default_factory=dict, description="Status of dependent services")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-10-18T10:30:00",
                "version": "1.0.0",
                "services": {
                    "database": "connected",
                    "ai_model": "ready",
                    "weather_api": "available"
                }
            }
        }


# ==================== BOOKING MODELS ====================

class CreateBookingRequest(BaseModel):
    """Request model for creating a booking through API"""
    booking_type: str = Field(..., description="Type: 'package' or 'hotel'")
    item_id: str = Field(..., description="ID of package or hotel")
    guest_name: str = Field(..., min_length=2, max_length=255, description="Guest name")
    guest_email: EmailStr = Field(..., description="Guest email")
    guest_phone: str = Field(..., min_length=10, max_length=20, description="Guest phone")
    total_participants: int = Field(1, ge=1, le=50, description="Number of participants")
    user_id: Optional[str] = Field(None, description="User ID if authenticated")
    
    class Config:
        json_schema_extra = {
            "example": {
                "booking_type": "package",
                "item_id": "550e8400-e29b-41d4-a716-446655440000",
                "guest_name": "John Doe",
                "guest_email": "john@example.com",
                "guest_phone": "+8801712345678",
                "total_participants": 2,
                "user_id": "user123"
            }
        }


class BookingResponse(BaseModel):
    """Response model for booking creation"""
    success: bool = Field(..., description="Whether booking was successful")
    message: str = Field(..., description="Status message")
    booking_reference: Optional[str] = Field(None, description="Booking reference number")
    booking_type: Optional[str] = Field(None, description="Type of booking")
    total_amount: Optional[float] = Field(None, description="Total booking amount")
    currency: Optional[str] = Field(None, description="Currency code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Booking created successfully",
                "booking_reference": "BK12345678",
                "booking_type": "package",
                "total_amount": 25000.0,
                "currency": "BDT"
            }
        }


# ==================== SEARCH MODELS ====================

class HotelSearchRequest(BaseModel):
    """Request model for hotel search"""
    city: Optional[str] = Field(None, description="City to search in")
    country: Optional[str] = Field(None, description="Country to search in")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    limit: int = Field(10, ge=1, le=50, description="Maximum results")


class PackageSearchRequest(BaseModel):
    """Request model for package search"""
    destination: Optional[str] = Field(None, description="Destination")
    country: Optional[str] = Field(None, description="Country")
    category: Optional[str] = Field(None, description="Category")
    max_price: Optional[float] = Field(None, gt=0, description="Maximum price")
    duration_days: Optional[int] = Field(None, gt=0, description="Duration in days")
    limit: int = Field(10, ge=1, le=50, description="Maximum results")


class PlaceSearchRequest(BaseModel):
    """Request model for place search"""
    country: Optional[str] = Field(None, description="Country")
    city: Optional[str] = Field(None, description="City")
    category: Optional[str] = Field(None, description="Category")
    near_city: Optional[str] = Field(None, description="Near this city")
    limit: int = Field(10, ge=1, le=50, description="Maximum results")


# ==================== GENERIC RESPONSE MODELS ====================

class DataResponse(BaseModel):
    """Generic data response"""
    success: bool = Field(..., description="Whether request was successful")
    count: int = Field(0, description="Number of items returned")
    data: List[Dict[str, Any]] = Field(default_factory=list, description="Response data")
    message: Optional[str] = Field(None, description="Optional message")
