#!/bin/bash

# Pipe Standards Pro v12 - Run Script
# This script sets up the environment and runs the application

echo "🔧 Pipe Standards Pro v12"
echo "=========================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/update requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "✨ Starting Pipe Standards Pro v12..."
echo ""
python pipe_standards_v12.py

# Deactivate on exit
deactivate
