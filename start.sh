#!/bin/bash

echo "========================================"
echo "GoTravel AI Backend - Quick Start"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    echo
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo

# Run the server
echo "Starting GoTravel AI Backend..."
echo "Server will be available at http://localhost:8000"
echo "API documentation at http://localhost:8000/docs"
echo
python main.py
