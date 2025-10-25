#!/usr/bin/env python3
"""
Shapes Animation for LED Board
Shows circle, square, and triangle appearing every 5 seconds in different colors
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class ShapesAnimation:
    def __init__(self):
        """Initialize the shapes animation."""
        self.led = LEDControllerExact()
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
        self.movement_speed = 1.5  # pixels per second
        self.shape_size = 8  # Size for all shapes
        
        # Movement state for each shape
        self.circle_dx = 1
        self.circle_dy = 1
        self.square_dx = -1
        self.square_dy = 1
        self.triangle_dx = 1
        self.triangle_dy = -1
        
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
    
    def calculate_bouncing_position(self, current_time, shape_start_time, shape_type):
        """Calculate bouncing position for a shape with realistic edge collision."""
        # Calculate time since shape started
        shape_time = current_time - shape_start_time
        
        # Get current direction for this shape
        if shape_type == 'circle':
            dx = self.circle_dx
            dy = self.circle_dy
        elif shape_type == 'square':
            dx = self.square_dx
            dy = self.square_dy
        else:  # triangle
            dx = self.triangle_dx
            dy = self.triangle_dy
        
        # Calculate new position
        x_offset = dx * shape_time * self.movement_speed
        y_offset = dy * shape_time * self.movement_speed
        
        # Start positions (different for each shape to avoid overlap)
        if shape_type == 'circle':
            start_x = self.shape_size // 2
            start_y = self.height // 2
        elif shape_type == 'square':
            start_x = self.width - self.shape_size // 2
            start_y = self.shape_size // 2
        else:  # triangle
            start_x = self.shape_size // 2
            start_y = self.height - self.shape_size // 2
        
        # Calculate current position
        x = start_x + x_offset
        y = start_y + y_offset
        
        # Check for edge collisions and bounce
        x, dx = self.check_edge_collision_x(x, dx, shape_type)
        y, dy = self.check_edge_collision_y(y, dy, shape_type)
        
        # Update direction for this shape
        if shape_type == 'circle':
            self.circle_dx = dx
            self.circle_dy = dy
        elif shape_type == 'square':
            self.square_dx = dx
            self.square_dy = dy
        else:  # triangle
            self.triangle_dx = dx
            self.triangle_dy = dy
        
        return int(x), int(y)
    
    def check_edge_collision_x(self, x, dx, shape_type):
        """Check for horizontal edge collision and reverse direction."""
        # Check left edge
        if x <= self.shape_size // 2:
            x = self.shape_size // 2
            dx = abs(dx)  # Reverse direction
        # Check right edge
        elif x >= self.width - self.shape_size // 2:
            x = self.width - self.shape_size // 2
            dx = -abs(dx)  # Reverse direction
        
        return x, dx
    
    def check_edge_collision_y(self, y, dy, shape_type):
        """Check for vertical edge collision and reverse direction."""
        # Check top edge
        if y <= self.shape_size // 2:
            y = self.shape_size // 2
            dy = abs(dy)  # Reverse direction
        # Check bottom edge
        elif y >= self.height - self.shape_size // 2:
            y = self.height - self.shape_size // 2
            dy = -abs(dy)  # Reverse direction
        
        return y, dy
    
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
                    circle_x, circle_y = self.calculate_bouncing_position(current_time, 0, 'circle')
                    self.draw_circle(frame, circle_x, circle_y, self.shape_size, self.colors['circle'])
                    print(f"Showing bouncing circle at ({circle_x}, {circle_y})... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 2:
                    # Show bouncing square (13.33-26.66 seconds)
                    square_x, square_y = self.calculate_bouncing_position(current_time, self.shape_duration, 'square')
                    self.draw_square(frame, square_x, square_y, self.shape_size, self.colors['square'])
                    print(f"Showing bouncing square at ({square_x}, {square_y})... ({current_time:.1f}s)")
                    
                elif current_time < self.shape_duration * 3:
                    # Show bouncing triangle (26.66-40 seconds)
                    triangle_x, triangle_y = self.calculate_bouncing_position(current_time, self.shape_duration * 2, 'triangle')
                    self.draw_triangle(frame, triangle_x, triangle_y, self.shape_size, self.colors['triangle'])
                    print(f"Showing bouncing triangle at ({triangle_x}, {triangle_y})... ({current_time:.1f}s)")
                
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