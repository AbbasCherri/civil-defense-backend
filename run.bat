@REM Windows batch script to run the Civil Defense Backend API

@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Civil Defense Emergency Management System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Note: Please update .env with your database credentials
    echo.
)

REM Create uploads directory if it doesn't exist
if not exist "uploads" (
    echo Creating uploads directory...
    mkdir uploads
)

REM Run migrations
echo.
echo Running database migrations...
call .\venv\Scripts\alembic.exe upgrade head

REM Start the server
echo.
echo ========================================
echo Starting Uvicorn server on http://localhost:8000
echo Documentation available at: http://localhost:8000/docs
echo ========================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
