#!/usr/bin/env python3
"""
LED Mapping Test for 32x40 Display
This script helps determine the correct LED strip mapping
"""

import time
import sys
from led_controller import LEDController
import config

class LEDMappingTest:
    def __init__(self):
        """Initialize the LED mapping test."""
        self.led = LEDController()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
    def test_sequential_mapping(self):
        """Test sequential LED mapping (0, 1, 2, 3, ...)."""
        print("Testing sequential LED mapping...")
        print("This will light up LEDs one by one from top-left to bottom-right")
        
        for i in range(config.TOTAL_LEDS):
            # Clear all LEDs
            self.led.clear()
            self.led.show()
            time.sleep(0.1)
            
            # Light up one LED
            self.led.strip.setPixelColorRGB(i, 255, 255, 255)  # White
            self.led.show()
            print(f"LED {i} should be lit (white)")
            time.sleep(1)
    
    def test_coordinate_mapping(self):
        """Test coordinate-based mapping."""
        print("Testing coordinate mapping...")
        print("This will light up pixels by (x,y) coordinates")
        
        # Test a few key positions
        test_positions = [
            (0, 0),      # Top-left
            (31, 0),     # Top-right
            (0, 39),     # Bottom-left
            (31, 39),    # Bottom-right
            (15, 19),    # Center
        ]
        
        for x, y in test_positions:
            print(f"Testing position ({x}, {y})")
            self.led.clear()
            self.led.set_pixel(x, y, (255, 255, 255))  # White
            self.led.show()
            time.sleep(2)
    
    def test_panel_mapping(self):
        """Test panel-by-panel mapping."""
        print("Testing panel mapping...")
        print("This will light up each panel separately")
        
        for panel in range(config.PANELS_COUNT):
            print(f"Testing panel {panel}")
            self.led.clear()
            self.led.fill_panel(panel, (255, 0, 0))  # Red
            self.led.show()
            time.sleep(2)
    
    def test_simple_pattern(self):
        """Test a simple pattern to see the mapping."""
        print("Testing simple pattern...")
        print("This will create a simple test pattern")
        
        # Create a simple pattern: red border
        self.led.clear()
        
        # Top border
        for x in range(self.width):
            self.led.set_pixel(x, 0, (255, 0, 0))  # Red
        
        # Bottom border
        for x in range(self.width):
            self.led.set_pixel(x, self.height-1, (255, 0, 0))  # Red
        
        # Left border
        for y in range(self.height):
            self.led.set_pixel(0, y, (255, 0, 0))  # Red
        
        # Right border
        for y in range(self.height):
            self.led.set_pixel(self.width-1, y, (255, 0, 0))  # Red
        
        # Center cross
        for i in range(min(self.width, self.height)):
            self.led.set_pixel(i, i, (0, 255, 0))  # Green diagonal
            self.led.set_pixel(self.width-1-i, i, (0, 0, 255))  # Blue diagonal
        
        self.led.show()
        print("Pattern displayed. Press Ctrl+C to stop.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run LED mapping tests."""
    print("LED Mapping Test for 32x40 Display")
    print("Choose a test:")
    print("1. Sequential LED mapping")
    print("2. Coordinate mapping")
    print("3. Panel mapping")
    print("4. Simple pattern test")
    print("5. All tests")
    
    try:
        choice = input("Enter your choice (1-5): ").strip()
        
        test = LEDMappingTest()
        
        if choice == "1":
            test.test_sequential_mapping()
        elif choice == "2":
            test.test_coordinate_mapping()
        elif choice == "3":
            test.test_panel_mapping()
        elif choice == "4":
            test.test_simple_pattern()
        elif choice == "5":
            test.test_sequential_mapping()
            test.test_coordinate_mapping()
            test.test_panel_mapping()
            test.test_simple_pattern()
        else:
            print("Invalid choice. Running simple pattern test.")
            test.test_simple_pattern()
        
        test.cleanup()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        test.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        test.cleanup()

if __name__ == "__main__":
    main() 