#!/usr/bin/env python3
"""
Fixed LED Controller using the exact mapping from the user's script
"""

import time
import numpy as np
import sys
import config

# Use mock modules on Windows, real modules on Raspberry Pi
if sys.platform.startswith('win'):
    from mock_rpi import WS281x
    PixelStrip = WS281x
    Color = lambda r, g, b: (r, g, b)
    print("Using mock Raspberry Pi modules for Windows development")
else:
    # Retry import with delay to handle race conditions during restart
    PixelStrip = None
    Color = None
    import time
    
    for attempt in range(3):
        try:
            from rpi_ws281x import PixelStrip, Color
            print("✅ rpi_ws281x imported successfully")
            break
        except ImportError as e:
            if attempt < 2:
                print(f"⚠️ rpi_ws281x import attempt {attempt + 1} failed, retrying...")
                time.sleep(0.5)  # Brief delay before retry
            else:
                print(f"❌ Warning: rpi_ws281x not found after {attempt + 1} attempts, using mock modules")
                print(f"   Error: {e}")
                from mock_rpi import WS281x
                PixelStrip = WS281x
                Color = lambda r, g, b: (r, g, b)

class LEDControllerFixed:
    def __init__(self):
        """Initialize the LED controller for the 32x48 display."""
        # Convert brightness to uint8 (0-255)
        brightness_uint8 = int(config.BRIGHTNESS * 255)
        
        self.strip = PixelStrip(
            config.TOTAL_LEDS,
            config.LED_PIN,
            config.LED_FREQ_HZ,
            config.LED_DMA,
            config.LED_INVERT,
            brightness_uint8,
            config.LED_CHANNEL
        )
        self.strip.begin()
        
        # Create display matrix (32x48)
        self.display_matrix = np.zeros((config.TOTAL_HEIGHT, config.TOTAL_WIDTH, 3), dtype=np.uint8)
        
        # Create LED to coordinate mapping
        self.led_to_coord_map = {}
        self.coord_to_led_map = {}
        self._create_mapping()
        
        # Clear display on startup
        self.clear()
        self.show()
    
    def _create_mapping(self):
        """Create the LED number to coordinate mapping."""
        for led_num in range(1, config.TOTAL_LEDS + 1):
            x, y = self._led_to_coordinate(led_num)
            if x is not None and y is not None:
                # Convert negative X to positive and ensure Y is within bounds
                x_positive = abs(x)
                if 0 <= x_positive < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                    self.led_to_coord_map[led_num] = (x_positive, y)
                    self.coord_to_led_map[(x_positive, y)] = led_num
    
    def _led_to_coordinate(self, led_num):
        """
        Convert LED number to X,Y coordinates for 6 stacked 32x8 matrices.
        
        Matrix layout (each 32x8 = 256 LEDs):
        Matrix 1: Y 0-7   (LEDs 1-256)   - Left to right serpentine
        Matrix 2: Y 8-15  (LEDs 257-512) - Right to left serpentine  
        Matrix 3: Y 16-23 (LEDs 513-768) - Left to right serpentine
        Matrix 4: Y 24-31 (LEDs 769-1024)- Right to left serpentine
        Matrix 5: Y 32-39 (LEDs 1025-1280)- Left to right serpentine
        Matrix 6: Y 40-47 (LEDs 1281-1536)- Right to left serpentine
        """
        
        if led_num < 1 or led_num > config.TOTAL_LEDS:
            return None, None
        
        # Convert to 0-based and find matrix
        led_index = led_num - 1
        matrix = led_index // 256  # Which matrix (0-5)
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
    
    def clear(self):
        """Clear the entire display."""
        self.display_matrix.fill(0)
        for i in range(config.TOTAL_LEDS):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
    
    def set_pixel(self, x, y, color):
        """Set a single pixel at position (x, y) with the given color."""
        if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
            self.display_matrix[y, x] = color
            
            # Find the LED number for this coordinate
            if (x, y) in self.coord_to_led_map:
                led_num = self.coord_to_led_map[(x, y)]
                # LED numbers are 1-based, but strip.setPixelColorRGB is 0-based
                led_index = led_num - 1
                r, g, b = int(color[0]), int(color[1]), int(color[2])
                self.strip.setPixelColorRGB(led_index, r, g, b)
    
    def fill_display(self, color):
        """Fill the entire display with a color."""
        self.display_matrix.fill(color)
        for led_num in range(1, config.TOTAL_LEDS + 1):
            led_index = led_num - 1
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            self.strip.setPixelColorRGB(led_index, r, g, b)
    
    def draw_rectangle(self, x1, y1, x2, y2, color, fill=False):
        """Draw a rectangle from (x1, y1) to (x2, y2)."""
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if fill or (x == x1 or x == x2 or y == y1 or y == y2):
                    self.set_pixel(x, y, color)
    
    def show(self):
        """Update the physical LED display."""
        self.strip.show()
    
    def set_brightness(self, brightness):
        """Set the brightness of all LEDs (0.0 to 1.0)."""
        brightness = max(0.0, min(1.0, brightness))
        brightness_uint8 = int(brightness * 255)
        self.strip.setBrightness(brightness_uint8)
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.clear()
            self.show()
            time.sleep(0.1)
            if hasattr(self, 'strip'):
                del self.strip
        except Exception as e:
            print(f"Cleanup warning: {e}") 