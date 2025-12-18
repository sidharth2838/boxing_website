#!/bin/bash
# Deployment preparation script for Boxing Project

echo "🥊 Boxing Project - Deployment Setup"
echo "===================================="

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "❌ Python is not installed. Please install Python first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "🔐 Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please update .env with your actual settings!"
else
    echo "✅ .env file already exists"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your production settings"
echo "2. Read DEPLOYMENT.md for deployment options"
echo "3. Run: python manage.py runserver"
echo ""
echo "Recommended deployment: Railway.app or Render.com"
