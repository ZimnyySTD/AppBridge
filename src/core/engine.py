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
    is_new = not prefix.exists()
    prefix.mkdir(parents=True, exist_ok=True)
    if is_new:
        # Initial prefix setup
        print(f"Initializing new prefix for {app_id}...")
        env = os.environ.copy()
        env['WINEPREFIX'] = str(prefix)
        env['WINEDEBUG'] = '-all'
        # Set Windows 10 version
        subprocess.run(['winecfg', '/v', 'win10'], env=env, capture_output=True)
        # Disable wine's desktop integration to prevent desktop clutter
        # We delete the 'Desktop' folder in the prefix to stop wine from creating shortcuts there
        desktop_path = prefix / "drive_c" / "users" / os.getlogin() / "Desktop"
        if desktop_path.exists():
            shutil.rmtree(desktop_path)
        # Create a file to prevent wine from recreating it easily (or just symlink it to /dev/null)
        os.symlink('/dev/null', str(desktop_path))

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

        # Also look for any other desktop files wine might have created in the system
        # though our desktop-to-null trick should prevent this, it's good practice.
        wine_desktop_dir = Path.home() / ".local/share/applications/wine/Programs"
        if wine_desktop_dir.exists():
            # This is complex to target precisely, so we rely on our prefix isolation.
            pass

        # Remove icons
        icon_path = config['apps'][app_id].get('icon_path')
        if icon_path and Path(icon_path).exists() and str(APPBRIDGE_DATA_DIR) in icon_path:
            Path(icon_path).unlink()

        # Remove data/prefix
        app_dir = APPS_DIR / app_id
        if app_dir.exists():
            # If it's a symlink (like our Desktop trick), unlink it first
            for item in app_dir.rglob('*'):
                if item.is_symlink():
                    item.unlink()
            shutil.rmtree(app_dir)

        del config['apps'][app_id]
        save_config(config)
        print(f"Uninstalled {app_id}")
    else:
        print(f"App {app_id} not found")
