import os
import subprocess
import sys
import json
import shutil
from pathlib import Path

APPBRIDGE_DATA_DIR = Path.home() / ".local/share/appbridge"
APPS_DIR = APPBRIDGE_DATA_DIR / "apps"
CONFIG_FILE = APPBRIDGE_DATA_DIR / "config.json"

def ensure_dirs():
    APPBRIDGE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    APPS_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"version": "0.1.0", "apps": {}}, f)

def get_config():
    ensure_dirs()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_wine_prefix(app_id):
    prefix = APPS_DIR / app_id / "prefix"
    prefix.mkdir(parents=True, exist_ok=True)
    return prefix

def run_in_wine(exe_path, app_id=None, env=None):
    process_env = os.environ.copy()
    if app_id:
        prefix = get_wine_prefix(app_id)
        process_env['WINEPREFIX'] = str(prefix)

    if env:
        process_env.update(env)

    cmd = ['wine', str(exe_path)]
    return subprocess.Popen(cmd, env=process_env)

def install_exe(installer_path, name):
    app_id = name.lower().replace(" ", "_")
    print(f"Installing {name}...")

    # Create prefix and run installer
    prefix = get_wine_prefix(app_id)
    env = os.environ.copy()
    env['WINEPREFIX'] = str(prefix)

    proc = subprocess.run(['wine', installer_path], env=env)

    if proc.returncode == 0:
        # After installation, we need to find the main executable.
        # This is the tricky part. For now, we'll ask the manager to help or
        # try to guess.
        print("Installation finished. Please use the manager to select the main executable if it was not automatically detected.")
        register_app(app_id, name, "", "") # Placeholder
    else:
        print("Installation failed.")

def register_app(app_id, name, exe_path, icon_path=""):
    config = get_config()
    config['apps'][app_id] = {
        "name": name,
        "exe_path": str(exe_path),
        "icon_path": str(icon_path)
    }
    save_config(config)
    create_desktop_file(app_id, name, exe_path, icon_path)

def create_desktop_file(app_id, name, exe_path, icon_path=""):
    desktop_dir = Path.home() / ".local/share/applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)

    # We use 'appbridge' as the command to run the app
    content = f"""[Desktop Entry]
Name={name}
Exec=appbridge run {app_id}
Type=Application
Terminal=false
Categories=Wine;
"""
    if icon_path:
        content += f"Icon={icon_path}\n"

    with open(desktop_dir / f"appbridge-{app_id}.desktop", 'w') as f:
        f.write(content)

def uninstall_app(app_id):
    config = get_config()
    if app_id in config['apps']:
        # Remove desktop file
        desktop_file = Path.home() / ".local/share/applications" / f"appbridge-{app_id}.desktop"
        if desktop_file.exists():
            desktop_file.unlink()

        # Remove data/prefix
        app_dir = APPS_DIR / app_id
        if app_dir.exists():
            shutil.rmtree(app_dir)

        del config['apps'][app_id]
        save_config(config)
        print(f"Uninstalled {app_id}")
    else:
        print(f"App {app_id} not found")
