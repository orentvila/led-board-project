#!/bin/bash
# Fix LED Board Service Path Issue
# This script fixes the virtual environment path issue

set -e

echo "🔧 Fixing LED Board Service Path Issue"
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

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CURRENT_USER=$(whoami)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Current user: $CURRENT_USER"

# Stop the failing service first
echo ""
echo "🛑 Stopping the failing service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Check what Python executables exist
echo ""
echo "🔍 Checking available Python executables..."

# Check system Python
if command -v python3 &> /dev/null; then
    SYSTEM_PYTHON=$(which python3)
    print_info "System Python found: $SYSTEM_PYTHON"
else
    print_error "System Python3 not found"
    exit 1
fi

# Check virtual environment
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    print_status "Virtual environment Python found: $VENV_PYTHON"
    USE_VENV=true
else
    print_warning "Virtual environment Python not found at: $VENV_PYTHON"
    USE_VENV=false
fi

# Check if venv/bin/python3 exists
VENV_PYTHON3="$PROJECT_DIR/venv/bin/python3"
if [ -f "$VENV_PYTHON3" ]; then
    print_status "Virtual environment Python3 found: $VENV_PYTHON3"
    USE_VENV=true
    VENV_PYTHON="$VENV_PYTHON3"
fi

# Check if venv exists but python is missing
if [ -d "$PROJECT_DIR/venv" ] && [ ! -f "$VENV_PYTHON" ]; then
    print_warning "Virtual environment directory exists but Python executable is missing"
    print_info "This might be a Windows-created venv. Let's check what's in venv/bin/"
    ls -la "$PROJECT_DIR/venv/bin/" 2>/dev/null || print_error "venv/bin directory not accessible"
fi

# Determine which Python to use
if [ "$USE_VENV" = true ] && [ -f "$VENV_PYTHON" ]; then
    PYTHON_EXEC="$VENV_PYTHON"
    print_status "Using virtual environment Python: $PYTHON_EXEC"
else
    PYTHON_EXEC="$SYSTEM_PYTHON"
    print_warning "Using system Python: $PYTHON_EXEC"
    print_info "Note: You may want to recreate your virtual environment"
fi

# Test the Python executable
echo ""
echo "🧪 Testing Python executable..."
if $PYTHON_EXEC --version; then
    print_status "Python executable works"
else
    print_error "Python executable failed"
    exit 1
fi

# Update the service file
echo ""
echo "📝 Updating service file with correct Python path..."

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
ExecStart=$PYTHON_EXEC $PROJECT_DIR/main_animation_controller.py
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

print_status "Service file updated with Python path: $PYTHON_EXEC"

# Reload systemd
echo ""
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload
print_status "Systemd daemon reloaded"

# Start the service
echo ""
echo "🚀 Starting LED board service..."
sudo systemctl start led-board.service
print_status "Service started"

# Check status
echo ""
echo "📊 Checking service status..."
sleep 3

if sudo systemctl is-active --quiet led-board.service; then
    print_status "✅ Service is now running successfully!"
else
    print_warning "⚠️  Service may still have issues"
fi

echo ""
echo "📋 Current Service Status:"
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 10

echo ""
echo "="*60
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service fixed and running!${NC}"
else
    echo -e "${YELLOW}⚠️  Service may need additional troubleshooting${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Check logs: sudo journalctl -u led-board -f"
    echo "2. Test manually: $PYTHON_EXEC $PROJECT_DIR/main_animation_controller.py"
    echo "3. Check file permissions and dependencies"
fi
echo "="*60
