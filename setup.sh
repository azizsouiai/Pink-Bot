#!/bin/bash
# Quick setup script for Pink-Bot

set -e

echo "🚀 Setting up Pink-Bot..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install package in editable mode
echo "📦 Installing package in editable mode..."
pip install -e .

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Add your GROQ_API_KEY to .env"
echo "3. Run: python -m chatbruti.main --interactive"
echo "   or: python example.py"
echo "   or: python -m chatbruti.api_server (for API)"

