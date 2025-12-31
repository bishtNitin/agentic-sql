#!/bin/bash
# Quick start script for Agentic SQL

set -e

echo "================================"
echo "Agentic SQL - Quick Start"
echo "================================"
echo ""

# Check if Docker is available
if command -v docker-compose &> /dev/null; then
    echo "✓ Docker Compose found"
    echo ""
    echo "Starting with Docker..."
    echo ""
    docker-compose up --build
else
    echo "Docker Compose not found. Starting locally..."
    echo ""
    
    # Check prerequisites
    echo "Checking prerequisites..."
    
    if ! command -v python3 &> /dev/null; then
        echo "✗ Python 3 is not installed"
        exit 1
    fi
    echo "✓ Python 3 found"
    
    if ! command -v node &> /dev/null; then
        echo "✗ Node.js is not installed"
        exit 1
    fi
    echo "✓ Node.js found"
    
    echo ""
    echo "Setting up backend..."
    cd backend
    
    # Create virtual environment if not exists
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -q -r requirements.txt
    
    # Setup database
    if [ ! -f "demo.db" ]; then
        python setup_demo_db.py
    fi
    
    # Copy .env if not exists
    if [ ! -f ".env" ]; then
        cp ../.env.example .env
    fi
    
    echo "✓ Backend setup complete"
    echo ""
    echo "Starting backend server..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    
    cd ..
    
    echo ""
    echo "Setting up frontend..."
    cd frontend
    
    # Install dependencies if not exists
    if [ ! -d "node_modules" ]; then
        npm install
    fi
    
    # Create .env.local if not exists
    if [ ! -f ".env.local" ]; then
        echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    fi
    
    echo "✓ Frontend setup complete"
    echo ""
    echo "Starting frontend server..."
    npm run dev &
    FRONTEND_PID=$!
    
    cd ..
    
    echo ""
    echo "================================"
    echo "✓ Agentic SQL is running!"
    echo "================================"
    echo ""
    echo "Frontend: http://localhost:3000"
    echo "Backend:  http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all servers"
    echo ""
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
    wait
fi
