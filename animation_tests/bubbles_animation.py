#!/usr/bin/env python3
"""
Bubbles Animation for LED Board
Shows colorful bubbles of different sizes rising from the bottom
"""

import time
import numpy as np
import random
from led_controller_exact import LEDControllerExact
import config

class BubblesAnimation:
    def __init__(self):
        """Initialize the bubbles animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors for bubbles - soft, translucent colors
        self.bubble_colors = [
            (100, 200, 255),  # Light blue
            (255, 150, 200),  # Pink
            (200, 255, 150),  # Light green
            (255, 200, 100),  # Orange
            (200, 150, 255),  # Purple
            (150, 255, 200),  # Mint green
            (255, 100, 150),  # Rose
            (100, 255, 255),  # Cyan
        ]
        
        self.background_color = (0, 0, 0)  # Black background
        
        # Animation parameters
        self.total_duration = 30.0  # 30 seconds
        self.bubble_spawn_rate = 0.3  # New bubble every 0.3 seconds
        self.max_bubbles = 15  # Maximum number of bubbles on screen
        
        # Bubble properties
        self.bubble_sizes = [2, 3, 4, 5]  # Different bubble sizes
        self.rise_speeds = [0.5, 0.8, 1.2, 1.5]  # Different rise speeds
        
        # Bubble storage
        self.bubbles = []
        self.last_spawn_time = 0
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        
    def draw_circle(self, array, center_x, center_y, radius, color):
        """Draw a circle (bubble) at the given position."""
        for y in range(center_y - radius, center_y + radius + 1):
            for x in range(center_x - radius, center_x + radius + 1):
                # Check if pixel is within circle
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance <= radius:
                    # Add some transparency effect by blending with background
                    if distance <= radius - 1:
                        # Solid center
                        self.safe_set_pixel(array, x, y, color)
                    else:
                        # Translucent edge
                        blend_factor = 0.7
                        blended_color = tuple(int(c * blend_factor + bg * (1 - blend_factor)) 
                                            for c, bg in zip(color, self.background_color))
                        self.safe_set_pixel(array, x, y, blended_color)
        
        # Add highlight for 3D effect
        highlight_x = center_x - radius // 3
        highlight_y = center_y - radius // 3
        if radius > 2:
            highlight_color = tuple(min(255, c + 50) for c in color)
            self.safe_set_pixel(array, highlight_x, highlight_y, highlight_color)
    
    def spawn_bubble(self, current_time):
        """Spawn a new bubble at the bottom."""
        if len(self.bubbles) < self.max_bubbles:
            # Random properties for the new bubble
            x = random.randint(2, self.width - 3)
            y = self.height + 2  # Start just below screen
            size = random.choice(self.bubble_sizes)
            color = random.choice(self.bubble_colors)
            speed = random.choice(self.rise_speeds)
            
            # Add some horizontal drift
            drift = random.uniform(-0.3, 0.3)
            
            bubble = {
                'x': x,
                'y': y,
                'size': size,
                'color': color,
                'speed': speed,
                'drift': drift,
                'spawn_time': current_time
            }
            
            self.bubbles.append(bubble)
    
    def update_bubbles(self, current_time):
        """Update all bubble positions."""
        # Remove bubbles that have risen off the top
        self.bubbles = [bubble for bubble in self.bubbles 
                       if bubble['y'] > -bubble['size']]
        
        # Update remaining bubbles
        for bubble in self.bubbles:
            # Move bubble upward
            bubble['y'] -= bubble['speed']
            
            # Add horizontal drift
            bubble['x'] += bubble['drift']
            
            # Keep bubble within horizontal bounds
            if bubble['x'] < bubble['size']:
                bubble['x'] = bubble['size']
                bubble['drift'] = abs(bubble['drift'])  # Bounce off left edge
            elif bubble['x'] > self.width - bubble['size']:
                bubble['x'] = self.width - bubble['size']
                bubble['drift'] = -abs(bubble['drift'])  # Bounce off right edge
    
    def draw_bubbles(self, array):
        """Draw all bubbles on the array."""
        for bubble in self.bubbles:
            x = int(bubble['x'])
            y = int(bubble['y'])
            size = bubble['size']
            color = bubble['color']
            
            # Only draw if bubble is visible
            if y + size >= 0 and y - size < self.height:
                self.draw_circle(array, x, y, size, color)
    
    def run_animation(self):
        """Run the complete bubbles animation."""
        print("🫧 Bubbles Animation 🫧")
        print("Duration: 30 seconds")
        print("Colorful bubbles rising from the bottom")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Spawn new bubbles
                if current_time - self.last_spawn_time > self.bubble_spawn_rate:
                    self.spawn_bubble(current_time)
                    self.last_spawn_time = current_time
                
                # Update bubble positions
                self.update_bubbles(current_time)
                
                # Create background
                frame = np.full((self.height, self.width, 3), self.background_color, dtype=np.uint8)
                
                # Draw all bubbles
                self.draw_bubbles(frame)
                
                # Display the frame
                for y in range(self.height):
                    for x in range(self.width):
                        self.led.set_pixel(x, y, frame[y, x])
                
                self.led.show()
                
                # Check if animation is complete
                if current_time >= self.total_duration:
                    print("Bubbles animation completed!")
                    break
                
                time.sleep(0.05)  # 20 FPS for smooth animation
                
        except KeyboardInterrupt:
            print("\nBubbles animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run bubbles animation."""
    try:
        bubbles = BubblesAnimation()
        bubbles.run_animation()
        bubbles.cleanup()
        
    except KeyboardInterrupt:
        print("\nBubbles animation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 