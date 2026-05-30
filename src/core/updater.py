import requests
import sys
import os
import subprocess
import shutil
from pathlib import Path

VERSION = "0.1.0"
REPO = "yourusername/AppBridge"

def check_for_updates():
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            # Assuming tag is like 'v0.1.1' or just '0.1.1'
            clean_latest = latest_version.lstrip('v')
            if clean_latest != VERSION:
                return latest_version
    except Exception as e:
        print(f"Update check failed: {e}")
    return None

def apply_update(tag):
    print(f"Updating to {tag}...")
    # We'll use curl and bash to run the installer script from the new version
    # This is the cleanest way to update system-wide files
    install_script_url = f"https://raw.githubusercontent/{REPO}/{tag}/install.sh"

    try:
        # Download and run the install script
        # Note: In a production app, you'd want more verification here
        cmd = f"curl -fsSL {install_script_url} | bash"
        subprocess.run(cmd, shell=True, check=True)
        print("Update applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply update: {e}")

def main():
    latest = check_for_updates()
    if latest:
        print(f"A new version is available: {latest}")
        confirm = input("Would you like to update now? (y/n): ")
        if confirm.lower() == 'y':
            apply_update(latest)
    else:
        print("AppBridge is up to date.")

if __name__ == "__main__":
    main()
