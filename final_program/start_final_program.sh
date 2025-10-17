#!/bin/bash
# Startup script for Final LED Program

echo "🚀 Starting Final LED Program..."
echo "=================================="

# Check if we're on Raspberry Pi or Windows
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Running on Linux (Raspberry Pi)"
    cd "$(dirname "$0")"
    sudo python3 main_controller.py
else
    echo "🪟 Running on Windows (Development)"
    cd "$(dirname "$0")"
    python main_controller.py
fi
