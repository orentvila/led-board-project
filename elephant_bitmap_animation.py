#!/usr/bin/env python3
"""
Elephant Bitmap Animation for LED Board
Displays an elephant image from binary bitmap data
"""

import time
import math
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
        self.ground_color = (139, 90, 43)  # Brown soil color
        
        # Animation settings
        self.ground_height = 3
        # Ground starts at y = height - ground_height = 48 - 3 = 45
        self.ground_y = self.height - self.ground_height  # y=45
        
        # Find the actual bottom row of the elephant in the bitmap
        # (the lowest row that has any pixels)
        self.elephant_bitmap_bottom = None
        for y in range(46, -1, -1):  # Check from bottom up, excluding row 47
            has_pixels = False
            for x in range(4, 32):  # Skip first 4 pixels
                if self.elephant_pixels[y][x] == 1:
                    has_pixels = True
                    break
            if has_pixels:
                self.elephant_bitmap_bottom = y
                break
        
        if self.elephant_bitmap_bottom is None:
            self.elephant_bitmap_bottom = 46  # Fallback
        
        print(f"Elephant bitmap bottom row: {self.elephant_bitmap_bottom}")
        print(f"Ground level: y={self.ground_y}")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_elephant(self, x_offset=0, y_offset=0):
        """Draw the elephant from the bitmap data with grey color and brown ground.
        
        Args:
            x_offset: Horizontal offset for walking animation
            y_offset: Vertical offset for walking bounce effect
        """
        self.led.clear()  # Black background
        
        # Draw ground/soil at the bottom
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
        
        # Draw elephant - positioned so its bottom pixels sit on the ground
        # Position the elephant's actual bottom row at ground level
        for bitmap_y in range(47):  # Rows 0-46 (excluding row 47)
            # Calculate actual screen Y position
            # Position elephant's bottom row (elephant_bitmap_bottom) at ground level
            # So: screen_y = ground_y - (elephant_bitmap_bottom - bitmap_y) + y_offset
            screen_y = self.ground_y - (self.elephant_bitmap_bottom - bitmap_y) + y_offset
            
            # Skip if outside screen bounds (above screen)
            # Allow pixels at ground level (y=45) so elephant sits on ground
            if screen_y < 0 or screen_y >= self.height:
                continue
            
            for bitmap_x in range(32):
                # Skip the first 4 pixels on the left (x < 4)
                if bitmap_x < 4:
                    continue
                    
                if self.elephant_pixels[bitmap_y][bitmap_x] == 1:
                    # Calculate actual screen X position
                    screen_x = bitmap_x - 4 + x_offset  # -4 because we skip first 4 pixels
                    
                    # Wrap around horizontally for continuous walking
                    if screen_x < 0:
                        screen_x = screen_x + self.width
                    elif screen_x >= self.width:
                        screen_x = screen_x - self.width
                    
                    # Draw elephant pixel (can be at ground level, elephant drawn on top of ground)
                    if screen_y >= 0 and screen_y < self.height:
                        self.safe_set_pixel(screen_x, screen_y, self.elephant_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the elephant walking animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🐘 Starting elephant walking animation...")
        
        # Animation parameters
        walk_speed = 8.0  # pixels per second (horizontal movement speed)
        bounce_amplitude = 0.8  # pixels (reduced for smoother vertical bounce)
        bounce_frequency = 1.5  # cycles per second (slower for smoother motion)
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐘 Elephant animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            
            # Calculate horizontal position using time-based smooth movement
            # Walk from left to right, looping continuously
            total_distance = self.width + 8  # +8 for smooth looping
            x_offset_float = (elapsed * walk_speed) % total_distance
            x_offset = round(x_offset_float)  # Use round instead of int for smoother motion
            
            # Calculate vertical bounce (subtle up/down motion for walking effect)
            # Use smoother sine wave with smaller amplitude
            y_offset_float = math.sin(elapsed * bounce_frequency * 2 * math.pi) * bounce_amplitude
            y_offset = round(y_offset_float)  # Use round instead of int for smoother motion
            
            self.draw_elephant(x_offset=x_offset, y_offset=y_offset)
            
            time.sleep(0.05)  # 20 FPS for smoother animation
        
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

