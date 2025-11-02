#!/usr/bin/env python3
"""
Duck Animation for LED Board
Shows a duck floating on water based on pixel art style
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class DuckAnimation:
    def __init__(self):
        """Initialize the duck animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors - pixel art style (black outline, light gray background)
        self.colors = {
            'background': (200, 200, 200),  # Light gray background
            'duck_outline': (0, 0, 0),       # Black outline
            'duck_body': (220, 220, 220),    # Slightly lighter gray for body fill (optional)
            'water': (100, 150, 200),        # Light blue for water
        }
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def create_duck(self):
        """Create a duck pattern based on pixel art style - minimalist black outline."""
        print("Creating duck pattern...")
        
        # Duck position (centered, facing left)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Clear display with light gray background
        for y in range(self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.colors['background'])
        
        # Duck body (larger rounded shape, elongated) - pixel art outline
        body_center_x = center_x + 2  # Slightly to the right
        body_center_y = center_y
        
        # Draw duck body as pixel art outline (black pixels on edge of ellipse)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - body_center_x) / 9.5
                dy = (y - body_center_y) / 6
                dist_from_center = dx*dx + dy*dy
                # Draw outline - pixels on the edge
                if 0.90 <= dist_from_center <= 1.05:
                    self.safe_set_pixel(x, y, self.colors['duck_outline'])
                # Fill some inner pixels for more visible body
                elif dist_from_center <= 0.85:
                    # Optional: add a subtle fill, but keeping minimalist style
                    pass
        
        # Duck head (smaller rounded shape, connected to body, on the left)
        head_center_x = center_x - 5
        head_center_y = center_y
        
        # Draw head outline
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - head_center_x) / 5.5
                dy = (y - head_center_y) / 4.5
                dist_from_center = dx*dx + dy*dy
                if 0.90 <= dist_from_center <= 1.05:
                    self.safe_set_pixel(x, y, self.colors['duck_outline'])
        
        # Beak (small, pointed, extending horizontally to the left)
        beak_points = [
            (head_center_x - 5, head_center_y),
            (head_center_x - 6, head_center_y - 1),
            (head_center_x - 6, head_center_y),
            (head_center_x - 6, head_center_y + 1),
        ]
        for px, py in beak_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['duck_outline'])
        
        # Eye (single black pixel, slightly above and behind beak)
        self.safe_set_pixel(head_center_x - 2, head_center_y - 2, self.colors['duck_outline'])
        
        # Tail (small, slightly upward-curving, at the back right)
        tail_base_x = body_center_x + 9
        tail_base_y = body_center_y
        tail_points = [
            (tail_base_x, tail_base_y),
            (tail_base_x + 1, tail_base_y - 1),
            (tail_base_x + 2, tail_base_y - 2),
            (tail_base_x + 2, tail_base_y - 1),
        ]
        for px, py in tail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.colors['duck_outline'])
        
        # Water waves (wavy line below duck, pixelated M/W shapes)
        water_y = center_y + 7  # Water level
        
        # Draw wavy water line (pixelated wave pattern - M/W shapes)
        for x in range(self.width):
            # Create wave pattern - pixelated M/W shape
            # Pattern repeats every 8 pixels
            pattern_pos = x % 8
            
            if pattern_pos < 4:
                # First half: upward curve (M pattern)
                wave_offset = pattern_pos
            else:
                # Second half: downward curve (W pattern)
                wave_offset = 8 - pattern_pos
            
            wave_y = water_y + wave_offset
            
            # Draw wave pixels
            if 0 <= wave_y < self.height:
                self.safe_set_pixel(x, wave_y, self.colors['duck_outline'])
                # Add connecting pixels for smoother wave
                if 0 <= wave_y - 1 < self.height and (pattern_pos == 0 or pattern_pos == 4):
                    self.safe_set_pixel(x, wave_y - 1, self.colors['duck_outline'])
                if 0 <= wave_y + 1 < self.height and (pattern_pos == 3 or pattern_pos == 7):
                    self.safe_set_pixel(x, wave_y + 1, self.colors['duck_outline'])
        
        print("Duck pattern created successfully")
    
    def run_animation(self, should_stop=None):
        """Run the duck animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🦆 Starting duck animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🦆 Duck animation stopped by user")
                break
            
            self.create_duck()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🦆 Duck animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run duck animation."""
    try:
        animation = DuckAnimation()
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

