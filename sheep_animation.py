#!/usr/bin/env python3
"""
Sheep Animation for LED Board
Displays a sheep bitmap for 8 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class SheepAnimation:
    def __init__(self):
        """Initialize the sheep animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Sheep bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x10, 0x00,
            0x00, 0x3f, 0xfc, 0x00, 0x00, 0x22, 0x4c, 0x00, 0x00, 0xe0, 0x07, 0x00, 0x01, 0x80, 0x01, 0x80,
            0x01, 0x00, 0x00, 0x80, 0x1f, 0x00, 0x00, 0xf0, 0x1f, 0xa0, 0x01, 0xf8, 0x18, 0xe0, 0x07, 0x18,
            0x18, 0xf6, 0x6f, 0x18, 0x08, 0xff, 0xff, 0x10, 0x0f, 0x80, 0x03, 0xf0, 0x07, 0x80, 0x03, 0xe0,
            0x00, 0x84, 0x23, 0x00, 0x00, 0x84, 0x23, 0x00, 0x00, 0x80, 0x03, 0x00, 0x00, 0xc0, 0x03, 0x00,
            0x00, 0xc0, 0x03, 0x00, 0x00, 0xc0, 0x03, 0x00, 0x00, 0x42, 0x42, 0x00, 0x00, 0x63, 0xc6, 0x00,
            0x00, 0x31, 0x8c, 0x00, 0x00, 0x39, 0x9c, 0x00, 0x00, 0x1f, 0xf0, 0x00, 0x00, 0x07, 0xe0, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.sheep_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                row_data.append(pixel_bit)
            self.sheep_pixels.append(row_data)
        
        self.sheep_color = (255, 255, 255)  # White sheep
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_sheep(self):
        """Draw the sheep bitmap."""
        self.led.clear()
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.sheep_pixels[y][x] == 1:
                    self.safe_set_pixel(x, y, self.sheep_color)
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the sheep animation for 8 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 8  # 8 seconds
        start_time = time.time()
        
        print("Starting sheep animation...")
        self.draw_sheep()
        
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("Sheep animation stopped by user")
                break
            time.sleep(0.1)
        
        print("Sheep animation completed!")
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run sheep animation."""
    try:
        animation = SheepAnimation()
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

