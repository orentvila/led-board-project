#!/usr/bin/env python3
"""
Snail Animation for LED Board
Displays a snail on light green ground
"""

import time
from led_controller_exact import LEDControllerExact
import config

class SnailStaticAnimationBitmap:
    def __init__(self):
        """Initialize the snail animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH
        self.height = config.TOTAL_HEIGHT
        
        # Snail bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x20, 0x00, 0x00, 0x01, 0x20, 0x00, 0x7f, 0x01, 0x20,
            0x00, 0xe1, 0xc1, 0xe0, 0x01, 0x80, 0x61, 0xc0, 0x03, 0x00, 0x23, 0xe0, 0x06, 0x38, 0x36, 0x20,
            0x04, 0x7c, 0x1e, 0x20, 0x04, 0x46, 0x1c, 0x60, 0x04, 0x42, 0x18, 0x40, 0x04, 0x02, 0x18, 0xc0,
            0x04, 0x07, 0xf0, 0xc0, 0x07, 0xff, 0xe1, 0x80, 0x03, 0x00, 0x01, 0x00, 0x06, 0x00, 0x03, 0x00,
            0x0c, 0x00, 0x06, 0x00, 0x0f, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.snail_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                # 1 = snail pixel, 0 = background
                row_data.append(pixel)
            self.snail_pixels.append(row_data)
        
        # Colors
        # Snail color: #384247 = RGB(56, 66, 71)
        self.snail_color = (56, 66, 71)
        # Ground: green
        self.ground_color = (0, 255, 0)  # Green
        self.ground_height = 7  # Height of ground at bottom
        
        # Find snail dimensions
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.snail_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.snail_actual_width = max_x - min_x + 1
        self.snail_actual_height = max_y - min_y + 1
        self.snail_offset_x = min_x
        self.snail_offset_y = min_y
        
        print(f"🐌 Snail dimensions: {self.snail_actual_width}x{self.snail_actual_height}, offset: ({self.snail_offset_x}, {self.snail_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw light green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_snail(self):
        """Draw the snail bitmap centered on the screen, positioned on ground."""
        # Center the snail horizontally
        center_x = self.width // 2
        x_pos = center_x - (self.snail_actual_width // 2) - self.snail_offset_x
        
        # Position snail vertically (bottom on ground)
        ground_y = self.height - self.ground_height
        snail_bottom_y = ground_y  # Snail bottom on ground line
        vertical_offset = snail_bottom_y - (self.snail_offset_y + self.snail_actual_height)
        
        # Draw snail pixels
        for y in range(48):
            for x in range(32):
                if self.snail_pixels[y][x] == 1:  # Snail pixel
                    screen_x = x + x_pos
                    screen_y = y + vertical_offset
                    
                    # Only draw if snail is on or above ground and within screen bounds
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        self.safe_set_pixel(screen_x, screen_y, self.snail_color)
    
    def run_animation(self, should_stop=None):
        """Display the snail as a static image centered on the screen."""
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🐌 Starting snail animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐌 Snail animation stopped by user")
                break
            
            # Draw static snail centered on screen
            self.led.clear()
            self.draw_ground()
            self.draw_snail()
            self.led.show()
            
            time.sleep(0.1)  # Update every 0.1 seconds (static display)
        
        print("🐌 Snail animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        self.led.cleanup()

