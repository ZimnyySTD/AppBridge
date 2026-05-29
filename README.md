# AppBridge

AppBridge is an Arch Linux application designed to make running Windows applications as seamless as native Linux apps. It uses Wine under the hood, but abstracts away the complexity by providing an easy-to-use manager and automatic system integration.

## Features

- **Easy Installation**: One-click (or one-command) installation of Windows executables.
- **System Integration**: Automatically creates `.desktop` files so Windows apps appear in your application launcher and can be pinned to your taskbar.
- **Management GUI**: A central application to manage, run, and uninstall your Windows apps.
- **Path Translation**: Handles pathing between Linux and Windows environments automatically.
- **Isolation**: Each application can be given its own Wine prefix for better stability and isolation.

## Installation

To install AppBridge on Arch Linux:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/AppBridge.git
   cd AppBridge
   ```
2. Run the installation script:
   ```bash
   ./install.sh
   ```

## Usage

### Command Line
AppBridge provides a command-line interface:
- `appbridge manager`: Opens the GUI manager.
- `appbridge install <path_to_exe>`: Installs a Windows application.
- `appbridge run <app_id>`: Runs an installed application.
- `appbridge list`: Lists all installed applications.
- `appbridge update`: Checks for updates from GitHub.

### GUI Manager
Search for "AppBridge Manager" in your application menu to launch the graphical interface. From there, you can easily install new apps, run them, or uninstall them.

## How Updates Work
AppBridge uses a tag-based update system. When you run `appbridge update`, it checks the latest release tag on GitHub. If a newer version is found, it will notify you and provide instructions on how to update (typically a `git pull` followed by running `./install.sh` again).

## Dependencies
- Wine
- Python 3
- Tkinter (for the GUI)
