#!/usr/bin/env python3
"""
Bouncing Triangle Animation for LED Board
A green triangle that bounces around the screen
"""

import time
import numpy as np
import math
from led_controller_exact import LEDControllerExact
import config

class BouncingTriangleAnimation:
    def __init__(self):
        """Initialize the bouncing triangle animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'green': (0, 255, 0),           # Green triangle
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.duration = 15  # seconds
        
        # Triangle position and movement
        self.triangle_x = 16
        self.triangle_y = 24
        self.triangle_dx = 2
        self.triangle_dy = 1
        
    def create_bouncing_triangle(self, frame):
        """Create a green triangle that bounces around the screen."""
        # Update triangle position
        self.triangle_x += self.triangle_dx
        self.triangle_y += self.triangle_dy
        
        # Bounce off edges
        if self.triangle_x <= 5 or self.triangle_x >= self.width - 5:
            self.triangle_dx = -self.triangle_dx
        if self.triangle_y <= 5 or self.triangle_y >= self.height - 5:
            self.triangle_dy = -self.triangle_dy
        
        # Keep triangle in bounds
        self.triangle_x = max(5, min(self.width - 5, self.triangle_x))
        self.triangle_y = max(5, min(self.height - 5, self.triangle_y))
        
        # Define triangle points
        triangle_size = 8
        triangle_points = [
            (self.triangle_x, self.triangle_y - triangle_size),  # Top
            (self.triangle_x - triangle_size, self.triangle_y + triangle_size),  # Bottom left
            (self.triangle_x + triangle_size, self.triangle_y + triangle_size)   # Bottom right
        ]
        
        # Draw triangle
        self.draw_polygon(frame, triangle_points, self.colors['green'])
    
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
        """Create a single frame of the bouncing triangle animation."""
        # Start with black background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create bouncing triangle
        self.create_bouncing_triangle(frame)
        
        return frame
    
    def display_bouncing_triangle(self):
        """Display the bouncing triangle animation."""
        print("🟢 Bouncing Triangle Animation 🟢")
        print(f"Displaying for {self.duration} seconds...")
        print("Features: Green triangle that bounces around the screen")
        
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
        
        print("Bouncing triangle animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run bouncing triangle animation."""
    try:
        triangle = BouncingTriangleAnimation()
        triangle.display_bouncing_triangle()
        triangle.cleanup()
        
    except KeyboardInterrupt:
        print("\nBouncing triangle animation interrupted by user")
        triangle.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        triangle.cleanup()

if __name__ == "__main__":
    main()
