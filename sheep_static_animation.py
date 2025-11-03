#!/usr/bin/env python3
"""
Sheep Static Image for LED Board
Displays a static sheep image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class SheepStaticAnimation:
    def __init__(self):
        """Initialize the sheep static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.sheep_color = (255, 255, 255)  # White for sheep outline
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_sheep(self):
        """Draw a simple sheep - fluffy, cloud-like shapes."""
        self.led.clear()  # Black background
        
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Head - small cloud shape
        head_x = center_x
        head_y = center_y - 8
        
        # Cloud-like head outline
        cloud_points_head = [
            (head_x - 2, head_y), (head_x - 1, head_y), (head_x, head_y), (head_x + 1, head_y), (head_x + 2, head_y),
            (head_x - 3, head_y + 1), (head_x - 2, head_y + 1), (head_x - 1, head_y + 1), (head_x, head_y + 1), 
            (head_x + 1, head_y + 1), (head_x + 2, head_y + 1), (head_x + 3, head_y + 1),
            (head_x - 2, head_y + 2), (head_x - 1, head_y + 2), (head_x, head_y + 2), (head_x + 1, head_y + 2), (head_x + 2, head_y + 2),
        ]
        for x, y in cloud_points_head:
            self.safe_set_pixel(x, y, self.sheep_color)
        
        # Ears
        self.safe_set_pixel(head_x - 3, head_y + 1, self.sheep_color)
        self.safe_set_pixel(head_x + 3, head_y + 1, self.sheep_color)
        
        # Eyes
        self.safe_set_pixel(head_x - 1, head_y + 1, self.sheep_color)
        self.safe_set_pixel(head_x + 1, head_y + 1, self.sheep_color)
        
        # Nose
        self.safe_set_pixel(head_x, head_y + 2, self.sheep_color)
        
        # Body - larger cloud shape
        body_x = center_x
        body_y = center_y
        
        cloud_points_body = [
            (body_x - 4, body_y), (body_x - 3, body_y), (body_x - 2, body_y), (body_x - 1, body_y),
            (body_x, body_y), (body_x + 1, body_y), (body_x + 2, body_y), (body_x + 3, body_y), (body_x + 4, body_y),
            (body_x - 5, body_y + 1), (body_x - 4, body_y + 1), (body_x - 3, body_y + 1), (body_x - 2, body_y + 1),
            (body_x - 1, body_y + 1), (body_x, body_y + 1), (body_x + 1, body_y + 1), (body_x + 2, body_y + 1),
            (body_x + 3, body_y + 1), (body_x + 4, body_y + 1), (body_x + 5, body_y + 1),
            (body_x - 4, body_y + 2), (body_x - 3, body_y + 2), (body_x - 2, body_y + 2), (body_x - 1, body_y + 2),
            (body_x, body_y + 2), (body_x + 1, body_y + 2), (body_x + 2, body_y + 2), (body_x + 3, body_y + 2), (body_x + 4, body_y + 2),
            (body_x - 3, body_y + 3), (body_x - 2, body_y + 3), (body_x - 1, body_y + 3), (body_x, body_y + 3),
            (body_x + 1, body_y + 3), (body_x + 2, body_y + 3), (body_x + 3, body_y + 3),
        ]
        for x, y in cloud_points_body:
            self.safe_set_pixel(x, y, self.sheep_color)
        
        # Legs - two short rectangles
        leg_y = body_y + 4
        for leg_x in [body_x - 2, body_x + 2]:
            for y in range(leg_y, leg_y + 4):
                for x in range(leg_x - 1, leg_x + 2):
                    self.safe_set_pixel(x, y, self.sheep_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the sheep static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🐑 Starting sheep static image...")
        
        self.draw_sheep()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐑 Sheep image stopped by user")
                break
            time.sleep(0.1)
        
        print("🐑 Sheep image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

