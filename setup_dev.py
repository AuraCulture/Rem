#!/usr/bin/env python3
"""
Quick setup script for remove-the-bg development environment
"""

import os
import subprocess
import sys
import platform

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"[BUILD] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("[SETUP] Setting up remove-the-bg development environment...\n")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 9):
        print(f"[ERROR] Python 3.9+ required, but you have {python_version.major}.{python_version.minor}")
        sys.exit(1)
    
    print(f"[SUCCESS] Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Determine virtual environment activation command
    if platform.system() == "Windows":
        venv_activate = ".venv\\Scripts\\activate"
        python_cmd = ".venv\\Scripts\\python.exe"
    else:
        venv_activate = "source .venv/bin/activate"
        python_cmd = ".venv/bin/python"
    
    # Setup steps
    steps = [
        ("python -m venv .venv", "Creating virtual environment"),
        (f"{python_cmd} -m pip install --upgrade pip", "Upgrading pip"),
        (f"{python_cmd} -m pip install -r requirements.txt", "Installing dependencies"),
        (f"{python_cmd} vendor_deps.py", "Vendoring dependencies"),
        (f"{python_cmd} build.py", "Building package"),
        (f"{python_cmd} test.py", "Running tests"),
    ]
    
    success_count = 0
    for cmd, desc in steps:
        if run_command(cmd, desc):
            success_count += 1
        else:
            print(f"\n[ERROR] Setup failed at step: {desc}")
            sys.exit(1)
        print()
    
    print("[SUCCESS] Setup completed successfully!")
    print("\n[NEXT] Next steps:")
    print(f"1. Activate virtual environment: {venv_activate}")
    print("2. Make your changes to the code")
    print("3. Test your changes: python test.py")
    print("4. Build package: python build.py")
    print("5. Submit a pull request")
    print("\n[INFO] See DEVELOPMENT.md for detailed development guide")

if __name__ == "__main__":
    main()
