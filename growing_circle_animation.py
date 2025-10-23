#!/usr/bin/env python3
"""
Growing Circle Animation for LED Board
A red circle that grows from small to big
"""

import time
import numpy as np
import math
from led_controller_exact import LEDControllerExact
import config

class GrowingCircleAnimation:
    def __init__(self):
        """Initialize the growing circle animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'red': (255, 0, 0),             # Red circle
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.duration = 15  # seconds
        
    def create_growing_circle(self, frame):
        """Create a red circle that grows from small to big."""
        center_x, center_y = self.width // 2, self.height // 2
        
        # Calculate current radius based on animation progress
        progress = (self.animation_timer % (self.duration * 20)) / (self.duration * 20)
        max_radius = min(self.width, self.height) // 2 - 2
        current_radius = int(progress * max_radius)
        
        # Draw circle
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= current_radius:
                    frame[y, x] = self.colors['red']
    
    def create_frame(self):
        """Create a single frame of the growing circle animation."""
        # Start with black background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create growing circle
        self.create_growing_circle(frame)
        
        return frame
    
    def display_growing_circle(self):
        """Display the growing circle animation."""
        print("🔴 Growing Circle Animation 🔴")
        print(f"Displaying for {self.duration} seconds...")
        print("Features: Red circle that grows from small to big")
        
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
        
        print("Growing circle animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run growing circle animation."""
    try:
        circle = GrowingCircleAnimation()
        circle.display_growing_circle()
        circle.cleanup()
        
    except KeyboardInterrupt:
        print("\nGrowing circle animation interrupted by user")
        circle.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        circle.cleanup()

if __name__ == "__main__":
    main()
