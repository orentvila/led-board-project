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
        """Draw the plane as a horizontal silhouette (tail left, nose right) with smoke.
        
        Args:
            x_offset: Horizontal offset for positioning
            y_offset: Vertical offset for positioning
            frame: Animation frame number for smoke
        """
        self.led.clear()  # Black background
        
        # Plane positioned horizontally (tail on left, nose on right)
        center_x = self.width // 2 + x_offset
        center_y = self.height // 2 + y_offset
        
        # Plane dimensions - smaller silhouette
        fuselage_width = 4  # Width of fuselage (vertical oval)
        fuselage_height = 12  # Height of fuselage
        wing_length = 8  # Wings extend left and right
        wing_thickness = 3  # Thickness of wing bar
        tail_width = 2  # Tail fin width
        tail_height = 6  # Tail fin height
        
        # Draw fuselage - vertical rounded rectangle/oval (thicker in middle)
        fuselage_x = center_x
        fuselage_start_y = center_y - fuselage_height // 2
        fuselage_end_y = center_y + fuselage_height // 2
        
        for y in range(fuselage_start_y, fuselage_end_y):
            # Width varies - wider in middle, narrower at ends
            progress = (y - fuselage_start_y) / fuselage_height
            # Create rounded ends
            if progress < 0.2 or progress > 0.8:
                width = int(fuselage_width * (1 - abs(progress * 2 - 1) * 2))
            else:
                width = fuselage_width
            
            for offset in range(-width // 2, width // 2 + 1):
                self.safe_set_pixel(fuselage_x + offset, y, self.plane_color)
        
        # Draw wings - horizontal bar intersecting fuselage (middle)
        wing_y = center_y
        wing_start_x = fuselage_x - wing_length
        wing_end_x = fuselage_x + wing_length
        
        for x in range(wing_start_x, wing_end_x):
            for offset in range(-wing_thickness // 2, wing_thickness // 2 + 1):
                self.safe_set_pixel(x, wing_y + offset, self.plane_color)
        
        # Round wing tips
        for offset in range(-wing_thickness // 2, wing_thickness // 2 + 1):
            for wy in range(wing_y - 1, wing_y + 2):
                self.safe_set_pixel(wing_start_x, wy, self.plane_color)
                self.safe_set_pixel(wing_end_x, wy, self.plane_color)
        
        # Draw tail fin - attached to left end of wing (vertical rounded rectangle)
        tail_x = wing_start_x - 1
        tail_start_y = wing_y
        tail_end_y = wing_y + tail_height
        
        for y in range(tail_start_y, tail_end_y):
            # Tail width varies slightly for rounded effect
            if y == tail_start_y or y == tail_end_y - 1:
                width = max(1, tail_width - 1)
            else:
                width = tail_width
            
            for offset in range(-width // 2, width // 2 + 1):
                self.safe_set_pixel(tail_x + offset, y, self.plane_color)
        
        # Round tail fin top
        for offset in range(-tail_width // 2, tail_width // 2 + 1):
            self.safe_set_pixel(tail_x + offset, tail_start_y, self.plane_color)
        
        # Draw smoke trailing from tail (to the left, opposite of plane direction)
        smoke_x = tail_x - 2  # Smoke comes from back of tail
        smoke_y = wing_y + 1
        self.draw_smoke(smoke_x, smoke_y, frame)
        
        self.led.show()
    
    def draw_smoke(self, tail_x, tail_y, frame):
        """Draw smoke trailing from the plane's tail.
        
        Args:
            tail_x, tail_y: Position of plane tail (where smoke originates)
            frame: Animation frame number for smoke animation
        """
        # Smoke moves to the left (opposite to plane's rightward movement)
        # Smoke trail consists of particles that fade out
        smoke_particles = 10  # Number of smoke particles in trail
        
        for i in range(smoke_particles):
            # Each particle is offset to the left (opposite direction)
            offset_x = -(i * 2 + (frame % 4))  # Move left
            # Add slight vertical spread for natural smoke effect
            offset_y = (i % 3 - 1) + ((frame // 2) % 3 - 1)
            
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
        
        # Animation path: plane flies horizontally from left to right
        # Smooth horizontal movement
        start_x = -20  # Start off-screen left
        end_x = self.width + 20  # End off-screen right
        center_y = self.height // 2  # Stay in vertical center
        
        # Use smooth easing for more natural movement
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("✈️ Plane animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            progress = min(1.0, elapsed / duration)
            
            # Smooth easing function for more natural motion
            # Ease-in-out: slow at start and end, fast in middle
            eased_progress = progress * progress * (3.0 - 2.0 * progress)
            
            # Calculate plane position (horizontal movement only)
            current_x = start_x + (end_x - start_x) * eased_progress
            current_y = center_y
            
            # Draw plane at current position with smoke
            self.draw_plane(x_offset=int(current_x - self.width // 2), 
                          y_offset=int(current_y - self.height // 2),
                          frame=frame)
            
            frame += 1
            time.sleep(0.03)  # ~33 FPS for smoother animation
        
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
