#!/usr/bin/env python3
"""
Dog Animation for LED Board
Shows a dog animation based on cat animation style
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class DogAnimation:
    def __init__(self):
        """Initialize the dog animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),     # Black background
            'dog_brown': (139, 69, 19),  # Brown dog
            'dog_black': (30, 30, 30),   # Black dog
            'dog_white': (220, 220, 220), # White dog
            'eyes': (255, 255, 255),     # White eyes
            'pupils': (0, 0, 0)          # Black pupils
        }
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def create_dog(self):
        """Create a dog pattern."""
        print("Creating dog pattern...")
        
        # Dog position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Clear display first
        self.led.clear()
        
        # Dog head (rounder than cat)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel(x, y, self.colors['dog_brown'])
        
        # Dog ears (floppy) - with strict bounds checking
        ear_y_start = max(0, center_y - 10)
        ear_y_end = min(self.height, center_y - 1)
        ear_x_start = max(0, center_x - 8)
        ear_x_end = min(self.width, center_x - 2)
        
        # Left ear
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= (x - (center_x - 8)) * 0.6:
                    self.safe_set_pixel(x, y, self.colors['dog_brown'])
        
        # Right ear
        ear_x_start = max(0, center_x + 2)
        ear_x_end = min(self.width, center_x + 8)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= ((center_x + 8) - x) * 0.6:
                    self.safe_set_pixel(x, y, self.colors['dog_brown'])
        
        # Dog eyes (bigger than cat)
        self.safe_set_pixel(center_x - 4, center_y - 3, self.colors['eyes'])  # Left eye
        self.safe_set_pixel(center_x + 4, center_y - 3, self.colors['eyes'])  # Right eye
        self.safe_set_pixel(center_x - 4, center_y - 3, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel(center_x + 4, center_y - 3, self.colors['pupils'])  # Right pupil
        
        # Dog nose (bigger)
        self.safe_set_pixel(center_x - 1, center_y, self.colors['dog_black'])
        self.safe_set_pixel(center_x, center_y, self.colors['dog_black'])
        self.safe_set_pixel(center_x + 1, center_y, self.colors['dog_black'])
        
        # Dog mouth (smile)
        self.safe_set_pixel(center_x - 2, center_y + 2, self.colors['dog_black'])
        self.safe_set_pixel(center_x - 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel(center_x + 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel(center_x + 2, center_y + 2, self.colors['dog_black'])
        
        # Dog body (larger than cat) - with strict bounds checking
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 15)
        body_x_start = max(0, center_x - 6)
        body_x_end = min(self.width, center_x + 7)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 11:
                    self.safe_set_pixel(x, y, self.colors['dog_brown'])
        
        # Dog legs - with strict bounds checking
        leg_y_start = max(0, center_y + 15)
        leg_y_end = min(self.height, center_y + 20)
        
        for y in range(leg_y_start, leg_y_end):
            for x in range(max(0, center_x - 5), min(self.width, center_x - 2)):  # Front left
                self.safe_set_pixel(x, y, self.colors['dog_brown'])
            for x in range(max(0, center_x + 2), min(self.width, center_x + 5)):  # Front right
                self.safe_set_pixel(x, y, self.colors['dog_brown'])
        
        # Dog tail (wagging)
        tail_points = [
            (center_x + 8, center_y + 10),
            (center_x + 10, center_y + 8),
            (center_x + 12, center_y + 6),
            (center_x + 14, center_y + 4)
        ]
        for px, py in tail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['dog_brown'])
        
        print("Dog pattern created successfully")
    
    def run_animation(self):
        """Run the dog animation."""
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐶 Starting dog animation...")
        
        while time.time() - start_time < duration:
            self.led.clear()
            self.create_dog()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🐶 Dog animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run dog animation."""
    try:
        animation = DogAnimation()
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

