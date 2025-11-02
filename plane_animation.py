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
        """Draw the plane as a diagonal top-down silhouette (nose upper-right, tail lower-left) with smoke.
        
        Args:
            x_offset: Horizontal offset for positioning
            y_offset: Vertical offset for positioning
            frame: Animation frame number for smoke
        """
        self.led.clear()  # Black background
        
        # Plane positioned diagonally (nose upper-right, tail lower-left)
        center_x = self.width // 2 + x_offset
        center_y = self.height // 2 + y_offset
        
        # Plane dimensions - smooth rounded silhouette
        fuselage_length = 10  # Main body length (diagonal)
        fuselage_width = 3  # Width of fuselage
        wing_length = 8  # Wings extend from fuselage
        wing_width = 3  # Wing thickness
        tail_stab_width = 6  # Horizontal stabilizer width
        
        # Draw fuselage - diagonal oval/rounded shape (nose upper-right, tail lower-left)
        for i in range(fuselage_length):
            progress = i / fuselage_length
            # Position along diagonal
            fx = center_x - fuselage_length // 2 + i
            fy = center_y + fuselage_length // 2 - i
            
            # Width - slightly wider in middle, rounded at ends
            if progress < 0.3 or progress > 0.7:
                width = int(fuselage_width * (0.5 + 0.5 * abs(progress * 2 - 1)))
            else:
                width = fuselage_width
            
            # Draw fuselage with rounded edges
            for offset in range(-width // 2, width // 2 + 1):
                for wy in range(fy - 1, fy + 2):
                    self.safe_set_pixel(fx + offset, wy, self.plane_color)
        
        # Round nose (upper-right)
        nose_x = center_x + fuselage_length // 2
        nose_y = center_y - fuselage_length // 2
        nose_radius = fuselage_width // 2 + 1
        for dx in range(-nose_radius, nose_radius + 1):
            for dy in range(-nose_radius, nose_radius + 1):
                if dx * dx + dy * dy <= nose_radius * nose_radius:
                    self.safe_set_pixel(nose_x + dx, nose_y + dy, self.plane_color)
        
        # Draw wings - extend horizontally from fuselage
        # Left wing points upper-left, right wing points lower-right
        wing_center_x = center_x
        wing_center_y = center_y
        
        # Left wing (upper-left direction)
        for i in range(wing_length):
            wx = wing_center_x - i
            wy = wing_center_y - i
            for offset in range(-wing_width // 2, wing_width // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Round left wing tip
        left_tip_x = wing_center_x - wing_length
        left_tip_y = wing_center_y - wing_length
        tip_radius = wing_width // 2 + 1
        for dx in range(-tip_radius, tip_radius + 1):
            for dy in range(-tip_radius, tip_radius + 1):
                if dx * dx + dy * dy <= tip_radius * tip_radius:
                    self.safe_set_pixel(left_tip_x + dx, left_tip_y + dy, self.plane_color)
        
        # Right wing (lower-right direction)
        for i in range(wing_length):
            wx = wing_center_x + i
            wy = wing_center_y + i
            for offset in range(-wing_width // 2, wing_width // 2 + 1):
                self.safe_set_pixel(wx + offset, wy, self.plane_color)
                self.safe_set_pixel(wx, wy + offset, self.plane_color)
        
        # Round right wing tip
        right_tip_x = wing_center_x + wing_length
        right_tip_y = wing_center_y + wing_length
        for dx in range(-tip_radius, tip_radius + 1):
            for dy in range(-tip_radius, tip_radius + 1):
                if dx * dx + dy * dy <= tip_radius * tip_radius:
                    self.safe_set_pixel(right_tip_x + dx, right_tip_y + dy, self.plane_color)
        
        # Draw tail section - horizontal stabilizer (in lower-left area)
        tail_x = center_x - fuselage_length // 2
        tail_y = center_y + fuselage_length // 2
        
        # Horizontal stabilizer - smooth rounded bar
        for i in range(tail_stab_width):
            stab_x = tail_x - tail_stab_width // 2 + i
            stab_y = tail_y
            for offset in range(-wing_width // 2, wing_width // 2 + 1):
                self.safe_set_pixel(stab_x, stab_y + offset, self.plane_color)
        
        # Round stabilizer ends
        for offset in range(-wing_width // 2, wing_width // 2 + 1):
            self.safe_set_pixel(tail_x - tail_stab_width // 2, tail_y + offset, self.plane_color)
            self.safe_set_pixel(tail_x + tail_stab_width // 2, tail_y + offset, self.plane_color)
        
        # Draw smoke trailing from tail (lower-left, opposite to plane direction upper-right)
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
