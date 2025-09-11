#!/bin/bash
# Startup script for random animation controller

echo "Starting Random Animation Controller..."
echo "Press button on GPIO 18 to start random animations"
echo "Press Ctrl+C to exit"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run the random animation controller
sudo ./venv/bin/python random_animation_controller.py
