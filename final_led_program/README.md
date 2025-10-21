# Final LED Program

A clean, organized 4-button LED controller with theme animations.

## Structure

```
final_led_program/
├── animations/           # Animation classes
│   ├── base_animation.py # Base class for all animations
│   ├── saturn_animation.py
│   ├── star_animation.py
│   └── bubbles_animation.py
├── themes/              # Theme configurations (future)
├── audio/               # Audio files (future)
├── main_controller.py   # Main program controller
├── start_final_program.sh
├── start_final_program.bat
└── README.md
```

## Current Animations

### Space Theme (Pin 18)
- **Saturn**: Rotating planet with rings and sparkles
- **Stars**: Twinkling stars with shooting stars

### Nature Theme (Pin 17)
- **Bubbles**: Floating bubbles with realistic physics

## Usage

### Linux/Raspberry Pi:
```bash
sudo ./start_final_program.sh
```

### Windows:
```bash
start_final_program.bat
```

### Direct Python:
```bash
# Linux
sudo ../venv/bin/python main_controller.py

# Windows
../venv/Scripts/python main_controller.py
```

## Adding New Animations

1. Create a new animation class in `animations/` directory
2. Inherit from `BaseAnimation`
3. Implement the `run(duration)` method
4. Add to theme configuration in `main_controller.py`

## Features

- ✅ Clean, organized structure
- ✅ Proper inheritance with BaseAnimation
- ✅ Thread-safe animation management
- ✅ Audio support (when available)
- ✅ 4-button theme system
- ✅ Easy to extend with new animations
