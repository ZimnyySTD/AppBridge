import requests
import sys
import os
from pathlib import Path

VERSION = "0.1.0"
REPO = "yourusername/AppBridge" # Placeholder

def check_for_updates():
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version != f"v{VERSION}":
                return latest_version
    except Exception as e:
        print(f"Update check failed: {e}")
    return None

def main():
    latest = check_for_updates()
    if latest:
        print(f"A new version is available: {latest}")
        print("To update, run: git pull && ./install.sh")
    else:
        print("AppBridge is up to date.")

if __name__ == "__main__":
    main()
