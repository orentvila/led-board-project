#!/usr/bin/env python3
"""
Elephant Bitmap Animation for LED Board
Displays an elephant image from binary bitmap data
"""

import time
from led_controller_exact import LEDControllerExact
import config

class ElephantBitmapAnimation:
    def __init__(self):
        """Initialize the elephant bitmap animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Elephant bitmap data (32x48 pixels)
        # Each byte represents 8 horizontal pixels (MSB first)
        # 32 pixels per row = 4 bytes per row
        # 48 rows total = 192 bytes
        bitmap_hex = [
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00,
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00,
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x30, 0x00,
            0xf0, 0x00, 0xff, 0x00, 0xf0, 0x1d, 0xff, 0xc0, 0xf0, 0x39, 0xff, 0xf0, 0xf0, 0x79, 0xff, 0xf0,
            0xf0, 0xf9, 0xfb, 0xf8, 0xf1, 0xfd, 0xfb, 0xf8, 0xf1, 0xfc, 0xfb, 0x78, 0xf1, 0xfe, 0xf3, 0xf8,
            0xf3, 0xfe, 0x77, 0xf8, 0xf3, 0xff, 0x27, 0xf8, 0xf3, 0xff, 0x8f, 0xf8, 0xf1, 0xff, 0xfd, 0xf8,
            0xf1, 0xff, 0xfc, 0x78, 0xf1, 0xff, 0xf8, 0x78, 0xf0, 0xff, 0xf8, 0x78, 0xf0, 0xff, 0xf9, 0xf8,
            0xf0, 0x7f, 0xf3, 0xf8, 0xf0, 0x78, 0xf7, 0xf0, 0xf0, 0x78, 0xf3, 0xe0, 0xf0, 0x78, 0xf0, 0x00,
            0xf0, 0x78, 0xf0, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00,
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00,
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00,
            0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xf0, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to 32x48 pixel array
        # Each byte has 8 bits, MSB first (bit 7 is leftmost pixel)
        # 32 pixels per row = 4 bytes per row
        # Bit value 1 = elephant pixel (draw), Bit value 0 = background (don't draw)
        self.elephant_pixels = []
        
        for row in range(48):
            row_data = []
            byte_start = row * 4  # 4 bytes per row
            for col in range(32):
                byte_index = byte_start + (col // 8)  # Which byte in the row
                bit_index = 7 - (col % 8)  # MSB first (bit 7 is leftmost pixel)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                # NO INVERSION: 1 = elephant pixel, 0 = background
                row_data.append(pixel)
            self.elephant_pixels.append(row_data)
        
        # Colors
        self.elephant_color = (255, 255, 255)  # White for elephant
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_elephant(self):
        """Draw the elephant from the bitmap data."""
        self.led.clear()  # Black background
        
        # Draw elephant - only draw pixels that are 1 in the bitmap
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.elephant_pixels[y][x] == 1:
                    self.safe_set_pixel(x, y, self.elephant_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the elephant bitmap animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐘 Starting elephant bitmap animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐘 Elephant animation stopped by user")
                break
            
            self.draw_elephant()
            time.sleep(0.1)  # 10 FPS
        
        print("🐘 Elephant animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run elephant bitmap animation."""
    try:
        animation = ElephantBitmapAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()

