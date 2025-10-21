#!/usr/bin/env python3
"""
Star Animation for LED Board
Features twinkling stars and shooting stars
"""

import time
import numpy as np
import math
import random
from .base_animation import BaseAnimation
import config

class StarAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the star animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'space': (0, 0, 0),           # Black space
            'star_bright': (255, 255, 255), # Bright white stars
            'star_medium': (200, 200, 255), # Medium blue-white stars
            'star_dim': (150, 150, 200),   # Dim blue stars
            'shooting_trail': (255, 255, 150), # Shooting star trail
            'shooting_head': (255, 255, 255), # Shooting star head
        }
        
        # Animation parameters
        self.stars = []
        self.shooting_stars = []
        self.star_timer = 0
        
    def create_star_field(self):
        """Create a field of twinkling stars."""
        frame = np.full((self.height, self.width, 3), self.colors['space'], dtype=np.uint8)
        
        # Add twinkling stars
        for star in self.stars:
            if star['active']:
                x, y = star['position']
                brightness = star['brightness']
                
                # Create star with brightness
                if brightness > 0.8:
                    color = self.colors['star_bright']
                elif brightness > 0.5:
                    color = self.colors['star_medium']
                else:
                    color = self.colors['star_dim']
                
                # Draw star
                frame[y, x] = color
                
                # Add twinkle effect
                if random.random() < 0.1:
                    star['brightness'] = random.uniform(0.3, 1.0)
        
        # Add shooting stars
        for shooting_star in self.shooting_stars:
            if shooting_star['active']:
                x, y = shooting_star['position']
                trail_length = shooting_star['trail_length']
                
                # Draw trail
                for i in range(trail_length):
                    trail_x = x - i
                    trail_y = y - i
                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        if i == 0:
                            frame[trail_y, trail_x] = self.colors['shooting_head']
                        else:
                            # Fade trail
                            fade = 1.0 - (i / trail_length)
                            color = tuple(int(c * fade) for c in self.colors['shooting_trail'])
                            frame[trail_y, trail_x] = color
        
        return frame
    
    def update_stars(self):
        """Update star positions and properties."""
        # Update existing stars
        for star in self.stars:
            if star['active']:
                # Twinkle effect
                star['brightness'] += random.uniform(-0.1, 0.1)
                star['brightness'] = max(0.1, min(1.0, star['brightness']))
        
        # Add new stars occasionally
        if random.random() < 0.05 and len(self.stars) < 30:
            new_star = {
                'position': (random.randint(0, self.width-1), random.randint(0, self.height-1)),
                'brightness': random.uniform(0.3, 1.0),
                'active': True
            }
            self.stars.append(new_star)
        
        # Remove old stars occasionally
        if len(self.stars) > 25:
            for star in self.stars:
                if random.random() < 0.02:
                    star['active'] = False
            self.stars = [star for star in self.stars if star['active']]
    
    def update_shooting_stars(self):
        """Update shooting star positions."""
        # Update existing shooting stars
        for shooting_star in self.shooting_stars:
            if shooting_star['active']:
                x, y = shooting_star['position']
                x -= 2  # Move left
                y += 1  # Move down slightly
                
                shooting_star['position'] = (x, y)
                shooting_star['trail_length'] = min(8, shooting_star['trail_length'] + 1)
                
                # Remove if off screen
                if x < -10 or y > self.height + 10:
                    shooting_star['active'] = False
        
        # Add new shooting stars occasionally
        if random.random() < 0.02 and len(self.shooting_stars) < 3:
            new_shooting_star = {
                'position': (self.width + 5, random.randint(0, self.height//2)),
                'trail_length': 1,
                'active': True
            }
            self.shooting_stars.append(new_shooting_star)
        
        # Remove inactive shooting stars
        self.shooting_stars = [ss for ss in self.shooting_stars if ss['active']]
    
    def run(self, duration=30):
        """Run the star animation."""
        print(f"⭐ Starting Star animation for {duration} seconds...")
        
        # Initialize stars
        for _ in range(15):
            star = {
                'position': (random.randint(0, self.width-1), random.randint(0, self.height-1)),
                'brightness': random.uniform(0.3, 1.0),
                'active': True
            }
            self.stars.append(star)
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Update animation
            self.update_stars()
            self.update_shooting_stars()
            
            # Create frame
            frame = self.create_star_field()
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"⭐ Star animation completed ({frame_count} frames)")
        self.cleanup()
