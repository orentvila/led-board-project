#!/bin/bash
# Start Final LED Program

echo "🚀 Starting Final LED Program..."
echo "=================================="

# Check if we're on Raspberry Pi or Windows
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Running on Linux (Raspberry Pi)"
    echo "Using virtual environment: ../venv/bin/python"
    cd "$(dirname "$0")"
    sudo ../venv/bin/python main_controller.py
else
    echo "🪟 Running on Windows (Development)"
    echo "Using virtual environment: ../venv/Scripts/python"
    cd "$(dirname "$0")"
    ../venv/Scripts/python main_controller.py
fi
