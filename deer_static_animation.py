#!/usr/bin/env python3
"""
Deer Static Image for LED Board
Displays a static deer image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class DeerStaticAnimation:
    def __init__(self):
        """Initialize the deer static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.deer_color = (255, 255, 255)  # White for deer outline
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_deer(self):
        """Draw a simple deer silhouette - profile view, facing right."""
        self.led.clear()  # Black background
        
        start_x = 8
        start_y = 10
        
        # Head - small, rounded with snout
        for y in range(start_y, start_y + 6):
            width = 3 if y < start_y + 3 else 2
            for x in range(start_x, start_x + width):
                self.safe_set_pixel(x, y, self.deer_color)
        
        # Eye
        self.safe_set_pixel(start_x + 2, start_y + 2, self.deer_color)
        
        # Ear
        self.safe_set_pixel(start_x + 3, start_y - 1, self.deer_color)
        self.safe_set_pixel(start_x + 4, start_y - 2, self.deer_color)
        
        # Antlers
        # Left antler
        self.safe_set_pixel(start_x + 3, start_y - 3, self.deer_color)
        self.safe_set_pixel(start_x + 4, start_y - 4, self.deer_color)
        self.safe_set_pixel(start_x + 3, start_y - 5, self.deer_color)
        self.safe_set_pixel(start_x + 5, start_y - 4, self.deer_color)
        
        # Right antler
        self.safe_set_pixel(start_x + 4, start_y - 3, self.deer_color)
        self.safe_set_pixel(start_x + 5, start_y - 4, self.deer_color)
        self.safe_set_pixel(start_x + 4, start_y - 5, self.deer_color)
        self.safe_set_pixel(start_x + 6, start_y - 4, self.deer_color)
        
        # Neck
        for y in range(start_y + 5, start_y + 12):
            for x in range(start_x - 1, start_x + 2):
                self.safe_set_pixel(x, y, self.deer_color)
        
        # Body - oval shape
        body_x = start_x - 2
        body_y = start_y + 12
        for y in range(body_y, body_y + 18):
            if y < body_y + 5:
                width = 5
            elif y < body_y + 12:
                width = 8
            else:
                width = 6
            for x in range(body_x, body_x + width):
                self.safe_set_pixel(x, y, self.deer_color)
        
        # Spots on flank
        spot_y = body_y + 8
        self.safe_set_pixel(body_x + 3, spot_y, self.deer_color)
        self.safe_set_pixel(body_x + 4, spot_y, self.deer_color)
        self.safe_set_pixel(body_x + 3, spot_y + 1, self.deer_color)
        
        # Front legs
        leg_y = body_y + 18
        for leg_x in [body_x + 1, body_x + 3]:
            for y in range(leg_y, leg_y + 8):
                for x in range(leg_x - 1, leg_x + 2):
                    self.safe_set_pixel(x, y, self.deer_color)
            # Hooves
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, leg_y + 8, self.deer_color)
        
        # Back legs
        for leg_x in [body_x + 5, body_x + 7]:
            for y in range(leg_y, leg_y + 8):
                for x in range(leg_x - 1, leg_x + 2):
                    self.safe_set_pixel(x, y, self.deer_color)
            # Hooves
            for x in range(leg_x - 1, leg_x + 2):
                self.safe_set_pixel(x, leg_y + 8, self.deer_color)
        
        # Tail
        self.safe_set_pixel(body_x - 1, body_y + 14, self.deer_color)
        self.safe_set_pixel(body_x - 2, body_y + 13, self.deer_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the deer static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🦌 Starting deer static image...")
        
        self.draw_deer()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🦌 Deer image stopped by user")
                break
            time.sleep(0.1)
        
        print("🦌 Deer image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

