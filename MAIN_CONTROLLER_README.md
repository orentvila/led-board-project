# Main Animation Controller

A single, continuous-running script that manages LED display animations with button control.

## 🎯 Overview

This is the **ONLY script you need to run**. It runs continuously and switches between random animations every time you press the button on GPIO 18.

## 🚀 Quick Start

### Run the Main Controller
```bash
./start_main_controller.sh
```

Or directly:
```bash
sudo ./venv/bin/python main_animation_controller.py
```

## 🎮 How It Works

1. **Starts automatically** with a random animation
2. **Button press on GPIO 18** → Immediately stops current animation and starts a new random one
3. **Runs continuously** until you press Ctrl+C
4. **No manual intervention** needed - just press the button to switch animations

## 🔧 Features

- ✅ **Single Script** - Only one script running at a time
- ✅ **Button Interrupt** - Each button press immediately switches animations
- ✅ **Random Selection** - Picks random animation from scripts folder
- ✅ **Process Management** - Properly stops/starts animations
- ✅ **Continuous Running** - Never stops until you exit
- ✅ **Clean Shutdown** - Ctrl+C properly stops everything

## 📋 Available Animations

The controller automatically finds all `*_animation.py` files in the `scripts/` folder:

- squares_animation.py (24 squares)
- star_animation.py
- shapes_animation.py
- bubbles_animation.py
- calming_ambient_animation.py
- car_driving_animation.py
- shark_animation.py
- ship_sailing_animation.py
- saturn_animation.py
- music_instruments_animation.py
- gravity_bend_animation.py
- dudi_paddleboarding_animation.py
- black_hole_animation.py
- big_shapes_animation.py
- animal_sequence_animation.py
- tree_growing_animation.py
- tree_growth_animation.py

## 🎬 Usage Examples

### Start the Controller
```bash
./start_main_controller.sh
```

### Output Example
```
🎬 Main Animation Controller Started
==================================================
📁 Found 17 animation scripts
🔘 Press button on GPIO 18 to switch animations
⏹️  Press Ctrl+C to exit
==================================================
🎲 Starting with random animation...
🎬 Starting: squares_animation.py
▶️  Running: sudo ./venv/bin/python scripts/squares_animation.py

🔘 Button pressed! Switching animation...
⏹️  Stopping current animation...
🎬 Starting: star_animation.py
▶️  Running: sudo ./venv/bin/python scripts/star_animation.py
```

## 🧪 Testing

### Test Button Connection
```bash
sudo ./venv/bin/python test_button.py
```

### Test Main Controller (Simulated)
```bash
python3 test_main_controller.py
```

## 🛠️ Troubleshooting

### Button Not Working
- Check GPIO 18 connection (button between GPIO 18 and GND)
- Run button test: `sudo ./venv/bin/python test_button.py`

### Animation Not Switching
- Check if scripts folder exists and contains `*_animation.py` files
- Verify file permissions: `chmod +x start_main_controller.sh`

### Permission Issues
- Always use `sudo` when running the controller
- Check virtual environment path: `./venv/bin/python`

## 📁 File Structure

```
led-board-project/
├── main_animation_controller.py    # 🎯 Main controller script
├── start_main_controller.sh        # 🚀 Startup script
├── test_main_controller.py         # 🧪 Test script
├── scripts/                        # 📁 Animation scripts folder
│   ├── *_animation.py             # Individual animations
│   └── README.md                  # Scripts documentation
└── MAIN_CONTROLLER_README.md      # 📖 This file
```

## 🎯 Key Benefits

1. **Simple** - Only one script to run
2. **Automatic** - Starts with random animation
3. **Responsive** - Button press immediately switches
4. **Reliable** - Proper process management
5. **Organized** - All animations in scripts folder

## 🔄 Workflow

1. **Start**: `./start_main_controller.sh`
2. **Watch**: Animation starts automatically
3. **Press Button**: Animation switches immediately
4. **Repeat**: Keep pressing button for new animations
5. **Exit**: Press Ctrl+C to stop

This is the **main script** for your LED display system! 🎬✨
