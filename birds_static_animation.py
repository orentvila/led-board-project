#!/usr/bin/env python3
"""
Birds Static Image for LED Board
Displays static birds image (3 birds) for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class BirdsStaticAnimation:
    def __init__(self):
        """Initialize the birds static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.bird_color = (255, 255, 255)  # White for bird silhouette
        self.eye_color = (255, 255, 255)  # White eye
        self.eye_pupil = (0, 0, 0)  # Black pupil (but we'll use black background)
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_bird(self, start_x, start_y, facing_right=True):
        """Draw a single bird.
        
        Args:
            start_x, start_y: Starting position
            facing_right: If True, bird faces right, else left
        """
        direction = 1 if facing_right else -1
        
        # Body - rounded
        body_width = 4
        body_height = 3
        
        for y in range(start_y, start_y + body_height):
            for x in range(start_x, start_x + body_width * direction, direction):
                if abs(x - start_x) <= body_width:
                    self.safe_set_pixel(x, y, self.bird_color)
        
        # Wing - extends from back
        wing_x = start_x + (body_width - 1) * direction if facing_right else start_x - (body_width - 1)
        for i in range(3):
            x = wing_x + i * direction
            self.safe_set_pixel(x, start_y + 1, self.bird_color)
            if i > 0:
                self.safe_set_pixel(x, start_y, self.bird_color)
        
        # Beak - pointed
        beak_x = start_x if facing_right else start_x + body_width - 1
        beak_y = start_y + 1
        self.safe_set_pixel(beak_x + direction, beak_y, self.bird_color)
        
        # Eye - white circle with black dot
        eye_x = start_x + direction * 2 if facing_right else start_x - 2
        eye_y = start_y
        self.safe_set_pixel(eye_x, eye_y, self.bird_color)
        # Pupil (smaller dot)
        # Note: We'll make the eye area slightly larger to show the pupil effect
        self.safe_set_pixel(eye_x, eye_y - 1, self.bird_color)
    
    def draw_birds(self):
        """Draw three birds in a cluster arrangement."""
        self.led.clear()  # Black background
        
        # Bird 1 - top, slightly right
        self.draw_bird(18, 12, facing_right=True)
        
        # Bird 2 - middle, slightly left
        self.draw_bird(14, 20, facing_right=True)
        
        # Bird 3 - bottom, slightly left
        self.draw_bird(12, 28, facing_right=True)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the birds static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🐦 Starting birds static image...")
        
        self.draw_birds()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐦 Birds image stopped by user")
                break
            time.sleep(0.1)
        
        print("🐦 Birds image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

