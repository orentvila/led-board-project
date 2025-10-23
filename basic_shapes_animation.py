#!/usr/bin/env python3
"""
Basic Shapes Animation for LED Board
Features: Growing circle, rotating square, bouncing triangle, pulsing diamond
"""

import time
import numpy as np
import math
import random
from led_controller_exact import LEDControllerExact
import config

class BasicShapesAnimation:
    def __init__(self):
        """Initialize the basic shapes animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'red': (255, 0, 0),             # Red circle
            'blue': (0, 0, 255),            # Blue square
            'green': (0, 255, 0),           # Green triangle
            'yellow': (255, 255, 0),        # Yellow diamond
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.current_shape = 0  # 0=circle, 1=square, 2=triangle, 3=diamond
        self.shape_duration = 200  # frames per shape
        
        # Shape-specific parameters
        self.circle_radius = 0
        self.square_rotation = 0
        self.triangle_x = 16
        self.triangle_y = 24
        self.triangle_dx = 2
        self.triangle_dy = 1
        self.diamond_pulse = 0
        
    def create_growing_circle(self, frame):
        """Create a red circle that grows from small to big."""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Calculate current radius based on animation progress
        progress = (self.animation_timer % self.shape_duration) / self.shape_duration
        max_radius = min(self.width, self.height) // 2 - 2
        current_radius = int(progress * max_radius)
        
        # Draw circle
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= current_radius:
                    frame[y, x] = self.colors['red']
    
    def create_rotating_square(self, frame):
        """Create a blue square that rotates clockwise."""
        center_x, center_y = self.width // 2, self.height // 2
        size = 12  # Square size
        
        # Calculate rotation angle
        rotation_angle = (self.animation_timer % self.shape_duration) * 0.1
        
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
    
    def create_pulsing_diamond(self, frame):
        """Create a yellow diamond that pulses in size."""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Calculate pulse size
        pulse_phase = (self.animation_timer % self.shape_duration) * 0.2
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
        """Create a single frame of the shapes animation."""
        # Start with black background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Determine current shape based on animation timer
        shape_index = (self.animation_timer // self.shape_duration) % 4
        
        if shape_index == 0:
            self.create_growing_circle(frame)
        elif shape_index == 1:
            self.create_rotating_square(frame)
        elif shape_index == 2:
            self.create_bouncing_triangle(frame)
        elif shape_index == 3:
            self.create_pulsing_diamond(frame)
        
        return frame
    
    def display_shapes_animation(self, duration=30):
        """Display the shapes animation."""
        print("🔷 Basic Shapes Animation 🔷")
        print(f"Displaying for {duration} seconds...")
        print("Features: Growing circle, rotating square, bouncing triangle, pulsing diamond")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
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
        
        print("Shapes animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run shapes animation."""
    try:
        shapes = BasicShapesAnimation()
        shapes.display_shapes_animation(30)
        shapes.cleanup()
        
    except KeyboardInterrupt:
        print("\nShapes animation interrupted by user")
        shapes.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        shapes.cleanup()

if __name__ == "__main__":
    main()
