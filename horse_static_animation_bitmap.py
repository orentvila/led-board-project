#!/usr/bin/env python3
"""
Horse Animation for LED Board
Displays a brown horse moving from left to right across green ground
"""

import time
from led_controller_exact import LEDControllerExact
import config

class HorseStaticAnimationBitmap:
    def __init__(self):
        """Initialize the horse animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Horse bitmap data (32x48 pixels) - single frame
        # Format: 0x00 = background, non-zero bits = horse pixels
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x01, 0xe0, 0x00, 0x00, 0x03, 0xe0, 0x00, 0x00, 0x0f, 0xf0,
            0x00, 0x00, 0x1f, 0xf8, 0x03, 0xff, 0xff, 0x98, 0x0f, 0xff, 0xff, 0x00, 0x1e, 0x7f, 0xfe, 0x00,
            0x30, 0xff, 0xfe, 0x00, 0x00, 0xff, 0xfe, 0x00, 0x01, 0xf7, 0xff, 0xc0, 0x03, 0xe0, 0x07, 0x20,
            0x06, 0xc0, 0x03, 0x10, 0x09, 0x80, 0x01, 0x0c, 0x31, 0x00, 0x00, 0x80, 0x61, 0x00, 0x00, 0xc0,
            0x01, 0x00, 0x00, 0x60, 0x00, 0x80, 0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        # 1 = horse pixel (black), 0 = background (white/transparent)
        self.horse_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                row_data.append(pixel)
            self.horse_pixels.append(row_data)
        
        # Colors
        self.horse_color = (139, 69, 19)  # Brown horse (saddle brown)
        self.ground_color = (34, 139, 34)  # Forest green ground
        self.ground_height = 4  # Height of ground at bottom
        
        # Find horse dimensions
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.horse_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.horse_actual_width = max_x - min_x + 1
        self.horse_actual_height = max_y - min_y + 1
        self.horse_offset_x = min_x
        self.horse_offset_y = min_y
        
        print(f"🐴 Horse dimensions: {self.horse_actual_width}x{self.horse_actual_height}, offset: ({self.horse_offset_x}, {self.horse_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_horse(self, x_pos):
        """Draw the horse bitmap at position x_pos."""
        # Position horse vertically (feet on ground)
        ground_y = self.height - self.ground_height
        horse_bottom_y = ground_y - 1  # Feet just above ground
        vertical_offset = horse_bottom_y - (self.horse_offset_y + self.horse_actual_height)
        
        # Draw horse pixels
        for y in range(48):
            for x in range(32):
                if self.horse_pixels[y][x] == 1:  # Horse pixel
                    screen_x = x + x_pos - self.horse_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if horse is on or above ground and within screen bounds
                    if 0 <= screen_x < self.width and screen_y < self.height - self.ground_height:
                        self.safe_set_pixel(screen_x, screen_y, self.horse_color)
    
    def run_animation(self, should_stop=None):
        """Run the horse animation - moves from left to right across the screen."""
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🐴 Starting horse animation...")
        
        # Animation parameters
        speed = 8.0  # pixels per second (horizontal speed)
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse animation stopped by user")
                break
            
            # Calculate horizontal position (horse moves from left to right, looping)
            # Start off-screen left, move across, then loop
            total_distance = self.width + self.horse_actual_width
            x_pos = int((elapsed * speed) % total_distance) - self.horse_actual_width
            
            # Clear and draw
            self.led.clear()
            self.draw_ground()
            self.draw_horse(x_pos)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐴 Horse animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
