#!/bin/bash
set -e

echo "Starting IncidentIQ..."

# Activate virtual environment if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Load env
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Start backend
echo "Starting backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd frontend && npm install --silent && npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop."

wait
