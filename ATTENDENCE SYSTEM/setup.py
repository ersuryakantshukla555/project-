#!/usr/bin/env python3
"""
Setup script for Attendance Management System
This script helps install dependencies and set up the system
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def create_directories():
    """Create necessary directories"""
    directories = ["exports", "static/css"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")

def main():
    print("🚀 Setting up Attendance Management System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Make sure MySQL is running on your system")
    print("2. Update database credentials in app.py if needed")
    print("3. Run: python database_setup.py")
    print("4. Run: python app.py")
    print("5. Open your browser and go to: http://localhost:5000")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main()
