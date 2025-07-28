#!/bin/bash
# Fix Raspberry Pi Permission Issues for WS281x LED Strip
# Run this script on your Raspberry Pi

echo "🔧 Fixing Raspberry Pi Permission Issues for WS281x"
echo "=================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root (sudo). Run it as a regular user."
    exit 1
fi

echo "📋 Step 1: Adding user to required groups..."

# Add user to gpio group
sudo usermod -a -G gpio $USER

# Add user to spi group (sometimes needed)
sudo usermod -a -G spi $USER

# Add user to i2c group (sometimes needed)
sudo usermod -a -G i2c $USER

echo "📋 Step 2: Creating udev rules for GPIO access..."

# Create udev rules for GPIO memory access
sudo tee /etc/udev/rules.d/99-gpio.rules > /dev/null <<EOF
SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", ACTION=="add", PROGRAM="/bin/sh -c 'chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio'"
SUBSYSTEM=="gpio", KERNEL=="gpio*", ACTION=="add", PROGRAM="/bin/sh -c 'chown root:gpio /sys/%p/active_low /sys/%p/direction /sys/%p/edge /sys/%p/value /sys/%p/export /sys/%p/unexport ; chmod 660 /sys/%p/active_low /sys/%p/direction /sys/%p/edge /sys/%p/value /sys/%p/export /sys/%p/unexport'"
EOF

# Create udev rules for SPI access (if needed)
sudo tee /etc/udev/rules.d/99-spi.rules > /dev/null <<EOF
SUBSYSTEM=="spidev", GROUP="spi", MODE="0660"
EOF

echo "📋 Step 3: Setting proper permissions..."

# Set permissions for GPIO memory
sudo chmod 666 /dev/gpiomem 2>/dev/null || echo "⚠️  /dev/gpiomem not found (this is normal on some Pi models)"

# Set permissions for GPIO sysfs
sudo chmod -R 770 /sys/class/gpio 2>/dev/null || echo "⚠️  GPIO sysfs not accessible"

# Set permissions for SPI (if exists)
sudo chmod 666 /dev/spidev* 2>/dev/null || echo "⚠️  SPI devices not found (this is normal if not using SPI)"

echo "📋 Step 4: Reloading udev rules..."

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "📋 Step 5: Checking groups..."

# Check current user groups
echo "Current user groups:"
groups $USER

echo ""
echo "📋 Step 6: Testing GPIO access..."

# Test GPIO access
python3 -c "
import RPi.GPIO as GPIO
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()
    print('✅ GPIO access test: PASSED')
except Exception as e:
    print(f'❌ GPIO access test: FAILED - {e}')
"

echo ""
echo "📋 Step 7: Testing WS281x access..."

# Test WS281x access (with minimal LED count)
python3 -c "
from rpi_ws281x import PixelStrip, Color
import time

try:
    # Test with just 1 LED to avoid overwhelming output
    strip = PixelStrip(1, 21, 800000, 10, False, 255, 0)
    strip.begin()
    strip.setPixelColor(0, Color(255, 0, 0))
    strip.show()
    time.sleep(0.1)
    strip.setPixelColor(0, Color(0, 0, 0))
    strip.show()
    strip = None
    print('✅ WS281x access test: PASSED')
except Exception as e:
    print(f'❌ WS281x access test: FAILED - {e}')
    print('This might require a reboot to take effect')
"

echo ""
echo "📋 Step 8: Checking system configuration..."

# Check if SPI is enabled
if grep -q "dtparam=spi=on" /boot/config.txt; then
    echo "✅ SPI is enabled in /boot/config.txt"
else
    echo "⚠️  SPI not enabled in /boot/config.txt (not needed for WS281x)"
fi

# Check if I2C is enabled
if grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
    echo "✅ I2C is enabled in /boot/config.txt"
else
    echo "⚠️  I2C not enabled in /boot/config.txt (not needed for WS281x)"
fi

echo ""
echo "🎯 IMPORTANT: You need to REBOOT for all changes to take effect!"
echo ""
echo "Run this command to reboot:"
echo "sudo reboot"
echo ""
echo "After reboot, test your LED strip again:"
echo "python3 test_basic.py"
echo ""
echo "If you still get permission errors after reboot, try:"
echo "sudo chmod 666 /dev/gpiomem"
echo "sudo chmod 666 /dev/mem" 