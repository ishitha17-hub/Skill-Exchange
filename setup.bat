@echo off
REM Skill-Exchange Platform - Local Setup Script
REM This script automates local development setup on Windows

echo.
echo ==========================================
echo Skill-Exchange Platform - Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    exit /b 1
)

echo [1/5] Python found!

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Git is not installed
    echo Download from: https://git-scm.com/download/win
    REM Continue anyway - Git is optional for local setup
)

echo [2/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    exit /b 1
)

echo [3/5] Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo .env file created! Please edit it with your MongoDB URI
) else (
    echo .env file already exists
)

echo [4/5] Configuration ready!
echo.
echo ==========================================
echo SETUP COMPLETE!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file with your MongoDB connection URI
echo 2. Make sure MongoDB is running (mongod)
echo 3. Run: cd backend
echo 4. Run: python app.py
echo 5. Visit: http://localhost:5005
echo.
echo Default Credentials:
echo   Admin: admin@site.com / admin123
echo   User: user@site.com / user123
echo.
pause
