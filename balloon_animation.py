#!/usr/bin/env python3
"""
Triangle Animation for LED Board
Displays a blue triangle that flies upward
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class BalloonAnimation:
    def __init__(self):
        """Initialize the triangle animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Triangle dimensions
        self.triangle_width = 24  # Width of triangle base
        self.triangle_height = 30  # Height of triangle
        self.triangle_color = (0, 100, 255)  # Blue color
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def is_inside_triangle(self, x, y, center_x, top_y):
        """Check if a point is inside the triangle.
        
        Args:
            x, y: Point coordinates
            center_x: X coordinate of triangle center (top point)
            top_y: Y coordinate of triangle top point
        """
        # Triangle: point at top (center_x, top_y), base at bottom
        # Base is at top_y + triangle_height
        base_y = top_y + self.triangle_height
        
        # Check if y is within triangle height
        if y < top_y or y >= base_y:
            return False
        
        # Calculate width at this y level
        # Triangle tapers linearly from point (width=1) to base (width=triangle_width)
        relative_y = y - top_y  # 0 at top, triangle_height-1 at bottom
        if relative_y == 0:
            # Top point - single pixel
            return x == center_x
        
        # Interpolate width from 1 pixel at top to triangle_width at base
        width_at_y = 1 + int((self.triangle_width - 1) * (relative_y / (self.triangle_height - 1)))
        
        # Check if x is within the width at this y level
        left_edge = center_x - (width_at_y - 1) // 2
        right_edge = center_x + width_at_y // 2
        
        return left_edge <= x <= right_edge
    
    def draw_balloon(self, brightness=1.0, y_offset=0):
        """Draw the triangle - blue, centered, with y_offset for animation.
        
        Args:
            brightness: Brightness multiplier (0.0 to 1.0)
            y_offset: Vertical offset for flying animation
        """
        self.led.clear()  # Black background
        
        # Calculate triangle position
        center_x = self.width // 2
        top_y = y_offset
        
        # Draw triangle - fill all pixels inside triangle
        for y in range(self.height):
            for x in range(self.width):
                if self.is_inside_triangle(x, y, center_x, top_y):
                    # Apply brightness to blue color
                    r = int(self.triangle_color[0] * brightness)
                    g = int(self.triangle_color[1] * brightness)
                    b = int(self.triangle_color[2] * brightness)
                    self.safe_set_pixel(x, y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the balloon animation flying upward.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("🔺 Starting triangle animation...")
        
        # Animation: triangle starts at bottom, flies up once over 20 seconds
        # Start from bottom (completely below screen) to top (completely above screen)
        start_y_offset = self.height + self.triangle_height  # Start below screen
        end_y_offset = -self.triangle_height  # End above screen
        total_distance = start_y_offset - end_y_offset
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🔺 Triangle animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            
            # Calculate y_offset for flying up - single cycle over full duration
            # Progress from 0.0 (start) to 1.0 (end)
            progress = min(1.0, elapsed / duration)
            
            # Linear interpolation from start to end
            y_offset = int(start_y_offset - progress * total_distance)
            
            # Subtle brightness pulse
            pulse = 0.9 + 0.1 * (1.0 + math.sin(elapsed * 1.5)) / 2.0  # 0.9 to 1.0
            
            self.draw_balloon(brightness=pulse, y_offset=y_offset)
            frame += 1
            time.sleep(0.05)  # 20 FPS for smoother animation
        
        print("🔺 Triangle animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run balloon animation."""
    try:
        animation = BalloonAnimation()
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

