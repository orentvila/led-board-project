# Windows Development Setup

This guide explains how to set up and use the LED Board Project for development on Windows.

## Overview

The LED Board Project is designed to run on Raspberry Pi hardware, but you can develop and test the code structure on Windows using mock modules that simulate the hardware behavior.

## Prerequisites

- Python 3.8 or higher
- Windows 10/11
- PowerShell

## Setup Instructions

### 1. Clone or Download the Project

Make sure you have the project files in your desired directory:
```
C:\Users\Oren\OneDrive\Documents\GitHub\led-board-project\
```

### 2. Create Virtual Environment

Open PowerShell in the project directory and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the Windows-compatible dependencies:

```powershell
pip install -r requirements-dev.txt
python -m pip install --upgrade pip
```

### 4. Verify Setup

Run the test script to verify everything is working:

```powershell
python test_windows.py
```

You should see all tests pass with the message:
```
🎉 All tests passed! Windows development environment is ready.
```

## Project Structure

### Core Files
- `main.py` - Main application entry point
- `led_controller.py` - LED display controller
- `button_controller.py` - Button input controller
- `display_patterns.py` - LED pattern implementations
- `config.py` - Configuration settings

### Development Files
- `mock_rpi.py` - Mock Raspberry Pi modules for Windows
- `requirements-dev.txt` - Windows-compatible dependencies
- `test_windows.py` - Windows development test suite
- `WINDOWS_DEVELOPMENT.md` - This guide

### Hardware Files (for reference)
- `requirements.txt` - Full dependencies (includes Raspberry Pi specific packages)
- `HARDWARE_SETUP.md` - Hardware setup instructions
- `led-display.service` - Systemd service file
- `start.sh` - Startup script

## Usage

### Running the Demo

To see the LED patterns in action (simulated):

```powershell
python main.py
```

This will run through a demo sequence showing various LED patterns. Since you're on Windows, the patterns are simulated and you'll see console output describing what would happen on real hardware.

### Developing New Patterns

1. Open `display_patterns.py` to see existing patterns
2. Add your new pattern methods to the `DisplayPatterns` class
3. Test your patterns by calling them from `main.py`

### Testing Your Code

Use the test script to verify your changes:

```powershell
python test_windows.py
```

## Mock Modules

The following mock modules simulate Raspberry Pi hardware:

### Mock GPIO (`mock_rpi.py`)
- Simulates GPIO pin operations
- Provides button input simulation
- Prints operations to console for debugging

### Mock WS281x (`mock_rpi.py`)
- Simulates LED strip operations
- Tracks pixel states in memory
- Prints LED operations to console

## Configuration

The `config.py` file contains all the configuration settings:

- `TOTAL_LEDS`: Total number of LEDs (1280 for 40x32 display)
- `TOTAL_WIDTH`: Display width in pixels (40)
- `TOTAL_HEIGHT`: Display height in pixels (32)
- `PANELS_COUNT`: Number of LED panels (5)
- `PANEL_WIDTH`: Width of each panel (8)
- `PANEL_HEIGHT`: Height of each panel (32)
- `LED_PIN`: GPIO pin for LED data (21)
- `BRIGHTNESS`: LED brightness (0.3 = 30%)

## Development Workflow

1. **Activate Virtual Environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Make Your Changes**
   - Edit pattern files
   - Modify configuration
   - Add new features

3. **Test Your Changes**
   ```powershell
   python test_windows.py
   python main.py
   ```

4. **Deploy to Raspberry Pi**
   - Copy your changes to the Raspberry Pi
   - Install full requirements: `pip install -r requirements.txt`
   - Run on real hardware

## Troubleshooting

### Virtual Environment Issues
- Make sure you're in the correct directory
- Use `.\venv\Scripts\Activate.ps1` (not `source venv/bin/activate`)
- If activation fails, recreate the virtual environment

### Import Errors
- Ensure you're using the virtual environment
- Check that `mock_rpi.py` is in the project directory
- Verify that `requirements-dev.txt` packages are installed

### Mock Module Issues
- Mock modules print operations to console for debugging
- Check console output to see what operations are being performed
- Mock modules simulate delays to mimic real hardware behavior

## Next Steps

Once you're comfortable with the Windows development environment:

1. **Study the Code**: Understand how the LED patterns work
2. **Create Patterns**: Add your own LED animations
3. **Test Thoroughly**: Use the test suite to verify your code
4. **Deploy**: Transfer your code to Raspberry Pi for real hardware testing

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your virtual environment is activated
3. Run `python test_windows.py` to check system health
4. Review the mock module output for debugging information

Happy coding! 🎉 