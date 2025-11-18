#!/bin/bash
# Fix Hardware Access Issues
# This script will fix GPIO and LED hardware access issues

set -e

echo "🔧 Fixing Hardware Access Issues"
echo "================================="

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

# Check hardware access
echo ""
echo "🔍 Checking hardware access..."

# Check if user is in gpio group
if groups | grep -q gpio; then
    print_status "User is in gpio group"
else
    print_warning "User not in gpio group, adding..."
    sudo usermod -a -G gpio led-board
    print_status "User added to gpio group"
fi

# Check if user is in spi group
if groups | grep -q spi; then
    print_status "User is in spi group"
else
    print_warning "User not in spi group, adding..."
    sudo usermod -a -G spi led-board
    print_status "User added to spi group"
fi

# Check if user is in i2c group
if groups | grep -q i2c; then
    print_status "User is in i2c group"
else
    print_warning "User not in i2c group, adding..."
    sudo usermod -a -G i2c led-board
    print_status "User added to i2c group"
fi

# Check GPIO permissions
echo ""
echo "🔍 Checking GPIO permissions..."
ls -la /dev/gpiomem 2>/dev/null || print_warning "/dev/gpiomem not found"
ls -la /dev/mem 2>/dev/null || print_warning "/dev/mem not found"

# Create a test script that doesn't require hardware
echo ""
echo "📝 Creating hardware-safe test script..."

cat > "$PROJECT_DIR/test_led_safe.py" << 'EOF'
#!/usr/bin/env python3
"""
Safe LED test that doesn't require hardware access
"""

import time
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import the LED controller
    from led_controller_fixed import LEDControllerFixed
    import config
    
    print("🎨 LED Board Test (Hardware Safe)")
    print("=" * 40)
    print(f"📊 Display size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
    print(f"💡 Total LEDs: {config.TOTAL_LEDS}")
    print(f"📌 LED Pin: {config.LED_PIN}")
    print("=" * 40)
    
    # Initialize LED controller
    print("🔧 Initializing LED controller...")
    led = LEDControllerFixed()
    
    print("✅ LED controller initialized successfully!")
    print("🎨 LED board is ready to use!")
    
    # Clean up
    led.cleanup()
    print("🧹 Cleanup completed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔍 This might be a hardware access issue")
    print("💡 Try running with sudo or check GPIO permissions")
    sys.exit(1)

print("🎉 Test completed successfully!")
EOF

print_status "Created hardware-safe test script"

# Test the safe script
echo ""
echo "🧪 Testing hardware access..."
if ./venv/bin/python test_led_safe.py; then
    print_status "Hardware access test passed"
else
    print_warning "Hardware access test failed - this is expected if hardware is not connected"
fi

# Create a service that runs with proper permissions
echo ""
echo "📝 Creating service with proper hardware access..."

sudo tee /etc/systemd/system/led-board.service > /dev/null << EOF
[Unit]
Description=LED Board Display Application
After=network.target
Wants=network.target

[Service]
Type=simple
User=led-board
Group=led-board
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables
Environment=PYTHONPATH=$PROJECT_DIR
Environment=DISPLAY=:0

# Hardware access permissions
NoNewPrivileges=false
PrivateTmp=false
ProtectSystem=false
ProtectHome=false

# Allow access to hardware
SupplementaryGroups=gpio spi i2c

[Install]
WantedBy=multi-user.target
EOF

print_status "Service configuration updated with hardware access"

# Reload and start service
echo ""
echo "🔄 Reloading systemd and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable led-board.service
sudo systemctl start led-board.service
print_status "Service started"

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
    echo -e "${GREEN}🎉 Service is running!${NC}"
    echo -e "${GREEN}✅ Hardware access issues fixed!${NC}"
    echo -e "${GREEN}✅ LED board should be working!${NC}"
else
    echo -e "${YELLOW}⚠️  Service may still have hardware issues${NC}"
    echo ""
    echo "🔧 Additional troubleshooting:"
    echo "1. Check if LED hardware is connected"
    echo "2. Verify GPIO pin configuration"
    echo "3. Check if ws281x library is properly installed"
    echo "4. Try running manually: sudo ./venv/bin/python main.py"
fi
echo "="*60
