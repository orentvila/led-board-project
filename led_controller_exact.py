#!/usr/bin/env python3
"""
LED Controller with Exact Mapping
Uses the precise LED mapping function provided by the user
"""

import time
import numpy as np
from led_controller_fixed import LEDControllerFixed
import config

class LEDControllerExact:
    def __init__(self):
        """Initialize the LED controller with exact mapping."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Build coordinate mapping dictionaries
        self.led_to_coord_map = {}
        self.coord_to_led_map = {}
        
        # Create mapping for all 1280 LEDs
        for led_num in range(1, 1281):
            x, y = self.led_to_coordinate(led_num)
            if x is not None and y is not None:
                # Convert to our coordinate system (0-based, positive coordinates)
                coord_x = -x  # Convert negative X to positive
                coord_y = y   # Y is already correct
                
                # Store mappings
                self.led_to_coord_map[led_num] = (coord_x, coord_y)
                self.coord_to_led_map[(coord_x, coord_y)] = led_num
        
        print(f"LED Controller initialized with {len(self.led_to_coord_map)} LED mappings")
    
    def led_to_coordinate(self, led_num):
        """
        Convert LED number to X,Y coordinates for 5 stacked 32x8 matrices.
        
        Matrix layout (each 32x8 = 256 LEDs):
        Matrix 1: Y 0-7   (LEDs 1-256)   - Left to right serpentine
        Matrix 2: Y 8-15  (LEDs 257-512) - Right to left serpentine  
        Matrix 3: Y 16-23 (LEDs 513-768) - Left to right serpentine
        Matrix 4: Y 24-31 (LEDs 769-1024)- Right to left serpentine
        Matrix 5: Y 32-39 (LEDs 1025-1280)- Left to right serpentine
        """
        
        if led_num < 1 or led_num > 1280:
            return None, None
        
        # Convert to 0-based and find matrix
        led_index = led_num - 1
        matrix = led_index // 256  # Which matrix (0-4)
        pos_in_matrix = led_index % 256  # Position within matrix (0-255)
        
        # Calculate column and row within matrix
        col_in_matrix = pos_in_matrix // 8
        
        if matrix % 2 == 0:  # Matrices 1,3,5: Left-to-right serpentine
            if col_in_matrix % 2 == 0:  # Even columns: bottom to top
                row_in_matrix = pos_in_matrix % 8
            else:  # Odd columns: top to bottom
                row_in_matrix = 7 - (pos_in_matrix % 8)
            col = col_in_matrix
        else:  # Matrices 2,4: Right-to-left serpentine
            col = 31 - int(pos_in_matrix/8)
            
            if (col%2 ==0):
                row_in_matrix = pos_in_matrix%8
            else:
                row_in_matrix = 8 - pos_in_matrix%8 - 1
        
        # Convert to original coordinate system
        x = -col
        y = matrix * 8 + row_in_matrix
        
        return x, y
    
    def set_pixel(self, x, y, color):
        """Set a pixel at coordinates (x, y) to the specified color."""
        # Check bounds
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        
        # Get LED number for this coordinate
        led_num = self.coord_to_led_map.get((x, y))
        if led_num is None:
            return
        
        # Set the LED color
        r, g, b = color
        self.led.set_pixel(led_num - 1, r, g, b)  # Convert to 0-based LED index
    
    def fill_display(self, color):
        """Fill the entire display with the specified color."""
        r, g, b = color
        for led_num in range(1, 1281):
            self.led.set_pixel(led_num - 1, r, g, b)  # Convert to 0-based LED index
    
    def clear(self):
        """Clear the display (turn off all LEDs)."""
        self.fill_display((0, 0, 0))
    
    def show(self):
        """Update the display with the current pixel data."""
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
    
    def test_mapping(self):
        """Test the LED mapping by lighting up specific patterns."""
        print("Testing LED mapping...")
        
        # Test 1: Light up corners
        corners = [(0, 0), (31, 0), (0, 39), (31, 39)]
        for x, y in corners:
            self.set_pixel(x, y, (255, 0, 0))  # Red corners
            print(f"Corner ({x}, {y}) -> LED {self.coord_to_led_map.get((x, y), 'Not found')}")
        
        # Test 2: Light up center
        center_x, center_y = self.width // 2, self.height // 2
        self.set_pixel(center_x, center_y, (0, 255, 0))  # Green center
        print(f"Center ({center_x}, {center_y}) -> LED {self.coord_to_led_map.get((center_x, center_y), 'Not found')}")
        
        # Test 3: Light up a border
        for x in range(self.width):
            self.set_pixel(x, 0, (0, 0, 255))  # Blue top border
            self.set_pixel(x, self.height - 1, (0, 0, 255))  # Blue bottom border
        
        for y in range(self.height):
            self.set_pixel(0, y, (0, 0, 255))  # Blue left border
            self.set_pixel(self.width - 1, y, (0, 0, 255))  # Blue right border
        
        self.show()
        print("Mapping test completed!")

def main():
    """Test the exact LED mapping."""
    try:
        led = LEDControllerExact()
        led.test_mapping()
        
        print("\nPress Ctrl+C to exit...")
        time.sleep(5)  # Show the test pattern for 5 seconds
        
        led.cleanup()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        led.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        led.cleanup()

if __name__ == "__main__":
    main()
