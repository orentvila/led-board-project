#!/usr/bin/env python3
"""
Rooster Animation for LED Board
Shows a rooster animation based on cat animation style
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class RoosterAnimation:
    def __init__(self):
        """Initialize the rooster animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),     # Black background
            'rooster_body': (255, 165, 0),  # Orange body
            'rooster_comb': (255, 0, 0),    # Red comb
            'rooster_tail': (255, 215, 0),  # Gold tail feathers
            'rooster_beak': (255, 140, 0),  # Orange beak
            'rooster_wattle': (255, 100, 100),  # Red wattle
            'eyes': (255, 255, 255),     # White eyes
            'pupils': (0, 0, 0)          # Black pupils
        }
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def create_rooster(self):
        """Create a rooster pattern."""
        print("Creating rooster pattern...")
        
        # Rooster position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Clear display first
        self.led.clear()
        
        # Rooster body (rounded, similar to cat head)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 9
                dy = (y - center_y) / 7
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel(x, y, self.colors['rooster_body'])
        
        # Rooster head (smaller circle on top)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 6
                dy = (y - (center_y - 6)) / 5
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel(x, y, self.colors['rooster_body'])
        
        # Comb (red crown on top of head)
        comb_points = [
            (center_x - 2, center_y - 12), (center_x - 1, center_y - 13),
            (center_x, center_y - 14), (center_x + 1, center_y - 13),
            (center_x + 2, center_y - 12)
        ]
        for px, py in comb_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['rooster_comb'])
        
        # Eyes
        self.safe_set_pixel(center_x - 2, center_y - 7, self.colors['eyes'])  # Left eye
        self.safe_set_pixel(center_x + 2, center_y - 7, self.colors['eyes'])  # Right eye
        self.safe_set_pixel(center_x - 2, center_y - 7, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel(center_x + 2, center_y - 7, self.colors['pupils'])  # Right pupil
        
        # Beak (triangular, pointing down)
        beak_points = [
            (center_x, center_y - 4),
            (center_x - 1, center_y - 3),
            (center_x + 1, center_y - 3)
        ]
        for px, py in beak_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['rooster_beak'])
        
        # Wattle (red hanging from beak)
        wattle_points = [
            (center_x, center_y - 2),
            (center_x, center_y - 1),
            (center_x, center_y)
        ]
        for px, py in wattle_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['rooster_wattle'])
        
        # Body extends down
        body_y_start = max(0, center_y + 3)
        body_y_end = min(self.height, center_y + 12)
        body_x_start = max(0, center_x - 5)
        body_x_end = min(self.width, center_x + 6)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 3) <= 9:
                    self.safe_set_pixel(x, y, self.colors['rooster_body'])
        
        # Tail feathers (fan-shaped, colorful, similar to cat tail but more elaborate)
        tail_points = [
            (center_x + 6, center_y + 5),
            (center_x + 8, center_y + 3),
            (center_x + 10, center_y + 1),
            (center_x + 12, center_y - 1),
            (center_x + 11, center_y + 2),
            (center_x + 13, center_y),
            (center_x + 9, center_y + 4),
            (center_x + 11, center_y + 5),
            (center_x + 7, center_y + 7)
        ]
        for px, py in tail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['rooster_tail'])
        
        # Legs (two thin legs at bottom)
        leg_y_start = max(0, center_y + 12)
        leg_y_end = min(self.height, center_y + 18)
        
        for y in range(leg_y_start, leg_y_end):
            # Left leg
            if center_x - 3 >= 0:
                self.safe_set_pixel(center_x - 3, y, self.colors['rooster_body'])
            # Right leg
            if center_x + 3 < self.width:
                self.safe_set_pixel(center_x + 3, y, self.colors['rooster_body'])
        
        print("Rooster pattern created successfully")
    
    def run_animation(self, should_stop=None):
        """Run the rooster animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐓 Starting rooster animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐓 Rooster animation stopped by user")
                break
            
            self.led.clear()
            self.create_rooster()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🐓 Rooster animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run rooster animation."""
    try:
        animation = RoosterAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()

