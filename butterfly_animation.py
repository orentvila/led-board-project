#!/usr/bin/env python3
"""
Butterfly Animation for LED Board
Displays a colorful butterfly using bitmap with fluttering motion
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class ButterflyAnimation:
    def __init__(self):
        """Initialize the butterfly animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Butterfly bitmap data (32x48 pixels)
        # Format: 0x00 = background, non-zero bits = butterfly pixels
        # Simple butterfly shape - wings spread
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        # 1 = butterfly pixel, 0 = background
        self.butterfly_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                row_data.append(pixel)
            self.butterfly_pixels.append(row_data)
        
        # Colors
        # #EC6290 = RGB(236, 98, 144) - Pink
        # #9B42B3 = RGB(155, 66, 179) - Purple
        self.color1 = (236, 98, 144)  # Pink
        self.color2 = (155, 66, 179)  # Purple
        
        # Find butterfly dimensions
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.butterfly_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.butterfly_actual_width = max_x - min_x + 1 if max_x >= min_x else 0
        self.butterfly_actual_height = max_y - min_y + 1 if max_y >= min_y else 0
        self.butterfly_offset_x = min_x
        self.butterfly_offset_y = min_y
        
        print(f"🦋 Butterfly dimensions: {self.butterfly_actual_width}x{self.butterfly_actual_height}, offset: ({self.butterfly_offset_x}, {self.butterfly_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_butterfly(self, x_pos, y_pos, wing_phase=0):
        """Draw the butterfly bitmap at position with color variation based on wing position.
        
        Args:
            x_pos, y_pos: Position to draw butterfly
            wing_phase: Phase for wing animation (0-2*pi) - used for color variation
        """
        # Alternate colors based on wing position (left vs right)
        # Use wing_phase to determine which color to use for each pixel
        color_phase = math.sin(wing_phase)  # -1 to 1
        
        for y in range(48):
            for x in range(32):
                if self.butterfly_pixels[y][x] == 1:  # Butterfly pixel
                    screen_x = x + x_pos - self.butterfly_offset_x
                    screen_y = y + y_pos - self.butterfly_offset_y
                    
                    if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                        # Determine color based on x position (left = pink, right = purple)
                        # Or alternate based on wing_phase for animation effect
                        if x < 16:  # Left side - pink
                            color = self.color1
                        else:  # Right side - purple
                            color = self.color2
                        
                        self.safe_set_pixel(screen_x, screen_y, color)
    
    def run_animation(self, should_stop=None):
        """Run the butterfly animation with fluttering motion."""
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🦋 Starting butterfly animation...")
        
        # Animation parameters
        flutter_speed = 8.0  # Wing flutter cycles per second
        horizontal_speed = 2.0  # Horizontal drift speed (pixels per second)
        vertical_speed = 1.5  # Vertical flutter speed (pixels per second)
        
        # Start position
        start_x = self.width // 4
        start_y = self.height // 2
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🦋 Butterfly animation stopped by user")
                break
            
            # Calculate butterfly position with gentle drift
            # Horizontal: gentle drift across screen
            x_pos = (start_x + elapsed * horizontal_speed) % (self.width + 10) - 5
            
            # Vertical: fluttering up and down motion
            vertical_flutter = math.sin(elapsed * vertical_speed * 2 * math.pi) * 3
            y_pos = start_y + int(vertical_flutter)
            
            # Wing fluttering phase
            wing_phase = elapsed * flutter_speed * 2 * math.pi
            
            # Clear and draw
            self.led.clear()
            self.draw_butterfly(int(x_pos), int(y_pos), wing_phase)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🦋 Butterfly animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
