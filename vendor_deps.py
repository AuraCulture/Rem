
"""
Automated script to vendor dependencies for remove-the-bg package.
This script downloads and copies required dependencies into the vendor directory.
"""

import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path


def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None


def copy_numpy_clean(source_dir, target_dir):
    """Copy numpy excluding source/build files that trigger source tree detection."""
    import fnmatch
    

    exclude_patterns = [
        "setup.py",
        "setup.cfg",
        "pyproject.toml",
        "meson.build",
        "meson_options.txt",
        "_build_utils",
        "tools/swig",
        "tools/travis*",
        "tools/ci",
        "tools/build_utils",
        "numpy.egg-info",
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".git*",
        "doc/",
        "docs/",
        "benchmarks/",
        "branding/",
        "tools/numpy*",
    ]
    
    def should_exclude(path, base_path):
        """Check if a path should be excluded."""
        rel_path = os.path.relpath(path, base_path)
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
        return False
    

    target_dir.mkdir(parents=True, exist_ok=True)
    

    for root, dirs, files in os.walk(source_dir):

        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), source_dir)]
        
        for file in files:
            src_path = os.path.join(root, file)
            if should_exclude(src_path, source_dir):
                continue
                
            rel_path = os.path.relpath(src_path, source_dir)
            dst_path = target_dir / rel_path
            

            dst_path.parent.mkdir(parents=True, exist_ok=True)
            

            shutil.copy2(src_path, dst_path)
    
    print(f"   Applied clean copying for numpy (excluded source files)")


def find_package_location(package_name, temp_dir):
    """Find the location of an installed package."""
    python_path = os.path.join(temp_dir, "Scripts", "python.exe") if os.name == "nt" else os.path.join(temp_dir, "bin", "python")
    if not os.path.exists(python_path):
        python_path = sys.executable
    
    command = f'"{python_path}" -c "import {package_name}; print({package_name}.__file__)"'
    result = run_command(command)
    
    if result:

        package_file = Path(result)
        if package_file.name == "__init__.py":
            return package_file.parent
        else:
            return package_file.parent.parent
    return None


def vendor_dependencies():
    """Main function to vendor all dependencies."""
    print("[START] Starting dependency vendoring process...")
    

    current_dir = Path(__file__).parent
    vendor_dir = current_dir / "remove_the_bg" / "vendor"
    

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        print(f"[TEMP] Using temporary directory: {temp_path}")
        

        dependencies = ["rembg", "Pillow", "numpy", "onnxruntime"]
        
        for dep in dependencies:
            print(f"[INSTALL] Installing {dep}...")
            cmd = f'pip install {dep} --target "{temp_path}"'
            if not run_command(cmd):
                print(f"[ERROR] Failed to install {dep}")
                return False
        

        package_mappings = {
            "rembg": "rembg",
            "PIL": "Pillow",
            "numpy": "numpy",
            "onnxruntime": "onnxruntime"
        }
        
        for import_name, package_name in package_mappings.items():
            print(f"[VENDOR] Vendoring {package_name} (import as {import_name})...")
            

            package_dirs = list(temp_path.glob(f"{import_name}*"))
            if not package_dirs:
                print(f"[ERROR] Could not find {import_name} in temporary directory")
                continue
            

            source_dir = package_dirs[0]
            target_dir = vendor_dir / import_name
            
            print(f"   Copying {source_dir} → {target_dir}")
            

            if target_dir.exists():
                shutil.rmtree(target_dir)
            

            if import_name == "numpy":
                copy_numpy_clean(source_dir, target_dir)
            else:
                shutil.copytree(source_dir, target_dir)
            print(f"[SUCCESS] Successfully vendored {import_name}")
        
        print("[COMPLETE] Dependency vendoring completed!")
        print(f"[INFO] Vendor directory size: {get_directory_size(vendor_dir):.1f} MB")
        
        return True


def get_directory_size(directory):
    """Calculate the total size of a directory in MB."""
    total_size = 0
    for path in Path(directory).rglob("*"):
        if path.is_file():
            total_size += path.stat().st_size
    return total_size / (1024 * 1024)


if __name__ == "__main__":
    print("[VENDOR] Remove-the-BG Dependency Vendoring Script")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("""
This script automatically vendors (bundles) all required dependencies
for the remove-the-bg package into the vendor/ directory.

Usage:
    python vendor_deps.py

Dependencies that will be vendored:
- rembg (background removal)
- Pillow (image processing)
- numpy (numerical operations)
- onnxruntime (model inference)

This ensures users can install your package with zero external dependencies.
        """)
        sys.exit(0)
    
    try:
        success = vendor_dependencies()
        if success:
            print("\n[SUCCESS] All dependencies have been successfully vendored!")
            print("[INFO] Your package is now self-contained and ready for distribution.")
        else:
            print("\n[ERROR] Vendoring process failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[CANCELLED] Vendoring cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
