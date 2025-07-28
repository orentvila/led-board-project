# Fix rpi-ws281x Import Issues

## 🚨 Quick Fix for "cannot import name 'PixelStrip'" Error

This error occurs when `rpi_ws281x` is installed but the `PixelStrip` class can't be imported. Here's how to fix it:

### **Step 1: Check Current Installation**
```bash
# Check if rpi_ws281x is installed
python3 -c "import rpi_ws281x; print('Module found')"

# Check what's available in the module
python3 -c "import rpi_ws281x; print(dir(rpi_ws281x))"
```

### **Step 2: Uninstall Problematic Installation**
```bash
# Remove all existing installations
pip uninstall rpi-ws281x -y
pip3 uninstall rpi-ws281x -y
sudo pip3 uninstall rpi-ws281x -y
```

### **Step 3: Install from Source (Recommended)**
```bash
# Navigate to home directory
cd ~

# Clone the repository
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x

# Build the library
sudo scons

# Install Python bindings
cd python
sudo python3 setup.py install

# Go back to your project
cd ~/led-board-project
```

### **Step 4: Test the Installation**
```bash
# Test import
python3 -c "from rpi_ws281x import PixelStrip, Color; print('✅ Success!')"

# Test basic functionality
python3 -c "
from rpi_ws281x import PixelStrip, Color
import time

strip = PixelStrip(1, 21, 800000, 10, False, 255, 0)
strip.begin()
strip.setPixelColor(0, Color(255, 0, 0))
strip.show()
time.sleep(0.1)
strip.setPixelColor(0, Color(0, 0, 0))
strip.show()
print('✅ Functionality test passed!')
"
```

## 🔧 Alternative Installation Methods

### **Method 1: Install via pip**
```bash
pip install rpi-ws281x
```

### **Method 2: Install system-wide**
```bash
sudo pip3 install rpi-ws281x
```

### **Method 3: Install in user space**
```bash
pip install --user rpi-ws281x
```

## 🐛 Common Issues and Solutions

### **Issue: "unknown location" error**
- **Cause**: Corrupted or incomplete installation
- **Solution**: Uninstall and reinstall from source

### **Issue: Import works but PixelStrip not found**
- **Cause**: Wrong version or incomplete installation
- **Solution**: Install from source (Step 3 above)

### **Issue: Compilation errors during source installation**
- **Cause**: Missing build tools
- **Solution**: 
```bash
sudo apt install build-essential cmake pkg-config
```

### **Issue: Permission errors during installation**
- **Cause**: Insufficient permissions
- **Solution**: Use sudo for system-wide installation

## 🔍 Debugging Steps

### **Check Python Environment**
```bash
# Check Python version
python3 --version

# Check if in virtual environment
echo $VIRTUAL_ENV

# Check pip installation location
pip show rpi-ws281x
```

### **Check Module Contents**
```bash
# See what's actually in the module
python3 -c "
import rpi_ws281x
print('Available attributes:')
for attr in dir(rpi_ws281x):
    if not attr.startswith('_'):
        print(f'  {attr}')
"
```

### **Check for Multiple Installations**
```bash
# Find all rpi_ws281x installations
find /usr -name "*ws281x*" 2>/dev/null
find ~/.local -name "*ws281x*" 2>/dev/null
```

## 🎯 Most Common Solution

**90% of the time, this fixes it:**
```bash
# 1. Uninstall everything
pip uninstall rpi-ws281x -y
sudo pip3 uninstall rpi-ws281x -y

# 2. Install from source
cd ~
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo scons
cd python
sudo python3 setup.py install

# 3. Test
python3 -c "from rpi_ws281x import PixelStrip, Color; print('Success!')"
```

## 📋 Complete Fix Script

Run the automated fix script:
```bash
chmod +x fix_ws281x_import.sh
./fix_ws281x_import.sh
```

After fixing the import issue, you should be able to run your LED board project successfully! 