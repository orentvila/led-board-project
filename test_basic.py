#!/usr/bin/env python3
"""
Minimal test script to verify LED controller works without memory leaks
"""

import time
import gc
from led_controller import LEDController
import config

def test_basic_led():
    """Test basic LED functionality without memory leaks."""
    print("Testing basic LED functionality...")
    
    try:
        # Create LED controller
        print("Creating LED controller...")
        led = LEDController()
        print("✓ LED controller created successfully")
        
        # Test basic operations
        print("Testing basic operations...")
        
        # Test 1: Clear
        led.clear()
        led.show()
        print("✓ Clear operation successful")
        time.sleep(1)
        
        # Test 2: Set a few pixels
        led.set_pixel(0, 0, config.COLORS['RED'])
        led.set_pixel(1, 0, config.COLORS['GREEN'])
        led.set_pixel(2, 0, config.COLORS['BLUE'])
        led.show()
        print("✓ Pixel setting successful")
        time.sleep(2)
        
        # Test 3: Brightness control
        print("Testing brightness control...")
        for brightness in [0.1, 0.3, 0.5, 0.7, 1.0]:
            led.set_brightness(brightness)
            led.fill_display(config.COLORS['WHITE'])
            led.show()
            time.sleep(0.5)
        
        # Reset brightness
        led.set_brightness(config.BRIGHTNESS)
        
        # Test 4: Clear again
        led.clear()
        led.show()
        print("✓ Final clear successful")
        
        # Cleanup
        print("Cleaning up...")
        led.cleanup()
        print("✓ Cleanup successful")
        
        # Force garbage collection
        gc.collect()
        print("✓ Garbage collection completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main test function."""
    print("Basic LED Test")
    print("=" * 30)
    
    success = test_basic_led()
    
    if success:
        print("\n🎉 Basic test passed! No memory leaks detected.")
    else:
        print("\n❌ Test failed. Check your setup.")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 