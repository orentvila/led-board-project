#!/bin/bash
# Start Final LED Program from Root Directory with Virtual Environment

echo "🚀 Starting Final LED Program from Root..."
echo "=========================================="

# Check if we're on Raspberry Pi or Windows
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Running on Linux (Raspberry Pi)"
    echo "Using virtual environment: ./venv/bin/python"
    sudo ./venv/bin/python final_main_controller.py
else
    echo "🪟 Running on Windows (Development)"
    echo "Using virtual environment: ./venv/Scripts/python"
    ./venv/Scripts/python final_main_controller.py
fi