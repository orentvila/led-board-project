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
        """Draw the plane as a solid black silhouette (pointing up-right).
        
        Args:
            x_offset: Horizontal offset for positioning
            y_offset: Vertical offset for positioning
        """
        self.led.clear()  # Black background
        
        # Plane positioned at center, angled diagonally (nose up-right, tail down-left)
        center_x = self.width // 2 + x_offset
        center_y = self.height // 2 + y_offset
        
        # Plane dimensions (adjusted for 32x48 display)
        fuselage_length = 16  # Main body length (diagonal)
        nose_width = 5  # Wider at front
        tail_width = 2  # Tapers to back
        
        # Draw fuselage (main body) - diagonal, tapering from front to back
        # Direction: from bottom-left (tail) to top-right (nose)
        for i in range(fuselage_length):
            # Position along diagonal
            progress = i / fuselage_length  # 0.0 at tail, 1.0 at nose
            fx = center_x - fuselage_length // 2 + i
            fy = center_y + fuselage_length // 2 - i
            
            # Width tapers from nose (wider) to tail (narrower)
            width = int(nose_width * (1 - progress) + tail_width * progress)
            
            # Draw fuselage with varying width
            for offset in range(-width // 2, width // 2 + 1):
                # Draw as filled shape
                for wy in range(fy - 1, fy + 2):
                    self.safe_set_pixel(fx + offset, wy, self.plane_color)
        
        # Draw rounded nose
        nose_x = center_x + fuselage_length // 2
        nose_y = center_y - fuselage_length // 2
        nose_radius = nose_width // 2
        for dx in range(-nose_radius, nose_radius + 1):
            for dy in range(-nose_radius, nose_radius + 1):
                if dx * dx + dy * dy <= nose_radius * nose_radius:
                    self.safe_set_pixel(nose_x + dx, nose_y + dy, self.plane_color)
        
        # Draw wings - extending horizontally from fuselage
        # Left wing points upper-left, right wing points lower-right
        wing_center_x = center_x
        wing_center_y = center_y
        wing_length = 10
        wing_width = 4
        
        # Left wing (upper-left direction)
        for i in range(wing_length):
            wx = wing_center_x - i
            wy = wing_center_y - i
            for offset in range(-wing_width // 2, wing_width // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Round left wing tip
        left_wing_tip_x = wing_center_x - wing_length
        left_wing_tip_y = wing_center_y - wing_length
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx * dx + dy * dy <= 4:
                    self.safe_set_pixel(left_wing_tip_x + dx, left_wing_tip_y + dy, self.plane_color)
        
        # Right wing (lower-right direction)
        for i in range(wing_length):
            wx = wing_center_x + i
            wy = wing_center_y + i
            for offset in range(-wing_width // 2, wing_width // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Round right wing tip
        right_wing_tip_x = wing_center_x + wing_length
        right_wing_tip_y = wing_center_y + wing_length
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx * dx + dy * dy <= 4:
                    self.safe_set_pixel(right_wing_tip_x + dx, right_wing_tip_y + dy, self.plane_color)
        
        # Draw tail - T-shaped (horizontal stabilizer wider, vertical shorter pointing down)
        tail_x = center_x - fuselage_length // 2
        tail_y = center_y + fuselage_length // 2
        
        # Horizontal stabilizer (wider, extends left-right)
        horiz_stab_width = 8
        for i in range(horiz_stab_width):
            hx = tail_x - horiz_stab_width // 2 + i
            hy = tail_y
            for offset in range(-1, 2):
                self.safe_set_pixel(hx, hy + offset, self.plane_color)
        
        # Vertical stabilizer (shorter, points down)
        vert_stab_height = 5
        for i in range(vert_stab_height):
            self.safe_set_pixel(tail_x, tail_y + i, self.plane_color)
            self.safe_set_pixel(tail_x - 1, tail_y + i, self.plane_color)
            self.safe_set_pixel(tail_x + 1, tail_y + i, self.plane_color)
        
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
