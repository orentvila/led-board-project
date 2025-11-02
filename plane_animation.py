#!/usr/bin/env python3
"""
Plane Animation for LED Board
Displays a plane image from binary bitmap data
"""

import time
from led_controller_exact import LEDControllerExact
import config

class PlaneAnimation:
    def __init__(self):
        """Initialize the plane animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Plane bitmap data (32x48 pixels)
        # Each byte represents 8 horizontal pixels (MSB first)
        # 32 pixels per row = 4 bytes per row
        # 48 rows total = 192 bytes
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xfd, 0xff, 0xff, 0x32, 0xf6, 0xff, 0xff, 0xf9, 0x6b, 0xff, 0xfe, 0x1f, 0xdd, 0xff,
            0xff, 0xc7, 0xbb, 0xff, 0xff, 0xf1, 0x77, 0xff, 0xff, 0xfc, 0xe7, 0xff, 0xff, 0xff, 0xdb, 0xff,
            0xff, 0xff, 0xbd, 0xff, 0xff, 0xff, 0x9b, 0xff, 0xff, 0x7f, 0xdd, 0xff, 0xfe, 0xeb, 0xcd, 0xff,
            0xff, 0x97, 0xed, 0xff, 0xff, 0xef, 0xe5, 0xff, 0xff, 0xef, 0xf7, 0xff, 0xff, 0x7b, 0xf3, 0xff,
            0xfe, 0xf7, 0xf9, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to 32x48 pixel array
        # Each byte has 8 bits, MSB first (bit 7 is leftmost pixel)
        # 32 pixels per row = 4 bytes per row
        self.plane_pixels = []
        
        for row in range(48):
            row_data = []
            byte_start = row * 4  # 4 bytes per row
            for col in range(32):
                byte_index = byte_start + (col // 8)  # Which byte in the row
                bit_index = 7 - (col % 8)  # MSB first (bit 7 is leftmost pixel)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                row_data.append(pixel)
            self.plane_pixels.append(row_data)
        
        # Colors
        self.plane_color = (255, 255, 255)  # White for plane
        self.bg_color = (0, 0, 0)  # Black background
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_plane(self):
        """Draw the plane from the bitmap data."""
        self.led.clear()
        
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.plane_pixels[y][x] == 1:
                    self.safe_set_pixel(x, y, self.plane_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the plane animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("✈️ Starting plane animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("✈️ Plane animation stopped by user")
                break
            
            self.draw_plane()
            time.sleep(0.1)  # 10 FPS
        
        print("✈️ Plane animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run plane animation."""
    try:
        animation = PlaneAnimation()
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

