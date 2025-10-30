#!/bin/bash
# Install rpi-ws281x library on Raspberry Pi

echo "🔧 Installing rpi-ws281x library on Raspberry Pi..."

# Update package list
sudo apt update

# Install required system dependencies
sudo apt install -y python3-dev python3-pip

# Install rpi-ws281x library
sudo pip3 install rpi-ws281x==4.3.4

echo "✅ rpi-ws281x installation completed!"
echo "You can now run the LED display application."
