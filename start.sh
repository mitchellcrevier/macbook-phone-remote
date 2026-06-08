#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Kill anything already on port 5050
lsof -ti:5050 | xargs kill -9 2>/dev/null || true

# Install deps if needed
if ! python3 -c "import flask_socketio, pyautogui, simple_websocket, gunicorn" 2>/dev/null; then
  echo "Installing dependencies..."
  pip3 install -r requirements.txt --quiet
fi

IP=$(python3 -c "import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); s.connect(('8.8.8.8',80)); print(s.getsockname()[0]); s.close()")
echo ""
echo "  Mac Remote running."
echo "  Open on your phone: http://$IP:5050"
echo ""

exec /Users/mitchellcrevier/Library/Python/3.9/bin/gunicorn \
  -w 1 --threads 100 \
  -b 0.0.0.0:5050 \
  --log-level error \
  "app:app"
