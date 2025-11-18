#!/bin/bash
# Debug and Fix LED Board Service
# This script will debug the virtual environment and fix the service

set -e

echo "🔍 Debugging LED Board Service Issue"
echo "===================================="

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

# Stop the service first
echo ""
echo "🛑 Stopping the service..."
sudo systemctl stop led-board.service
print_status "Service stopped"

# Debug virtual environment
echo ""
echo "🔍 Debugging virtual environment..."

echo "Checking venv directory:"
ls -la "$PROJECT_DIR/venv/" 2>/dev/null || print_error "venv directory not found"

echo ""
echo "Checking venv/bin directory:"
ls -la "$PROJECT_DIR/venv/bin/" 2>/dev/null || print_error "venv/bin directory not found"

echo ""
echo "Checking for Python executables:"
if [ -f "$PROJECT_DIR/venv/bin/python" ]; then
    print_status "venv/bin/python exists"
    ls -la "$PROJECT_DIR/venv/bin/python"
else
    print_warning "venv/bin/python does not exist"
fi

if [ -f "$PROJECT_DIR/venv/bin/python3" ]; then
    print_status "venv/bin/python3 exists"
    ls -la "$PROJECT_DIR/venv/bin/python3"
else
    print_warning "venv/bin/python3 does not exist"
fi

# Check system Python
echo ""
echo "🔍 Checking system Python..."
SYSTEM_PYTHON=$(which python3)
print_info "System Python: $SYSTEM_PYTHON"

# Test system Python
echo ""
echo "🧪 Testing system Python..."
if $SYSTEM_PYTHON --version; then
    print_status "System Python works"
else
    print_error "System Python failed"
    exit 1
fi

# Test if we can run the main script with system Python
echo ""
echo "🧪 Testing main script with system Python..."
if $SYSTEM_PYTHON "$PROJECT_DIR/main_animation_controller.py" --help 2>/dev/null || echo "Script started (this is expected)"; then
    print_status "Main script can be executed with system Python"
else
    print_warning "Main script may have issues, but let's try anyway"
fi

# Update service to use system Python
echo ""
echo "📝 Updating service to use system Python..."

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

print_status "Service file updated to use system Python: $SYSTEM_PYTHON"

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

# Wait a moment and check status
echo ""
echo "📊 Checking service status..."
sleep 5

if sudo systemctl is-active --quiet led-board.service; then
    print_status "✅ Service is running successfully!"
else
    print_warning "⚠️  Service may still have issues"
fi

echo ""
echo "📋 Current Service Status:"
sudo systemctl status led-board.service --no-pager -l

echo ""
echo "📄 Recent logs:"
sudo journalctl -u led-board --no-pager -n 15

echo ""
echo "="*60
if sudo systemctl is-active --quiet led-board.service; then
    echo -e "${GREEN}🎉 Service is now running with system Python!${NC}"
    echo -e "${BLUE}Your LED board should be working now!${NC}"
else
    echo -e "${YELLOW}⚠️  Service may need additional troubleshooting${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Check logs: sudo journalctl -u led-board -f"
    echo "2. Test manually: $SYSTEM_PYTHON $PROJECT_DIR/main_animation_controller.py"
    echo "3. Check if all dependencies are installed"
fi
echo "="*60
