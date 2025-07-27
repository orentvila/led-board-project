#!/bin/bash

# LED Display Startup Script
# This script starts the LED display application

echo "Starting LED Display Application..."
echo "=================================="

# Check if running as root (needed for GPIO access)
if [ "$EUID" -ne 0 ]; then
    echo "Warning: This script should be run as root for GPIO access"
    echo "Run with: sudo ./start.sh"
    echo ""
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import rpi_ws281x, numpy, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
fi

# Check if SPI is enabled
if ! grep -q "spi" /boot/config.txt; then
    echo "Warning: SPI might not be enabled. Run 'sudo raspi-config' to enable SPI"
fi

# Start the application
echo "Starting LED display..."
python3 main.py

echo "Application stopped." 