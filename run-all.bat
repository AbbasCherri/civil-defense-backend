@echo off
REM Start both backend and frontend for the Civil Defense Emergency Management System

echo ========================================
echo Civil Defense Emergency Management System
echo ========================================
echo.

REM Start backend in new terminal
echo Starting Backend on http://localhost:8000...
start cmd /k "cd /d "%~dp0" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in new terminal 
echo Starting Frontend on http://localhost:3000...
start cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ========================================
echo Both services are starting!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs:     http://localhost:8000/docs
echo.
echo Press Ctrl+C in each terminal to stop
echo ========================================
