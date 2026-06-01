#!/bin/bash
PLIST_NAME="com.mitchellcrevier.macremote"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

launchctl unload "$PLIST_DEST" 2>/dev/null || true
rm -f "$PLIST_DEST"
echo "Uninstalled. Mac Remote will no longer start at login."
