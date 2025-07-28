#!/bin/bash
# Fix rpi-ws281x import issues on Raspberry Pi
# Run this script on your Raspberry Pi

echo "🔧 Fixing rpi-ws281x import issues"
echo "=================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root (sudo). Run it as a regular user."
    exit 1
fi

echo "📋 Step 1: Checking current rpi-ws281x installation..."

# Check what's currently installed
python3 -c "
try:
    import rpi_ws281x
    print('✅ rpi_ws281x module found')
    print(f'Location: {rpi_ws281x.__file__}')
    print(f'Version: {rpi_ws281x.__version__ if hasattr(rpi_ws281x, \"__version__\") else \"Unknown\"}')
except ImportError as e:
    print(f'❌ rpi_ws281x not found: {e}')
"

echo ""
echo "📋 Step 2: Testing PixelStrip import..."

# Test PixelStrip import
python3 -c "
try:
    from rpi_ws281x import PixelStrip, Color
    print('✅ PixelStrip and Color imported successfully')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    print('This indicates an installation problem')
"

echo ""
echo "📋 Step 3: Uninstalling problematic installations..."

# Uninstall any existing rpi-ws281x installations
pip uninstall rpi-ws281x -y 2>/dev/null || echo "No pip installation found"
pip3 uninstall rpi-ws281x -y 2>/dev/null || echo "No pip3 installation found"
sudo pip3 uninstall rpi-ws281x -y 2>/dev/null || echo "No system-wide installation found"

echo ""
echo "📋 Step 4: Installing rpi-ws281x from source..."

# Navigate to home directory
cd ~

# Remove any existing source installation
rm -rf rpi_ws281x

# Clone the repository
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x

# Build the library
echo "Building rpi_ws281x library..."
sudo scons

# Install Python bindings
echo "Installing Python bindings..."
cd python
sudo python3 setup.py install

# Go back to project directory
cd ~/led-board-project

echo ""
echo "📋 Step 5: Testing the installation..."

# Test the installation
python3 -c "
try:
    from rpi_ws281x import PixelStrip, Color
    print('✅ PixelStrip and Color imported successfully!')
    
    # Test basic functionality
    strip = PixelStrip(1, 21, 800000, 10, False, 255, 0)
    strip.begin()
    strip.setPixelColor(0, Color(255, 0, 0))
    strip.show()
    import time
    time.sleep(0.1)
    strip.setPixelColor(0, Color(0, 0, 0))
    strip.show()
    print('✅ Basic functionality test passed!')
    
except ImportError as e:
    print(f'❌ Import still failed: {e}')
    print('Trying alternative installation method...')
    
    # Try alternative installation
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'rpi-ws281x'])
        from rpi_ws281x import PixelStrip, Color
        print('✅ Alternative installation successful!')
    except Exception as e2:
        print(f'❌ Alternative installation failed: {e2}')
        print('Manual intervention required')
"

echo ""
echo "📋 Step 6: Checking for common issues..."

# Check if we're on a Raspberry Pi
if [ -f "/proc/cpuinfo" ]; then
    if grep -q "Raspberry Pi" /proc/cpuinfo; then
        echo "✅ Running on Raspberry Pi"
    else
        echo "⚠️  Not running on Raspberry Pi - this library is Pi-specific"
    fi
else
    echo "⚠️  Cannot determine if running on Raspberry Pi"
fi

# Check Python version
echo "Python version: $(python3 --version)"

# Check if running in virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Running in virtual environment: $VIRTUAL_ENV"
else
    echo "⚠️  Not running in virtual environment"
fi

echo ""
echo "📋 Step 7: Alternative installation methods..."

echo "If the above didn't work, try these commands manually:"
echo ""
echo "Method 1 - Install via pip:"
echo "pip install rpi-ws281x"
echo ""
echo "Method 2 - Install system-wide:"
echo "sudo pip3 install rpi-ws281x"
echo ""
echo "Method 3 - Install in user space:"
echo "pip install --user rpi-ws281x"
echo ""
echo "Method 4 - Manual source installation:"
echo "cd ~"
echo "git clone https://github.com/jgarff/rpi_ws281x.git"
echo "cd rpi_ws281x"
echo "sudo scons"
echo "cd python"
echo "sudo python3 setup.py install"
echo ""
echo "After installation, test with:"
echo "python3 -c \"from rpi_ws281x import PixelStrip, Color; print('Success!')\"" 