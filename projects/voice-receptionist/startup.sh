#!/bin/bash
set -e

echo "🚀 Voice Receptionist - Startup Script"
echo "======================================"

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

echo "✓ Activating virtual environment..."
source venv/bin/activate

echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Check environment setup
echo "✓ Checking environment variables..."
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found. Copying from .env.example..."
    cp .env.example .env.local
    echo "📝 Edit .env.local with your API keys"
fi

# Load environment
set -a
source .env.local
set +a

# Initialize database
echo "✓ Initializing database..."
python3 -c "from voice_receptionist.database import Database; db = Database(); print('✓ Database ready')"

# Check Skill Bridge health
echo "✓ Checking Skill Bridge connectivity..."
if curl -s http://localhost:9000/health > /dev/null 2>&1; then
    echo "✅ Skill Bridge is healthy (localhost:9000)"
else
    echo "⚠️  Warning: Skill Bridge not responding at localhost:9000"
    echo "   Make sure automation executor is running"
fi

# Health check endpoint
echo "✓ Testing Flask app health check..."
python3 -c "
from app import app
with app.test_client() as client:
    response = client.get('/health')
    if response.status_code == 200:
        print('✅ Flask app is ready')
    else:
        print('❌ Flask health check failed')
        exit(1)
"

echo ""
echo "✅ All checks passed! Starting voice receptionist..."
echo ""
echo "Server will run at: http://localhost:5001"
echo "Health check: curl http://localhost:5001/health"
echo "Demo mode: python3 demo.py"
echo ""

# Start Flask app
python3 app.py
