#!/bin/bash

# Start the Automation Dashboard
# Usage: ./start_dashboard.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Starting Automation Dashboard..."
echo "================================"
echo ""
echo "Dashboard will be available at: http://localhost:8080"
echo "API Documentation: http://localhost:8080/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    python3 -m pip install flask -q
fi

# Check if Flask-CORS is installed
if ! python3 -c "import flask_cors" 2>/dev/null; then
    echo "Installing Flask-CORS..."
    python3 -m pip install flask-cors -q
fi

echo "Starting Flask server..."
python3 dashboard.py
