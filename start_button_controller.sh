#!/bin/bash
# Startup script for Button LED Controller

echo "🚀 Starting Button LED Controller..."
echo "=================================="

# Check if we're on Raspberry Pi or Windows
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Running on Linux (Raspberry Pi)"
    python3 button_led_controller.py
else
    echo "🪟 Running on Windows (Development)"
    python button_led_controller.py
fi
