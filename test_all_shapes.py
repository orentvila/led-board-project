#!/usr/bin/env python3
"""
Test All Shapes - Run each shape animation for 5 seconds
"""

import time
import subprocess
import sys

def test_shape_animation(shape_file, duration=5):
    """Test a single shape animation."""
    print(f"\n🎬 Testing {shape_file} for {duration} seconds...")
    print("=" * 50)
    
    try:
        # Run the animation
        process = subprocess.Popen([
            sys.executable, shape_file
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the specified duration
        time.sleep(duration)
        
        # Stop the animation
        process.terminate()
        process.wait()
        
        print(f"✅ {shape_file} test completed")
        
    except Exception as e:
        print(f"❌ Error testing {shape_file}: {e}")

def main():
    """Test all shape animations."""
    print("🔷 Testing All Shape Animations 🔷")
    print("Each animation will run for 5 seconds")
    
    shape_files = [
        "growing_circle_animation.py",
        "rotating_square_animation.py",
        "bouncing_triangle_animation.py", 
        "pulsing_diamond_animation.py"
    ]
    
    for shape_file in shape_files:
        test_shape_animation(shape_file, 5)
        time.sleep(1)  # Brief pause between tests
    
    print("\n🎉 All shape animations tested!")

if __name__ == "__main__":
    main()
