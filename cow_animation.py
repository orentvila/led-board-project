#!/usr/bin/env python3
"""
Cow Animation for LED Board
Displays a cow bitmap for 8 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class CowAnimation:
    def __init__(self):
        """Initialize the cow animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Cow bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x60, 0x0c, 0x00, 0x00, 0x60, 0x0e, 0x00, 0x00, 0xe0,
            0x0f, 0xff, 0xff, 0xe0, 0x0f, 0xff, 0xff, 0xe0, 0x06, 0x3c, 0x78, 0xc0, 0x07, 0x70, 0x1d, 0xc0,
            0x0f, 0xe0, 0x0f, 0xe0, 0x0f, 0xc0, 0x07, 0xe0, 0x0c, 0xc0, 0x06, 0x60, 0x06, 0xc0, 0x03, 0x60,
            0x07, 0x98, 0x33, 0xc0, 0x03, 0x98, 0x33, 0x80, 0x00, 0x80, 0x03, 0x00, 0x00, 0xc0, 0x03, 0x00,
            0x00, 0xc7, 0xc6, 0x00, 0x00, 0xff, 0xf6, 0x00, 0x00, 0x78, 0x3c, 0x00, 0x00, 0x30, 0x1c, 0x00,
            0x00, 0x66, 0x4c, 0x00, 0x00, 0x66, 0x4c, 0x00, 0x00, 0x66, 0x4c, 0x00, 0x00, 0x60, 0x0c, 0x00,
            0x00, 0x70, 0x1c, 0x00, 0x00, 0x3f, 0xf8, 0x00, 0x00, 0x1f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.cow_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                row_data.append(pixel_bit)
            self.cow_pixels.append(row_data)
        
        self.cow_color = (139, 69, 19)  # Brown cow
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_cow(self):
        """Draw the cow bitmap."""
        self.led.clear()
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.cow_pixels[y][x] == 1:
                    self.safe_set_pixel(x, y, self.cow_color)
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the cow animation for 8 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 8  # 8 seconds
        start_time = time.time()
        
        print("Starting cow animation...")
        self.draw_cow()
        
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("Cow animation stopped by user")
                break
            time.sleep(0.1)
        
        print("Cow animation completed!")
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run cow animation."""
    try:
        animation = CowAnimation()
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

