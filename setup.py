#!/usr/bin/env python3
"""Setup script for stock-eda environment using uv."""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def get_uv_path():
    """Find uv executable path."""
    # Check common locations
    possible_paths = [
        "uv",  # In PATH
        os.path.expanduser("~/.local/bin/uv"),  # Linux/Mac default
        os.path.expanduser("~/.cargo/bin/uv"),  # Alternative location
    ]

    for path in possible_paths:
        try:
            subprocess.run([path, "--version"], check=True, capture_output=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return None

def main():
    """Set up the development environment."""
    print("Stock EDA Environment Setup")
    print("="*60)

    # Find uv
    uv_cmd = get_uv_path()

    if uv_cmd is None:
        print("uv not found. Installing uv...")
        install_script = "curl -LsSf https://astral.sh/uv/install.sh | sh"
        result = subprocess.run(install_script, shell=True, capture_output=True, text=True)

        # Try to find uv again after installation
        uv_cmd = get_uv_path()

        if uv_cmd is None:
            print("\n⚠️  uv installation had issues. Falling back to pip + venv...")
            # Fallback to standard Python approach
            if not run_command("python3 -m venv .venv", "Creating virtual environment"):
                return False
            if not run_command(".venv/bin/pip install -e .", "Installing dependencies"):
                return False
            venv_python = ".venv/bin/python"
        else:
            print(f"✓ Found uv at: {uv_cmd}")
            # Create virtual environment
            if not run_command(f"{uv_cmd} venv", "Creating virtual environment"):
                return False
            # Install dependencies
            if not run_command(f"{uv_cmd} pip install -e .", "Installing dependencies"):
                return False
            venv_python = ".venv/bin/python"
    else:
        print(f"✓ Found uv at: {uv_cmd}")
        # Create virtual environment
        if not run_command(f"{uv_cmd} venv", "Creating virtual environment"):
            return False
        # Install dependencies
        if not run_command(f"{uv_cmd} pip install -e .", "Installing dependencies"):
            return False
        venv_python = ".venv/bin/python"

    # Setup Jupyter kernel
    venv_python = ".venv/bin/python" if os.path.exists(".venv/bin/python") else ".venv/Scripts/python.exe"
    if not run_command(f"{venv_python} -m ipykernel install --user --name=stock-eda",
                      "Setting up Jupyter kernel"):
        return False

    print("\n" + "="*60)
    print("Setup completed successfully!")
    print("="*60)
    print("\nTo activate the environment:")
    print("  source .venv/bin/activate  (Linux/Mac)")
    print("  .venv\\Scripts\\activate     (Windows)")
    print("\nTo start Jupyter:")
    print("  jupyter notebook")
    print("\nOpen 'stock_analysis.ipynb' and select 'stock-eda' kernel")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
