import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import subprocess
import threading
import platform
import os
import json
from pathlib import Path
import sys
from datetime import datetime

class ConfigManager:
    """Simple config management with JSON file"""
    
    def __init__(self):
        # Save config in same directory as the script
        script_dir = Path(__file__).parent
        self.config_dir = script_dir / ".python_project_manager"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            "projects_dir": str(Path.home() / "Projects"),
            "venvs_dir": str(Path.home() / "venvs"),
            "project_venv_mapping": {},
            "active_project": None
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except (json.JSONDecodeError, IOError):
                pass
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError:
            pass
    
    def get_projects_dir(self):
        return Path(self.config["projects_dir"])
    
    def get_venvs_dir(self):
        return Path(self.config["venvs_dir"])

class Terminal:
    """Simple terminal widget"""
    
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Terminal", padding=5)
        
        # Terminal output
        self.output = scrolledtext.ScrolledText(
            self.frame,
            height=15,
            bg="black",
            fg="lightgreen",
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.output.pack(fill="both", expand=True, pady=(0, 5))
        
        # Command input
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="Command:").pack(side="left")
        self.command_entry = ttk.Entry(input_frame)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))
        self.command_entry.bind("<Return>", self.execute_command)
        
        ttk.Button(input_frame, text="Run", command=self.execute_command).pack(side="right")
        
        self.current_dir = str(Path.home())
        self.active_venv = None
        
        self.write_line("=== Python Project Manager Terminal ===")
        self.write_line(f"Platform: {platform.system()}")
        self.write_line("")
        self.show_prompt()  # Show initial prompt
    
    def write_line(self, text):
        """Write a line to terminal output"""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.update()
    
    def write_command(self, command):
        """Display a command being executed"""
        prompt = self.get_prompt()
        self.output.insert(tk.END, f"{prompt} {command}\n")
        self.output.see(tk.END)
        self.output.update()
    
    def show_prompt(self):
        """Show the current prompt without newline"""
        prompt = self.get_prompt()
        self.output.insert(tk.END, f"{prompt} ")
        self.output.see(tk.END)
        self.output.update()
    
    def get_prompt(self):
    	"""Generate command prompt"""
    	venv_prefix = f"({self.active_venv}) " if self.active_venv else ""
    	if platform.system() == "Windows":
        	return f"{venv_prefix}{self.current_dir}>"
    	else:
        	return f"{venv_prefix}{self.current_dir}$"
    
    def execute_command(self, event=None):
        """Execute user command"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        self.command_entry.delete(0, tk.END)
        
        # Clear the current prompt line and show the command
        self.output.delete("end-1c linestart", "end-1c")
        self.write_command(command)
        
        def run():
            try:
                # Handle cd command
                if command.lower().startswith('cd '):
                    new_dir = command[3:].strip().strip('"\'')
                    if new_dir:
                        if new_dir == '..':
                            new_path = Path(self.current_dir).parent
                        elif new_dir == '~':
                            new_path = Path.home()
                        elif Path(new_dir).is_absolute():
                            new_path = Path(new_dir)
                        else:
                            new_path = Path(self.current_dir) / new_dir
                        
                        if new_path.exists() and new_path.is_dir():
                            self.current_dir = str(new_path.resolve())
                        else:
                            self.write_line("Directory not found")
                    else:
                        self.current_dir = str(Path.home())
                    
                    self.show_prompt()
                    return
                
                # Handle clear
                if command.lower() in ['clear', 'cls']:
                    self.output.delete(1.0, tk.END)
                    self.show_prompt()
                    return
                
                # Execute other commands
                env = os.environ.copy()
                if self.active_venv:
                    venv_path = Path.home() / "venvs" / self.active_venv
                    if platform.system() == "Windows":
                        env["PATH"] = f"{venv_path}\\Scripts;{env['PATH']}"
                        env["VIRTUAL_ENV"] = str(venv_path)
                    else:
                        env["PATH"] = f"{venv_path}/bin:{env['PATH']}"
                        env["VIRTUAL_ENV"] = str(venv_path)
                
                # Run command
                if platform.system() == "Windows":
                    shell_cmd = ["cmd", "/c", command]
                else:
                    shell_cmd = ["bash", "-c", command]
                
                process = subprocess.Popen(
                    shell_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self.current_dir,
                    env=env
                )
                
                stdout, stderr = process.communicate()
                
                if stdout:
                    self.write_line(stdout.rstrip())
                if stderr:
                    self.write_line(stderr.rstrip())
                
                # Always show prompt after command execution
                self.show_prompt()
                
            except Exception as e:
                self.write_line(f"Error: {str(e)}")
                self.show_prompt()
        
        threading.Thread(target=run, daemon=True).start()
    
    def set_directory(self, directory):
        """Set current directory"""
        self.current_dir = str(directory)
        self.write_command(f'cd "{directory}"')
        self.show_prompt()  # Show new prompt after cd
    
    def activate_venv(self, venv_name):
        """Activate virtual environment"""
        self.active_venv = venv_name
        venv_path = Path.home() / "venvs" / venv_name
        if platform.system() == "Windows":
            cmd = f'"{venv_path}\\Scripts\\activate.bat"'
        else:
            cmd = f'source "{venv_path}/bin/activate"'
        self.write_command(cmd)
        self.write_line(f"✓ Activated virtual environment: {venv_name}")
        self.show_prompt()  # Show new prompt with venv
    
    def deactivate_venv(self):
        """Deactivate virtual environment"""
        if self.active_venv:
            self.write_command("deactivate")
            self.write_line(f"✓ Deactivated virtual environment: {self.active_venv}")
            self.active_venv = None
            self.show_prompt()  # Show new prompt without venv

class ProjectManager:
    """Manage projects"""
    
    def __init__(self, config, terminal):
        self.config = config
        self.terminal = terminal
    
    def create_project(self, name):
        """Create new project directory"""
        project_path = self.config.get_projects_dir() / name
        if project_path.exists():
            messagebox.showerror("Error", f"Project '{name}' already exists!")
            return False
        
        try:
            self.config.get_projects_dir().mkdir(parents=True, exist_ok=True)
            project_path.mkdir()
            self.terminal.write_command(f'mkdir "{project_path}"')
            self.terminal.write_line(f"✓ Created project: {name}")
            self.terminal.show_prompt()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")
            return False
    
    def delete_project(self, name):
        """Delete project"""
        project_path = self.config.get_projects_dir() / name
        if not project_path.exists():
            return False
        
        if messagebox.askyesno("Confirm", f"Delete project '{name}' and all its files?"):
            try:
                import shutil
                shutil.rmtree(project_path)
                if name in self.config.config["project_venv_mapping"]:
                    del self.config.config["project_venv_mapping"][name]
                if self.config.config.get("active_project") == name:
                    self.config.config["active_project"] = None
                self.config.save_config()
                self.terminal.write_line(f"✓ Deleted project: {name}")
                self.terminal.show_prompt()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete project: {str(e)}")
        return False
    
    def list_projects(self):
        """List all projects"""
        projects_dir = self.config.get_projects_dir()
        if not projects_dir.exists():
            return []
        
        try:
            return [item.name for item in projects_dir.iterdir() 
                   if item.is_dir() and not item.name.startswith('.')]
        except:
            return []
    
    def open_project(self, name):
        """Open project (just cd, no venv activation)"""
        project_path = self.config.get_projects_dir() / name
        if not project_path.exists():
            return False
        
        # Just change directory
        self.terminal.set_directory(str(project_path))
        self.config.config["active_project"] = name
        self.config.save_config()
        return True
    
    def switch_to_project(self, name):
        """Switch to project (cd + activate venv if assigned)"""
        project_path = self.config.get_projects_dir() / name
        if not project_path.exists():
            return False
        
        # Change directory
        self.terminal.set_directory(str(project_path))
        
        # Activate venv if assigned
        venv_name = self.config.config["project_venv_mapping"].get(name)
        if venv_name:
            venv_path = self.config.get_venvs_dir() / venv_name
            if venv_path.exists():
                self.terminal.activate_venv(venv_name)
        
        self.config.config["active_project"] = name
        self.config.save_config()
        return True

class VenvManager:
    """Manage virtual environments"""
    
    def __init__(self, config, terminal):
        self.config = config
        self.terminal = terminal
    
    def create_venv(self, name):
        """Create new virtual environment"""
        venv_path = self.config.get_venvs_dir() / name
        if venv_path.exists():
            messagebox.showerror("Error", f"Virtual environment '{name}' already exists!")
            return False
        
        python_cmd = "python" if platform.system() == "Windows" else "python3"
        self.terminal.write_command(f'{python_cmd} -m venv "{venv_path}"')
        
        def create():
            try:
                self.config.get_venvs_dir().mkdir(parents=True, exist_ok=True)
                
                process = subprocess.Popen(
                    [python_cmd, "-m", "venv", str(venv_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    self.terminal.write_line(f"✓ Created virtual environment: {name}")
                else:
                    self.terminal.write_line(f"✗ Failed to create virtual environment: {name}")
                    if stderr:
                        self.terminal.write_line(stderr)
                
                self.terminal.show_prompt()
                        
            except Exception as e:
                self.terminal.write_line(f"✗ Error creating virtual environment: {str(e)}")
                self.terminal.show_prompt()
        
        threading.Thread(target=create, daemon=True).start()
        return True
    
    def delete_venv(self, name):
        """Delete virtual environment"""
        venv_path = self.config.get_venvs_dir() / name
        if not venv_path.exists():
            return False
        
        # Check if any projects use this venv
        projects_using = [proj for proj, venv in self.config.config["project_venv_mapping"].items() 
                         if venv == name]
        
        warning = f"Delete virtual environment '{name}'?"
        if projects_using:
            warning += f"\n\nWarning: Used by {len(projects_using)} project(s):\n"
            warning += "\n".join(f"• {p}" for p in projects_using)
        
        if messagebox.askyesno("Confirm", warning):
            try:
                import shutil
                shutil.rmtree(venv_path)
                
                # Remove from project mappings
                for project in projects_using:
                    del self.config.config["project_venv_mapping"][project]
                
                if self.terminal.active_venv == name:
                    self.terminal.deactivate_venv()
                
                self.config.save_config()
                self.terminal.write_line(f"✓ Deleted virtual environment: {name}")
                self.terminal.show_prompt()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete virtual environment: {str(e)}")
        return False
    
    def list_venvs(self):
        """List all virtual environments"""
        venvs_dir = self.config.get_venvs_dir()
        if not venvs_dir.exists():
            return []
        
        try:
            venvs = []
            for item in venvs_dir.iterdir():
                if item.is_dir():
                    # Check if it's a valid venv
                    if (item / "pyvenv.cfg").exists():
                        venvs.append(item.name)
            return venvs
        except:
            return []

class SettingsDialog:
    """Simple settings dialog"""
    
    def __init__(self, parent, config):
        self.config = config
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("700x600")  # Made larger
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        # Main scrollable frame
        canvas = tk.Canvas(self.dialog)
        scrollbar = ttk.Scrollbar(self.dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Content in the scrollable frame
        main_frame = ttk.Frame(scrollable_frame, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # JSON display
        ttk.Label(main_frame, text="Configuration JSON:", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        
        self.json_text = scrolledtext.ScrolledText(main_frame, height=20, width=70)
        self.json_text.pack(fill="both", expand=True, pady=(5, 15))
        
        # Load current config
        try:
            config_json = json.dumps(self.config.config, indent=2)
            self.json_text.insert(tk.END, config_json)
        except:
            self.json_text.insert(tk.END, "Error loading configuration")
        
        # Directory settings
        dirs_frame = ttk.LabelFrame(main_frame, text="Directory Settings", padding=10)
        dirs_frame.pack(fill="x", pady=(0, 15))
        
        # Projects directory
        ttk.Label(dirs_frame, text="Projects Directory:").pack(anchor="w")
        proj_frame = ttk.Frame(dirs_frame)
        proj_frame.pack(fill="x", pady=(2, 10))
        
        self.projects_dir_var = tk.StringVar(value=self.config.config["projects_dir"])
        proj_entry = ttk.Entry(proj_frame, textvariable=self.projects_dir_var, state="readonly")
        proj_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(proj_frame, text="Browse", 
                  command=self.browse_projects_dir).pack(side="right", padx=(5, 0))
        
        # Venvs directory
        ttk.Label(dirs_frame, text="Virtual Environments Directory:").pack(anchor="w")
        venv_frame = ttk.Frame(dirs_frame)
        venv_frame.pack(fill="x", pady=(2, 0))
        
        self.venvs_dir_var = tk.StringVar(value=self.config.config["venvs_dir"])
        venv_entry = ttk.Entry(venv_frame, textvariable=self.venvs_dir_var, state="readonly")
        venv_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(venv_frame, text="Browse", 
                  command=self.browse_venvs_dir).pack(side="right", padx=(5, 0))
        
        # Buttons - Fixed at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Save", command=self.save).pack(side="right")
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux
    
    def browse_projects_dir(self):
        """Browse for projects directory"""
        directory = filedialog.askdirectory(title="Select Projects Directory")
        if directory:
            self.projects_dir_var.set(directory)
    
    def browse_venvs_dir(self):
        """Browse for virtual environments directory"""
        directory = filedialog.askdirectory(title="Select Virtual Environments Directory")
        if directory:
            self.venvs_dir_var.set(directory)
    
    def save(self):
        """Save settings"""
        self.config.config["projects_dir"] = self.projects_dir_var.get()
        self.config.config["venvs_dir"] = self.venvs_dir_var.get()
        self.config.save_config()
        self.result = True
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()

class MainGUI:
    """Main application GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Project Manager")
        self.root.geometry("1000x700")
        
        # Initialize components
        self.config = ConfigManager()
        self.setup_ui()
        self.terminal = Terminal(self.terminal_frame)
        self.project_manager = ProjectManager(self.config, self.terminal)
        self.venv_manager = VenvManager(self.config, self.terminal)
        
        # Pack terminal
        self.terminal.frame.pack(fill="both", expand=True)
        
        # Load data
        self.refresh_all()
    
    def setup_ui(self):
        """Setup main UI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Top bar with settings button
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(top_frame, text="Settings", command=self.show_settings).pack(side="right")
        
        # Main content - projects and venvs side by side
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Projects section (left)
        projects_frame = ttk.LabelFrame(content_frame, text="Projects", padding=5)
        projects_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Projects buttons
        proj_buttons = ttk.Frame(projects_frame)
        proj_buttons.pack(fill="x", pady=(0, 5))
        
        ttk.Button(proj_buttons, text="Open", command=self.open_project).pack(side="left", padx=(0, 5))
        ttk.Button(proj_buttons, text="Create New", command=self.create_project).pack(side="left", padx=(0, 5))
        ttk.Button(proj_buttons, text="Change Virtual Environment", command=self.change_venv).pack(side="left", padx=(0, 5))
        ttk.Button(proj_buttons, text="Delete", command=self.delete_project).pack(side="right")
        
        # Projects list
        self.projects_list = tk.Listbox(projects_frame, height=10)
        self.projects_list.pack(fill="both", expand=True)
        self.projects_list.bind("<Double-Button-1>", self.switch_project)
        
        # Virtual environments section (right)
        venvs_frame = ttk.LabelFrame(content_frame, text="Virtual Environments", padding=5)
        venvs_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Venvs buttons top row
        venv_buttons1 = ttk.Frame(venvs_frame)
        venv_buttons1.pack(fill="x", pady=(0, 2))
        
        ttk.Button(venv_buttons1, text="Activate", command=self.activate_venv).pack(side="left", padx=(0, 5))
        ttk.Button(venv_buttons1, text="Deactivate", command=self.deactivate_venv).pack(side="left")
        
        # Venvs buttons bottom row
        venv_buttons2 = ttk.Frame(venvs_frame)
        venv_buttons2.pack(fill="x", pady=(0, 5))
        
        ttk.Button(venv_buttons2, text="Create New", command=self.create_venv).pack(side="left", padx=(0, 5))
        ttk.Button(venv_buttons2, text="Delete", command=self.delete_venv).pack(side="right")
        
        # Venvs list
        self.venvs_list = tk.Listbox(venvs_frame, height=10)
        self.venvs_list.pack(fill="both", expand=True)
        
        # Terminal frame (will be populated later)
        self.terminal_frame = ttk.Frame(main_frame)
        self.terminal_frame.pack(fill="both", expand=True, pady=(10, 0))
    
    def refresh_all(self):
        """Refresh all lists"""
        self.refresh_projects()
        self.refresh_venvs()
    
    def refresh_projects(self):
        """Refresh projects list"""
        self.projects_list.delete(0, tk.END)
        projects = self.project_manager.list_projects()
        active_project = self.config.config.get("active_project")
        
        for project in projects:
            venv = self.config.config["project_venv_mapping"].get(project)
            display = f"{project} -> {venv}" if venv else f"{project} (no venv)"
            if project == active_project:
                display = f"* {display}"
            self.projects_list.insert(tk.END, display)
    
    def refresh_venvs(self):
        """Refresh virtual environments list"""
        self.venvs_list.delete(0, tk.END)
        venvs = self.venv_manager.list_venvs()
        
        for venv in venvs:
            # Count projects using this venv
            count = sum(1 for v in self.config.config["project_venv_mapping"].values() if v == venv)
            display = f"{venv} ({count} project{'s' if count != 1 else ''})"
            if venv == self.terminal.active_venv:
                display = f"* {display}"
            self.venvs_list.insert(tk.END, display)
    
    # Event handlers
    def open_project(self):
        """Open selected project (just cd, no venv)"""
        selection = self.projects_list.curselection()
        if selection:
            display = self.projects_list.get(selection[0])
            name = display.split(" -> ")[0].split(" (no venv)")[0].lstrip("* ")
            if self.project_manager.open_project(name):
                self.refresh_projects()
    
    def create_project(self):
        """Create new project"""
        name = tk.simpledialog.askstring("Create Project", "Project name:")
        if name and name.strip():
            if self.project_manager.create_project(name.strip()):
                self.refresh_projects()
    
    def delete_project(self):
        """Delete selected project"""
        selection = self.projects_list.curselection()
        if selection:
            display = self.projects_list.get(selection[0])
            name = display.split(" -> ")[0].split(" (no venv)")[0].lstrip("* ")
            if self.project_manager.delete_project(name):
                self.refresh_all()
    
    def switch_project(self, event):
        """Switch to selected project"""
        selection = self.projects_list.curselection()
        if selection:
            display = self.projects_list.get(selection[0])
            name = display.split(" -> ")[0].split(" (no venv)")[0].lstrip("* ")
            if self.project_manager.switch_to_project(name):
                self.refresh_all()
    
    def change_venv(self):
        """Change virtual environment for selected project"""
        selection = self.projects_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a project first.")
            return
        
        display = self.projects_list.get(selection[0])
        project = display.split(" -> ")[0].split(" (no venv)")[0].lstrip("* ")
        
        # Simple dialog for venv selection
        available_venvs = self.venv_manager.list_venvs()
        if not available_venvs:
            messagebox.showinfo("No Virtual Environments", "Create a virtual environment first.")
            return
        
        # Create selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Virtual Environment")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Select venv for project '{project}':", padding=10).pack()
        
        var = tk.StringVar()
        for venv in available_venvs:
            ttk.Radiobutton(dialog, text=venv, variable=var, value=venv).pack(anchor="w", padx=20)
        
        ttk.Radiobutton(dialog, text="No virtual environment", variable=var, value="none").pack(anchor="w", padx=20)
        
        if available_venvs:
            var.set(available_venvs[0])
        
        def apply():
            selected = var.get()
            if selected == "none":
                if project in self.config.config["project_venv_mapping"]:
                    del self.config.config["project_venv_mapping"][project]
            else:
                self.config.config["project_venv_mapping"][project] = selected
            self.config.save_config()
            self.refresh_projects()
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Apply", command=apply).pack(side="right")
    
    def create_venv(self):
        """Create new virtual environment"""
        name = tk.simpledialog.askstring("Create Virtual Environment", "Virtual environment name:")
        if name and name.strip():
            if self.venv_manager.create_venv(name.strip()):
                self.root.after(2000, self.refresh_venvs)  # Refresh after creation
    
    def delete_venv(self):
        """Delete selected virtual environment"""
        selection = self.venvs_list.curselection()
        if selection:
            display = self.venvs_list.get(selection[0])
            name = display.split(" (")[0].lstrip("* ")
            if self.venv_manager.delete_venv(name):
                self.refresh_all()
    
    def activate_venv(self):
        """Activate selected virtual environment"""
        selection = self.venvs_list.curselection()
        if selection:
            display = self.venvs_list.get(selection[0])
            name = display.split(" (")[0].lstrip("* ")
            self.terminal.activate_venv(name)
            self.refresh_venvs()
    
    def deactivate_venv(self):
        """Deactivate current virtual environment"""
        self.terminal.deactivate_venv()
        self.refresh_venvs()
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.root, self.config)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            self.refresh_all()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Import simpledialog here to avoid circular imports
import tkinter.simpledialog

if __name__ == "__main__":
    app = MainGUI()
    app.run()
