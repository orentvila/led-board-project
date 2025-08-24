#!/usr/bin/env python3
"""
Simple test script for the LED display
Run this to test basic functionality without the full application
"""

import time
from led_controller import LEDController
import config

def test_basic_functionality():
    """Test basic LED display functionality."""
    print("Testing LED Display Basic Functionality")
    print("=" * 40)
    
    try:
        # Initialize LED controller
        print("Initializing LED controller...")
        led = LEDController()
        print("✓ LED controller initialized")
        
        # Test 1: Clear display
        print("\nTest 1: Clearing display...")
        led.clear()
        led.show()
        print("✓ Display cleared")
        time.sleep(1)
        
        # Test 2: Fill display with red
        print("\nTest 2: Filling display with red...")
        led.fill_display(config.COLORS['RED'])
        led.show()
        print("✓ Display filled with red")
        time.sleep(2)
        
        # Test 3: Fill display with green
        print("\nTest 3: Filling display with green...")
        led.fill_display(config.COLORS['GREEN'])
        led.show()
        print("✓ Display filled with green")
        time.sleep(2)
        
        # Test 4: Fill display with blue
        print("\nTest 4: Filling display with blue...")
        led.fill_display(config.COLORS['BLUE'])
        led.show()
        print("✓ Display filled with blue")
        time.sleep(2)
        
        # Test 5: Panel test
        print("\nTest 6: Testing individual panels...")
        for panel in range(config.PANELS_COUNT):
            print(f"  Lighting panel {panel + 1}...")
            led.fill_panel(panel, config.COLORS['WHITE'])
            led.show()
            time.sleep(1)
            led.fill_panel(panel, config.COLORS['BLACK'])
            led.show()
        
        # Test 6: Draw some shapes
        print("\nTest 6: Drawing shapes...")
        led.clear()
        
        # Draw rectangle
        led.draw_rectangle(10, 2, 30, 5, config.COLORS['YELLOW'], fill=False)
        led.show()
        time.sleep(1)
        
        # Draw filled rectangle
        led.draw_rectangle(35, 2, 55, 5, config.COLORS['CYAN'], fill=True)
        led.show()
        time.sleep(1)
        
        # Draw lines
        led.draw_line(5, 1, 15, 6, config.COLORS['MAGENTA'])
        led.draw_line(20, 6, 30, 1, config.COLORS['ORANGE'])
        led.show()
        time.sleep(2)
        
        # Test 7: Text display
        print("\nTest 7: Displaying text...")
        led.clear()
        led.draw_text("HI", 10, 1, config.COLORS['WHITE'])
        led.show()
        time.sleep(2)
        
        # Test 8: Brightness control
        print("\nTest 8: Testing brightness control...")
        for brightness in [0.1, 0.3, 0.5, 0.7, 1.0]:
            print(f"  Setting brightness to {brightness}")
            led.set_brightness(brightness)
            led.fill_display(config.COLORS['WHITE'])
            led.show()
            time.sleep(1)
        
        # Reset brightness
        led.set_brightness(config.BRIGHTNESS)
        
        # Final cleanup
        print("\nTest 9: Final cleanup...")
        led.clear()
        led.show()
        print("✓ All tests completed successfully!")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("LED Display Test Script")
    print("=" * 40)
    print(f"Display Configuration:")
    print(f"  Total LEDs: {config.TOTAL_LEDS}")
    print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
    print(f"  Panels: {config.PANELS_COUNT}")
    print(f"  LED Pin: {config.LED_PIN}")
    print()
    
    success = test_basic_functionality()
    
    if success:
        print("\n🎉 All tests passed! Your LED display is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check your hardware connections.")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 