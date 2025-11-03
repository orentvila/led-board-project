#!/usr/bin/env python3
"""
Horse Static Image for LED Board
Displays a static horse image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class HorseStaticAnimation:
    def __init__(self):
        """Initialize the horse static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.horse_color = (255, 255, 255)  # White for horse silhouette
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_horse(self):
        """Draw a simple horse silhouette - walking/trotting, profile view, facing right."""
        self.led.clear()  # Black background
        
        start_x = 6
        start_y = 8
        
        # Head - high, with rounded muzzle
        for y in range(start_y, start_y + 8):
            if y < start_y + 2:
                width = 3
            elif y < start_y + 5:
                width = 4
            else:
                width = 3
            for x in range(start_x, start_x + width):
                self.safe_set_pixel(x, y, self.horse_color)
        
        # Ears
        self.safe_set_pixel(start_x + 1, start_y - 1, self.horse_color)
        self.safe_set_pixel(start_x + 2, start_y - 2, self.horse_color)
        
        # Neck - curved
        neck_x = start_x - 1
        neck_y = start_y + 8
        for y in range(neck_y, neck_y + 10):
            width = 2 + (y - neck_y) // 3
            for x in range(neck_x - width, neck_x + 1):
                self.safe_set_pixel(x, y, self.horse_color)
        
        # Body - robust, arched back
        body_x = neck_x - 5
        body_y = neck_y + 8
        
        for y in range(body_y, body_y + 14):
            if y < body_y + 3:
                width = 6
            elif y < body_y + 8:
                width = 10
            else:
                width = 8
            for x in range(body_x, body_x + width):
                self.safe_set_pixel(x, y, self.horse_color)
        
        # Front right leg (lifted, bent)
        leg_x = body_x + 2
        leg_y = body_y + 14
        # Upper leg
        for y in range(leg_y, leg_y + 3):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        # Lower leg
        leg_x2 = leg_x - 1
        for y in range(leg_y + 3, leg_y + 8):
            for x in range(leg_x2 - 1, leg_x2 + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        # Hoof
        for x in range(leg_x2 - 1, leg_x2 + 2):
            self.safe_set_pixel(x, leg_y + 8, self.horse_color)
        
        # Front left leg (planted)
        leg_x = body_x + 4
        for y in range(leg_y, leg_y + 10):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        # Hoof
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y + 10, self.horse_color)
        
        # Hind right leg (lifted, bent)
        leg_x = body_x + 6
        leg_y2 = body_y + 12
        for y in range(leg_y2, leg_y2 + 3):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        leg_x2 = leg_x + 1
        for y in range(leg_y2 + 3, leg_y2 + 8):
            for x in range(leg_x2 - 1, leg_x2 + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        # Hoof
        for x in range(leg_x2 - 1, leg_x2 + 2):
            self.safe_set_pixel(x, leg_y2 + 8, self.horse_color)
        
        # Hind left leg (planted)
        leg_x = body_x + 8
        for y in range(leg_y2, leg_y2 + 10):
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, y, self.horse_color)
        # Hoof
        for x in range(leg_x - 1, leg_x + 2):
            self.safe_set_pixel(x, leg_y2 + 10, self.horse_color)
        
        # Tail - long and flowing
        tail_x = body_x - 2
        tail_y = body_y + 2
        for i in range(8):
            x = tail_x - i
            y = tail_y + i // 2
            self.safe_set_pixel(x, y, self.horse_color)
            if i > 4:
                self.safe_set_pixel(x, y + 1, self.horse_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the horse static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🐴 Starting horse static image...")
        
        self.draw_horse()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse image stopped by user")
                break
            time.sleep(0.1)
        
        print("🐴 Horse image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

