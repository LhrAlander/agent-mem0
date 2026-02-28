#!/bin/bash

# Navigate to the directory where the script is located
cd "$(dirname "$0")"

echo "====================================="
echo " Starting Mem0 Neo4j Memory Service  "
echo "        (Mac / Linux / Unix)         "
echo "====================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Installing required dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "Activating existing virtual environment..."
    source venv/bin/activate
fi

echo "Verifying environment variables..."
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please configure your .env file with real credentials if the start fails."
fi

echo "Starting FastAPI server on Port 3899..."
uvicorn main:app --host 0.0.0.0 --port 3899 --reload
