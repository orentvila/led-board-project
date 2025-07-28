#!/usr/bin/env python3
"""
Test Corrected LED Mapping
"""

import time
from led_controller import LEDController
import config

def main():
    """Test the corrected LED mapping."""
    print("Testing Corrected LED Mapping")
    print(f"Display: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
    
    led = LEDController()
    
    try:
        # Test 1: Clear display
        print("1. Clearing display...")
        led.clear()
        led.show()
        time.sleep(1)
        
        # Test 2: Light up corners
        print("2. Lighting up corners...")
        led.set_pixel(0, 0, (255, 0, 0))      # Top-left: Red
        led.set_pixel(31, 0, (0, 255, 0))     # Top-right: Green
        led.set_pixel(0, 39, (0, 0, 255))     # Bottom-left: Blue
        led.set_pixel(31, 39, (255, 255, 0))  # Bottom-right: Yellow
        led.show()
        time.sleep(3)
        
        # Test 3: Light up center
        print("3. Lighting up center...")
        led.clear()
        led.set_pixel(15, 19, (255, 255, 255))  # Center: White
        led.show()
        time.sleep(2)
        
        # Test 4: Simple border
        print("4. Creating border...")
        led.clear()
        
        # Top border (red)
        for x in range(config.TOTAL_WIDTH):
            led.set_pixel(x, 0, (255, 0, 0))
        
        # Bottom border (blue)
        for x in range(config.TOTAL_WIDTH):
            led.set_pixel(x, config.TOTAL_HEIGHT-1, (0, 0, 255))
        
        # Left border (green)
        for y in range(config.TOTAL_HEIGHT):
            led.set_pixel(0, y, (0, 255, 0))
        
        # Right border (yellow)
        for y in range(config.TOTAL_HEIGHT):
            led.set_pixel(config.TOTAL_WIDTH-1, y, (255, 255, 0))
        
        led.show()
        print("Border displayed. Press Ctrl+C to stop.")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        led.clear()
        led.show()
        led.cleanup()

if __name__ == "__main__":
    main() 