#!/usr/bin/env python3
"""
Test the animation wrapper script
"""

import subprocess
import os

def test_wrapper():
    """Test the animation wrapper with a simple script."""
    print("🧪 Testing animation wrapper...")
    
    # Test with squares animation
    try:
        cmd = ['sudo', './venv/bin/python', 'run_animation_wrapper.py', 'squares_animation.py']
        print(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, timeout=10, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Wrapper test successful!")
            print("Output:", result.stdout)
        else:
            print("❌ Wrapper test failed!")
            print("Error:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out (this is expected for animations)")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_wrapper()
