# LED Display Animation Controller

A Raspberry Pi LED display system with organized animation scripts and button control.

## 📁 Project Structure

```
led-board-project/
├── scripts/                          # All animation scripts
│   ├── *_animation.py               # Individual animation scripts
│   └── README.md                    # Scripts documentation
├── random_animation_controller.py   # Main random animation controller
├── start_random_animations.sh       # Startup script
├── test_button.py                   # Button test script
├── list_animations.py               # List all available animations
├── run_animation.py                 # Run specific animation
└── ANIMATION_CONTROLLER_README.md   # This file
```

## 🎮 Button Control

- **GPIO 18**: Press to start random animation
- **Ctrl+C**: Stop current animation and exit

## 🚀 Quick Start

### 1. Test Your Button
```bash
sudo ./venv/bin/python test_button.py
```

### 2. Run Random Animations
```bash
./start_random_animations.sh
```

### 3. List Available Animations
```bash
python3 list_animations.py
```

### 4. Run Specific Animation
```bash
python3 run_animation.py squares_animation
```

## 📋 Available Animations (17 total)

1. `animal_sequence_animation.py` - Animal sequence animation
2. `big_shapes_animation.py` - Big shapes animation
3. `black_hole_animation.py` - Black hole animation
4. `bubbles_animation.py` - Bubbles animation
5. `calming_ambient_animation.py` - Calming ambient animation
6. `car_driving_animation.py` - Car driving animation
7. `dudi_paddleboarding_animation.py` - Dudi paddleboarding animation
8. `gravity_bend_animation.py` - Gravity bend animation
9. `music_instruments_animation.py` - Music instruments animation
10. `saturn_animation.py` - Saturn animation
11. `shapes_animation.py` - Shapes animation
12. `shark_animation.py` - Shark animation
13. `ship_sailing_animation.py` - Ship sailing animation
14. `squares_animation.py` - 24 squares animation (6 rows × 4 columns)
15. `star_animation.py` - Star animation
16. `tree_growing_animation.py` - Tree growing animation
17. `tree_growth_animation.py` - Tree growth animation

## 🔧 How It Works

1. **Button Press** → Randomly selects one of 17 available animations
2. **Stops Current Animation** → If one is running, stops it first
3. **Runs New Animation** → Uses command: `sudo ./venv/bin/python scripts/<script>`
4. **Waits for Completion** → Animation runs until finished
5. **Ready for Next Press** → Button ready for next random animation

## 📝 Adding New Animations

1. Create your animation script with `_animation.py` suffix
2. Place it in the `scripts/` folder
3. The random controller will automatically detect it
4. Make sure your script has a `main()` function for standalone execution

## 🛠️ Troubleshooting

### Button Not Working
- Check GPIO 18 connection
- Run `sudo ./venv/bin/python test_button.py`
- Verify button is connected between GPIO 18 and GND

### Animation Not Running
- Check if script exists in `scripts/` folder
- Verify script has `_animation.py` suffix
- Run `python3 list_animations.py` to see available scripts

### Permission Issues
- Make sure to use `sudo` when running scripts
- Check file permissions: `chmod +x start_random_animations.sh`

## 🎯 Features

- ✅ **Random Selection** - Each button press picks a random animation
- ✅ **Process Management** - Properly starts/stops animations
- ✅ **Error Handling** - Continues working even if an animation fails
- ✅ **Clean Shutdown** - Ctrl+C properly stops everything
- ✅ **Status Messages** - Shows which animation is running
- ✅ **Organized Structure** - All animations in dedicated scripts folder
- ✅ **Easy Management** - Simple commands to list and run animations
