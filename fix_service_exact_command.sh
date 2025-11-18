#!/bin/bash
# Fix LED Board Service to use the exact working command
# This uses the exact command that works: sudo ./venv/bin/python main_animation_controller.py

set -e

echo "🔧 Fixing LED Board Service with Exact Working Command"
echo "======================================================"

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

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Current user: $CURRENT_USER"

# Check if the venv python exists
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    print_info "Found venv Python: $VENV_PYTHON"
else
    print_info "venv Python not found, checking for python3..."
    VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"
    if [ -f "$VENV_PYTHON" ]; then
        print_info "Found venv Python3: $VENV_PYTHON"
    else
        print_info "Using system Python as fallback"
        VENV_PYTHON=$(which python3)
    fi
fi

# Stop the current service
echo ""
echo "🛑 Stopping current service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Create service file with the exact working command
echo ""
echo "📝 Creating service file with exact working command..."

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
ExecStart=$VENV_PYTHON $PROJECT_DIR/main_animation_controller.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH=$PROJECT_DIR
Environment=DISPLAY=:0

# Security settings
NoNewPrivileges=false
PrivateTmp=false
ProtectSystem=false
ProtectHome=false

[Install]
WantedBy=multi-user.target
EOF

print_status "Service file created with: $VENV_PYTHON"

# Reload systemd
echo ""
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload
print_status "Systemd reloaded"

# Enable service
echo ""
echo "🔗 Enabling service for auto-start..."
sudo systemctl enable led-board.service
print_status "Service enabled"

# Start service
echo ""
echo "🚀 Starting LED board service..."
sudo systemctl start led-board.service
print_status "Service started"

# Wait and check status
echo ""
echo "📊 Checking service status..."
sleep 5

sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 15

echo ""
echo "="*60
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service is running with the exact working command!${NC}"
    echo -e "${GREEN}✅ Buttons should now work properly!${NC}"
    echo -e "${GREEN}✅ Service will start automatically on boot!${NC}"
else
    echo -e "${GREEN}⚠️  Check the logs above for any issues${NC}"
fi
echo "="*60

echo ""
echo "🧪 To test buttons:"
echo "1. Try pressing the buttons on your LED board"
echo "2. Check logs: sudo journalctl -u led-board -f"
echo "3. Test manually: sudo $VENV_PYTHON $PROJECT_DIR/main_animation_controller.py"
