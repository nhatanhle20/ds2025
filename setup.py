import os
import shutil
import subprocess

def install_dependencies():
    """Install required Python dependencies."""
    print("[Setup] Installing Python dependencies...")
    try:
        subprocess.check_call(["pip", "install", "mpi4py"])
        print("[Setup] Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print("[Setup] Failed to install dependencies:", e)
        exit(1)

def create_project_structure():
    """Create the directory structure for the project."""
    print("[Setup] Creating project directories...")
    dirs = ["src", "checkpoints", "logs"]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print("[Setup] Directories created!")

def copy_project_files():
    """Copy server and client code to the project directory."""
    print("[Setup] Copying project files...")
    files = {
        "server.py": "src/server.py",
        "client.py": "src/client.py",
    }
    for source, destination in files.items():
        if os.path.exists(source):
            shutil.copy(source, destination)
        else:
            print(f"[Setup] Warning: {source} not found! Skipping.")
    print("[Setup] Files copied!")

def display_instructions():
    """Display instructions to run the project."""
    instructions = """
[Setup Complete]

To run the project:
1. Navigate to the `src` directory:
   cd src

2. Start the server and clients using MPI:
   mpiexec -n <number_of_processes> python server.py

3. Ensure one process acts as the server and others as clients.

Note: Use the checkpoints directory to store persistent data.
"""
    print(instructions)

if __name__ == "__main__":
    print("[Setup] Starting project setup...")
    install_dependencies()
    create_project_structure()
    copy_project_files()
    display_instructions()
