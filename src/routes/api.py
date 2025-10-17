"""
FastAPI Routes
API endpoints for the GoTravel AI Backend
"""
from fastapi import APIRouter, HTTPException, status
from src.models import (
    ChatRequest, ChatResponse, ChatErrorResponse,
    SessionInfoRequest, SessionInfoResponse,
    ClearHistoryRequest, ClearHistoryResponse,
    HealthCheckResponse,
    CreateBookingRequest, BookingResponse
)
from src.services.agent import travel_agent
from src.services.database import supabase_client
from src.config import settings
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# ==================== HEALTH CHECK ====================

@router.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the API and its dependencies"
)
async def health_check():
    """Health check endpoint"""
    services_status = {}
    
    # Check Supabase connection
    try:
        # Try a simple query
        result = supabase_client.client.table("hotels").select("id").limit(1).execute()
        services_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        services_status["database"] = "error"
    
    # Check AI model
    try:
        if travel_agent.llm:
            services_status["ai_model"] = "ready"
        else:
            services_status["ai_model"] = "not_initialized"
    except Exception as e:
        logger.error(f"AI model health check failed: {e}")
        services_status["ai_model"] = "error"
    
    # Check weather API config
    if settings.openweather_api_key:
        services_status["weather_api"] = "configured"
    else:
        services_status["weather_api"] = "not_configured"
    
    overall_status = "healthy" if all(
        s in ["connected", "ready", "configured", "available"] 
        for s in services_status.values()
    ) else "degraded"
    
    return HealthCheckResponse(
        status=overall_status,
        timestamp=datetime.now(),
        version="1.0.0",
        services=services_status
    )


# ==================== CHAT ENDPOINTS ====================

@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        500: {"model": ChatErrorResponse, "description": "Internal server error"}
    },
    summary="Chat with AI Assistant",
    description="Send a message to the AI travel assistant and receive a response"
)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for interacting with the AI travel assistant.
    
    The AI can help with:
    - Searching for hotels, packages, and tourist places
    - Getting weather information
    - Creating bookings
    - Answering travel-related questions
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{uuid.uuid4().hex[:12]}"
        
        # Process the message
        result = await travel_agent.process_message(
            message=request.message,
            session_id=session_id,
            user_context={"user_id": request.user_id} if request.user_id else None
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to process message")
            )
        
        return ChatResponse(
            success=True,
            response=result.get("response"),
            session_id=result.get("session_id"),
            tools_used=[
                {"tool": t["tool"], "input": t["input"]}
                for t in result.get("tools_used", [])
            ],
            message_count=result.get("message_count", 0),
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your message: {str(e)}"
        )


@router.post(
    "/session/info",
    response_model=SessionInfoResponse,
    summary="Get Session Info",
    description="Get information about a chat session"
)
async def get_session_info(request: SessionInfoRequest):
    """Get information about a specific chat session"""
    try:
        info = travel_agent.get_session_info(request.session_id)
        return SessionInfoResponse(
            exists=info.get("exists", False),
            session_id=request.session_id,
            message_count=info.get("message_count", 0)
        )
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve session information"
        )


@router.post(
    "/session/clear",
    response_model=ClearHistoryResponse,
    summary="Clear Session History",
    description="Clear chat history for a specific session"
)
async def clear_session_history(request: ClearHistoryRequest):
    """Clear chat history for a session"""
    try:
        success = travel_agent.clear_history(request.session_id)
        return ClearHistoryResponse(
            success=success,
            session_id=request.session_id,
            message="Chat history cleared successfully" if success else "Session not found"
        )
    except Exception as e:
        logger.error(f"Error clearing session history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear session history"
        )


# ==================== DIRECT BOOKING ENDPOINT ====================

@router.post(
    "/booking",
    response_model=BookingResponse,
    summary="Create Booking",
    description="Create a booking directly without using the chat interface"
)
async def create_booking_direct(request: CreateBookingRequest):
    """
    Direct booking endpoint (alternative to chat-based booking).
    This allows frontend to create bookings programmatically.
    """
    try:
        # Validate booking type
        if request.booking_type not in ["package", "hotel"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid booking type. Must be 'package' or 'hotel'"
            )
        
        # Get item details
        if request.booking_type == "package":
            item = supabase_client.get_package_by_id(request.item_id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Package not found with ID: {request.item_id}"
                )
            total_amount = float(item.get("price", 0)) * request.total_participants
            currency = item.get("currency", "BDT")
        else:
            item = supabase_client.get_hotel_by_id(request.item_id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Hotel not found with ID: {request.item_id}"
                )
            # For hotel, you'd typically need room selection
            total_amount = 5000.0  # Placeholder
            currency = "BDT"
        
        # Create user ID if not provided
        user_id = request.user_id or str(uuid.uuid4())
        
        # Create booking
        booking = supabase_client.create_booking(
            user_id=user_id,
            booking_type=request.booking_type,
            item_id=request.item_id,
            primary_guest_name=request.guest_name,
            primary_guest_email=request.guest_email,
            primary_guest_phone=request.guest_phone,
            total_amount=total_amount,
            total_participants=request.total_participants,
            base_price=total_amount,
            currency=currency
        )
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create booking"
            )
        
        return BookingResponse(
            success=True,
            message="Booking created successfully",
            booking_reference=booking.get("booking_reference"),
            booking_type=booking.get("booking_type"),
            total_amount=booking.get("total_amount"),
            currency=booking.get("currency")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create booking: {str(e)}"
        )


# ==================== ROOT ENDPOINT ====================

@router.get(
    "/",
    summary="API Root",
    description="Welcome endpoint with API information"
)
async def root():
    """Root endpoint with API information"""
    return {
        "service": "GoTravel AI Backend",
        "version": "1.0.0",
        "description": "AI-powered travel booking assistant using FastAPI, LangChain, and Supabase",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "session_info": "/api/session/info",
            "clear_session": "/api/session/clear",
            "create_booking": "/api/booking",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "Search hotels by location and rating",
            "Discover travel packages",
            "Find tourist places and attractions",
            "Get real-time weather information",
            "Create bookings through natural language",
            "Conversational AI with context awareness"
        ],
        "model": settings.model_name,
        "status": "operational"
    }
