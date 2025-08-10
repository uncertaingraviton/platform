#!/usr/bin/env bash

# =============================
# Reasoning Chatbot: Unified Dev Runner
# =============================
# This script starts both the FastAPI backend and the React (Vite) frontend.
# Use in a Unix-like shell (Linux, macOS, WSL, or Git Bash on Windows).
#
# If you see errors like $'\r': command not found, convert this file to Unix (LF) line endings:
#   dos2unix run_all.sh
# Or in VS Code: click "CRLF" in the bottom right, change to "LF", and save.
# =============================

# Get your local IP address (works for most Linux setups)
LOCAL_IP=$(ip -4 addr show $(ip route get 1 | awk '{print $5; exit}') | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)

cat <<EOF
========================================
Your local IP is: $LOCAL_IP
Starting backend (FastAPI) on 0.0.0.0:8000
Starting frontend (Vite React) on 0.0.0.0:5174

Access the app at: http://$LOCAL_IP:5174 from your computer or phone (on the same WiFi)
========================================
EOF

# --- Start backend ---
if [ ! -d backend ]; then
  echo "[ERROR] backend directory not found!"; exit 1
fi
cd backend
if [ ! -d venv ]; then
  echo "[ERROR] Python venv not found in backend/. Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"; exit 1
fi
source venv/bin/activate
if ! command -v uvicorn >/dev/null 2>&1; then
  echo "[ERROR] uvicorn not found in venv. Please run: pip install uvicorn"; exit 1
fi
cd ..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# --- Start frontend ---
if ! command -v npm >/dev/null 2>&1; then
  echo "[ERROR] npm not found. Please install Node.js and npm."; kill $BACKEND_PID; exit 1
fi
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

# --- Wait and cleanup ---
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait 