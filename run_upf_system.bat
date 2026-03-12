@echo off
TITLE UPF Management System Production Server
COLOR 0A

:: Set working directory to project root
cd /d "%~dp0"

echo ==========================================
echo    UPF Management System Startup
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.9 or higher.
    pause
    exit /b
)

:: Check if virtual environment exists, if not create one
if not exist "venv" (
    echo [INFO] Creating Virtual Environment...
    python -m venv venv
)

:: Activate virtual environment and install dependencies
echo [INFO] Activating Virtual Environment and Checking Dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Start Backend (FastAPI) in a separate window
echo [INFO] Starting Backend Server (Uvicorn) on port 8000...
start "UPF Backend" cmd /c "venv\Scripts\activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4"

:: Wait for backend to initialize
echo [INFO] Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

:: Start Frontend (Streamlit)
echo [INFO] Starting Frontend Dashboard (Streamlit) on port 8501...
start "UPF Frontend" cmd /c "venv\Scripts\activate && streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ==========================================
echo    SYSTEM RUNNING
echo ==========================================
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo ==========================================
echo.
echo Press any key to stop all services...
pause >nul

:: Kill processes when script is closed
taskkill /FI "WINDOWTITLE eq UPF Backend*" /F /T
taskkill /FI "WINDOWTITLE eq UPF Frontend*" /F /T

echo All services stopped.
exit
