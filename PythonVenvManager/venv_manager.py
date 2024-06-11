import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import shutil
import sys


class VenvManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Virtual Environment Manager")
        self.geometry("500x400")

        self.python_versions = self.get_python_versions()
        self.venv_list = []

        self.create_widgets()

    def create_widgets(self):
        # Python version selection
        self.python_label = tk.Label(self, text="Select Python Version:")
        self.python_label.pack(pady=5)

        self.python_combobox = ttk.Combobox(self, values=self.python_versions)
        self.python_combobox.pack(pady=5)

        # Environment name input
        self.env_name_label = tk.Label(self, text="Environment Name:")
        self.env_name_label.pack(pady=5)

        self.env_name_entry = tk.Entry(self)
        self.env_name_entry.pack(pady=5)

        # Create environment button
        self.create_button = tk.Button(self, text="Create Environment", command=self.create_environment)
        self.create_button.pack(pady=10)

        # Existing environments dropdown
        self.env_label = tk.Label(self, text="Select Environment:")
        self.env_label.pack(pady=5)

        self.env_combobox = ttk.Combobox(self, values=self.venv_list)
        self.env_combobox.pack(pady=5)

        # Activate environment button
        self.activate_button = tk.Button(self, text="Activate Environment", command=self.activate_environment)
        self.activate_button.pack(pady=5)

        # Deactivate environment button
        self.deactivate_button = tk.Button(self, text="Deactivate Environment", command=self.deactivate_environment)
        self.deactivate_button.pack(pady=5)

        # Remove environment button
        self.remove_button = tk.Button(self, text="Remove Environment", command=self.remove_environment)
        self.remove_button.pack(pady=10)

        # Refresh button
        self.refresh_button = tk.Button(self, text="Refresh Environments", command=self.refresh_env_list)
        self.refresh_button.pack(pady=5)

        self.refresh_env_list()

    def get_python_versions(self):
        versions = []
        for path in os.environ["PATH"].split(os.pathsep):
            try:
                if os.name == 'nt':
                    for exe in os.listdir(path):
                        if exe.startswith("python") and exe.endswith(".exe"):
                            versions.append(os.path.join(path, exe))
                else:
                    versions += [os.path.join(path, exe) for exe in os.listdir(path) if exe.startswith("python")]
            except FileNotFoundError:
                continue
        return versions

    def refresh_env_list(self):
        venv_path = os.path.join(os.getcwd(), "venvs")
        if not os.path.exists(venv_path):
            os.makedirs(venv_path)
        self.venv_list = [d for d in os.listdir(venv_path) if os.path.isdir(os.path.join(venv_path, d))]
        self.env_combobox['values'] = self.venv_list

    def create_environment(self):
        python_path = self.python_combobox.get()
        env_name = self.env_name_entry.get()
        if python_path and env_name:
            venv_dir = os.path.join(os.getcwd(), "venvs", env_name)
            try:
                subprocess.check_call([python_path, "-m", "venv", venv_dir])
                messagebox.showinfo("Success", f"Environment '{env_name}' created successfully!")
                self.refresh_env_list()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to create environment: {e}")
        else:
            messagebox.showwarning("Input Error", "Please select a Python version and enter an environment name.")

    def activate_environment(self):
        env_name = self.env_combobox.get()
        if env_name:
            if os.name == 'nt':
                activate_script = os.path.join(os.getcwd(), "venvs", env_name, "Scripts", "activate.bat")
            else:
                activate_script = os.path.join(os.getcwd(), "venvs", env_name, "bin", "activate")
            os.system(f'start cmd /K "{activate_script}"')
        else:
            messagebox.showwarning("Selection Error", "Please select an environment to activate.")

    def deactivate_environment(self):
        messagebox.showinfo("Info",
                            "Deactivate the environment by closing the command prompt window where it is activated.")

    def remove_environment(self):
        env_name = self.env_combobox.get()
        if env_name:
            venv_dir = os.path.join(os.getcwd(), "venvs", env_name)
            try:
                shutil.rmtree(venv_dir)
                messagebox.showinfo("Success", f"Environment '{env_name}' removed successfully!")
                self.refresh_env_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove environment: {e}")
        else:
            messagebox.showwarning("Selection Error", "Please select an environment to remove.")


if __name__ == "__main__":
    app = VenvManager()
    app.mainloop()
