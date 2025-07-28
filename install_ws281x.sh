#!/bin/bash
# Install rpi-ws281x and dependencies on Raspberry Pi
# Run this script on your Raspberry Pi

echo "🔧 Installing rpi-ws281x and dependencies on Raspberry Pi"
echo "========================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root (sudo). Run it as a regular user."
    exit 1
fi

echo "📋 Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

echo "📋 Step 2: Installing system dependencies..."
sudo apt install -y python3-pip python3-dev python3-venv
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y git

echo "📋 Step 3: Installing additional libraries..."
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev

echo "📋 Step 4: Setting up virtual environment..."
cd ~/led-board-project

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

echo "📋 Step 5: Upgrading pip..."
pip install --upgrade pip

echo "📋 Step 6: Installing rpi-ws281x..."

# Try installing from pip first
echo "Attempting to install rpi-ws281x from pip..."
pip install rpi-ws281x

# Check if installation was successful
python3 -c "import rpi_ws281x; print('✅ rpi-ws281x installed successfully from pip')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  pip installation failed, trying from source..."
    
    # Install from source
    cd ~
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    
    # Build the library
    sudo scons
    
    # Install Python bindings
    cd python
    sudo python3 setup.py install
    
    # Go back to project directory
    cd ~/led-board-project
    source venv/bin/activate
    
    # Test installation
    python3 -c "import rpi_ws281x; print('✅ rpi-ws281x installed successfully from source')" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Installation failed. Trying alternative method..."
        
        # Alternative: install in user space
        pip install --user rpi-ws281x
        
        # Test again
        python3 -c "import rpi_ws281x; print('✅ rpi-ws281x installed successfully (user space)')" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "❌ All installation methods failed. Please check your system."
            exit 1
        fi
    fi
fi

echo "📋 Step 7: Installing other requirements..."
pip install -r requirements.txt

echo "📋 Step 8: Testing installation..."

# Test basic imports
python3 -c "
try:
    import rpi_ws281x
    print('✅ rpi_ws281x import: SUCCESS')
except ImportError as e:
    print(f'❌ rpi_ws281x import: FAILED - {e}')

try:
    import RPi.GPIO as GPIO
    print('✅ RPi.GPIO import: SUCCESS')
except ImportError as e:
    print(f'❌ RPi.GPIO import: FAILED - {e}')

try:
    import numpy
    print('✅ numpy import: SUCCESS')
except ImportError as e:
    print(f'❌ numpy import: FAILED - {e}')

try:
    from PIL import Image
    print('✅ Pillow import: SUCCESS')
except ImportError as e:
    print(f'❌ Pillow import: FAILED - {e}')
"

echo "📋 Step 9: Testing WS281x functionality..."

# Test WS281x with minimal configuration
python3 -c "
from rpi_ws281x import PixelStrip, Color
import time

try:
    # Test with just 1 LED
    strip = PixelStrip(1, 21, 800000, 10, False, 255, 0)
    strip.begin()
    strip.setPixelColor(0, Color(255, 0, 0))  # Red
    strip.show()
    time.sleep(0.1)
    strip.setPixelColor(0, Color(0, 0, 0))    # Off
    strip.show()
    strip = None
    print('✅ WS281x functionality test: SUCCESS')
except Exception as e:
    print(f'❌ WS281x functionality test: FAILED - {e}')
    print('This might be a permission issue. Run the permission fix script.')
"

echo ""
echo "🎯 Installation completed!"
echo ""
echo "Next steps:"
echo "1. If you got permission errors, run: ./fix_pi_permissions.sh"
echo "2. Test your application: python3 main.py"
echo "3. If you still have issues, try: sudo python3 main.py (temporary)"
echo ""
echo "To activate the virtual environment in the future:"
echo "cd ~/led-board-project"
echo "source venv/bin/activate" 