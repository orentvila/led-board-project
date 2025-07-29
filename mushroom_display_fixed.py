#!/usr/bin/env python3
"""
Mushroom Display for LED Board - Fixed Version
Creates a mushroom image on the 32x40 LED display using the correct mapping
"""

import time
import numpy as np
from led_controller_fixed import LEDControllerFixed
import config

class MushroomDisplayFixed:
    def __init__(self):
        """Initialize the mushroom display."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Mushroom colors
        self.colors = {
            'stem': (139, 69, 19),      # Brown
            'cap': (255, 0, 0),         # Red
            'spots': (200, 200, 200),   # Light gray
            'background': (0, 0, 0)     # Black
        }
    
    def create_mushroom_pattern(self):
        """Create a mushroom pattern for 32x40 display."""
        # Create empty display matrix
        display = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Mushroom dimensions (scaled for 32x40 display)
        # Stem: 12 pixels tall, 8 pixels wide
        # Cap: 18 pixels tall, 24 pixels wide
        
        # Calculate center position
        center_x = self.width // 2  # 16
        
        # Draw stem (brown)
        stem_width = 8
        stem_height = 12
        stem_x = center_x - stem_width // 2  # 12
        stem_y = self.height - stem_height - 4  # 24 (4 pixels above bottom)
        
        for y in range(stem_height):
            for x in range(stem_width):
                if 0 <= stem_x + x < self.width and 0 <= stem_y + y < self.height:
                    display[stem_y + y, stem_x + x] = self.colors['stem']
        
        # Draw cap (red) - make it more rounded
        cap_width = 24
        cap_height = 18
        cap_x = center_x - cap_width // 2  # 4
        cap_y = 6  # Start 6 pixels from top
        
        for y in range(cap_height):
            for x in range(cap_width):
                # Make the cap rounded (ellipse equation)
                rel_x = (x - cap_width / 2) / (cap_width / 2)
                rel_y = (y - cap_height / 2) / (cap_height / 2)
                if rel_x**2 + (rel_y * 1.3)**2 <= 1.0:
                    if 0 <= cap_x + x < self.width and 0 <= cap_y + y < self.height:
                        display[cap_y + y, cap_x + x] = self.colors['cap']
        
        # Add white spots on cap (manually placed for aesthetics)
        spots = [
            (center_x - 8, cap_y + 4),
            (center_x + 6, cap_y + 3),
            (center_x, cap_y + 8),
            (center_x - 6, cap_y + 12),
            (center_x + 8, cap_y + 13),
            (center_x - 10, cap_y + 10),
            (center_x + 10, cap_y + 7),
            (center_x - 4, cap_y + 6),
            (center_x + 4, cap_y + 11),
        ]
        
        for spot_x, spot_y in spots:
            for dy in range(2):
                for dx in range(2):
                    x = spot_x + dx
                    y = spot_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        display[y, x] = self.colors['spots']
        
        return display
    
    def display_mushroom(self, duration=10):
        """Display the mushroom for a specified duration."""
        print("Displaying mushroom pattern...")
        print(f"Display resolution: {self.width}x{self.height} pixels")
        print(f"Panel layout: {config.PANELS_COUNT} panels of {config.PANEL_WIDTH}x{config.PANEL_HEIGHT} each")
        
        # Create mushroom pattern
        mushroom = self.create_mushroom_pattern()
        
        # Display the pattern
        start_time = time.time()
        while time.time() - start_time < duration:
            # Copy pattern to LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = mushroom[y, x]
                    self.led.set_pixel(x, y, color)
            
            # Update display
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("Mushroom display completed!")
    
    def display_mushroom_animation(self, duration=15):
        """Display an animated mushroom (fade in/out, color cycling)."""
        print("Displaying animated mushroom...")
        
        mushroom = self.create_mushroom_pattern()
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create animated version with color cycling
            animated = mushroom.copy()
            
            # Add some animation effects
            t = time.time() - start_time
            
            # Color cycling effect on cap
            for y in range(self.height):
                for x in range(self.width):
                    if np.array_equal(mushroom[y, x], self.colors['cap']):
                        # Cycle through red, orange, yellow
                        hue = int((t * 50) % 360)
                        if hue < 120:
                            animated[y, x] = (255, int(255 * (hue / 120)), 0)  # Red to Orange
                        else:
                            animated[y, x] = (255, 255, int(255 * ((hue - 120) / 120)))  # Orange to Yellow
            
            # Display animated pattern
            for y in range(self.height):
                for x in range(self.width):
                    color = animated[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.1)
        
        print("Animated mushroom display completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run mushroom display."""
    try:
        mushroom = MushroomDisplayFixed()
        
        # Display static mushroom
        mushroom.display_mushroom(duration=5)
        
        # Display animated mushroom
        mushroom.display_mushroom_animation(duration=10)
        
        # Clean up
        mushroom.cleanup()
        
    except KeyboardInterrupt:
        print("\nMushroom display interrupted by user")
        mushroom.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        mushroom.cleanup()

if __name__ == "__main__":
    main() 