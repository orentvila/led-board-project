#!/bin/bash
# Setup script to configure LED board project to run on boot
# Run this script with: sudo ./setup_boot_service.sh

set -e  # Exit on any error

echo "🔧 Setting up LED Board Project to run on boot..."

# Get the current directory (project root)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Get the current user (should be led-board)
CURRENT_USER=$(whoami)
echo "👤 Current user: $CURRENT_USER"

# Check if we're running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please run this script as a regular user (not root). The script will use sudo when needed."
    exit 1
fi

# Check if the project directory exists and has the required files
if [ ! -f "$PROJECT_DIR/main.py" ]; then
    echo "❌ Error: main.py not found in project directory"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/venv/bin/python" ]; then
    echo "❌ Error: Virtual environment not found. Please run the project setup first."
    exit 1
fi

echo "✅ Project files found"

# Create the systemd service file
echo "📝 Creating systemd service file..."

sudo tee /etc/systemd/system/led-board.service > /dev/null << EOF
[Unit]
Description=LED Board Display Application
After=network.target
Wants=network.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH=$PROJECT_DIR
Environment=DISPLAY=:0

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$PROJECT_DIR

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created"

# Reload systemd daemon
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service
echo "🔗 Enabling LED board service..."
sudo systemctl enable led-board.service

# Start the service
echo "🚀 Starting LED board service..."
sudo systemctl start led-board.service

# Check service status
echo "📊 Checking service status..."
sudo systemctl status led-board.service --no-pager

echo ""
echo "✅ LED Board service has been configured and started!"
echo ""
echo "📋 Useful commands:"
echo "  Check status:    sudo systemctl status led-board"
echo "  View logs:       sudo journalctl -u led-board -f"
echo "  Stop service:    sudo systemctl stop led-board"
echo "  Start service:   sudo systemctl start led-board"
echo "  Restart service: sudo systemctl restart led-board"
echo "  Disable service: sudo systemctl disable led-board"
echo ""
echo "🔄 The service will now start automatically on boot!"
echo "📱 Your LED board should be running now. Check the logs above for any issues."
