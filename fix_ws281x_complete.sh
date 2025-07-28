#!/bin/bash
# Complete fix for rpi-ws281x import issues
# Run this script on your Raspberry Pi

echo "🔧 Complete Fix for rpi-ws281x Import Issues"
echo "============================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root (sudo). Run it as a regular user."
    exit 1
fi

echo "📋 Step 1: Finding your project directory..."

# Try to find the project directory
PROJECT_DIR=""
if [ -d "/home/led-board/Desktop/led-board-project" ]; then
    PROJECT_DIR="/home/led-board/Desktop/led-board-project"
    echo "✅ Found project at: $PROJECT_DIR"
elif [ -d "/home/led-board/led-board-project" ]; then
    PROJECT_DIR="/home/led-board/led-board-project"
    echo "✅ Found project at: $PROJECT_DIR"
elif [ -d "$HOME/led-board-project" ]; then
    PROJECT_DIR="$HOME/led-board-project"
    echo "✅ Found project at: $PROJECT_DIR"
else
    echo "❌ Project directory not found. Please navigate to your project directory manually."
    echo "Current directory: $(pwd)"
    echo "Available directories:"
    ls -la
    exit 1
fi

cd "$PROJECT_DIR"
echo "✅ Navigated to project directory: $(pwd)"

echo ""
echo "📋 Step 2: Installing system dependencies..."

# Install build tools and dependencies
sudo apt update
sudo apt install -y build-essential cmake pkg-config scons git

echo ""
echo "📋 Step 3: Setting up virtual environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

echo ""
echo "📋 Step 4: Uninstalling problematic rpi-ws281x installations..."

# Uninstall any existing installations
pip uninstall rpi-ws281x -y 2>/dev/null || echo "No pip installation found"
pip3 uninstall rpi-ws281x -y 2>/dev/null || echo "No pip3 installation found"
sudo pip3 uninstall rpi-ws281x -y 2>/dev/null || echo "No system-wide installation found"

echo ""
echo "📋 Step 5: Installing rpi-ws281x from source..."

# Navigate to home directory
cd ~

# Remove any existing source installation
rm -rf rpi_ws281x

# Clone the repository
echo "Cloning rpi_ws281x repository..."
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
cd "$PROJECT_DIR"
source venv/bin/activate

echo ""
echo "📋 Step 6: Installing other requirements..."

# Install other requirements
pip install numpy Pillow

echo ""
echo "📋 Step 7: Testing the installation..."

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
    print(f'❌ Import failed: {e}')
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
echo "📋 Step 8: Testing your project..."

# Test the main application
if [ -f "main.py" ]; then
    echo "Testing main.py..."
    python3 -c "
try:
    from led_controller import LEDController
    print('✅ LEDController imported successfully!')
except Exception as e:
    print(f'❌ LEDController import failed: {e}')
"
else
    echo "⚠️  main.py not found in current directory"
fi

echo ""
echo "🎯 Installation completed!"
echo ""
echo "Next steps:"
echo "1. If you got permission errors, run: ./fix_pi_permissions.sh"
echo "2. Test your application: python3 main.py"
echo "3. If you still have issues, try: sudo python3 main.py (temporary)"
echo ""
echo "To activate the virtual environment in the future:"
echo "cd $PROJECT_DIR"
echo "source venv/bin/activate" 