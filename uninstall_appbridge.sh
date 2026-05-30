#!/bin/bash

# AppBridge Uninstaller

INSTALL_DIR="/opt/appbridge"
BIN_DIR="/usr/local/bin"
DATA_DIR="$HOME/.local/share/appbridge"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "--- AppBridge Uninstaller ---"

read -p "Do you want to remove all installed Windows applications as well? (y/n): " REMOVE_APPS

# Remove system-wide files
echo "Removing system files..."
sudo rm -rf $INSTALL_DIR
sudo rm $BIN_DIR/appbridge
sudo rm /usr/share/applications/appbridge-manager.desktop

if [ "$REMOVE_APPS" = "y" ] || [ "$REMOVE_APPS" = "Y" ]; then
    echo "Removing all Windows applications and data..."
    rm -rf $DATA_DIR
    # Remove app-specific desktop files
    rm $DESKTOP_DIR/appbridge-*.desktop
else
    echo "Keeping Windows applications data in $DATA_DIR."
fi

echo "AppBridge has been uninstalled."
