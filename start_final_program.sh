#!/bin/bash
# Start the final program from the root directory

echo "🚀 Starting Final LED Program..."
echo "=================================="

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Run the final program
sudo ./venv/bin/python final_program/main_controller.py
