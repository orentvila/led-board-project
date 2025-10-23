#!/usr/bin/env python3
"""
Rotating Square Animation for LED Board
A blue square that rotates clockwise
"""

import time
import numpy as np
import math
from led_controller_exact import LEDControllerExact
import config

class RotatingSquareAnimation:
    def __init__(self):
        """Initialize the rotating square animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'blue': (0, 0, 255),            # Blue square
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.duration = 15  # seconds
        
    def create_rotating_square(self, frame):
        """Create a blue square that rotates clockwise."""
        center_x, center_y = self.width // 2, self.height // 2
        size = 12  # Square size
        
        # Calculate rotation angle
        rotation_angle = (self.animation_timer % (self.duration * 20)) * 0.1
        
        # Define square corners (before rotation)
        corners = [
            (-size//2, -size//2),
            (size//2, -size//2),
            (size//2, size//2),
            (-size//2, size//2)
        ]
        
        # Rotate corners
        rotated_corners = []
        for x, y in corners:
            cos_a = math.cos(rotation_angle)
            sin_a = math.sin(rotation_angle)
            new_x = x * cos_a - y * sin_a
            new_y = x * sin_a + y * cos_a
            rotated_corners.append((new_x + center_x, new_y + center_y))
        
        # Draw rotated square using scanline algorithm
        self.draw_polygon(frame, rotated_corners, self.colors['blue'])
    
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
        """Create a single frame of the rotating square animation."""
        # Start with black background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create rotating square
        self.create_rotating_square(frame)
        
        return frame
    
    def display_rotating_square(self):
        """Display the rotating square animation."""
        print("🔵 Rotating Square Animation 🔵")
        print(f"Displaying for {self.duration} seconds...")
        print("Features: Blue square that rotates clockwise")
        
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
        
        print("Rotating square animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run rotating square animation."""
    try:
        square = RotatingSquareAnimation()
        square.display_rotating_square()
        square.cleanup()
        
    except KeyboardInterrupt:
        print("\nRotating square animation interrupted by user")
        square.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        square.cleanup()

if __name__ == "__main__":
    main()
