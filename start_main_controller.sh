#!/bin/bash
# Startup script for main animation controller

echo "🎬 LED Display Main Animation Controller"
echo "========================================"
echo "Single script that runs continuously"
echo "Press button on GPIO 18 to switch animations"
echo "Press Ctrl+C to exit"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Check if scripts folder exists
if [ ! -d "scripts" ]; then
    echo "❌ Scripts folder not found!"
    echo "Please make sure all animation scripts are in the 'scripts/' folder"
    exit 1
fi

# Count available animations
animation_count=$(ls scripts/*_animation.py 2>/dev/null | wc -l)
echo "📁 Found $animation_count animation scripts in scripts/ folder"
echo ""

# Run the main animation controller
sudo ./venv/bin/python main_animation_controller.py
