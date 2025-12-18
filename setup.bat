@echo off
REM Deployment preparation script for Boxing Project (Windows)

echo 🥊 Boxing Project - Deployment Setup
echo ====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file
echo 🔐 Creating .env file...
if not exist .env (
    copy .env.example .env
    echo ⚠️  Please update .env with your actual settings!
) else (
    echo ✅ .env file already exists
)

REM Run migrations
echo 🗄️  Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ✨ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your production settings
echo 2. Read DEPLOYMENT.md for deployment options
echo 3. Run: python manage.py runserver
echo.
echo Recommended deployment: Railway.app or Render.com
pause
