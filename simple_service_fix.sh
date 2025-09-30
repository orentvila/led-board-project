#!/bin/bash
# Simple Service Fix - Just run the main script directly
# This bypasses the complex animation controller and runs the main.py directly

set -e

echo "🔧 Simple Service Fix - Running Main Script Directly"
echo "==================================================="

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

# Check what main files exist
echo ""
echo "🔍 Checking available main files..."
if [ -f "$PROJECT_DIR/main.py" ]; then
    print_info "Found main.py"
    MAIN_FILE="main.py"
elif [ -f "$PROJECT_DIR/main_animation_controller.py" ]; then
    print_info "Found main_animation_controller.py"
    MAIN_FILE="main_animation_controller.py"
else
    print_info "No main files found, will use main.py"
    MAIN_FILE="main.py"
fi

# Check Python executable
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    print_info "Using venv Python: $VENV_PYTHON"
    PYTHON_EXEC="$VENV_PYTHON"
else
    print_info "Using system Python"
    PYTHON_EXEC=$(which python3)
fi

# Stop current service
echo ""
echo "🛑 Stopping current service..."
sudo systemctl stop led-board.service 2>/dev/null || true
print_status "Service stopped"

# Create simple service file
echo ""
echo "📝 Creating simple service file..."

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
ExecStart=$PYTHON_EXEC $PROJECT_DIR/$MAIN_FILE
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH=$PROJECT_DIR
Environment=DISPLAY=:0

# Minimal security settings
NoNewPrivileges=false

[Install]
WantedBy=multi-user.target
EOF

print_status "Service file created"

# Reload and enable
echo ""
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl enable led-board.service
print_status "Service enabled"

# Start service
echo ""
echo "🚀 Starting service..."
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
    echo -e "${GREEN}🎉 Service is running!${NC}"
    echo -e "${GREEN}✅ LED board should be working now!${NC}"
    echo -e "${GREEN}✅ Will start automatically on boot!${NC}"
else
    echo -e "${GREEN}⚠️  Check logs above for issues${NC}"
fi
echo "="*50

echo ""
echo "🧪 To test:"
echo "1. Check if LEDs are working"
echo "2. Try buttons if available"
echo "3. View logs: sudo journalctl -u led-board -f"
echo "4. Test manually: $PYTHON_EXEC $PROJECT_DIR/$MAIN_FILE"
