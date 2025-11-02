#!/usr/bin/env python3
"""
Horse Animation for LED Board
Shows a horse animation based on pixel art style
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class HorseAnimation:
    def __init__(self):
        """Initialize the horse animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors - pixel art style matching the image
        self.colors = {
            'background': (0, 0, 0),           # Black background
            'horse_body': (255, 215, 0),      # Bright yellow/gold body
            'horse_mane_tail': (255, 255, 200), # Light yellow/white for mane, tail, highlights
        }
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def create_horse(self):
        """Create a horse pattern based on pixel art style - profile view facing right."""
        print("Creating horse pattern...")
        
        # Horse position (centered, facing right)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Clear display with black background
        self.led.clear()
        
        # Fill black background
        for y in range(self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.colors['background'])
        
        # Horse head (small, pointed, facing right)
        head_start_x = center_x - 8
        head_end_x = center_x - 2
        head_center_y = center_y
        
        # Draw horse head (blocky pixel art style)
        head_points = [
            # Head outline/body
            (head_start_x + 2, head_center_y - 1),
            (head_start_x + 3, head_center_y - 2),
            (head_start_x + 4, head_center_y - 2),
            (head_start_x + 5, head_center_y - 1),
            (head_start_x + 5, head_center_y),
            (head_start_x + 4, head_center_y + 1),
            (head_start_x + 3, head_center_y + 1),
            (head_start_x + 2, head_center_y),
            # Snout
            (head_start_x, head_center_y - 1),
            (head_start_x, head_center_y),
            (head_start_x + 1, head_center_y),
        ]
        for px, py in head_points:
            self.safe_set_pixel(px, py, self.colors['horse_body'])
        
        # Neck (thick, curved, connecting head to body)
        neck_y_start = head_center_y - 3
        neck_y_end = head_center_y + 2
        for y in range(neck_y_start, neck_y_end + 1):
            for offset in range(0, 4):
                px = head_end_x + offset
                if 0 <= px < self.width and 0 <= y < self.height:
                    self.safe_set_pixel(px, y, self.colors['horse_body'])
        
        # Mane (prominent, spiky, light yellow/white)
        mane_points = [
            # Main mane along neck and head
            (head_end_x, head_center_y - 4),
            (head_end_x + 1, head_center_y - 5),
            (head_end_x + 2, head_center_y - 5),
            (head_end_x + 3, head_center_y - 4),
            (head_end_x + 1, head_center_y - 3),
            (head_end_x + 2, head_center_y - 3),
            # Spiky tufts
            (head_end_x - 1, head_center_y - 4),
            (head_end_x - 2, head_center_y - 5),
            (head_start_x + 4, head_center_y - 3),
            (head_start_x + 3, head_center_y - 4),
        ]
        for px, py in mane_points:
            self.safe_set_pixel(px, py, self.colors['horse_mane_tail'])
        
        # Body (main body, bright yellow/gold, elongated blocky shape)
        body_start_x = center_x - 2
        body_end_x = center_x + 8
        body_y_start = center_y - 4
        body_y_end = center_y + 4
        
        # Draw main body (blocky rectangle-like shape)
        for y in range(body_y_start, body_y_end + 1):
            for x in range(body_start_x, body_end_x + 1):
                # Make body slightly rounded on top and bottom
                y_offset = abs(y - center_y)
                if y_offset <= 4:
                    self.safe_set_pixel(x, y, self.colors['horse_body'])
        
        # Back highlight (lighter yellow on top of back)
        for x in range(body_start_x + 1, body_end_x - 2):
            self.safe_set_pixel(x, body_y_start, self.colors['horse_mane_tail'])
        
        # Front legs (thick, blocky, slightly bent)
        front_leg_x = center_x + 2
        
        # Left front leg (closer to viewer)
        for y in range(body_y_end + 1, body_y_end + 6):
            for offset_x in range(-1, 2):
                px = front_leg_x + offset_x
                self.safe_set_pixel(px, y, self.colors['horse_body'])
        
        # Right front leg
        for y in range(body_y_end + 1, body_y_end + 7):
            px = front_leg_x + 3
            self.safe_set_pixel(px, y, self.colors['horse_body'])
        # Light yellow highlight on lower leg
        self.safe_set_pixel(front_leg_x + 3, body_y_end + 5, self.colors['horse_mane_tail'])
        self.safe_set_pixel(front_leg_x + 3, body_y_end + 6, self.colors['horse_mane_tail'])
        
        # Hind legs (thick, bent at hock)
        hind_leg_x = center_x + 7
        
        # Left hind leg
        for y in range(body_y_end + 1, body_y_end + 6):
            px = hind_leg_x
            self.safe_set_pixel(px, y, self.colors['horse_body'])
        # Light yellow highlight on lower leg
        self.safe_set_pixel(hind_leg_x, body_y_end + 4, self.colors['horse_mane_tail'])
        self.safe_set_pixel(hind_leg_x, body_y_end + 5, self.colors['horse_mane_tail'])
        
        # Right hind leg (bent at hock)
        hind_leg_points = [
            (hind_leg_x + 2, body_y_end + 1),
            (hind_leg_x + 2, body_y_end + 2),
            (hind_leg_x + 1, body_y_end + 3),
            (hind_leg_x + 1, body_y_end + 4),
            (hind_leg_x + 2, body_y_end + 5),
            (hind_leg_x + 2, body_y_end + 6),
        ]
        for px, py in hind_leg_points:
            self.safe_set_pixel(px, py, self.colors['horse_body'])
        # Light yellow highlight on lower leg
        self.safe_set_pixel(hind_leg_x + 2, body_y_end + 4, self.colors['horse_mane_tail'])
        self.safe_set_pixel(hind_leg_x + 2, body_y_end + 5, self.colors['horse_mane_tail'])
        
        # Tail (short, upward-curving, light yellow/white)
        tail_base_x = body_end_x
        tail_base_y = center_y + 2
        tail_points = [
            (tail_base_x, tail_base_y),
            (tail_base_x + 1, tail_base_y - 1),
            (tail_base_x + 2, tail_base_y - 2),
            (tail_base_x + 2, tail_base_y - 1),
            (tail_base_x + 1, tail_base_y),
        ]
        for px, py in tail_points:
            self.safe_set_pixel(px, py, self.colors['horse_mane_tail'])
        
        print("Horse pattern created successfully")
    
    def run_animation(self, should_stop=None):
        """Run the horse animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐴 Starting horse animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse animation stopped by user")
                break
            
            self.create_horse()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🐴 Horse animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run horse animation."""
    try:
        animation = HorseAnimation()
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

