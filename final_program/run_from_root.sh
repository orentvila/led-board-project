#!/bin/bash
# Run the final program from the root directory

echo "🚀 Starting Final LED Program from Root..."
echo "=========================================="

# Go to the root directory
cd "$(dirname "$0")/.."

# Run the final program
sudo ./venv/bin/python final_program/main_controller.py
