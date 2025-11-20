#!/usr/bin/env python3
"""
Duck Animation for LED Board
Displays a duck bitmap for 8 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class DuckAnimation:
    def __init__(self):
        """Initialize the duck animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Duck bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x0f, 0x80,
            0x00, 0x00, 0x0f, 0x80, 0x00, 0x00, 0x1f, 0xe0, 0x00, 0x00, 0x1f, 0x70, 0x00, 0x00, 0x1f, 0x00,
            0x00, 0x00, 0x1f, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x0f, 0x80,
            0x00, 0x01, 0xf7, 0x80, 0x08, 0xc7, 0xef, 0x80, 0x0c, 0xef, 0xdf, 0xc0, 0x0e, 0xf0, 0x3f, 0xc0,
            0x07, 0x7f, 0xff, 0xc0, 0x07, 0xbf, 0xff, 0xc0, 0x01, 0xbf, 0xff, 0xc0, 0x03, 0xaf, 0xff, 0xc0,
            0x03, 0xb0, 0x7f, 0x80, 0x03, 0xf7, 0xff, 0x80, 0x03, 0xd7, 0xff, 0x00, 0x01, 0xe9, 0xde, 0x00,
            0x00, 0xff, 0xfc, 0x00, 0x00, 0x7f, 0xf0, 0x00, 0x00, 0x0f, 0x88, 0x00, 0x00, 0x00, 0x08, 0x00,
            0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.duck_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                row_data.append(pixel_bit)
            self.duck_pixels.append(row_data)
        
        self.duck_color = (204, 208, 212)  # #CCD0D4 - Light gray duck
        self.beak_color = (230, 39, 39)  # #E62727 - Red beak
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def is_beak_pixel(self, x, y):
        """Check if pixel is part of the beak (front area)."""
        # Beak is typically in the front area of the duck head
        # Approximate beak area: x around 18-26, y around 10-18
        if 18 <= x <= 26 and 10 <= y <= 18:
            return True
        return False
    
    def draw_duck(self):
        """Draw the duck bitmap."""
        self.led.clear()
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.duck_pixels[y][x] == 1:
                    # Check if this is a beak pixel
                    if self.is_beak_pixel(x, y):
                        self.safe_set_pixel(x, y, self.beak_color)
                    else:
                        self.safe_set_pixel(x, y, self.duck_color)
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the duck animation for 8 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 8  # 8 seconds
        start_time = time.time()
        
        print("Starting duck animation...")
        self.draw_duck()
        
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("Duck animation stopped by user")
                break
            time.sleep(0.1)
        
        print("Duck animation completed!")
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run duck animation."""
    try:
        animation = DuckAnimation()
        animation.run_animation()
        animation.cleanup()
    except KeyboardInterrupt:
        print("\nAnimation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()
