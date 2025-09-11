# Troubleshooting Guide

## 🔧 Import Issues Fixed

The main issue was that animation scripts couldn't find the required modules (`led_controller`, `config`, etc.) because they were running from the `scripts/` folder.

### ✅ Solution Implemented

1. **Wrapper Script**: Created `run_animation_wrapper.py` that sets up the Python path correctly
2. **Updated Main Controller**: Now uses the wrapper to run all animations
3. **Proper Path Handling**: All scripts now run from the project root directory

## 🧪 Testing Scripts

### Test Single Animation
```bash
python3 test_single_animation.py squares_animation.py
```

### Test Wrapper
```bash
python3 test_wrapper.py
```

### Test Button
```bash
sudo ./venv/bin/python test_button.py
```

## 🚀 Running the Fixed System

### Start Main Controller
```bash
./start_main_controller.sh
```

### Or run directly
```bash
sudo ./venv/bin/python main_animation_controller.py
```

## 🔍 Common Issues and Solutions

### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'led_controller'`

**Solution**: The wrapper script now handles this automatically. Make sure you're using the updated main controller.

### 2. Permission Errors
**Problem**: Permission denied when running scripts

**Solution**: Always use `sudo` when running the main controller:
```bash
sudo ./venv/bin/python main_animation_controller.py
```

### 3. Button Not Working
**Problem**: Button presses not detected

**Solution**: 
1. Check GPIO 18 connection (button between GPIO 18 and GND)
2. Test button: `sudo ./venv/bin/python test_button.py`
3. Verify button controller is working

### 4. Animation Not Switching
**Problem**: Button pressed but animation doesn't change

**Solution**:
1. Check if main controller is running
2. Look for error messages in the output
3. Test with a single animation first

### 5. Scripts Not Found
**Problem**: Animation scripts not found

**Solution**:
1. Verify `scripts/` folder exists
2. Check that scripts end with `_animation.py`
3. Run: `python3 list_animations.py`

## 📋 Debugging Steps

### 1. Check System Status
```bash
python3 check_status.py
```

### 2. List Available Animations
```bash
python3 list_animations.py
```

### 3. Test Button Connection
```bash
sudo ./venv/bin/python test_button.py
```

### 4. Test Single Animation
```bash
python3 test_single_animation.py squares_animation.py
```

### 5. Check File Permissions
```bash
ls -la *.py
ls -la scripts/*.py
```

## 🎯 Expected Behavior

### When Starting
```
🎬 Main Animation Controller Started
==================================================
📁 Found 17 animation scripts
🔘 Press button on GPIO 18 to switch animations
⏹️  Press Ctrl+C to exit
==================================================
🎲 Starting with random animation...
🎬 Starting: squares_animation.py
▶️  Running: sudo ./venv/bin/python run_animation_wrapper.py squares_animation.py
```

### When Button Pressed
```
🔘 Button pressed! Switching animation...
⏹️  Stopping current animation...
🎬 Starting: star_animation.py
▶️  Running: sudo ./venv/bin/python run_animation_wrapper.py star_animation.py
```

## 🛠️ File Structure

```
led-board-project/
├── main_animation_controller.py    # Main controller (FIXED)
├── run_animation_wrapper.py        # Import fix wrapper
├── test_single_animation.py        # Test single animation
├── test_wrapper.py                 # Test wrapper
├── check_status.py                 # Status checker
├── scripts/                        # Animation scripts folder
│   ├── squares_animation.py       # 24 squares animation
│   ├── star_animation.py          # Star animation
│   └── ... (15 more animations)   # Other animations
└── TROUBLESHOOTING.md             # This file
```

## ✅ Verification Checklist

- [ ] Main controller starts without errors
- [ ] Button press is detected
- [ ] Animation switches on button press
- [ ] No import errors in output
- [ ] Animations run successfully
- [ ] Ctrl+C stops everything cleanly

## 🆘 Still Having Issues?

1. **Check the output** - Look for specific error messages
2. **Test components individually** - Use the test scripts
3. **Verify file structure** - Make sure all files are in place
4. **Check permissions** - Ensure scripts are executable
5. **Test button connection** - Verify GPIO 18 wiring

The system should now work correctly with the import issues resolved! 🎬✨
