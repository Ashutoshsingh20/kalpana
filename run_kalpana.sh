#!/bin/bash

echo "🔵 Initializing Kalpana AGI..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

# Create Virtual Environment if not exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate Venv
source venv/bin/activate

# Install Dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start Backend
echo "🚀 Starting Kalpana Core..."
python3 -m backend.main
