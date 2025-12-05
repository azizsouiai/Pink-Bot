#!/bin/bash

# Simple script to start the Chatbruti API server

cd "$(dirname "$0")"

echo "🚀 Starting Chatbruti API Server..."
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pip install -e ."
    exit 1
fi

# Check if package is installed
python -c "import chatbruti" 2>/dev/null || {
    echo "📦 Installing chatbruti package..."
    pip install -e .
}

echo ""
echo "🔧 Starting API server on http://localhost:8000"
echo "📚 API docs will be available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m chatbruti.api_server

