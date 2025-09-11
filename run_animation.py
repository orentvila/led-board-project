#!/usr/bin/env python3
"""
Run a specific animation script
Usage: python3 run_animation.py <animation_name>
Example: python3 run_animation.py squares_animation
"""

import sys
import os
import subprocess

def run_animation(animation_name):
    """Run a specific animation script."""
    # Add .py extension if not provided
    if not animation_name.endswith('.py'):
        animation_name += '.py'
    
    # Check if it's an animation script
    if not animation_name.endswith('_animation.py'):
        print(f"❌ Error: '{animation_name}' is not an animation script")
        print("Animation scripts must end with '_animation.py'")
        return False
    
    # Check if script exists
    script_path = os.path.join('scripts', animation_name)
    if not os.path.exists(script_path):
        print(f"❌ Error: Animation script '{animation_name}' not found in scripts/ folder")
        return False
    
    # Run the script
    try:
        print(f"🎬 Running animation: {animation_name}")
        cmd = ['sudo', './venv/bin/python', script_path]
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running animation: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python3 run_animation.py <animation_name>")
        print("Example: python3 run_animation.py squares_animation")
        print("\nAvailable animations:")
        
        # List available animations
        if os.path.exists('scripts'):
            for file in sorted(os.listdir('scripts')):
                if file.endswith('_animation.py'):
                    name = file.replace('_animation.py', '')
                    print(f"  - {name}")
        sys.exit(1)
    
    animation_name = sys.argv[1]
    success = run_animation(animation_name)
    
    if success:
        print("✅ Animation completed successfully")
    else:
        print("❌ Animation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
