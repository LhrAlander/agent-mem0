@echo off
setlocal

cd /d "%~dp0"

echo =====================================
echo  Starting Mem0 Neo4j Memory Service
echo             (Windows)
echo =====================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo Installing required dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Activating existing virtual environment...
    call venv\Scripts\activate.bat
)

echo Verifying environment variables...
if not exist ".env" (
    echo Warning: .env file not found. Copying from .env.example...
    copy .env.example .env
    echo Please configure your .env file with real credentials if the start fails.
)

echo Starting FastAPI server on Port 3899...
uvicorn main:app --host 0.0.0.0 --port 3899 --reload
