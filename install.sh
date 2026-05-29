#!/bin/bash

# AppBridge Installer for Arch Linux

echo "Starting AppBridge Installation..."

# Check for Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo "Warning: This script is intended for Arch Linux. It might not work on other distributions."
fi

# Install dependencies
echo "Checking dependencies..."
sudo pacman -Sy --needed --noconfirm wine python tk python-requests

# Create necessary directories
INSTALL_DIR="/opt/appbridge"
BIN_DIR="/usr/local/bin"

echo "Installing to $INSTALL_DIR..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r . $INSTALL_DIR

# Create symlink for the main command
echo "Creating symlink in $BIN_DIR..."
sudo ln -sf "$INSTALL_DIR/bin/appbridge" "$BIN_DIR/appbridge"

# Create a desktop file for the manager itself
echo "Creating desktop entry for AppBridge Manager..."
DESKTOP_ENTRY="/usr/share/applications/appbridge-manager.desktop"
sudo bash -c "cat > $DESKTOP_ENTRY <<EOF
[Desktop Entry]
Name=AppBridge Manager
Comment=Manage Windows Applications on Arch Linux
Exec=appbridge manager
Icon=system-software-install
Type=Application
Terminal=false
Categories=System;Utility;
EOF"

echo "AppBridge installed successfully!"
echo "You can now run 'appbridge manager' or just search for 'AppBridge Manager' in your application menu."
