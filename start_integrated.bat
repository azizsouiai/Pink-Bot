@echo off
REM Script to start both the Chatbruti API server and the React widget (Windows)
REM This script helps you run both services together for development

echo.
echo 🚀 Starting Chatbruti Integrated System
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "widget-UI" (
    echo ❌ Error: widget-UI directory not found!
    echo Please run this script from the Chatbruti project root directory.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
    echo 📦 Installing Python dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    pip install -e .
) else (
    call venv\Scripts\activate.bat
)

REM Check if widget-UI has node_modules
if not exist "widget-UI\node_modules" (
    echo ⚠️  Node modules not found. Installing...
    cd widget-UI
    call npm install
    cd ..
)

REM Create .env file for widget if it doesn't exist
if not exist "widget-UI\.env" (
    echo 📝 Creating .env file for widget-UI...
    echo VITE_API_URL=http://localhost:8000/chat > widget-UI\.env
)

echo.
echo ✅ Setup complete!
echo.
echo Starting services...
echo.
echo 📡 API Server will run on: http://localhost:8000
echo 🎨 Widget will run on: http://localhost:5173 (or next available port)
echo.
echo Press Ctrl+C to stop both services
echo.

REM Start API server in a new window
echo 🔧 Starting Python API server...
start "Chatbruti API Server" cmd /k "python -m chatbruti.api_server"

REM Wait a bit for API to start
timeout /t 3 /nobreak >nul

REM Start React widget in a new window
echo 🎨 Starting React widget...
cd widget-UI
start "Chatbruti Widget" cmd /k "npm run dev"
cd ..

echo.
echo ✅ Both services are starting in separate windows!
echo Close the windows or press Ctrl+C in each to stop them.
pause

