#!/usr/bin/env python3
"""
Cat Animation for LED Board
Shows a cat animation (rotated 180 degrees)
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class CatAnimation:
    def __init__(self):
        """Initialize the cat animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),     # Black background
            'cat_orange': (255, 165, 0), # Orange cat
            'cat_black': (50, 50, 50),   # Dark gray cat
            'cat_white': (200, 200, 200), # Light gray cat
            'cat_pink': (255, 192, 203), # Pink nose
            'eyes': (255, 255, 255),     # White eyes
            'pupils': (0, 0, 0)          # Black pupils
        }
    
    def rotate_180(self, x, y):
        """Rotate coordinates 180 degrees."""
        return (self.width - 1 - x, self.height - 1 - y)
    
    def safe_set_pixel_rotated(self, x, y, color):
        """Safely set a pixel with 180-degree rotation."""
        rot_x, rot_y = self.rotate_180(x, y)
        if 0 <= rot_x < self.width and 0 <= rot_y < self.height:
            self.led.set_pixel(rot_x, rot_y, color)
    
    def create_cat_rotated(self):
        """Create a cat pattern rotated 180 degrees."""
        print("Creating rotated cat pattern...")
        self.led.clear()
        
        # Cat position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Cat head (oval shape) - rotated
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 8
                dy = (y - center_y) / 6
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat ears (triangular) - rotated
        # Left ear
        ear_y_start = max(0, center_y - 8)
        ear_y_end = min(self.height, center_y - 2)
        ear_x_start = max(0, center_x - 6)
        ear_x_end = min(self.width, center_x - 1)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= (x - (center_x - 6)) * 0.8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Right ear
        ear_x_start = max(0, center_x + 1)
        ear_x_end = min(self.width, center_x + 6)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= ((center_x + 6) - x) * 0.8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat eyes - rotated
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['eyes'])  # Left eye
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['eyes'])  # Right eye
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['pupils'])  # Right pupil
        
        # Cat nose - rotated
        self.safe_set_pixel_rotated(center_x, center_y, self.colors['cat_pink'])
        
        # Cat mouth - rotated
        self.safe_set_pixel_rotated(center_x - 1, center_y + 2, self.colors['cat_black'])
        self.safe_set_pixel_rotated(center_x + 1, center_y + 2, self.colors['cat_black'])
        
        # Cat whiskers - rotated
        for i in range(3):
            self.safe_set_pixel_rotated(center_x - 5 - i, center_y, self.colors['cat_white'])  # Left whiskers
            self.safe_set_pixel_rotated(center_x + 5 + i, center_y, self.colors['cat_white'])  # Right whiskers
        
        # Cat body - rotated
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 12)
        body_x_start = max(0, center_x - 4)
        body_x_end = min(self.width, center_x + 5)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat tail (curved) - rotated
        tail_points = [
            (center_x + 6, center_y + 8),
            (center_x + 8, center_y + 6),
            (center_x + 10, center_y + 4),
            (center_x + 12, center_y + 2)
        ]
        for px, py in tail_points:
            self.safe_set_pixel_rotated(px, py, self.colors['cat_orange'])
    
    def run_animation(self, should_stop=None):
        """Run the cat animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐱 Starting cat animation (rotated)...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐱 Cat animation stopped by user")
                break
            
            self.create_cat_rotated()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🐱 Cat animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run cat animation."""
    try:
        animation = CatAnimation()
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

