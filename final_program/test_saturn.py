#!/usr/bin/env python3
"""
Test script for Saturn animation
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from led_controller import LEDController
from themes.shapes.saturn_animation import SaturnAnimation

def main():
    """Test the Saturn animation."""
    print("🪐 Testing Saturn Animation")
    print("=" * 30)
    
    try:
        led = LEDController()
        saturn = SaturnAnimation(led)
        
        print("Starting 10-second test...")
        saturn.run(duration=10)
        
        led.cleanup()
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
