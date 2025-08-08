#!/usr/bin/env python3
"""
Star Animation for LED Board
Features twinkling stars, shooting stars, constellations, and cosmic effects
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class StarAnimation:
    def __init__(self):
        """Initialize the star animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'space': (0, 0, 20),            # Deep space blue-black
            'star_white': (255, 255, 255),  # Bright white stars
            'star_yellow': (255, 255, 200), # Yellow stars
            'star_blue': (200, 200, 255),   # Blue stars
            'star_red': (255, 200, 200),    # Red stars
            'star_orange': (255, 220, 150), # Orange stars
            'shooting_star': (255, 255, 255), # Bright shooting star
            'shooting_trail': (100, 100, 150), # Shooting star trail
            'nebula_purple': (150, 100, 200), # Purple nebula
            'nebula_blue': (100, 150, 200),   # Blue nebula
            'nebula_pink': (200, 100, 150),   # Pink nebula
            'constellation': (150, 150, 200), # Constellation lines
            'moon': (240, 240, 250),         # Moon glow
            'aurora_green': (100, 255, 100), # Green aurora
            'aurora_blue': (100, 100, 255),  # Blue aurora
            'aurora_purple': (200, 100, 255) # Purple aurora
        }
        
        # Animation parameters
        self.time = 0
        self.shooting_stars = []
        self.constellation_timer = 0
        self.nebula_timer = 0
        self.aurora_timer = 0
        
        # Initialize shooting stars
        self.init_shooting_stars()
        
    def init_shooting_stars(self):
        """Initialize shooting stars."""
        self.shooting_stars = [
            {'x': -5, 'y': 5, 'dx': 2, 'dy': 1, 'life': 0, 'max_life': 20},
            {'x': -3, 'y': 15, 'dx': 1.5, 'dy': 0.8, 'life': 10, 'max_life': 25},
            {'x': -8, 'y': 25, 'dx': 2.5, 'dy': 1.2, 'life': 5, 'max_life': 18}
        ]
    
    def create_star_field(self, frame):
        """Create a field of twinkling stars."""
        # Fixed star positions for consistent constellations
        star_positions = [
            (5, 5), (25, 8), (8, 15), (28, 12), (3, 25),
            (22, 30), (15, 35), (30, 35), (10, 38), (20, 38),
            (12, 10), (18, 18), (6, 32), (26, 28), (14, 22),
            (24, 15), (4, 18), (16, 8), (28, 25), (2, 35),
            (20, 12), (8, 28), (26, 35), (12, 32), (22, 18)
        ]
        
        for i, (x, y) in enumerate(star_positions):
            if 0 <= x < self.width and 0 <= y < self.height:
                # Star twinkling effect
                twinkle = math.sin(self.time * 0.1 + i * 0.5) * 0.5 + 0.5
                
                # Different star colors
                if i % 5 == 0:
                    star_color = self.colors['star_white']
                elif i % 5 == 1:
                    star_color = self.colors['star_yellow']
                elif i % 5 == 2:
                    star_color = self.colors['star_blue']
                elif i % 5 == 3:
                    star_color = self.colors['star_red']
                else:
                    star_color = self.colors['star_orange']
                
                # Apply twinkling
                final_color = tuple(int(c * twinkle) for c in star_color)
                frame[y, x] = final_color
                
                # Add star glow for brighter stars
                if twinkle > 0.7:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            glow_x, glow_y = x + dx, y + dy
                            if (0 <= glow_x < self.width and 0 <= glow_y < self.height and 
                                (dx != 0 or dy != 0)):
                                glow_intensity = twinkle * 0.3 * (1 - (abs(dx) + abs(dy)) * 0.3)
                                current = frame[glow_y, glow_x]
                                frame[glow_y, glow_x] = tuple(int(c + (col - c) * glow_intensity) 
                                                            for c, col in zip(current, final_color))
    
    def create_shooting_stars(self, frame):
        """Create shooting stars with trails."""
        for star in self.shooting_stars:
            # Update star position
            star['x'] += star['dx']
            star['y'] += star['dy']
            star['life'] += 1
            
            # Draw shooting star trail
            trail_length = 8
            for i in range(trail_length):
                trail_x = int(star['x'] - star['dx'] * i)
                trail_y = int(star['y'] - star['dy'] * i)
                
                if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                    # Trail fades out
                    trail_intensity = 1 - (i / trail_length)
                    trail_intensity *= (star['max_life'] - star['life']) / star['max_life']
                    
                    if i == 0:  # Bright head
                        trail_color = self.colors['shooting_star']
                    else:  # Fading trail
                        trail_color = self.colors['shooting_trail']
                    
                    final_color = tuple(int(c * trail_intensity) for c in trail_color)
                    frame[trail_y, trail_x] = final_color
            
            # Reset shooting star when it goes off screen or dies
            if (star['x'] > self.width + 10 or star['y'] > self.height + 10 or 
                star['life'] > star['max_life']):
                star['x'] = np.random.randint(-10, -5)
                star['y'] = np.random.randint(0, self.height // 2)
                star['dx'] = np.random.uniform(1.5, 3.0)
                star['dy'] = np.random.uniform(0.5, 1.5)
                star['life'] = 0
                star['max_life'] = np.random.randint(15, 30)
    
    def create_constellations(self, frame):
        """Create constellation patterns."""
        # Big Dipper constellation
        big_dipper = [(5, 5), (8, 8), (12, 6), (15, 10), (18, 8), (20, 12), (22, 10)]
        
        # Draw constellation lines
        for i in range(len(big_dipper) - 1):
            x1, y1 = big_dipper[i]
            x2, y2 = big_dipper[i + 1]
            
            # Draw line between stars
            steps = max(abs(x2 - x1), abs(y2 - y1))
            if steps > 0:
                for step in range(int(steps) + 1):
                    t = step / steps
                    line_x = int(x1 + (x2 - x1) * t)
                    line_y = int(y1 + (y2 - y1) * t)
                    
                    if 0 <= line_x < self.width and 0 <= line_y < self.height:
                        # Constellation line with subtle glow
                        line_intensity = math.sin(self.constellation_timer * 0.1 + step) * 0.3 + 0.7
                        line_color = tuple(int(c * line_intensity) for c in self.colors['constellation'])
                        frame[line_y, line_x] = line_color
        
        # Orion's Belt
        orion = [(10, 20), (16, 20), (22, 20)]
        for i in range(len(orion) - 1):
            x1, y1 = orion[i]
            x2, y2 = orion[i + 1]
            
            steps = max(abs(x2 - x1), abs(y2 - y1))
            if steps > 0:
                for step in range(int(steps) + 1):
                    t = step / steps
                    line_x = int(x1 + (x2 - x1) * t)
                    line_y = int(y1 + (y2 - y1) * t)
                    
                    if 0 <= line_x < self.width and 0 <= line_y < self.height:
                        line_intensity = math.sin(self.constellation_timer * 0.15 + step) * 0.4 + 0.6
                        line_color = tuple(int(c * line_intensity) for c in self.colors['constellation'])
                        frame[line_y, line_x] = line_color
    
    def create_nebula_clouds(self, frame):
        """Create colorful nebula clouds."""
        nebula_centers = [
            (self.width // 4, self.height // 3),
            (3 * self.width // 4, 2 * self.height // 3),
            (self.width // 2, self.height // 4)
        ]
        
        for i, (cx, cy) in enumerate(nebula_centers):
            nebula_radius = 8 + math.sin(self.nebula_timer * 0.05 + i) * 2
            
            for y in range(self.height):
                for x in range(self.width):
                    distance = math.sqrt((x - cx)**2 + (y - cy)**2)
                    
                    if distance < nebula_radius:
                        # Nebula color based on position and time
                        color_phase = (self.nebula_timer * 0.02 + distance * 0.1) % (2 * math.pi)
                        
                        if color_phase < math.pi / 3:
                            nebula_color = self.colors['nebula_purple']
                        elif color_phase < 2 * math.pi / 3:
                            nebula_color = self.colors['nebula_blue']
                        else:
                            nebula_color = self.colors['nebula_pink']
                        
                        # Nebula intensity
                        intensity = 1 - (distance / nebula_radius)
                        intensity = max(0, intensity * 0.3)  # Subtle effect
                        
                        # Blend with existing frame
                        current = frame[y, x]
                        frame[y, x] = tuple(int(c + (n - c) * intensity) 
                                          for c, n in zip(current, nebula_color))
    
    def create_aurora_effect(self, frame):
        """Create aurora borealis effect."""
        for y in range(self.height):
            for x in range(self.width):
                # Aurora wave patterns
                aurora1 = math.sin((x + self.aurora_timer * 0.3) * 0.2) * 0.4
                aurora2 = math.sin((y + self.aurora_timer * 0.2) * 0.15) * 0.3
                aurora3 = math.sin((x - y + self.aurora_timer * 0.1) * 0.1) * 0.2
                
                aurora_intensity = (aurora1 + aurora2 + aurora3) / 3
                
                if aurora_intensity > 0.1:
                    # Aurora colors
                    color_phase = (self.aurora_timer * 0.05 + x * 0.1) % (2 * math.pi)
                    
                    if color_phase < math.pi / 3:
                        aurora_color = self.colors['aurora_green']
                    elif color_phase < 2 * math.pi / 3:
                        aurora_color = self.colors['aurora_blue']
                    else:
                        aurora_color = self.colors['aurora_purple']
                    
                    # Blend with existing frame
                    current = frame[y, x]
                    blend_factor = (aurora_intensity - 0.1) * 0.3
                    frame[y, x] = tuple(int(c + (a - c) * blend_factor) 
                                      for c, a in zip(current, aurora_color))
    
    def create_moon(self, frame):
        """Create a glowing moon."""
        moon_x = int(self.width * 0.8)
        moon_y = int(self.height * 0.2)
        moon_radius = 4
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - moon_x)**2 + (y - moon_y)**2)
                
                if distance < moon_radius:
                    # Moon glow
                    intensity = 1 - (distance / moon_radius)
                    intensity = max(0, intensity)
                    
                    moon_color = tuple(int(c * intensity) for c in self.colors['moon'])
                    
                    # Blend with existing frame
                    current = frame[y, x]
                    frame[y, x] = tuple(int(c + (m - c) * 0.6) 
                                      for c, m in zip(current, moon_color))
    
    def create_frame(self):
        """Create a complete star animation frame."""
        frame = np.full((self.height, self.width, 3), self.colors['space'], dtype=np.uint8)
        
        # Create scene elements
        self.create_nebula_clouds(frame)
        self.create_aurora_effect(frame)
        self.create_star_field(frame)
        self.create_constellations(frame)
        self.create_shooting_stars(frame)
        self.create_moon(frame)
        
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
            self.time += 1
            self.constellation_timer += 1
            self.nebula_timer += 1
            self.aurora_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Star animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run star animation."""
    try:
        stars = StarAnimation()
        stars.display_star_animation(30)
        stars.cleanup()
        
    except KeyboardInterrupt:
        print("\nStar animation interrupted by user")
        stars.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        stars.cleanup()

if __name__ == "__main__":
    main() 