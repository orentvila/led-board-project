#!/usr/bin/env python3
"""
Shapes Animation for LED Board
Shows circle, square, and triangle appearing every 5 seconds in different colors
"""

import time
import numpy as np
from led_controller_fixed import LEDControllerFixed
import config

class ShapesAnimation:
    def __init__(self):
        """Initialize the shapes animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors for each shape
        self.colors = {
            'background': (0, 0, 0),         # Black background
            'circle': (255, 100, 100),       # Red circle
            'square': (100, 255, 100),       # Green square
            'triangle': (100, 100, 255)      # Blue triangle
        }
        
        # Animation timing
        self.total_duration = 40.0  # 40 seconds total
        self.shape_duration = 13.33  # Each shape shows for ~13.33 seconds
        
        # Movement parameters
        self.movement_speed = 2.0  # pixels per second
        self.shape_size = 8  # Size for all shapes
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        
    def draw_circle(self, array, center_x, center_y, radius, color):
        """Draw a circle at the given position."""
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                # Check if pixel is within circle
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance <= radius:
                    self.safe_set_pixel(array, x, y, color)
    
    def draw_square(self, array, center_x, center_y, size, color):
        """Draw a square at the given position."""
        half_size = size // 2
        for y in range(center_y - half_size, center_y + half_size + 1):
            for x in range(center_x - half_size, center_x + half_size + 1):
                self.safe_set_pixel(array, x, y, color)
    
    def draw_triangle(self, array, center_x, center_y, size, color):
        """Draw a triangle at the given position."""
        # Triangle points
        top_y = center_y - size // 2
        bottom_y = center_y + size // 2
        left_x = center_x - size // 2
        right_x = center_x + size // 2
        
        # Draw triangle using line algorithm
        for y in range(top_y, bottom_y + 1):
            # Calculate left and right edges for this row
            if y <= center_y:
                # Upper half of triangle
                progress = (y - top_y) / (center_y - top_y)
                left_edge = center_x - int((center_x - left_x) * progress)
                right_edge = center_x + int((right_x - center_x) * progress)
            else:
                # Lower half of triangle
                progress = (y - center_y) / (bottom_y - center_y)
                left_edge = left_x + int((center_x - left_x) * progress)
                right_edge = right_x - int((right_x - center_x) * progress)
            
            # Draw horizontal line for this row
            for x in range(left_edge, right_edge + 1):
                self.safe_set_pixel(array, x, y, color)
    
    def calculate_bouncing_position(self, current_time, shape_start_time, direction=1):
        """Calculate bouncing position for a shape."""
        # Calculate time since shape started
        shape_time = current_time - shape_start_time
        
        # Calculate position with bouncing
        distance = shape_time * self.movement_speed
        
        # Bounce off edges
        max_distance = self.width - self.shape_size
        if max_distance <= 0:
            max_distance = self.width // 2
        
        # Calculate bouncing position
        position = distance % (2 * max_distance)
        if position > max_distance:
            position = 2 * max_distance - position
        
        return int(position + self.shape_size // 2)
    
    def run_animation(self):
        """Run the complete shapes animation."""
        print("🔴🟢🔵 Bouncing Shapes Animation 🔴🟢🔵")
        print("Duration: 40 seconds")
        print("Sequence: Circle (13.33s) → Square (13.33s) → Triangle (13.33s)")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Create background
                frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
                
                # Determine which shape to show based on time
                if current_time < self.shape_duration:
                    # Show bouncing circle (0-13.33 seconds)
                    circle_x = self.calculate_bouncing_position(current_time, 0)
                    self.draw_circle(frame, circle_x, self.height // 2, self.shape_size, self.colors['circle'])
                    print(f"Showing bouncing circle at x={circle_x}... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 2:
                    # Show bouncing square (13.33-26.66 seconds)
                    square_x = self.calculate_bouncing_position(current_time, self.shape_duration)
                    self.draw_square(frame, square_x, self.height // 2, self.shape_size, self.colors['square'])
                    print(f"Showing bouncing square at x={square_x}... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 3:
                    # Show bouncing triangle (26.66-40 seconds)
                    triangle_x = self.calculate_bouncing_position(current_time, self.shape_duration * 2)
                    self.draw_triangle(frame, triangle_x, self.height // 2, self.shape_size, self.colors['triangle'])
                    print(f"Showing bouncing triangle at x={triangle_x}... ({current_time:.1f}s)")
                
                # Display the frame
                for y in range(self.height):
                    for x in range(self.width):
                        self.led.set_pixel(x, y, frame[y, x])
                
                self.led.show()
                
                # Check if animation is complete
                if current_time >= self.total_duration:
                    print("Shapes animation completed!")
                    break
                
                time.sleep(0.05)  # 20 FPS for smooth animation
                
        except KeyboardInterrupt:
            print("\nShapes animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run shapes animation."""
    try:
        shapes = ShapesAnimation()
        shapes.run_animation()
        shapes.cleanup()
        
    except KeyboardInterrupt:
        print("\nShapes animation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 