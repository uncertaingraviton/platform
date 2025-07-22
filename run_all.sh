#!/usr/bin/env bash

# Get your local IP address (works for most Linux setups)
LOCAL_IP=$(ip -4 addr show $(ip route get 1 | awk '{print $5; exit}') | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)

# Print info
cat <<EOF
========================================
Your local IP is: $LOCAL_IP
Starting backend (FastAPI) on 0.0.0.0:8000
Starting frontend (static server) on 0.0.0.0:8080

Access the app at: http://$LOCAL_IP:8080 from your computer or phone (on the same WiFi)
========================================
EOF

# Start backend with hot reload (from project root)
cd backend
source venv/bin/activate
cd ..
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Start frontend static server
cd frontend
python3 -m http.server 8080 --bind 0.0.0.0 &
FRONTEND_PID=$!
cd ..

# Wait for user to press Ctrl+C, then clean up
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait 