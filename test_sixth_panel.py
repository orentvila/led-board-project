#!/usr/bin/env python3
"""
Test script to verify the sixth panel configuration
"""

import config
from led_controller_fixed import LEDControllerFixed
import time

def test_sixth_panel():
    """Test that the sixth panel is properly configured and accessible."""
    print("Testing sixth panel configuration...")
    print(f"Total panels: {config.PANELS_COUNT}")
    print(f"Panel dimensions: {config.PANEL_WIDTH}x{config.PANEL_HEIGHT}")
    print(f"Total display: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
    print(f"Total LEDs: {config.TOTAL_LEDS}")
    
    # Initialize LED controller
    led = LEDControllerFixed()
    
    try:
        # Test that we can access the top row (sixth panel)
        print("\nTesting sixth panel (top row)...")
        led.clear()
        
        # Light up the top row (y=0) in red
        for x in range(config.TOTAL_WIDTH):
            led.set_pixel(x, 0, (255, 0, 0))  # Red
        
        led.show()
        print("Top row should be red (sixth panel)")
        time.sleep(3)
        
        # Test that we can access the bottom row (first panel)
        print("\nTesting first panel (bottom row)...")
        led.clear()
        
        # Light up the bottom row in blue
        for x in range(config.TOTAL_WIDTH):
            led.set_pixel(x, config.TOTAL_HEIGHT - 1, (0, 0, 255))  # Blue
        
        led.show()
        print("Bottom row should be blue (first panel)")
        time.sleep(3)
        
        # Test a pattern that spans all panels
        print("\nTesting pattern across all panels...")
        led.clear()
        
        # Create a rainbow pattern across all panels
        for y in range(config.TOTAL_HEIGHT):
            for x in range(config.TOTAL_WIDTH):
                # Create a rainbow effect
                r = int(255 * (x / config.TOTAL_WIDTH))
                g = int(255 * (y / config.TOTAL_HEIGHT))
                b = int(255 * ((x + y) / (config.TOTAL_WIDTH + config.TOTAL_HEIGHT)))
                led.set_pixel(x, y, (r, g, b))
        
        led.show()
        print("Rainbow pattern should be visible across all 6 panels")
        time.sleep(5)
        
        print("\nSixth panel test completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        led.clear()
        led.show()
        led.cleanup()

if __name__ == "__main__":
    test_sixth_panel() 