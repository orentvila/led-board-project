#!/usr/bin/env python3
"""
Rooster Animation for LED Board
Displays a rooster bitmap for 8 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class RoosterAnimation:
    def __init__(self):
        """Initialize the rooster animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Rooster bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf0,
            0x00, 0x00, 0x00, 0xf8, 0x00, 0x00, 0x01, 0xf8, 0x00, 0x00, 0x03, 0xf8, 0x00, 0x00, 0x03, 0xfc,
            0x00, 0x00, 0x07, 0xf8, 0x0f, 0xe0, 0x0f, 0xf8, 0x1f, 0xf0, 0x0f, 0xf8, 0x1f, 0xf8, 0x1f, 0xe0,
            0x3f, 0xfc, 0x3f, 0xe0, 0x3f, 0xfe, 0xff, 0xe0, 0x3f, 0xfd, 0xff, 0xe0, 0x3f, 0xfd, 0xfd, 0xe0,
            0x3f, 0xfb, 0xfb, 0xe0, 0x1f, 0xe7, 0xf7, 0xe0, 0x1f, 0xf1, 0xe7, 0xc0, 0x07, 0xff, 0x1f, 0xc0,
            0x03, 0xff, 0xff, 0xc0, 0x00, 0x7f, 0xff, 0x80, 0x00, 0x3f, 0xff, 0x00, 0x00, 0x1f, 0xff, 0x00,
            0x00, 0x0f, 0xfe, 0x00, 0x00, 0x07, 0xf8, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x60, 0x00,
            0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.rooster_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                row_data.append(pixel_bit)
            self.rooster_pixels.append(row_data)
        
        self.rooster_color = (255, 140, 0)  # Orange rooster
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_rooster(self):
        """Draw the rooster bitmap."""
        self.led.clear()
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.rooster_pixels[y][x] == 1:
                    self.safe_set_pixel(x, y, self.rooster_color)
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the rooster animation for 8 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 8  # 8 seconds
        start_time = time.time()
        
        print("Starting rooster animation...")
        self.draw_rooster()
        
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("Rooster animation stopped by user")
                break
            time.sleep(0.1)
        
        print("Rooster animation completed!")
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run rooster animation."""
    try:
        animation = RoosterAnimation()
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
