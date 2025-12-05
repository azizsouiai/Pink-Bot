#!/bin/bash

# Script to start both the Chatbruti API server and the React widget
# This script helps you run both services together for development

echo "🚀 Starting Chatbruti Integrated System"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -d "widget-UI" ]; then
    echo "❌ Error: widget-UI directory not found!"
    echo "Please run this script from the Chatbruti project root directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "📦 Installing Python dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
else
    source venv/bin/activate
fi

# Check if widget-UI has node_modules
if [ ! -d "widget-UI/node_modules" ]; then
    echo "⚠️  Node modules not found. Installing..."
    cd widget-UI
    npm install
    cd ..
fi

# Create .env file for widget if it doesn't exist
if [ ! -f "widget-UI/.env" ]; then
    echo "📝 Creating .env file for widget-UI..."
    echo "VITE_API_URL=http://localhost:8000/chat" > widget-UI/.env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting services..."
echo ""
echo "📡 API Server will run on: http://localhost:8000"
echo "🎨 Widget will run on: http://localhost:5173 (or next available port)"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $API_PID $WIDGET_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start API server in background
echo "🔧 Starting Python API server..."
python -m chatbruti.api_server &
API_PID=$!

# Wait a bit for API to start
sleep 3

# Start React widget in background
echo "🎨 Starting React widget..."
cd widget-UI
npm run dev &
WIDGET_PID=$!
cd ..

# Wait for both processes
wait $API_PID $WIDGET_PID

