#!/bin/bash

# Start both backend and frontend for the Civil Defense Emergency Management System

echo "========================================"
echo "Civil Defense Emergency Management System"
echo "========================================"
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start backend
echo "Starting Backend on http://localhost:8000..."
cd "$DIR"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting Frontend on http://localhost:3000..."
cd "$DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Both services are starting!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo "========================================"
echo ""

# Wait for both processes to finish or for Ctrl+C
wait

# Kill both processes on exit
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
