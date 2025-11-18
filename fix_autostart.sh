#!/bin/bash
# Fix LED Board Service Auto-Start on Boot
# This script ensures the service starts automatically after reboot

set -e

echo "🔧 Fixing LED Board Auto-Start on Boot"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER=$(whoami)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Current user: $CURRENT_USER"

# Check current service status
echo ""
echo "📊 Current service status:"
sudo systemctl status led-board.service --no-pager -l

# Check if service is enabled
echo ""
echo "🔍 Checking if service is enabled for auto-start..."
if sudo systemctl is-enabled led-board.service >/dev/null 2>&1; then
    print_status "Service is already enabled for auto-start"
else
    print_warning "Service is not enabled for auto-start"
    echo "🔗 Enabling service for auto-start..."
    sudo systemctl enable led-board.service
    print_status "Service enabled for auto-start"
fi

# Check service dependencies
echo ""
echo "🔍 Checking service dependencies..."
echo "Network target status:"
sudo systemctl status network.target --no-pager || print_warning "Network target not available"

# Update service file to ensure proper boot sequence
echo ""
echo "📝 Updating service file for better boot compatibility..."

# Get system Python path
SYSTEM_PYTHON=$(which python3)
print_info "Using system Python: $SYSTEM_PYTHON"

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

print_status "Service file updated with better boot dependencies"

# Reload systemd
echo ""
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload
print_status "Systemd daemon reloaded"

# Re-enable the service
echo ""
echo "🔗 Re-enabling service for auto-start..."
sudo systemctl enable led-board.service
print_status "Service re-enabled for auto-start"

# Check enable status
echo ""
echo "🔍 Verifying service is enabled..."
if sudo systemctl is-enabled led-board.service; then
    print_status "✅ Service is properly enabled for auto-start"
else
    print_error "❌ Service is still not enabled"
    exit 1
fi

# Start the service now
echo ""
echo "🚀 Starting service now..."
sudo systemctl start led-board.service
print_status "Service started"

# Check final status
echo ""
echo "📊 Final service status:"
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 10

echo ""
echo "="*60
echo -e "${GREEN}🎉 Auto-start configuration complete!${NC}"
echo ""
echo -e "${BLUE}📋 What was fixed:${NC}"
echo "• Service is now enabled for auto-start on boot"
echo "• Updated dependencies to wait for network"
echo "• Service will start after multi-user.target"
echo ""
echo -e "${YELLOW}🧪 To test auto-start:${NC}"
echo "1. Reboot the system: sudo reboot"
echo "2. After reboot, check: sudo systemctl status led-board"
echo "3. View logs: sudo journalctl -u led-board -f"
echo ""
echo -e "${GREEN}✅ Your LED board will now start automatically on boot!${NC}"
echo "="*60
