#!/bin/bash

# AppBridge Standalone Installer
# Repository: https://github.com/ZimnyySTD/AppBridge/

REPO="ZimnyySTD/AppBridge"
INSTALL_DIR="/opt/appbridge"
BIN_DIR="/usr/local/bin"

echo "--- AppBridge Installer ---"

# Install system dependencies
echo "Installing dependencies..."
sudo pacman -S --needed --noconfirm wine python tk python-requests curl tar

# Get latest release tag from GitHub
echo "Fetching latest version information..."
LATEST_TAG=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$LATEST_TAG" ] || [ "$1" == "--local" ]; then
    if [ "$1" == "--local" ]; then
        echo "Local installation requested."
    else
        echo "Warning: Could not find latest release. Falling back to local files if available."
    fi

    if [ -d "./src" ]; then
        echo "Installing from current directory..."
        sudo mkdir -p $INSTALL_DIR
        sudo cp -r ./* $INSTALL_DIR/
    else
        echo "Error: No local source found and no release found on GitHub."
        exit 1
    fi
else
    echo "Latest version is $LATEST_TAG. Downloading from GitHub..."
    DOWNLOAD_URL="https://github.com/$REPO/archive/refs/tags/$LATEST_TAG.tar.gz"
    TEMP_DIR=$(mktemp -d)

    if curl -L "$DOWNLOAD_URL" -o "$TEMP_DIR/appbridge.tar.gz"; then
        echo "Extracting..."
        tar -xzf "$TEMP_DIR/appbridge.tar.gz" -C "$TEMP_DIR"
        # The folder name inside tarball usually includes the repo name and tag/branch
        SRC_FOLDER=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "AppBridge-*" | head -n 1)

        if [ -d "$SRC_FOLDER" ]; then
            echo "Installing to $INSTALL_DIR..."
            sudo mkdir -p $INSTALL_DIR
            sudo cp -r "$SRC_FOLDER"/* $INSTALL_DIR/
        else
            echo "Error: Could not find source folder after extraction."
            exit 1
        fi
    else
        echo "Error: Download failed."
        exit 1
    fi
    rm -rf "$TEMP_DIR"
fi

# Set permissions
sudo chmod +x "$INSTALL_DIR/bin/appbridge"
sudo chmod +x "$INSTALL_DIR/uninstall_appbridge.sh"

# Create symlink
sudo ln -sf "$INSTALL_DIR/bin/appbridge" "$BIN_DIR/appbridge"

# Create desktop entry
echo "Creating desktop entry..."
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

echo "------------------------------------------------"
echo "AppBridge has been installed successfully!"
echo "Run 'appbridge manager' to get started."
