#!/usr/bin/env python3
"""
Cat Static Image for LED Board
Displays a static cat image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class CatStaticAnimation:
    def __init__(self):
        """Initialize the cat static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.cat_color = (255, 255, 255)  # White for cat silhouette
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_cat(self):
        """Draw a simple cat silhouette - walking pose, facing right."""
        self.led.clear()  # Black background
        
        start_x = 8
        start_y = 12
        
        # Head - with pointed ears
        # Left ear
        self.safe_set_pixel(start_x + 1, start_y, self.cat_color)
        self.safe_set_pixel(start_x + 2, start_y - 1, self.cat_color)
        self.safe_set_pixel(start_x + 1, start_y - 1, self.cat_color)
        
        # Right ear
        self.safe_set_pixel(start_x + 4, start_y, self.cat_color)
        self.safe_set_pixel(start_x + 5, start_y - 1, self.cat_color)
        self.safe_set_pixel(start_x + 4, start_y - 1, self.cat_color)
        
        # Head body
        for y in range(start_y, start_y + 6):
            width = 5 if y < start_y + 4 else 4
            for x in range(start_x, start_x + width):
                self.safe_set_pixel(x, y, self.cat_color)
        
        # Body - curved back, straight belly
        body_y = start_y + 6
        body_start_x = start_x - 1
        
        for y in range(body_y, body_y + 12):
            if y < body_y + 3:
                width = 6
            elif y < body_y + 8:
                width = 8
            else:
                width = 6
            for x in range(body_start_x, body_start_x + width):
                self.safe_set_pixel(x, y, self.cat_color)
        
        # Front right leg (extended forward)
        leg_x = body_start_x + 3
        leg_y = body_y + 12
        for y in range(leg_y, leg_y + 6):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.cat_color)
        # Paw
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y + 6, self.cat_color)
        
        # Front left leg (behind)
        leg_x = body_start_x + 1
        leg_y = body_y + 10
        for y in range(leg_y, leg_y + 8):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.cat_color)
        # Paw
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y + 8, self.cat_color)
        
        # Back left leg (extended forward)
        leg_x = body_start_x + 5
        leg_y = body_y + 12
        for y in range(leg_y, leg_y + 6):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.cat_color)
        # Paw
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y + 6, self.cat_color)
        
        # Back right leg (behind)
        leg_x = body_start_x + 7
        leg_y = body_y + 10
        for y in range(leg_y, leg_y + 8):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.cat_color)
        # Paw
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y + 8, self.cat_color)
        
        # Tail - curved upward
        tail_points = [
            (body_start_x + 8, body_y + 6),
            (body_start_x + 9, body_y + 4),
            (body_start_x + 10, body_y + 2),
            (body_start_x + 11, body_y + 1),
            (body_start_x + 11, body_y),
        ]
        for x, y in tail_points:
            self.safe_set_pixel(x, y, self.cat_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the cat static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🐱 Starting cat static image...")
        
        self.draw_cat()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐱 Cat image stopped by user")
                break
            time.sleep(0.1)
        
        print("🐱 Cat image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

