# Raspberry Pi LED Display Project

This project controls 5 LED panels (32x8 each) to create a 40x32 display using WS2812B LEDs on a Raspberry Pi 4.

## Hardware Setup

### LED Panels Configuration
- **5 LED panels**: Each 32x8 pixels (WS2812B type)
- **Total display**: 40x32 pixels
- **Connection**: All panels connected through GPIO pin 21
- **Power**: 5V power supply required for WS2812B LEDs

### Panel Layout
```
Panel 1 (32x8) | Panel 2 (32x8) | Panel 3 (32x8) | Panel 4 (32x8) | Panel 5 (32x8)
                |                |                |                |
                |                |                |                |
                |                |                |                |
```

### Button Setup (Future Implementation)
- 4 buttons for different interactions
- Currently not connected

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure SPI is enabled on your Raspberry Pi:
```bash
sudo raspi-config
# Navigate to Interface Options > SPI > Enable
```

## Usage

Run the main application:
```bash
python main.py
```

## Features

- **Matrix Display**: 40x32 pixel display
- **Color Control**: Full RGB color support
- **Animation Support**: Various display patterns and animations
- **Button Integration**: Ready for 4-button control (to be implemented)

## File Structure

- `main.py`: Main application entry point
- `led_controller.py`: LED display controller
- `display_patterns.py`: Various display patterns and animations
- `button_controller.py`: Button input handling (future)
- `config.py`: Configuration settings
- `requirements.txt`: Python dependencies

## Configuration

Edit `config.py` to modify:
- LED pin number
- Display dimensions
- Brightness settings
- Animation speeds 