import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

# Adjust path to import core engine, resolving symlinks
sys.path.append(str(Path(__file__).resolve().parent.parent))
from core import engine

class AppBridgeManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AppBridge Manager")
        self.geometry("600x400")

        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        # Main layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # List of apps
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Path"), show='headings')
        self.tree.heading("ID", text="App ID")
        self.tree.heading("Name", text="Application Name")
        self.tree.heading("Path", text="Executable Path")
        self.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        ttk.Button(btn_frame, text="Install New App", command=self.install_app).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Run Selected", command=self.run_app).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Uninstall Selected", command=self.uninstall_app).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)

    def refresh_list(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        config = engine.get_config()
        for app_id, app in config['apps'].items():
            self.tree.insert("", tk.END, values=(app_id, app['name'], app['exe_path']))

    def install_app(self):
        file_path = filedialog.askopenfilename(
            title="Select Windows Installer",
            filetypes=[("Executable", "*.exe"), ("MSI", "*.msi"), ("All files", "*.*")]
        )
        if file_path:
            name = os.path.basename(file_path).replace(".exe", "").replace(".msi", "")
            # In a real app, we might want to run this in a thread
            engine.install_exe(file_path, name)
            self.refresh_list()
            messagebox.showinfo("Installation", f"Started installation for {name}. Please follow the installer instructions.")

    def run_app(self):
        selected = self.tree.selection()
        if not selected:
            return

        app_id = self.tree.item(selected[0])['values'][0]
        config = engine.get_config()
        app = config['apps'][app_id]

        if not app['exe_path']:
             # If path is empty, ask user to locate the installed exe
             exe_path = filedialog.askopenfilename(
                 title=f"Locate executable for {app['name']}",
                 initialdir=str(engine.get_wine_prefix(app_id) / "drive_c"),
                 filetypes=[("Executable", "*.exe")]
             )
             if exe_path:
                 engine.register_app(app_id, app['name'], exe_path)
                 self.refresh_list()
                 engine.run_in_wine(exe_path, app_id)
        else:
            engine.run_in_wine(app['exe_path'], app_id)

    def uninstall_app(self):
        selected = self.tree.selection()
        if not selected:
            return

        app_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to uninstall {app_id}?"):
            engine.uninstall_app(app_id)
            self.refresh_list()

def main():
    app = AppBridgeManager()
    app.mainloop()

if __name__ == "__main__":
    main()
