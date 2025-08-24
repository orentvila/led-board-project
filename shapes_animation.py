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
        self.total_duration = 15.0  # 15 seconds total (5 seconds per shape)
        self.shape_duration = 5.0   # Each shape shows for 5 seconds
        
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
    
    def run_animation(self):
        """Run the complete shapes animation."""
        print("🔴🟢🔵 Shapes Animation 🔴🟢🔵")
        print("Duration: 15 seconds")
        print("Sequence: Circle (5s) → Square (5s) → Triangle (5s)")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Create background
                frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
                
                # Determine which shape to show based on time
                if current_time < self.shape_duration:
                    # Show circle (0-5 seconds)
                    self.draw_circle(frame, self.width // 2, self.height // 2, 8, self.colors['circle'])
                    print(f"Showing circle... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 2:
                    # Show square (5-10 seconds)
                    self.draw_square(frame, self.width // 2, self.height // 2, 12, self.colors['square'])
                    print(f"Showing square... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 3:
                    # Show triangle (10-15 seconds)
                    self.draw_triangle(frame, self.width // 2, self.height // 2, 12, self.colors['triangle'])
                    print(f"Showing triangle... ({current_time:.1f}s)")
                
                # Display the frame
                for y in range(self.height):
                    for x in range(self.width):
                        self.led.set_pixel(x, y, frame[y, x])
                
                self.led.show()
                
                # Check if animation is complete
                if current_time >= self.total_duration:
                    print("Shapes animation completed!")
                    break
                
                time.sleep(0.1)  # 10 FPS for smooth animation
                
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