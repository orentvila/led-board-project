#!/usr/bin/env python3
"""
Simple test for Saturn animation without full controller
"""

import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from led_controller import LEDController
from themes.shapes.saturn_animation import SaturnAnimation

def main():
    """Test the Saturn animation directly."""
    print("🪐 Testing Saturn Animation (Simple)")
    print("=" * 40)
    
    try:
        print("Initializing LED controller...")
        led = LEDController()
        
        print("Creating Saturn animation...")
        saturn = SaturnAnimation(led)
        
        print("Starting 5-second test...")
        saturn.run(duration=5)
        
        print("Cleaning up...")
        led.cleanup()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
