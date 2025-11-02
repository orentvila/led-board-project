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
        self.plane_color = (150, 255, 150)  # Light green for plane body
        self.smoke_colors = [
            (200, 200, 200),  # Light gray
            (150, 150, 150),  # Medium gray
            (100, 100, 100),  # Dark gray
            (60, 60, 60),     # Very dark gray
        ]
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_plane(self, x_offset=0, y_offset=0, frame=0):
        """Draw a simple plane from scratch (light green) pointing upper-right with smoke.
        
        Args:
            x_offset: Horizontal offset for positioning (absolute x coordinate)
            y_offset: Vertical offset for positioning (absolute y coordinate)
            frame: Animation frame number for smoke
        """
        self.led.clear()  # Black background
        
        # Plane center position (absolute coordinates)
        plane_x = x_offset
        plane_y = y_offset
        
        # Simple plane design - clean and recognizable
        # Main fuselage (diagonal body)
        fuselage_length = 12  # Length of main body
        fuselage_width = 3  # Width of body
        
        # Draw fuselage - diagonal line from bottom-left to top-right
        for i in range(fuselage_length):
            fx = plane_x + i
            fy = plane_y + i
            # Draw with some width
            for offset in range(-fuselage_width // 2, fuselage_width // 2 + 1):
                self.safe_set_pixel(fx + offset, fy, self.plane_color)
                self.safe_set_pixel(fx, fy + offset, self.plane_color)
        
        # Draw rounded nose (top-right end)
        nose_x = plane_x + fuselage_length
        nose_y = plane_y + fuselage_length
        nose_radius = 2
        for dx in range(-nose_radius, nose_radius + 1):
            for dy in range(-nose_radius, nose_radius + 1):
                if dx * dx + dy * dy <= nose_radius * nose_radius:
                    self.safe_set_pixel(nose_x + dx, nose_y + dy, self.plane_color)
        
        # Draw wings - main wings extending from middle of fuselage
        wing_mid_x = plane_x + fuselage_length // 2
        wing_mid_y = plane_y + fuselage_length // 2
        wing_length = 7  # How far wings extend
        wing_thickness = 2
        
        # Front wing (extends up-left from fuselage)
        for i in range(wing_length):
            wx = wing_mid_x - i
            wy = wing_mid_y - i
            for offset in range(-wing_thickness // 2, wing_thickness // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Back wing (extends down-right from fuselage)
        for i in range(wing_length):
            wx = wing_mid_x + i
            wy = wing_mid_y + i
            for offset in range(-wing_thickness // 2, wing_thickness // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Draw tail fin (small vertical stabilizer at back)
        tail_x = plane_x
        tail_y = plane_y
        tail_height = 5
        
        for i in range(tail_height):
            self.safe_set_pixel(tail_x, tail_y + i, self.plane_color)
            self.safe_set_pixel(tail_x - 1, tail_y + i, self.plane_color)
        
        # Draw smoke trailing from tail (back of plane - bottom-left area)
        smoke_x = tail_x - 2
        smoke_y = tail_y
        self.draw_smoke(smoke_x, smoke_y, frame)
        
        self.led.show()
    
    def draw_smoke(self, tail_x, tail_y, frame):
        """Draw smoke trailing from the plane's tail.
        
        Args:
            tail_x, tail_y: Position of plane tail (where smoke originates)
            frame: Animation frame number for smoke animation
        """
        # Smoke moves down-left (opposite to plane's upper-right movement)
        # Smoke trail consists of particles that fade out
        smoke_particles = 10  # Number of smoke particles in trail
        
        for i in range(smoke_particles):
            # Each particle is offset down-left (opposite to plane's upper-right direction)
            offset_x = -(i * 2 + (frame % 4))  # Move left
            offset_y = i * 2 + (frame % 4)  # Move down
            
            smoke_x = tail_x + offset_x
            smoke_y = tail_y + offset_y
            
            # Fade out smoke as it gets further
            if i < len(self.smoke_colors):
                smoke_color = self.smoke_colors[min(i, len(self.smoke_colors) - 1)]
            else:
                smoke_color = (40, 40, 40)  # Very faint
            
            # Draw smoke particle with some spread (larger particles for visibility)
            particle_size = 2 if i < 3 else 1
            for dx in range(-particle_size, particle_size + 1):
                for dy in range(-particle_size, particle_size + 1):
                    if dx * dx + dy * dy <= particle_size * particle_size:
                        self.safe_set_pixel(smoke_x + dx, smoke_y + dy, smoke_color)
    
    def run_animation(self, should_stop=None):
        """Run the plane animation - flying across screen with smoke.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("✈️ Starting plane animation...")
        
        # Animation path: plane flies diagonally from bottom-left to upper-right
        # Start: bottom-left corner (off-screen)
        # End: upper-right corner (off-screen)
        start_x = -15  # Start off-screen bottom-left
        start_y = self.height + 10  # Start off-screen bottom
        end_x = self.width + 15  # End off-screen upper-right
        end_y = -10  # End off-screen top
        
        # Use smooth easing for more natural movement
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("✈️ Plane animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            progress = min(1.0, elapsed / duration)
            
            # Smooth easing function for very natural motion
            # Smooth ease-in-out curve
            eased_progress = progress * progress * (3.0 - 2.0 * progress)
            
            # Calculate plane position (diagonal movement from bottom-left to upper-right)
            current_x = start_x + (end_x - start_x) * eased_progress
            current_y = start_y + (end_y - start_y) * eased_progress
            
            # Draw plane at current absolute position with smoke
            self.draw_plane(x_offset=int(current_x), 
                          y_offset=int(current_y),
                          frame=frame)
            
            frame += 1
            time.sleep(0.03)  # ~33 FPS for very smooth animation
        
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
