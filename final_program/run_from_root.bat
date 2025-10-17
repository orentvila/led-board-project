@echo off
echo 🚀 Starting Final LED Program from Root...
echo ==========================================

cd /d "%~dp0\.."
sudo ./venv/bin/python final_program/main_controller.py

pause
