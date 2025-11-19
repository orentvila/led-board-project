#!/usr/bin/env python3
"""
Cat Walking Animation for LED Board
Displays a cat walking across the screen for 10 seconds
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class CatWalkingAnimation:
    def __init__(self):
        """Initialize the cat walking animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Cat bitmap data (32x48 pixels)
        # Format: 0x00 = background, non-zero = cat pixel
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00,
            0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00,
            0x07, 0x00, 0x00, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0xc0, 0x03, 0x80, 0x00, 0xff, 0x07, 0xc0,
            0x00, 0xff, 0xff, 0xc0, 0x00, 0xff, 0xff, 0xc0, 0x00, 0xff, 0xfe, 0x00, 0x00, 0xff, 0xfe, 0x00,
            0x01, 0xff, 0xfe, 0x00, 0x03, 0xff, 0xfe, 0x00, 0x03, 0x70, 0x66, 0x00, 0x06, 0x70, 0xc7, 0x00,
            0x04, 0x60, 0xc3, 0x80, 0x04, 0x30, 0xc1, 0xc0, 0x00, 0x18, 0xc0, 0x40, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        # Format: 1 = cat pixel, 0 = background
        self.cat_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                # If bit is 1, it's a cat pixel
                row_data.append(pixel_bit)
            self.cat_pixels.append(row_data)
        
        # Find cat dimensions for proper positioning
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.cat_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.cat_width = max_x - min_x + 1
        self.cat_height = max_y - min_y + 1
        self.cat_offset_x = min_x
        self.cat_offset_y = min_y
        
        print(f"Cat dimensions: {self.cat_width}x{self.cat_height}, offset: ({self.cat_offset_x}, {self.cat_offset_y})")
        
        # Colors
        self.cat_color = (255, 165, 0)  # Orange cat
        self.ground_color = (34, 139, 34)  # Forest green ground
        self.ground_height = 4  # Height of ground at bottom
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        ground_y = self.height - self.ground_height
        for y in range(ground_y, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_cat(self, x_pos, y_bounce=0):
        """Draw the cat at the specified position with optional vertical bounce.
        
        Args:
            x_pos: X position (can be negative or > width for off-screen)
            y_bounce: Vertical bounce offset for walking animation
        """
        # Calculate cat position
        # The cat's bottom should align with the top of the ground
        # Ground starts at: height - ground_height = 48 - 4 = 44
        # Cat's bottom in bitmap is at: offset_y + cat_height = 15 + 20 = 35
        # So we need: cat_y + 35 = 44, therefore cat_y = 9
        cat_x = x_pos - self.cat_offset_x
        ground_top = self.height - self.ground_height  # 44
        cat_bottom_in_bitmap = self.cat_offset_y + self.cat_height  # 35
        cat_y = ground_top - cat_bottom_in_bitmap + y_bounce  # 44 - 35 = 9
        
        # Draw cat pixels
        for y in range(48):
            for x in range(32):
                if self.cat_pixels[y][x] == 1:
                    screen_x = cat_x + x
                    screen_y = cat_y + y
                    if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                        self.safe_set_pixel(screen_x, screen_y, self.cat_color)
    
    def run_animation(self, should_stop=None):
        """Run the cat walking animation for 10 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 10  # 10 seconds
        start_time = time.time()
        
        print("Starting cat walking animation...")
        print(f"Animation duration: {duration} seconds")
        
        # Animation: cat walks from left to right across screen
        # Start: cat enters from left (x = -cat_width)
        # End: cat exits to right (x = width)
        start_x = -self.cat_width
        end_x = self.width
        
        fps = 20  # 20 frames per second for smooth animation
        frame_duration = 1.0 / fps
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("Cat walking animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            progress = min(1.0, elapsed / duration)
            
            # Calculate horizontal position (linear movement)
            x_pos = int(start_x + progress * (end_x - start_x))
            
            # Add vertical bounce for walking effect (subtle up/down movement)
            # Bounce cycle: 0.3 seconds per cycle
            bounce_cycle = (elapsed * 3.33) % 1.0  # 3.33 cycles per second
            y_bounce = int(2 * math.sin(bounce_cycle * 2 * math.pi))  # -2 to +2 pixels
            
            # Clear and draw
            self.led.clear()
            self.draw_ground()
            self.draw_cat(x_pos, y_bounce)
            self.led.show()
            
            time.sleep(frame_duration)
        
        print("Cat walking animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run cat walking animation."""
    try:
        animation = CatWalkingAnimation()
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

