"""
Configuration module for the GoTravel AI Backend
Loads environment variables and provides configuration settings
"""
import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""
    
    # Google AI Configuration
    google_api_key: str = ""
    
    # OpenWeatherMap API
    openweather_api_key: str = ""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Settings - can be "*" for all origins or comma-separated list
    allowed_origins: Union[str, List[str]] = ["http://localhost:3000", "http://localhost:5173"]
    
    # AI Model Configuration
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            # If it's "*", return as list with single element
            if v.strip() == "*":
                return ["*"]
            # Otherwise split by comma
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        """Parse debug boolean from string"""
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes")
        return v


# Create a global settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """Validate that all critical settings are configured"""
    missing = []
    
    if not settings.supabase_url:
        missing.append("SUPABASE_URL")
    if not settings.supabase_key:
        missing.append("SUPABASE_KEY")
    if not settings.google_api_key:
        missing.append("GOOGLE_API_KEY")
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please check your .env file."
        )


if __name__ == "__main__":
    validate_settings()
    print("✅ Configuration validated successfully!")
    print(f"Supabase URL: {settings.supabase_url}")
    print(f"Model: {settings.model_name}")
