#!/usr/bin/env python3
"""
Saturn Animation for LED Board
Features rotating rings, planet details, and sparkle effects
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class SaturnAnimation:
    def __init__(self):
        """Initialize the Saturn animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'space': (0, 0, 0),           # Black space
            'saturn_body': (255, 200, 100), # Golden Saturn
            'saturn_dark': (200, 150, 80),  # Darker Saturn bands
            'rings_gold': (255, 215, 0),    # Golden rings
            'rings_light': (255, 235, 100), # Light ring sections
            'rings_dark': (180, 140, 60),   # Dark ring sections
            'stars': (255, 255, 255),       # White stars
            'sparkle': (255, 255, 200),     # Sparkle effect
            'shadow': (50, 30, 20)          # Ring shadow on planet
        }
        
        # Animation parameters
        self.ring_rotation = 0
        self.sparkle_timer = 0
        self.star_timer = 0
        
    def create_saturn_frame(self, ring_angle=0):
        """Create a single frame of Saturn with rotating rings."""
        frame = np.full((self.height, self.width, 3), self.colors['space'], dtype=np.uint8)
        
        # Saturn position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Saturn planet body (oval shape)
        planet_radius_x = 8
        planet_radius_y = 6
        
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / planet_radius_x
                dy = (y - center_y) / planet_radius_y
                if dx*dx + dy*dy <= 1:
                    # Add some banding to Saturn
                    if abs(dy) < 0.3:
                        frame[y, x] = self.colors['saturn_dark']  # Dark band
                    else:
                        frame[y, x] = self.colors['saturn_body']
        
        # Saturn rings (elliptical)
        ring_outer_x = 14
        ring_outer_y = 4
        ring_inner_x = 10
        ring_inner_y = 2
        
        # Rotate rings
        cos_a = math.cos(ring_angle)
        sin_a = math.sin(ring_angle)
        
        for y in range(self.height):
            for x in range(self.width):
                # Transform coordinates for rotation
                dx = x - center_x
                dy = y - center_y
                
                # Apply rotation
                rx = dx * cos_a - dy * sin_a
                ry = dx * sin_a + dy * cos_a
                
                # Check if point is in ring area
                outer_dist = (rx / ring_outer_x)**2 + (ry / ring_outer_y)**2
                inner_dist = (rx / ring_inner_x)**2 + (ry / ring_inner_y)**2
                
                if 0.8 <= outer_dist <= 1.2 and inner_dist >= 0.8:
                    # Ring pattern - alternating light and dark sections
                    angle = math.atan2(ry, rx)
                    section = int((angle + math.pi) / (math.pi / 6)) % 12
                    
                    if section < 6:
                        frame[y, x] = self.colors['rings_gold']
                    else:
                        frame[y, x] = self.colors['rings_dark']
                    
                    # Add some variation
                    if abs(rx) < ring_inner_x * 0.8:
                        frame[y, x] = self.colors['rings_light']
        
        # Ring shadow on planet
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / planet_radius_x
                dy = (y - center_y) / planet_radius_y
                if dx*dx + dy*dy <= 1:
                    # Check if this point is shadowed by rings
                    shadow_x = x - center_x
                    shadow_y = y - center_y
                    
                    # Apply same rotation as rings
                    rx = shadow_x * cos_a - shadow_y * sin_a
                    ry = shadow_x * sin_a + shadow_y * sin_a
                    
                    shadow_dist = (rx / ring_outer_x)**2 + (ry / ring_outer_y)**2
                    if 0.8 <= shadow_dist <= 1.2:
                        # Blend with shadow color
                        original = frame[y, x]
                        shadow = self.colors['shadow']
                        frame[y, x] = tuple(int(0.7 * o + 0.3 * s) for o, s in zip(original, shadow))
        
        return frame
    
    def add_stars(self, frame):
        """Add twinkling stars to the background."""
        # Static stars
        star_positions = [
            (5, 5), (25, 8), (8, 15), (28, 12), (3, 25),
            (22, 30), (15, 35), (30, 35), (10, 38), (20, 38)
        ]
        
        for x, y in star_positions:
            if 0 <= x < self.width and 0 <= y < self.height:
                # Twinkling effect
                twinkle = abs(math.sin(self.star_timer * 0.1 + x + y)) * 0.5 + 0.5
                star_color = tuple(int(c * twinkle) for c in self.colors['stars'])
                frame[y, x] = star_color
        
        # Random sparkles
        if self.sparkle_timer % 20 == 0:
            sparkle_x = np.random.randint(0, self.width)
            sparkle_y = np.random.randint(0, self.height)
            if 0 <= sparkle_x < self.width and 0 <= sparkle_y < self.height:
                frame[sparkle_y, sparkle_x] = self.colors['sparkle']
    
    def display_saturn_animation(self, duration=15):
        """Display the Saturn animation."""
        print("🪐 Saturn Animation 🪐")
        print(f"Displaying for {duration} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create Saturn frame with rotating rings
            frame = self.create_saturn_frame(self.ring_rotation)
            
            # Add stars and sparkles
            self.add_stars(frame)
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.ring_rotation += 0.1  # Rotate rings
            self.sparkle_timer += 1
            self.star_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Saturn animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run Saturn animation."""
    try:
        saturn = SaturnAnimation()
        saturn.display_saturn_animation(15)
        saturn.cleanup()
        
    except KeyboardInterrupt:
        print("\nSaturn animation interrupted by user")
        saturn.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        saturn.cleanup()

if __name__ == "__main__":
    main() 