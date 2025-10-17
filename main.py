"""
GoTravel AI Backend - Main Application
FastAPI server for AI-powered travel booking assistant
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import sys
from datetime import datetime

from src.config import settings, validate_settings
from src.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('gotravel_backend.log')
    ]
)

logger = logging.getLogger(__name__)


# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown
    """
    # Startup
    logger.info("🚀 Starting GoTravel AI Backend...")
    
    try:
        # Validate configuration
        validate_settings()
        logger.info("✅ Configuration validated")
        
        # Log configuration (without sensitive data)
        logger.info(f"Model: {settings.model_name}")
        logger.info(f"Supabase URL: {settings.supabase_url}")
        logger.info(f"Debug Mode: {settings.debug}")
        logger.info(f"Allowed Origins: {settings.allowed_origins}")
        
        logger.info("✅ GoTravel AI Backend started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down GoTravel AI Backend...")


# Create FastAPI application
app = FastAPI(
    title="GoTravel AI Backend",
    description="""
    🌍 **AI-Powered Travel Booking Assistant**
    
    An intelligent backend system that powers a conversational AI travel assistant.
    Built with FastAPI, LangChain, Google Gemini, and Supabase.
    
    ## Features
    
    * 🤖 **Intelligent Chat Interface** - Natural language conversation with context awareness
    * 🏨 **Hotel Search** - Find accommodations by location, rating, and preferences
    * ✈️ **Package Discovery** - Explore travel packages by destination, category, and price
    * 🗺️ **Place Recommendations** - Discover tourist attractions and destinations
    * 🌤️ **Weather Information** - Real-time weather data for any location
    * 📝 **Smart Bookings** - Create bookings through natural conversation
    * 🔄 **Session Management** - Maintain conversation context across interactions
    
    ## Technology Stack
    
    * **Framework**: FastAPI
    * **AI/ML**: LangChain + Google Gemini 2.0 Flash
    * **Database**: Supabase (PostgreSQL)
    * **APIs**: OpenWeatherMap
    
    ## Getting Started
    
    1. Try the `/api/chat` endpoint to interact with the AI assistant
    2. Check `/api/health` to verify system status
    3. Explore the interactive docs at `/docs`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An internal server error occurred",
            "detail": str(exc) if settings.debug else "Please try again later",
            "timestamp": datetime.now().isoformat()
        }
    )


# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation error",
            "detail": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.now()
    
    # Log request
    logger.info(f"📨 {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"📤 {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.3f}s"
    )
    
    return response


# Include API routes with prefix
app.include_router(router, prefix="/api", tags=["API"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic API information"""
    return {
        "service": "GoTravel AI Backend",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "root_info": "/api/"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server with uvicorn...")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
