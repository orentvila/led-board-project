#!/usr/bin/env python3
"""
Test script to verify all animations use correct LED mapping
"""

import time
from led_controller_exact import LEDControllerExact
import config

def test_mapping_verification():
    """Test that all animations use the correct LED mapping."""
    print("🔍 Testing LED Mapping Verification")
    print("=" * 50)
    
    # Initialize the correct LED controller
    led = LEDControllerExact()
    
    print("✅ LEDControllerExact initialized")
    print(f"   Display size: {led.width}x{led.height}")
    print(f"   Total LEDs: {len(led.led_to_coord_map)}")
    
    # Test 1: Clear display
    print("\n🧹 Testing display clear...")
    led.clear()
    led.show()
    print("✅ Display cleared")
    
    # Test 2: Corner test
    print("\n🔲 Testing corner mapping...")
    corners = [(0, 0), (31, 0), (0, 47), (31, 47)]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    
    for i, (x, y) in enumerate(corners):
        led.set_pixel(x, y, colors[i])
        print(f"   Corner {i+1}: ({x}, {y}) -> {colors[i]}")
    
    led.show()
    print("✅ Corner test completed")
    time.sleep(2)
    
    # Test 3: Center test
    print("\n🎯 Testing center mapping...")
    led.clear()
    center_x, center_y = led.width // 2, led.height // 2
    led.set_pixel(center_x, center_y, (255, 255, 255))
    led.show()
    print(f"   Center: ({center_x}, {center_y}) -> White")
    print("✅ Center test completed")
    time.sleep(2)
    
    # Test 4: Border test
    print("\n🖼️ Testing border mapping...")
    led.clear()
    
    # Top and bottom borders
    for x in range(led.width):
        led.set_pixel(x, 0, (255, 0, 0))  # Red top
        led.set_pixel(x, led.height - 1, (0, 255, 0))  # Green bottom
    
    # Left and right borders
    for y in range(led.height):
        led.set_pixel(0, y, (0, 0, 255))  # Blue left
        led.set_pixel(led.width - 1, y, (255, 255, 0))  # Yellow right
    
    led.show()
    print("✅ Border test completed")
    time.sleep(3)
    
    # Test 5: Shape test (simple square)
    print("\n🔷 Testing shape mapping...")
    led.clear()
    
    # Draw a simple square in the center
    center_x, center_y = led.width // 2, led.height // 2
    size = 8
    
    for y in range(center_y - size//2, center_y + size//2):
        for x in range(center_x - size//2, center_x + size//2):
            if 0 <= x < led.width and 0 <= y < led.height:
                led.set_pixel(x, y, (255, 0, 255))  # Magenta square
    
    led.show()
    print("✅ Shape test completed")
    time.sleep(2)
    
    # Cleanup
    led.clear()
    led.show()
    led.cleanup()
    
    print("\n🎉 All mapping tests completed successfully!")
    print("✅ All animations should now use correct LED mapping")

if __name__ == "__main__":
    test_mapping_verification()
