#!/bin/bash
set -e
cd "$(dirname "$0")/.."
echo "Starting Sprechen..."

# Check Python venv
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
fi

# Check .env
if [ ! -f ".env" ]; then
  echo "ERROR: .env file not found. Copy .env.example to .env and add your API keys."
  exit 1
fi

# Seed lessons if DB is fresh
.venv/bin/python scripts/seed_db.py

# Start FastAPI in background
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "Backend running on http://localhost:8000"

# Start Vite frontend
cd ../sprechen-web
if [ ! -d "node_modules" ]; then
  npm install
fi
npm run dev &
FRONTEND_PID=$!
echo "Frontend running on http://localhost:5173"
echo ""
echo "Sprechen is ready! Open http://localhost:5173"
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
