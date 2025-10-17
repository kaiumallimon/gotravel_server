"""
Vercel Entry Point
This file is used by Vercel to deploy the FastAPI application
"""
from main import app

# Vercel expects the app to be named 'app' at module level
# This is already the case in main.py, but we import it here for clarity
__all__ = ["app"]
