#!/bin/bash
# Quick fix for LED Board Service
# This will fix the service to use system Python and enable auto-start

set -e

echo "🔧 Quick Fix for LED Board Service"
echo "=================================="

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Get project directory and user
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER=$(whoami)
SYSTEM_PYTHON=$(which python3)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Current user: $CURRENT_USER"
echo "🐍 System Python: $SYSTEM_PYTHON"

# Stop the failing service
echo ""
echo "🛑 Stopping the failing service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Create the correct service file
echo ""
echo "📝 Creating correct service file..."

sudo tee /etc/systemd/system/led-board.service > /dev/null << EOF
[Unit]
Description=LED Board Display Application
After=network-online.target
Wants=network-online.target
After=multi-user.target

[Service]
Type=simple
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$SYSTEM_PYTHON $PROJECT_DIR/main_animation_controller.py
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

print_status "Service file created with system Python"

# Reload and enable
echo ""
echo "🔄 Reloading systemd and enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable led-board.service
print_status "Service enabled for auto-start"

# Start the service
echo ""
echo "🚀 Starting LED board service..."
sudo systemctl start led-board.service
print_status "Service started"

# Check status
echo ""
echo "📊 Service status:"
sleep 3
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 10

echo ""
echo "="*50
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service is now running and will start on boot!${NC}"
else
    echo -e "${GREEN}⚠️  Check the logs above for any remaining issues${NC}"
fi
echo "="*50
