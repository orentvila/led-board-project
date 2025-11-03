#!/usr/bin/env python3
"""
Snail Static Image for LED Board
Displays a static snail image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class SnailStaticAnimation:
    def __init__(self):
        """Initialize the snail static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.snail_color = (255, 255, 255)  # White for snail outline
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_snail(self):
        """Draw a simple snail - profile view, facing right, with spiral shell."""
        self.led.clear()  # Black background
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Shell - spiral design
        shell_center_x = center_x - 5
        shell_center_y = center_y - 5
        
        # Draw spiral
        import math
        for angle in range(0, 720, 10):  # 2 full rotations
            rad = math.radians(angle)
            radius = 3 + (angle / 720.0) * 6
            x = int(shell_center_x + radius * math.cos(rad))
            y = int(shell_center_y + radius * math.sin(rad))
            self.safe_set_pixel(x, y, self.snail_color)
        
        # Shell outline
        shell_radius = 9
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(shell_center_x + shell_radius * math.cos(rad))
            y = int(shell_center_y + shell_radius * math.sin(rad))
            self.safe_set_pixel(x, y, self.snail_color)
        
        # Body - elongated, rounded top, flat base
        body_start_x = center_x - 8
        body_y = center_y + 2
        
        for y in range(body_y, body_y + 8):
            if y < body_y + 2:
                width = 4
            elif y < body_y + 6:
                width = 6
            else:
                width = 8  # Foot
            for x in range(body_start_x, body_start_x + width):
                self.safe_set_pixel(x, y, self.snail_color)
        
        # Head
        head_x = body_start_x + 6
        head_y = body_y + 1
        for y in range(head_y - 1, head_y + 3):
            width = 2 if y < head_y + 1 else 3
            for x in range(head_x, head_x + width):
                self.safe_set_pixel(x, y, self.snail_color)
        
        # Antennae
        antenna_y = head_y
        for offset in [0, 2]:
            # Antenna
            for y in range(antenna_y - 3, antenna_y):
                self.safe_set_pixel(head_x + offset, y, self.snail_color)
            # Eye at tip
            self.safe_set_pixel(head_x + offset, antenna_y - 4, self.snail_color)
        
        # Smile
        self.safe_set_pixel(head_x + 1, head_y + 1, self.snail_color)
        self.safe_set_pixel(head_x + 2, head_y + 1, self.snail_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the snail static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🐌 Starting snail static image...")
        
        self.draw_snail()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐌 Snail image stopped by user")
                break
            time.sleep(0.1)
        
        print("🐌 Snail image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

