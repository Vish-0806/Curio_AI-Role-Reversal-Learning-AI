@echo off
cd /d "%~dp0"
echo Activating venv...
call venv\Scripts\activate.bat
echo Running FastAPI app to check for errors...
python -c "import traceback; import app.main" > error_log.txt 2>&1
echo Done. Please check error_log.txt
pause
