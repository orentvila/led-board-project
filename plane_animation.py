#!/usr/bin/env python3
"""
Plane Animation for LED Board
Displays a plane from top-down angled perspective
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class PlaneAnimation:
    def __init__(self):
        """Initialize the plane animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.plane_color = (255, 255, 255)  # White for plane body
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_plane(self, x_offset=0, y_offset=0):
        """Draw the plane from top-down angled perspective (pointing up-right).
        
        Args:
            x_offset: Horizontal offset for positioning
            y_offset: Vertical offset for positioning
        """
        self.led.clear()  # Black background
        
        # Plane positioned at center, angled up-right (diagonal)
        center_x = self.width // 2 + x_offset
        center_y = self.height // 2 + y_offset
        
        # Plane dimensions (adjusted for 32x48 display)
        fuselage_length = 14  # Main body length (diagonal)
        wing_span = 16  # Wing width
        tail_height = 6  # Vertical stabilizer height
        
        # Draw fuselage (main body) - diagonal line from bottom-left to top-right
        # Simplified: draw as diagonal line with width
        for i in range(fuselage_length):
            # Diagonal direction (up-right)
            fx = center_x - fuselage_length // 2 + i
            fy = center_y - fuselage_length // 4 + i // 2
            # Draw fuselage with some width
            for offset in range(-2, 3):
                self.safe_set_pixel(fx + offset, fy, self.plane_color)
                self.safe_set_pixel(fx, fy + offset, self.plane_color)
        
        # Draw wings - extending perpendicular to fuselage
        wing_center_x = center_x
        wing_center_y = center_y
        
        # Left wing (extends down-left)
        for i in range(wing_span // 2):
            wx = wing_center_x - i
            wy = wing_center_y + i // 2
            for offset in range(-1, 2):
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Right wing (extends up-right)
        for i in range(wing_span // 2):
            wx = wing_center_x + i
            wy = wing_center_y - i // 2
            for offset in range(-1, 2):
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Draw engines - small circles under wings
        engine_size = 2
        engine_positions = [
            (center_x - wing_span // 4, center_y + 2),  # Left wing engine
            (center_x + wing_span // 4, center_y - 2),  # Right wing engine
        ]
        
        for ex, ey in engine_positions:
            for dx in range(-engine_size, engine_size + 1):
                for dy in range(-engine_size, engine_size + 1):
                    if dx * dx + dy * dy <= engine_size * engine_size:
                        self.safe_set_pixel(ex + dx, ey + dy, self.plane_color)
        
        # Draw tail - vertical stabilizer at back (bottom-left)
        tail_x = center_x - fuselage_length // 2
        tail_y = center_y - fuselage_length // 4
        
        for i in range(tail_height):
            self.safe_set_pixel(tail_x - 1, tail_y - i, self.plane_color)
            self.safe_set_pixel(tail_x, tail_y - i, self.plane_color)
            self.safe_set_pixel(tail_x + 1, tail_y - i, self.plane_color)
        
        # Draw horizontal stabilizer
        for i in range(4):
            self.safe_set_pixel(tail_x - 2 + i, tail_y - 1, self.plane_color)
        
        # Draw motion lines trailing from wings (diagonal lines)
        motion_line_length = 4
        
        # Left wing motion lines
        for i in range(3):
            start_x = center_x - wing_span // 2
            start_y = center_y + i - 1
            for j in range(motion_line_length):
                self.safe_set_pixel(start_x - j, start_y + j // 2, self.plane_color)
        
        # Right wing motion lines
        for i in range(3):
            start_x = center_x + wing_span // 2
            start_y = center_y - i + 1
            for j in range(motion_line_length):
                self.safe_set_pixel(start_x + j, start_y - j // 2, self.plane_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the plane animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("✈️ Starting plane animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("✈️ Plane animation stopped by user")
                break
            
            # Draw static plane for now (we'll add animation later)
            self.draw_plane()  # Static plane pointing up-right
            time.sleep(0.1)  # 10 FPS
        
        print("✈️ Plane animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run plane animation."""
    try:
        animation = PlaneAnimation()
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
