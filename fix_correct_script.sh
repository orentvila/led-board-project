#!/bin/bash
# Fix Service to Run Correct Script
# This script will configure the service to run main_animation_controller.py instead of main.py

set -e

echo "🔧 Fixing Service to Run Correct Script"
echo "======================================"

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

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 Project directory: $PROJECT_DIR"

# Stop the current service
echo ""
echo "🛑 Stopping current service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Update service to run main_animation_controller.py
echo ""
echo "📝 Updating service to run main_animation_controller.py..."

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
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/main_animation_controller.py
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

print_status "Service updated to run main_animation_controller.py"

# Reload and start service
echo ""
echo "🔄 Reloading systemd and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable led-board.service
sudo systemctl start led-board.service
print_status "Service started with correct script"

# Check status
echo ""
echo "📊 Service status:"
sleep 3
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 15

echo ""
echo "="*60
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service is now running main_animation_controller.py!${NC}"
    echo -e "${GREEN}✅ Button support should work!${NC}"
    echo -e "${GREEN}✅ Animation switching should work!${NC}"
    echo -e "${GREEN}✅ Will start automatically on boot!${NC}"
else
    echo -e "${GREEN}⚠️  Check logs above for any issues${NC}"
fi
echo "="*60

echo ""
echo "🧪 To test:"
echo "1. Check if buttons work to switch animations"
echo "2. View logs: sudo journalctl -u led-board -f"
echo "3. Test manually: sudo ./venv/bin/python main_animation_controller.py"

