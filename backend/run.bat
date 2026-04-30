@echo off
echo ============================================
echo   Curio AI - Backend Setup and Run
echo ============================================
echo.

cd /d "%~dp0"

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt

echo [4/4] Starting Curio AI server...
echo.
echo ============================================
echo   Server running at http://localhost:8001
echo   API docs at http://localhost:8001/docs
echo   Health check: http://localhost:8001/health
echo   Press Ctrl+C to stop
echo ============================================
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
pause
