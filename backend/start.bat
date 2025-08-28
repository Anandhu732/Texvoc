@echo off
echo Starting TxVoc Backend Server...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo Dependencies not found. Installing...
    pip install -r requirements.txt
)

REM Start the server
echo.
echo ====================================
echo TxVoc Backend API Server
echo ====================================
echo Server will start at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo ====================================
echo.

python main.py
