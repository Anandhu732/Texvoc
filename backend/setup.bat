@echo off
echo ====================================
echo TxVoc Backend Setup Script
echo ====================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo.

echo [2/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

echo [3/4] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

echo [4/4] Creating storage directories...
mkdir storage\voices 2>nul
mkdir storage\audio 2>nul
mkdir storage\temp 2>nul
echo Storage directories created
echo.

echo ====================================
echo Setup completed successfully!
echo ====================================
echo.
echo To start the server:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run the server: python main.py
echo.
echo The API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
pause
