#!/bin/bash

# Legacy AppBridge Cleanup Script
# This script removes the early version of AppBridge from your system.

echo "--- Legacy AppBridge Cleanup ---"

# Remove system-wide files
echo "Removing system files..."
sudo rm -rf /opt/appbridge
sudo rm -f /usr/local/bin/appbridge
sudo rm -f /usr/share/applications/appbridge-manager.desktop

# Remove user data
echo "Removing application data and Wine prefixes..."
rm -rf "$HOME/.local/share/appbridge"
rm -f "$HOME/.local/share/applications/appbridge-"*.desktop

echo "Cleanup complete. You can now install the new version of AppBridge."
