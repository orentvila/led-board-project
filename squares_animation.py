#!/usr/bin/env python3
"""
Squares Animation for LED Display
Splits the screen into 24 squares (6 rows × 4 columns) and shows each square
with a different soft color for 2 seconds, appearing randomly.
"""

import time
import random
import math
from led_controller_exact import LEDControllerExact
import config

class SquaresAnimation:
    def __init__(self, led_controller):
        """Initialize the squares animation."""
        self.led = led_controller
        self.running = False
        
        # Calculate square dimensions
        self.squares_per_row = 4
        self.squares_per_col = 6
        self.total_squares = self.squares_per_row * self.squares_per_col  # 24 squares
        
        # Calculate pixel dimensions for each square
        self.square_width = config.TOTAL_WIDTH // self.squares_per_row  # 32 // 4 = 8 pixels
        self.square_height = config.TOTAL_HEIGHT // self.squares_per_col  # 48 // 6 = 8 pixels
        
        # Generate 24 soft colors
        self.soft_colors = self._generate_soft_colors()
        
    def _generate_soft_colors(self):
        """Generate 24 different soft colors."""
        colors = []
        
        # Base colors for soft variations
        base_colors = [
            (255, 200, 200),  # Soft red
            (200, 255, 200),  # Soft green
            (200, 200, 255),  # Soft blue
            (255, 255, 200),  # Soft yellow
            (255, 200, 255),  # Soft magenta
            (200, 255, 255),  # Soft cyan
            (255, 220, 180),  # Soft orange
            (220, 200, 255),  # Soft purple
            (255, 180, 220),  # Soft pink
            (180, 255, 220),  # Soft mint
            (220, 255, 180),  # Soft lime
            (180, 220, 255),  # Soft sky blue
            (255, 200, 180),  # Soft peach
            (200, 180, 255),  # Soft lavender
            (180, 255, 200),  # Soft mint green
            (255, 180, 200),  # Soft rose
            (200, 255, 180),  # Soft spring green
            (180, 200, 255),  # Soft periwinkle
            (240, 200, 200),  # Soft coral
            (200, 240, 200),  # Soft sage
            (200, 200, 240),  # Soft powder blue
            (240, 240, 200),  # Soft cream
            (240, 200, 240),  # Soft orchid
            (200, 240, 240),  # Soft aqua
        ]
        
        return base_colors
    
    def _get_square_bounds(self, square_index):
        """Get the pixel bounds for a given square index."""
        row = square_index // self.squares_per_row
        col = square_index % self.squares_per_row
        
        start_x = col * self.square_width
        end_x = start_x + self.square_width
        start_y = row * self.square_height
        end_y = start_y + self.square_height
        
        return start_x, end_x, start_y, end_y
    
    def _draw_square(self, square_index, color):
        """Draw a specific square with the given color."""
        start_x, end_x, start_y, end_y = self._get_square_bounds(square_index)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.led.set_pixel(x, y, color)
    
    def _clear_square(self, square_index):
        """Clear a specific square (set to black)."""
        self._draw_square(square_index, config.COLORS['BLACK'])
    
    def run_animation(self, duration=None):
        """Run the squares animation."""
        self.running = True
        start_time = time.time()
        
        # Create a list of all square indices and shuffle them
        square_indices = list(range(self.total_squares))
        random.shuffle(square_indices)
        
        # Keep track of which squares have been shown
        shown_squares = set()
        
        print(f"Starting squares animation with {self.total_squares} squares")
        print(f"Square dimensions: {self.square_width}x{self.square_height} pixels")
        
        while self.running and (duration is None or time.time() - start_time < duration):
            # Check if all squares have been shown
            if len(shown_squares) >= self.total_squares:
                print("All squares have been shown! Animation complete.")
                break
            
            # Pick a random square that hasn't been shown yet
            available_squares = [i for i in square_indices if i not in shown_squares]
            if not available_squares:
                break
                
            square_index = random.choice(available_squares)
            color = self.soft_colors[square_index]
            
            # Show the square
            self._draw_square(square_index, color)
            self.led.show()
            
            # Mark as shown
            shown_squares.add(square_index)
            
            print(f"Showing square {square_index + 1}/{self.total_squares} with color {color}")
            
            # Wait for 2 seconds
            time.sleep(2.0)
        
        # Keep all squares lit for a final moment
        if shown_squares:
            print("Keeping all squares lit for final display...")
            time.sleep(3.0)
        
        # Clear the display
        self.led.clear()
        self.led.show()
        
        print("Squares animation completed!")
    
    def stop(self):
        """Stop the animation."""
        self.running = False

def main():
    """Test the squares animation."""
    try:
        # Initialize LED controller
        led = LEDController()
        
        # Create and run the animation
        animation = SquaresAnimation(led)
        animation.run_animation()
        
        # Cleanup
        led.cleanup()
        
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
