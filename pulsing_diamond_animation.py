#!/usr/bin/env python3
"""
Pulsing Diamond Animation for LED Board
A yellow diamond that pulses in size
"""

import time
import numpy as np
import math
from led_controller_exact import LEDControllerExact
import config

class PulsingDiamondAnimation:
    def __init__(self):
        """Initialize the pulsing diamond animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'yellow': (255, 255, 0),        # Yellow diamond
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.duration = 15  # seconds
        
    def create_pulsing_diamond(self, frame):
        """Create a yellow diamond that pulses in size."""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Calculate pulse size
        pulse_phase = (self.animation_timer % (self.duration * 20)) * 0.2
        pulse_size = int(8 + 4 * math.sin(pulse_phase))
        
        # Define diamond points
        diamond_points = [
            (center_x, center_y - pulse_size),      # Top
            (center_x + pulse_size, center_y),      # Right
            (center_x, center_y + pulse_size),       # Bottom
            (center_x - pulse_size, center_y)        # Left
        ]
        
        # Draw diamond
        self.draw_polygon(frame, diamond_points, self.colors['yellow'])
    
    def draw_polygon(self, frame, points, color):
        """Draw a polygon using scanline algorithm."""
        if len(points) < 3:
            return
        
        # Get bounding box
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
        
        # Scan each horizontal line
        for y in range(int(min_y), int(max_y) + 1):
            if y < 0 or y >= self.height:
                continue
                
            intersections = []
            
            # Find intersections with each edge
            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]
                
                # Check if edge intersects with horizontal line
                if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                    if p2[1] != p1[1]:  # Avoid division by zero
                        x = p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])
                        intersections.append(x)
            
            # Sort intersections and fill between pairs
            intersections.sort()
            for i in range(0, len(intersections), 2):
                if i + 1 < len(intersections):
                    start_x = int(intersections[i])
                    end_x = int(intersections[i + 1])
                    
                    for x in range(start_x, end_x + 1):
                        if 0 <= x < self.width:
                            frame[y, x] = color
    
    def create_frame(self):
        """Create a single frame of the pulsing diamond animation."""
        # Start with black background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create pulsing diamond
        self.create_pulsing_diamond(frame)
        
        return frame
    
    def display_pulsing_diamond(self):
        """Display the pulsing diamond animation."""
        print("🟡 Pulsing Diamond Animation 🟡")
        print(f"Displaying for {self.duration} seconds...")
        print("Features: Yellow diamond that pulses in size")
        
        start_time = time.time()
        
        while time.time() - start_time < self.duration:
            # Create the frame
            frame = self.create_frame()
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.animation_timer += 1
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("Pulsing diamond animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run pulsing diamond animation."""
    try:
        diamond = PulsingDiamondAnimation()
        diamond.display_pulsing_diamond()
        diamond.cleanup()
        
    except KeyboardInterrupt:
        print("\nPulsing diamond animation interrupted by user")
        diamond.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        diamond.cleanup()

if __name__ == "__main__":
    main()
