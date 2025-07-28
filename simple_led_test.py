#!/usr/bin/env python3
"""
Simple LED Test - Light up LEDs one by one to understand the mapping
"""

import time
from led_controller import LEDController
import config

def main():
    """Simple test to light up LEDs one by one."""
    print("Simple LED Test")
    print(f"Total LEDs: {config.TOTAL_LEDS}")
    print("This will light up LEDs one by one from 0 to the end")
    print("Press Ctrl+C to stop")
    
    led = LEDController()
    
    try:
        # Clear all LEDs first
        led.clear()
        led.show()
        time.sleep(1)
        
        # Light up LEDs one by one
        for i in range(config.TOTAL_LEDS):
            print(f"Lighting up LED {i}")
            
            # Clear previous LED
            if i > 0:
                led.strip.setPixelColorRGB(i-1, 0, 0, 0)
            
            # Light up current LED
            led.strip.setPixelColorRGB(i, 255, 255, 255)  # White
            led.show()
            
            time.sleep(0.5)
        
        # Keep the last LED lit for a moment
        time.sleep(2)
        
        # Clear all
        led.clear()
        led.show()
        
    except KeyboardInterrupt:
        print("\nTest stopped by user")
        led.clear()
        led.show()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        led.cleanup()

if __name__ == "__main__":
    main() 