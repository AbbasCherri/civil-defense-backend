#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please update it with your configuration."
fi

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head

# Start the server
echo "Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
