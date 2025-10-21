@echo off
echo 🚀 Starting Final LED Program...
echo ==================================

echo 🪟 Running on Windows (Development)
echo Using virtual environment: ../venv/Scripts/python
cd /d "%~dp0"
..\venv\Scripts\python main_controller.py

pause
