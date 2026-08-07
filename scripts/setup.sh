#!/bin/bash
# Hermes Kill Setup Script

set -e

echo "🚀 Setting up Hermes Kill..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data output examples/results

# Copy environment template
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your API keys"
echo "  2. Run tests: pytest tests/"
echo "  3. Start using: python scripts/crawler.py"
