import requests
import sys
import os
import subprocess
import shutil
from pathlib import Path

VERSION = "1.0.0"
REPO = "ZimnyySTD/AppBridge"

def parse_version(v_str):
    # Handles v1.0.0 or 1.0.0
    return [int(x) for x in v_str.lstrip('vV').split('.')]

def format_version(v_list):
    return ".".join(map(str, v_list))

def check_for_updates():
    try:
        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        if response.status_code == 200:
            latest_tag = response.json()["tag_name"]

            curr_v = parse_version(VERSION)
            late_v = parse_version(latest_tag)

            if late_v > curr_v:
                return latest_tag
    except Exception as e:
        print(f"Update check failed: {e}")
    return None

def apply_update(tag):
    print(f"Updating to {tag}...")
    # The URL for raw files from a specific tag
    install_script_url = f"https://raw.githubusercontent.com/{REPO}/{tag}/install.sh"

    try:
        # Download the install script and run it
        print(f"Downloading installer from {install_script_url}")
        response = requests.get(install_script_url)
        if response.status_code == 200:
            with open("/tmp/appbridge_install.sh", "w") as f:
                f.write(response.text)

            subprocess.run(["bash", "/tmp/appbridge_install.sh"], check=True)
            print("Update applied successfully.")
        else:
            print(f"Failed to download installer: HTTP {response.status_code}")
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
