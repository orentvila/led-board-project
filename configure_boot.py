#!/usr/bin/env python3
"""
Configuration script to set up LED board project to run on boot
This script creates a systemd service and enables it for automatic startup
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True, capture_output=False):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e}")
        if check:
            sys.exit(1)
        return e

def check_requirements():
    """Check if all requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check if running on Linux
    if sys.platform != 'linux':
        print("❌ This script is designed for Linux systems")
        sys.exit(1)
    
    # Check if running as non-root user
    if os.geteuid() == 0:
        print("❌ Please run this script as a regular user (not root)")
        sys.exit(1)
    
    # Get current directory
    project_dir = Path.cwd()
    print(f"📁 Project directory: {project_dir}")
    
    # Check if main.py exists
    main_file = project_dir / "main.py"
    if not main_file.exists():
        print("❌ main.py not found in current directory")
        print("   Please run this script from your project directory")
        sys.exit(1)
    
    # Check if virtual environment exists
    venv_python = project_dir / "venv" / "bin" / "python"
    if not venv_python.exists():
        print("❌ Virtual environment not found")
        print("   Please create a virtual environment first:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if systemctl is available
    if not shutil.which('systemctl'):
        print("❌ systemctl not found. This script requires systemd.")
        sys.exit(1)
    
    print("✅ All requirements met")
    return project_dir

def create_service_file(project_dir, main_file="main.py"):
    """Create the systemd service file."""
    print("📝 Creating systemd service file...")
    
    current_user = os.getenv('USER', 'led-board')
    project_path = str(project_dir)
    
    service_content = f"""[Unit]
Description=LED Board Display Application
After=network.target
Wants=network.target

[Service]
Type=simple
User={current_user}
Group={current_user}
WorkingDirectory={project_path}
ExecStart={project_path}/venv/bin/python {project_path}/{main_file}
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH={project_path}
Environment=DISPLAY=:0

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths={project_path}

[Install]
WantedBy=multi-user.target
"""
    
    # Write service file
    service_file = "/etc/systemd/system/led-board.service"
    try:
        with open(service_file, 'w') as f:
            f.write(service_content)
        print(f"✅ Service file created: {service_file}")
    except PermissionError:
        print("❌ Permission denied. Please run with sudo or as root")
        sys.exit(1)

def setup_service():
    """Set up and enable the systemd service."""
    print("🔧 Setting up systemd service...")
    
    # Reload systemd daemon
    print("🔄 Reloading systemd daemon...")
    run_command("sudo systemctl daemon-reload")
    
    # Enable the service
    print("🔗 Enabling LED board service...")
    run_command("sudo systemctl enable led-board.service")
    
    # Start the service
    print("🚀 Starting LED board service...")
    run_command("sudo systemctl start led-board.service")

def check_service_status():
    """Check and display service status."""
    print("📊 Checking service status...")
    
    # Get service status
    result = run_command("sudo systemctl status led-board.service --no-pager", 
                        check=False, capture_output=True)
    
    if result.returncode == 0:
        print("✅ Service is running successfully!")
        print(result.stdout)
    else:
        print("⚠️  Service may have issues:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)

def show_usage_instructions():
    """Show usage instructions for managing the service."""
    print("\n" + "="*60)
    print("📋 LED Board Service Management Commands:")
    print("="*60)
    print("Check status:    sudo systemctl status led-board")
    print("View logs:       sudo journalctl -u led-board -f")
    print("Stop service:    sudo systemctl stop led-board")
    print("Start service:   sudo systemctl start led-board")
    print("Restart service: sudo systemctl restart led-board")
    print("Disable service: sudo systemctl disable led-board")
    print("Enable service:  sudo systemctl enable led-board")
    print("\n🔍 To view real-time logs:")
    print("   sudo journalctl -u led-board -f")
    print("\n🔄 The service will now start automatically on boot!")

def main():
    """Main function."""
    print("🔧 LED Board Boot Configuration Script")
    print("="*50)
    
    # Check requirements
    project_dir = check_requirements()
    
    # Ask for main file name if needed
    main_file = "main.py"
    if len(sys.argv) > 1:
        main_file = sys.argv[1]
        if not (project_dir / main_file).exists():
            print(f"❌ File {main_file} not found in project directory")
            sys.exit(1)
    
    print(f"📄 Using main file: {main_file}")
    
    # Create service file
    create_service_file(project_dir, main_file)
    
    # Setup service
    setup_service()
    
    # Check status
    check_service_status()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n✅ LED Board boot configuration completed!")
    print("🎉 Your LED board will now start automatically on boot!")

if __name__ == "__main__":
    main()
