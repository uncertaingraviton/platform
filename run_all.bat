@echo off
REM ========================================
REM Reasoning Chatbot: Unified Dev Runner (Windows)
REM ========================================
REM This script starts both the FastAPI backend and the React (Vite) frontend.
REM Use in Command Prompt or PowerShell.
REM ========================================

REM Get local IP address using PowerShell
for /f "usebackq tokens=*" %%i in (`powershell -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*' }).IPAddress | Select-Object -First 1"`) do set LOCAL_IP=%%i

REM Print info
echo ========================================
echo Your local IP is: %LOCAL_IP%
echo Starting backend (FastAPI) on 0.0.0.0:8000
echo Starting frontend (Vite React) on 0.0.0.0:5174

echo Access the app at: http://%LOCAL_IP%:5174 from your computer or phone (on the same WiFi)
echo ========================================

REM --- Start backend ---
if not exist backend ( echo [ERROR] backend directory not found! & exit /b 1 )
if not exist backend\venv ( echo [ERROR] Python venv not found in backend\. Please run: python -m venv venv && backend\venv\Scripts\activate && pip install -r requirements.txt & exit /b 1 )
REM Always start in project root, then cd into backend to activate venv, then cd back to root to run uvicorn
start "FastAPI Backend" cmd /k "cd /d %cd% && cd backend && call venv\Scripts\activate && cd .. && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

REM --- Start frontend ---
where npm >nul 2>nul || ( echo [ERROR] npm not found. Please install Node.js and npm. & exit /b 1 )
start "Vite Frontend" cmd /k "cd /d %cd% && npm run dev -- --host 0.0.0.0"

REM --- Instructions ---
echo.
echo Both servers are running in new terminals. Press Ctrl+C in those windows to stop them.
echo If you see errors, check the terminal windows for details.
echo.
