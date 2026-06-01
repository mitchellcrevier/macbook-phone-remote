#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.mitchellcrevier.macremote"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

# Inject actual script path into the plist
sed "s|SCRIPT_DIR|$SCRIPT_DIR|g" "$PLIST_SRC" > "$PLIST_DEST"

# Unload if already loaded, then load
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "Installed. Mac Remote will now start automatically at login."
echo "It's running now — open your phone to http://$(python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
print(s.getsockname()[0])
s.close()
"):5050"
