#!/bin/bash

# Setup and Run Script for Todo App - Phase II
# This script will help you set up and run the full-stack application

echo "==========================================="
echo "Todo App - Phase II Setup and Run Script"
echo "==========================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.13+."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install Node.js and npm."
    exit 1
fi

echo "✅ Python 3 is available"
echo "✅ npm is available"

# Check if backend dependencies are installed
echo "Checking backend dependencies..."
if python3 -c "import fastapi, sqlmodel, pydantic" &>/dev/null; then
    echo "✅ Backend dependencies are installed"
else
    echo "Installing backend dependencies..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
    echo "✅ Backend dependencies installed"
fi

# Check if frontend dependencies are installed
echo "Checking frontend dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo "✅ Frontend dependencies are installed"
else
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
    echo "✅ Frontend dependencies installed"
fi

echo ""
echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 - Start the backend:"
echo "  cd backend && uvicorn main:app --reload --port 8000"
echo ""
echo "Terminal 2 - Start the frontend:"
echo "  cd frontend && npm run dev"
echo ""
echo "Then open your browser to http://localhost:3000"
echo ""
echo "For a complete setup with both servers running:"
echo "  1. Run the backend in one terminal: bash start_backend.py"
echo "  2. Run the frontend in another terminal: node start_frontend.js"
echo ""