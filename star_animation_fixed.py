#!/usr/bin/env python3
"""
Star Animation for LED Board - Fixed Version
Features twinkling stars, shooting stars, and cosmic effects
"""

import time
import numpy as np
import math
import random
from led_controller_exact import LEDControllerExact
import config

class StarAnimationFixed:
    def __init__(self):
        """Initialize the star animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Colors
        self.colors = {
            'space': (0, 0, 0),           # Black space
            'star_bright': (255, 255, 255), # Bright white stars
            'star_medium': (200, 200, 255), # Medium blue-white stars
            'star_dim': (150, 150, 200),   # Dim blue stars
            'shooting_trail': (255, 255, 150), # Shooting star trail
            'shooting_head': (255, 255, 255), # Shooting star head
            'nebula': (100, 50, 150),     # Purple nebula
            'aurora': (0, 255, 100),      # Green aurora
        }
        
        # Animation parameters
        self.stars = []
        self.shooting_stars = []
        self.star_timer = 0
        self.aurora_timer = 0
        
        # Initialize star field
        self._create_star_field()
        
    def _create_star_field(self):
        """Create a field of twinkling stars."""
        # Create 25 fixed stars in various positions
        for _ in range(25):
            star = {
                'x': random.randint(0, self.width - 1),
                'y': random.randint(0, self.height - 1),
                'brightness': random.uniform(0.3, 1.0),
                'twinkle_speed': random.uniform(0.05, 0.15),
                'twinkle_phase': random.uniform(0, 2 * math.pi),
                'color_type': random.choice(['bright', 'medium', 'dim'])
            }
            self.stars.append(star)
    
    def create_star_field(self, frame):
        """Create a field of twinkling stars."""
        # Add twinkling stars
        for star in self.stars:
            x, y = star['x'], star['y']
            brightness = star['brightness']
            
            # Twinkling effect
            twinkle = math.sin(self.star_timer * star['twinkle_speed'] + star['twinkle_phase']) * 0.3 + 0.7
            final_brightness = brightness * twinkle
            
            # Choose star color based on type
            if star['color_type'] == 'bright':
                base_color = self.colors['star_bright']
            elif star['color_type'] == 'medium':
                base_color = self.colors['star_medium']
            else:
                base_color = self.colors['star_dim']
            
            # Apply brightness
            color = tuple(int(c * final_brightness) for c in base_color)
            
            # Set pixel if within bounds
            if 0 <= x < self.width and 0 <= y < self.height:
                frame[y, x] = color
    
    def create_shooting_stars(self, frame):
        """Create shooting stars with trails."""
        # Add new shooting stars occasionally
        if random.random() < 0.02:  # 2% chance per frame
            shooting_star = {
                'x': random.randint(0, self.width - 1),
                'y': 0,  # Start from top
                'trail_length': random.randint(3, 8),
                'speed': random.uniform(0.5, 1.5),
                'life': 1.0
            }
            self.shooting_stars.append(shooting_star)
        
        # Update existing shooting stars
        for shooting_star in self.shooting_stars[:]:
            # Move shooting star
            shooting_star['y'] += shooting_star['speed']
            shooting_star['life'] -= 0.05
            
            # Remove if off screen or dead
            if shooting_star['y'] >= self.height or shooting_star['life'] <= 0:
                self.shooting_stars.remove(shooting_star)
                continue
            
            # Draw trail
            trail_length = int(shooting_star['trail_length'] * shooting_star['life'])
            for i in range(trail_length):
                trail_y = int(shooting_star['y'] - i)
                if 0 <= trail_y < self.height:
                    # Trail gets dimmer towards the end
                    trail_brightness = (trail_length - i) / trail_length
                    trail_color = tuple(int(c * trail_brightness) for c in self.colors['shooting_trail'])
                    frame[trail_y, shooting_star['x']] = trail_color
            
            # Draw head
            if 0 <= shooting_star['y'] < self.height:
                frame[shooting_star['y'], shooting_star['x']] = self.colors['shooting_head']
    
    def create_constellations(self, frame):
        """Create constellation patterns."""
        # Big Dipper
        big_dipper = [
            (5, 5), (8, 3), (12, 4), (15, 2), (18, 6), (20, 8), (22, 10)
        ]
        
        for x, y in big_dipper:
            if 0 <= x < self.width and 0 <= y < self.height:
                frame[y, x] = self.colors['star_bright']
        
        # Orion's Belt
        orion_belt = [
            (10, 15), (15, 16), (20, 17)
        ]
        
        for x, y in orion_belt:
            if 0 <= x < self.width and 0 <= y < self.height:
                frame[y, x] = self.colors['star_medium']
    
    def create_nebula_clouds(self, frame):
        """Create nebula clouds."""
        # Add some nebula effects
        for _ in range(3):
            center_x = random.randint(5, self.width - 5)
            center_y = random.randint(5, self.height - 5)
            radius = random.randint(3, 8)
            
            for y in range(max(0, center_y - radius), min(self.height, center_y + radius)):
                for x in range(max(0, center_x - radius), min(self.width, center_x + radius)):
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if distance <= radius:
                        # Fade nebula color based on distance
                        fade = 1 - (distance / radius) * 0.7
                        nebula_color = tuple(int(c * fade) for c in self.colors['nebula'])
                        
                        # Blend with existing color
                        current = frame[y, x]
                        if not np.array_equal(current, self.colors['space']):
                            blended = tuple(int(c + (n - c) * 0.3) for c, n in zip(current, nebula_color))
                            frame[y, x] = blended
                        else:
                            frame[y, x] = nebula_color
    
    def create_aurora_effect(self, frame):
        """Create aurora borealis effect."""
        # Create flowing aurora patterns
        for x in range(self.width):
            # Create wave pattern
            wave = math.sin(x * 0.3 + self.aurora_timer * 0.1) * 3
            aurora_y = int(self.height * 0.3 + wave)
            
            # Draw aurora line
            for y in range(max(0, aurora_y - 2), min(self.height, aurora_y + 2)):
                if 0 <= y < self.height:
                    # Fade aurora color
                    fade = 1 - abs(y - aurora_y) / 2
                    aurora_color = tuple(int(c * fade) for c in self.colors['aurora'])
                    
                    # Blend with existing color
                    current = frame[y, x]
                    if not np.array_equal(current, self.colors['space']):
                        blended = tuple(int(c + (a - c) * 0.4) for c, a in zip(current, aurora_color))
                        frame[y, x] = blended
                    else:
                        frame[y, x] = aurora_color
    
    def create_frame(self):
        """Create a single frame of the star animation."""
        # Start with black space
        frame = np.full((self.height, self.width, 3), self.colors['space'], dtype=np.uint8)
        
        # Add nebula clouds
        self.create_nebula_clouds(frame)
        
        # Add star field
        self.create_star_field(frame)
        
        # Add constellations
        self.create_constellations(frame)
        
        # Add shooting stars
        self.create_shooting_stars(frame)
        
        # Add aurora effect
        self.create_aurora_effect(frame)
        
        return frame
    
    def display_star_animation(self, duration=30):
        """Display the star animation."""
        print("⭐ Star Animation ⭐")
        print(f"Displaying for {duration} seconds...")
        print("Features: Twinkling stars, shooting stars, constellations, nebula, aurora")
        
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
            self.star_timer += 1
            self.aurora_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Star animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run star animation."""
    try:
        star = StarAnimationFixed()
        star.display_star_animation(30)
        star.cleanup()
        
    except KeyboardInterrupt:
        print("\nStar animation interrupted by user")
        star.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        star.cleanup()

if __name__ == "__main__":
    main()
