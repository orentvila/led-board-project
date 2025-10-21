#!/usr/bin/env python3
"""
Big Shapes Animation for LED Board
Features large triangle, square, star, sun, and circle that fill the display
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class BigShapesAnimation:
    def __init__(self):
        """Initialize the big shapes animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors for each shape
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'triangle': (255, 100, 100),    # Red triangle
            'square': (100, 255, 100),      # Green square
            'star': (255, 255, 100),        # Yellow star
            'sun': (255, 200, 100),         # Orange sun
            'circle': (100, 100, 255),      # Blue circle
            'triangle_outline': (255, 150, 150), # Light red outline
            'square_outline': (150, 255, 150),   # Light green outline
            'star_outline': (255, 255, 150),     # Light yellow outline
            'sun_outline': (255, 220, 150),      # Light orange outline
            'circle_outline': (150, 150, 255)    # Light blue outline
        }
        
        # Animation parameters
        self.rotation = 0
        self.pulse_timer = 0
        self.current_shape = 0
        self.shape_duration = 5  # seconds per shape
        
    def create_big_triangle(self, frame, rotation=0):
        """Create a large triangle that fills most of the display."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Triangle size (as big as possible)
        triangle_size = min(self.width, self.height) * 0.8
        
        for y in range(self.height):
            for x in range(self.width):
                # Transform coordinates for rotation
                dx = x - center_x
                dy = y - center_y
                
                # Apply rotation
                cos_r = math.cos(rotation)
                sin_r = math.sin(rotation)
                rx = dx * cos_r - dy * sin_r
                ry = dx * sin_r + dy * cos_r
                
                # Triangle shape (equilateral)
                # Check if point is inside triangle
                size = triangle_size
                
                # Triangle vertices (rotated)
                v1_x, v1_y = 0, -size * 0.6  # Top vertex
                v2_x, v2_y = -size * 0.5, size * 0.3  # Bottom left
                v3_x, v3_y = size * 0.5, size * 0.3   # Bottom right
                
                # Check if point (rx, ry) is inside triangle
                def point_in_triangle(px, py, v1x, v1y, v2x, v2y, v3x, v3y):
                    # Barycentric coordinate method
                    def sign(px, py, v1x, v1y, v2x, v2y):
                        return (px - v2x) * (v1y - v2y) - (v1x - v2x) * (py - v2y)
                    
                    d1 = sign(px, py, v1x, v1y, v2x, v2y)
                    d2 = sign(px, py, v2x, v2y, v3x, v3y)
                    d3 = sign(px, py, v3x, v3y, v1x, v1y)
                    
                    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
                    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
                    
                    return not (has_neg and has_pos)
                
                if point_in_triangle(rx, ry, v1_x, v1_y, v2_x, v2_y, v3_x, v3_y):
                    # Add some variation based on position
                    variation = math.sin(rx * 0.1 + ry * 0.1 + self.pulse_timer * 0.1) * 0.2 + 0.8
                    color = tuple(int(c * variation) for c in self.colors['triangle'])
                    frame[y, x] = color
    
    def create_big_square(self, frame, rotation=0):
        """Create a large square that fills most of the display."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Square size (as big as possible)
        square_size = min(self.width, self.height) * 0.7
        
        for y in range(self.height):
            for x in range(self.width):
                # Transform coordinates for rotation
                dx = x - center_x
                dy = y - center_y
                
                # Apply rotation
                cos_r = math.cos(rotation)
                sin_r = math.sin(rotation)
                rx = dx * cos_r - dy * sin_r
                ry = dx * sin_r + dy * cos_r
                
                # Check if point is inside square
                if abs(rx) <= square_size and abs(ry) <= square_size:
                    # Add some variation based on position
                    variation = math.sin(rx * 0.1 + ry * 0.1 + self.pulse_timer * 0.1) * 0.2 + 0.8
                    color = tuple(int(c * variation) for c in self.colors['square'])
                    frame[y, x] = color
    
    def create_big_star(self, frame, rotation=0):
        """Create a large star that fills most of the display."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Star size (as big as possible)
        star_size = min(self.width, self.height) * 0.6
        
        for y in range(self.height):
            for x in range(self.width):
                # Transform coordinates for rotation
                dx = x - center_x
                dy = y - center_y
                
                # Apply rotation
                cos_r = math.cos(rotation)
                sin_r = math.sin(rotation)
                rx = dx * cos_r - dy * sin_r
                ry = dx * sin_r + dy * cos_r
                
                # Calculate distance and angle
                distance = math.sqrt(rx**2 + ry**2)
                angle = math.atan2(ry, rx)
                
                # 5-pointed star shape
                star_angle = (angle + math.pi) / (2 * math.pi) * 10  # 10 for 5-pointed star
                star_angle = star_angle % 2
                
                # Star radius varies with angle
                if star_angle < 1:
                    # Outer points
                    radius = star_size
                else:
                    # Inner points
                    radius = star_size * 0.4
                
                if distance <= radius:
                    # Add some variation based on position
                    variation = math.sin(rx * 0.1 + ry * 0.1 + self.pulse_timer * 0.1) * 0.2 + 0.8
                    color = tuple(int(c * variation) for c in self.colors['star'])
                    frame[y, x] = color
    
    def create_big_sun(self, frame, rotation=0):
        """Create a large sun with rays that fills most of the display."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Sun size (as big as possible)
        sun_size = min(self.width, self.height) * 0.5
        
        for y in range(self.height):
            for x in range(self.width):
                # Transform coordinates for rotation
                dx = x - center_x
                dy = y - center_y
                
                # Apply rotation
                cos_r = math.cos(rotation)
                sin_r = math.sin(rotation)
                rx = dx * cos_r - dy * sin_r
                ry = dx * sin_r + dy * cos_r
                
                # Calculate distance and angle
                distance = math.sqrt(rx**2 + ry**2)
                angle = math.atan2(ry, rx)
                
                # Sun rays (12 rays)
                ray_angle = (angle + math.pi) / (2 * math.pi) * 12
                ray_angle = ray_angle % 1
                
                # Ray pattern
                if ray_angle < 0.3:  # Ray
                    radius = sun_size * 1.2
                else:  # Between rays
                    radius = sun_size
                
                if distance <= radius:
                    # Add pulsing effect
                    pulse = math.sin(self.pulse_timer * 0.2) * 0.3 + 0.7
                    color = tuple(int(c * pulse) for c in self.colors['sun'])
                    frame[y, x] = color
    
    def create_big_circle(self, frame, rotation=0):
        """Create a large circle that fills most of the display."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Circle size (as big as possible)
        circle_size = min(self.width, self.height) * 0.8
        
        for y in range(self.height):
            for x in range(self.width):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= circle_size:
                    # Add some variation based on position
                    variation = math.sin(dx * 0.1 + dy * 0.1 + self.pulse_timer * 0.1) * 0.2 + 0.8
                    color = tuple(int(c * variation) for c in self.colors['circle'])
                    frame[y, x] = color
    
    def display_shape(self, shape_name, shape_func, duration=5):
        """Display a specific shape for the given duration."""
        print(f"Displaying BIG {shape_name.upper()} for {duration} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create frame with current shape
            frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
            
            # Draw the shape
            shape_func(frame, self.rotation)
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.rotation += 0.05  # Rotate shape
            self.pulse_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print(f"{shape_name.capitalize()} display completed!")
    
    def display_big_shapes_sequence(self):
        """Display the sequence of big shapes."""
        print("🔺🔲⭐☀️⭕ BIG SHAPES ANIMATION 🔺🔲⭐☀️⭕")
        print("Sequence: Triangle → Square → Star → Sun → Circle")
        print("Each shape is as BIG as possible!")
        
        try:
            # Define shapes and their functions
            shapes = [
                ("triangle", self.create_big_triangle),
                ("square", self.create_big_square),
                ("star", self.create_big_star),
                ("sun", self.create_big_sun),
                ("circle", self.create_big_circle)
            ]
            
            for shape_name, shape_func in shapes:
                # Display the shape
                self.display_shape(shape_name, shape_func, self.shape_duration)
                
                # Brief pause between shapes
                if shape_name != "circle":  # Don't pause after the last shape
                    print("Transitioning to next shape...")
                    time.sleep(1)
            
            print("Big shapes animation completed!")
            
        except KeyboardInterrupt:
            print("\nBig shapes animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run big shapes animation."""
    try:
        shapes = BigShapesAnimation()
        shapes.display_big_shapes_sequence()
        shapes.cleanup()
        
    except KeyboardInterrupt:
        print("\nBig shapes animation interrupted by user")
        shapes.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        shapes.cleanup()

if __name__ == "__main__":
    main() 