#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Install deps if needed
if ! python3 -c "import flask_socketio, pynput, eventlet" 2>/dev/null; then
  echo "Installing dependencies..."
  pip3 install -r requirements.txt --quiet
fi

python3 app.py
