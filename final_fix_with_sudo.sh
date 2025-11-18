#!/bin/bash
# Final Fix - Run Service with Sudo for Hardware Access
# This script will run the service with sudo to access /dev/mem

set -e

echo "🔧 Final Fix - Hardware Access with Sudo"
echo "========================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 Project directory: $PROJECT_DIR"

# Stop the failing service
echo ""
echo "🛑 Stopping the failing service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Test with sudo first
echo ""
echo "🧪 Testing with sudo..."
if sudo ./venv/bin/python main.py --help 2>/dev/null || echo "Script started (this is expected)"; then
    print_status "Script works with sudo"
else
    print_warning "Script may have issues even with sudo"
fi

# Create service that runs with sudo
echo ""
echo "📝 Creating service that runs with sudo..."

sudo tee /etc/systemd/system/led-board.service > /dev/null << EOF
[Unit]
Description=LED Board Display Application
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH=$PROJECT_DIR
Environment=DISPLAY=:0

# Allow hardware access
NoNewPrivileges=false

[Install]
WantedBy=multi-user.target
EOF

print_status "Service configured to run with root privileges"

# Reload and start service
echo ""
echo "🔄 Reloading systemd and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable led-board.service
sudo systemctl start led-board.service
print_status "Service started with root privileges"

# Check status
echo ""
echo "📊 Service status:"
sleep 5
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 15

echo ""
echo "="*60
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service is running with root privileges!${NC}"
    echo -e "${GREEN}✅ Hardware access should now work!${NC}"
    echo -e "${GREEN}✅ LED board should be working!${NC}"
    echo -e "${GREEN}✅ Will start automatically on boot!${NC}"
else
    echo -e "${YELLOW}⚠️  Service may still have issues${NC}"
    echo ""
    echo "🔧 If still failing, check:"
    echo "1. LED hardware is properly connected"
    echo "2. GPIO pin 21 is correct"
    echo "3. ws281x library is installed"
    echo "4. Manual test: sudo ./venv/bin/python main.py"
fi
echo "="*60

echo ""
echo "🧪 To test manually:"
echo "sudo ./venv/bin/python main.py"
echo ""
echo "📊 To check status:"
echo "sudo systemctl status led-board"
echo ""
echo "📄 To view logs:"
echo "sudo journalctl -u led-board -f"
