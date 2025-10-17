@echo off
echo ========================================
echo GoTravel AI Backend - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Run the server
echo Starting GoTravel AI Backend...
echo Server will be available at http://localhost:8000
echo API documentation at http://localhost:8000/docs
echo.
python main.py
