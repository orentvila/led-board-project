#!/bin/bash
# Automatic LED Board Boot Configuration Script
# This script configures everything automatically for main_animation_controller.py
# Run with: chmod +x auto_setup_boot.sh && ./auto_setup_boot.sh

set -e  # Exit on any error

echo "🚀 LED Board Automatic Boot Configuration"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Get the current directory (project root)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${BLUE}📁 Project directory: $PROJECT_DIR${NC}"

# Get the current user
CURRENT_USER=$(whoami)
echo -e "${BLUE}👤 Current user: $CURRENT_USER${NC}"

# Check if we're running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please run this script as a regular user (not root). The script will use sudo when needed."
    exit 1
fi

# Check if main_animation_controller.py exists
MAIN_FILE="main_animation_controller.py"
if [ ! -f "$PROJECT_DIR/$MAIN_FILE" ]; then
    print_warning "main_animation_controller.py not found, checking for main.py..."
    if [ -f "$PROJECT_DIR/main.py" ]; then
        MAIN_FILE="main.py"
        print_info "Using main.py instead"
    else
        print_error "Neither main_animation_controller.py nor main.py found in project directory"
        exit 1
    fi
else
    print_status "Found $MAIN_FILE"
fi

# Check if virtual environment exists
if [ ! -f "$PROJECT_DIR/venv/bin/python" ]; then
    print_error "Virtual environment not found. Please create it first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi
print_status "Virtual environment found"

# Check if systemctl is available
if ! command -v systemctl &> /dev/null; then
    print_error "systemctl not found. This script requires systemd."
    exit 1
fi
print_status "systemctl available"

echo ""
echo "🔧 Creating systemd service file..."

# Create the systemd service file
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
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/$MAIN_FILE
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

print_status "Service file created at /etc/systemd/system/led-board.service"

echo ""
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload
print_status "Systemd daemon reloaded"

echo ""
echo "🔗 Enabling LED board service..."
sudo systemctl enable led-board.service
print_status "Service enabled for auto-start on boot"

echo ""
echo "🚀 Starting LED board service..."
sudo systemctl start led-board.service
print_status "Service started"

echo ""
echo "📊 Checking service status..."
sleep 2  # Give the service a moment to start

# Check service status
if sudo systemctl is-active --quiet led-board.service; then
    print_status "Service is running successfully!"
else
    print_warning "Service may have issues starting"
fi

echo ""
echo "📋 Service Status:"
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "="*60
echo -e "${GREEN}🎉 LED Board Boot Configuration Complete!${NC}"
echo "="*60
echo ""
echo -e "${BLUE}📋 Management Commands:${NC}"
echo "  Check status:    sudo systemctl status led-board"
echo "  View logs:       sudo journalctl -u led-board -f"
echo "  Stop service:    sudo systemctl stop led-board"
echo "  Start service:   sudo systemctl start led-board"
echo "  Restart service: sudo systemctl restart led-board"
echo "  Disable service: sudo systemctl disable led-board"
echo ""
echo -e "${GREEN}🔄 Your LED board will now start automatically on boot!${NC}"
echo -e "${BLUE}📱 Check the status above to see if it's running properly.${NC}"
echo ""

# Show recent logs
echo -e "${BLUE}📄 Recent service logs:${NC}"
sudo journalctl -u led-board --no-pager -n 10

echo ""
echo -e "${GREEN}✅ Setup complete! Your LED board service is configured and running.${NC}"
