#!/usr/bin/env python3
"""
Lion Static Image for LED Board
Displays a static lion image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class LionStaticAnimation:
    def __init__(self):
        """Initialize the lion static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.lion_color = (255, 255, 255)  # White for lion outline
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_lion(self):
        """Draw a simple lion silhouette - seated, facing forward."""
        self.led.clear()  # Black background
        
        # Head and mane - centered
        center_x = self.width // 2
        
        # Mane - jagged, circular outline
        mane_points = [
            (center_x, 8), (center_x-1, 8), (center_x+1, 8),
            (center_x-2, 9), (center_x+2, 9),
            (center_x-3, 10), (center_x+3, 10),
            (center_x-4, 11), (center_x+4, 11),
            (center_x-5, 12), (center_x-4, 12), (center_x-3, 12), (center_x-2, 12), 
            (center_x-1, 12), (center_x, 12), (center_x+1, 12), (center_x+2, 12),
            (center_x+3, 12), (center_x+4, 12), (center_x+5, 12),
            (center_x-5, 13), (center_x+5, 13),
            (center_x-4, 14), (center_x+4, 14),
            (center_x-3, 15), (center_x+3, 15),
        ]
        
        for x, y in mane_points:
            self.safe_set_pixel(x, y, self.lion_color)
        
        # Face - inverted bell shape
        face_y_start = 12
        for y in range(face_y_start, face_y_start + 8):
            width = 3 + (y - face_y_start) // 2
            for x in range(center_x - width, center_x + width + 1):
                if y == face_y_start + 2:  # Eyes
                    if x == center_x - 1 or x == center_x + 1:
                        self.safe_set_pixel(x, y, self.lion_color)
                elif y == face_y_start + 4:  # Nose
                    if abs(x - center_x) <= 1:
                        self.safe_set_pixel(x, y, self.lion_color)
                elif y == face_y_start + 6:  # Mouth - smile
                    if abs(x - center_x) <= 2:
                        self.safe_set_pixel(x, y, self.lion_color)
                else:
                    if abs(x - center_x) <= width:
                        self.safe_set_pixel(x, y, self.lion_color)
        
        # Body - rounded, wider at bottom
        body_y_start = 20
        for y in range(body_y_start, body_y_start + 15):
            if y < body_y_start + 5:
                width = 6
            elif y < body_y_start + 10:
                width = 8
            else:
                width = 9
            for x in range(center_x - width, center_x + width + 1):
                self.safe_set_pixel(x, y, self.lion_color)
        
        # Front legs
        leg_y = body_y_start + 15
        for leg_offset in [-4, 4]:
            for y in range(leg_y, leg_y + 6):
                for x in range(center_x + leg_offset - 1, center_x + leg_offset + 2):
                    self.safe_set_pixel(x, y, self.lion_color)
            # Paws - toes
            for toe in [-1, 0, 1]:
                self.safe_set_pixel(center_x + leg_offset + toe, leg_y + 6, self.lion_color)
        
        # Tail - curved with tuft
        tail_points = [
            (center_x + 8, body_y_start + 5),
            (center_x + 10, body_y_start + 3),
            (center_x + 11, body_y_start + 1),
            (center_x + 12, body_y_start),
        ]
        for x, y in tail_points:
            self.safe_set_pixel(x, y, self.lion_color)
        # Tuft
        self.safe_set_pixel(center_x + 12, body_y_start - 1, self.lion_color)
        self.safe_set_pixel(center_x + 13, body_y_start, self.lion_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the lion static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🦁 Starting lion static image...")
        
        self.draw_lion()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🦁 Lion image stopped by user")
                break
            time.sleep(0.1)
        
        print("🦁 Lion image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

