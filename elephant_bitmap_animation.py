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
        self.elephant_color = (150, 150, 150)  # Grey for elephant
        self.ground_color = (34, 139, 34)  # Forest green ground (same as horse)
        
        # Animation settings
        self.ground_height = 4  # Height of ground at bottom (same as horse)
        self.ground_y = self.height - self.ground_height
        
        # Find elephant dimensions for proper positioning
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.elephant_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.elephant_actual_width = max_x - min_x + 1
        self.elephant_actual_height = max_y - min_y + 1
        self.elephant_offset_x = min_x
        self.elephant_offset_y = min_y
        
        print(f"🐘 Elephant dimensions: {self.elephant_actual_width}x{self.elephant_actual_height}, offset: ({self.elephant_offset_x}, {self.elephant_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_elephant(self, x_pos):
        """Draw the elephant bitmap at horizontal position x_pos."""
        # Position elephant vertically (feet touching ground) - same logic as horse
        ground_y = self.height - self.ground_height
        elephant_bottom_y = ground_y  # Feet on ground line
        vertical_offset = elephant_bottom_y - (self.elephant_offset_y + self.elephant_actual_height)
        
        # Draw elephant pixels
        for y in range(48):
            for x in range(32):
                if self.elephant_pixels[y][x] == 1:  # Elephant pixel
                    screen_x = x + x_pos - self.elephant_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if elephant is on or above ground and within screen bounds
                    # Allow drawing at ground level (screen_y <= ground_y) so elephant touches ground
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        self.safe_set_pixel(screen_x, screen_y, self.elephant_color)
    
    def run_animation(self, should_stop=None):
        """Run the elephant animation - moves from left to right in a straight line."""
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐘 Starting elephant animation...")
        
        # Animation parameters
        speed = (self.width + self.elephant_actual_width) / duration  # pixels per second
        
        # Draw first frame immediately to prevent blinking
        elapsed = 0
        x_pos = int(elapsed * speed) - self.elephant_actual_width
        self.led.clear()
        self.draw_ground()
        self.draw_elephant(x_pos)
        self.led.show()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐘 Elephant animation stopped by user")
                break
            
            # Calculate horizontal position (elephant moves from left to right)
            # Start off-screen left, move across, exit off-screen right
            x_pos = int(elapsed * speed) - self.elephant_actual_width
            
            # Draw frame
            self.led.clear()
            self.draw_ground()
            self.draw_elephant(x_pos)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
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

