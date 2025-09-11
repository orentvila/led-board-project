#!/usr/bin/env python3
"""
Check status of animation controller and running processes
"""

import subprocess
import os

def check_status():
    """Check the status of the animation system."""
    print("🔍 Animation Controller Status Check")
    print("=" * 40)
    
    # Check if main controller is running
    try:
        result = subprocess.run(['pgrep', '-f', 'main_animation_controller.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"✅ Main controller running (PID: {', '.join(pids)})")
        else:
            print("❌ Main controller not running")
    except Exception as e:
        print(f"⚠️  Error checking main controller: {e}")
    
    # Check if any animation scripts are running
    try:
        result = subprocess.run(['pgrep', '-f', '_animation.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"🎬 Animation scripts running (PID: {', '.join(pids)})")
        else:
            print("📺 No animation scripts currently running")
    except Exception as e:
        print(f"⚠️  Error checking animation scripts: {e}")
    
    # Check scripts folder
    if os.path.exists('scripts'):
        script_count = len([f for f in os.listdir('scripts') if f.endswith('_animation.py')])
        print(f"📁 Scripts folder: {script_count} animation scripts found")
    else:
        print("❌ Scripts folder not found")
    
    # Check button controller
    try:
        result = subprocess.run(['pgrep', '-f', 'button_controller'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("🔘 Button controller active")
        else:
            print("🔘 Button controller not detected (may be part of main controller)")
    except Exception as e:
        print(f"⚠️  Error checking button controller: {e}")

if __name__ == "__main__":
    check_status()
