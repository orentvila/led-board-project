# Raspberry Pi Setup Guide

## Prerequisites

- Raspberry Pi with Raspberry Pi OS (Raspbian)
- Internet connection
- SSH access (recommended)

## Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Python Dependencies

```bash
# Install system dependencies
sudo apt install -y python3-pip python3-dev python3-venv

# Install required system packages for WS281x
sudo apt install -y build-essential cmake pkg-config

# Install additional libraries
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev
```

## Step 3: Setup Virtual Environment

```bash
cd ~/led-board-project
python3 -m venv venv
source venv/bin/activate
```

## Step 4: Install Python Packages

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements (including Raspberry Pi specific packages)
pip install -r requirements.txt
```

## Step 5: Configure GPIO Access

```bash
# Add your user to the gpio group
sudo usermod -a -G gpio $USER

# Create udev rules for GPIO access
echo 'SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/99-gpio.rules

# Reload udev rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

## Step 6: Test Installation

```bash
# Test basic functionality
python3 test_basic.py

# Test display patterns
python3 test_display.py
```

## Step 7: Run the Application

```bash
# Run the main application
python3 main.py
```

## Troubleshooting

### Permission Issues
If you get permission errors:
```bash
sudo chmod 666 /dev/gpiomem
```

### WS281x Installation Issues
If rpi-ws281x fails to install:
```bash
# Install from source
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo scons
cd python
sudo python3 setup.py install
```

### GPIO Issues
If GPIO access fails:
```bash
# Check if user is in gpio group
groups $USER

# Reboot if needed
sudo reboot
```

## Hardware Testing

### Test LED Strip
```bash
# Simple LED test
python3 -c "
from rpi_ws281x import PixelStrip, Color
import time

strip = PixelStrip(1280, 21, 800000, 10, False, 255, 0)
strip.begin()

# Test red color
for i in range(1280):
    strip.setPixelColor(i, Color(255, 0, 0))
strip.show()
time.sleep(2)

# Clear
for i in range(1280):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()
"
```

### Test Buttons
```bash
# Simple button test
python3 -c "
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Press button on GPIO 17...')
while True:
    if GPIO.input(17) == GPIO.LOW:
        print('Button pressed!')
        break
    time.sleep(0.1)
"
```

## Service Setup (Optional)

To run as a system service:

```bash
# Copy service file
sudo cp led-display.service /etc/systemd/system/

# Enable and start service
sudo systemctl enable led-display.service
sudo systemctl start led-display.service

# Check status
sudo systemctl status led-display.service
``` 