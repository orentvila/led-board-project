# Quick Fix for WS281x Permission Issues

## 🚨 Immediate Fix (Run these commands on your Raspberry Pi)

### Step 1: Fix Memory Access Permissions
```bash
# Fix GPIO memory access
sudo chmod 666 /dev/gpiomem

# Fix general memory access (if needed)
sudo chmod 666 /dev/mem
```

### Step 2: Add User to GPIO Group
```bash
# Add your user to the gpio group
sudo usermod -a -G gpio $USER

# Check if it worked
groups $USER
```

### Step 3: Create Proper Udev Rules
```bash
# Create udev rules for GPIO access
echo 'SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/99-gpio.rules

# Reload udev rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### Step 4: REBOOT (Important!)
```bash
sudo reboot
```

### Step 5: Test After Reboot
```bash
# Test basic functionality
python3 test_basic.py

# Test your main application
python3 main.py
```

## 🔧 Alternative Solutions

### If the above doesn't work, try running as root (temporary fix):
```bash
sudo python3 main.py
```

### If you get SPI errors, enable SPI:
```bash
sudo raspi-config
# Navigate to: Interface Options > SPI > Enable
```

### Check your GPIO pin configuration:
```bash
# Make sure you're using the correct pin (GPIO 21 in your config)
gpio readall
```

## 🐛 Common Error Messages and Solutions

### "Can't open /dev/mem: Permission denied"
- **Solution**: `sudo chmod 666 /dev/mem`

### "ws2811_init failed with code -5 (mmap() failed)"
- **Solution**: `sudo chmod 666 /dev/gpiomem` and reboot

### "Segmentation fault"
- **Solution**: Check your LED count and pin configuration
- Make sure `TOTAL_LEDS` matches your actual hardware

### "No module named 'rpi_ws281x'"
- **Solution**: `pip install rpi-ws281x`

## 📋 Complete Fix Script

If you want to run the complete automated fix:

```bash
# Make the script executable
chmod +x fix_pi_permissions.sh

# Run the fix script
./fix_pi_permissions.sh
```

## 🔍 Debugging Steps

### Check your hardware connections:
1. **LED Data Pin**: GPIO 21 (Pin 40 on Pi)
2. **Power**: 5V for LED strips
3. **Ground**: Common ground between Pi and LED strips

### Check your configuration:
```python
# In config.py, verify these settings:
LED_PIN = 21          # GPIO pin for LED data
TOTAL_LEDS = 1280     # Total number of LEDs
BRIGHTNESS = 0.3      # Brightness level (0.0 to 1.0)
```

### Test with minimal configuration:
```python
# Test with just 1 LED first
from rpi_ws281x import PixelStrip, Color
import time

strip = PixelStrip(1, 21, 800000, 10, False, 255, 0)
strip.begin()
strip.setPixelColor(0, Color(255, 0, 0))  # Red
strip.show()
time.sleep(1)
strip.setPixelColor(0, Color(0, 0, 0))    # Off
strip.show()
```

## 🎯 Most Common Solution

**90% of the time, this fixes it:**
```bash
sudo chmod 666 /dev/gpiomem
sudo usermod -a -G gpio $USER
sudo reboot
```

After reboot, try running your application again! 