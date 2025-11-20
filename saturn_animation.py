#!/usr/bin/env python3
"""
Saturn Animation for LED Board
Features rotating rings, planet details, and sparkle effects
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class SaturnAnimation:
    def __init__(self):
        """Initialize the Saturn animation."""
        self.led = LEDControllerExact()
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
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_saturn(self, ring_angle=0):
        """Draw Saturn with rotating rings."""
        # Saturn position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Saturn planet body (round ball shape)
        planet_radius_x = 7
        planet_radius_y = 7  # Equal radii for perfect circle
        
        # Draw planet body
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / planet_radius_x
                dy = (y - center_y) / planet_radius_y
                if dx*dx + dy*dy <= 1:
                    # Add some banding to Saturn
                    if abs(dy) < 0.3:
                        self.safe_set_pixel(x, y, self.colors['saturn_dark'])  # Dark band
                    else:
                        self.safe_set_pixel(x, y, self.colors['saturn_body'])
        
        # Saturn rings (elliptical)
        ring_outer_x = 14
        ring_outer_y = 4
        ring_inner_x = 10
        ring_inner_y = 2
        
        # Rotate rings
        cos_a = math.cos(ring_angle)
        sin_a = math.sin(ring_angle)
        
        # Draw rings
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
                        self.safe_set_pixel(x, y, self.colors['rings_gold'])
                    else:
                        self.safe_set_pixel(x, y, self.colors['rings_dark'])
                    
                    # Add some variation
                    if abs(rx) < ring_inner_x * 0.8:
                        self.safe_set_pixel(x, y, self.colors['rings_light'])
        
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
                        # Get current pixel color (should be Saturn body color)
                        # Blend with shadow color
                        if abs(dy) < 0.3:
                            original = self.colors['saturn_dark']
                        else:
                            original = self.colors['saturn_body']
                        shadow = self.colors['shadow']
                        blended = tuple(int(0.7 * o + 0.3 * s) for o, s in zip(original, shadow))
                        self.safe_set_pixel(x, y, blended)
    
    def draw_stars(self):
        """Draw twinkling stars in the background."""
        import random
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
                self.safe_set_pixel(x, y, star_color)
        
        # Random sparkles
        if self.sparkle_timer % 20 == 0:
            sparkle_x = random.randint(0, self.width - 1)
            sparkle_y = random.randint(0, self.height - 1)
            self.safe_set_pixel(sparkle_x, sparkle_y, self.colors['sparkle'])
    
    def run_animation(self, should_stop=None):
        """Run the Saturn animation with stop callback support."""
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🪐 Starting Saturn animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🪐 Saturn animation stopped by user")
                break
            
            # Clear display
            self.led.clear()
            
            # Draw Saturn with rotating rings
            self.draw_saturn(self.ring_rotation)
            
            # Add stars and sparkles
            self.draw_stars()
            
            # Update display
            self.led.show()
            
            # Update animation parameters
            self.ring_rotation += 0.1  # Rotate rings
            self.sparkle_timer += 1
            self.star_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        # Fade out the Saturn animation smoothly
        print("🪐 Fading out Saturn animation...")
        fade_out_duration = 2  # 2 seconds fade-out
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🪐 Saturn animation stopped during fade-out")
                break
            
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_intensity = 1.0 - fade_progress  # Fade from 1.0 to 0.0
            
            # Clear display
            self.led.clear()
            
            # Draw Saturn with rotating rings (with fade-out)
            center_x = self.width // 2
            center_y = self.height // 2
            planet_radius_x = 7
            planet_radius_y = 7  # Equal radii for perfect circle
            
            # Draw planet body with fade-out
            for y in range(self.height):
                for x in range(self.width):
                    dx = (x - center_x) / planet_radius_x
                    dy = (y - center_y) / planet_radius_y
                    if dx*dx + dy*dy <= 1:
                        if abs(dy) < 0.3:
                            color = tuple(int(c * fade_intensity) for c in self.colors['saturn_dark'])
                        else:
                            color = tuple(int(c * fade_intensity) for c in self.colors['saturn_body'])
                        self.safe_set_pixel(x, y, color)
            
            # Draw rings with fade-out
            ring_outer_x = 14
            ring_outer_y = 4
            ring_inner_x = 10
            ring_inner_y = 2
            
            cos_a = math.cos(self.ring_rotation)
            sin_a = math.sin(self.ring_rotation)
            
            for y in range(self.height):
                for x in range(self.width):
                    dx = x - center_x
                    dy = y - center_y
                    rx = dx * cos_a - dy * sin_a
                    ry = dx * sin_a + dy * cos_a
                    
                    outer_dist = (rx / ring_outer_x)**2 + (ry / ring_outer_y)**2
                    inner_dist = (rx / ring_inner_x)**2 + (ry / ring_inner_y)**2
                    
                    if 0.8 <= outer_dist <= 1.2 and inner_dist >= 0.8:
                        angle = math.atan2(ry, rx)
                        section = int((angle + math.pi) / (math.pi / 6)) % 12
                        
                        if section < 6:
                            color = tuple(int(c * fade_intensity) for c in self.colors['rings_gold'])
                        else:
                            color = tuple(int(c * fade_intensity) for c in self.colors['rings_dark'])
                        
                        if abs(rx) < ring_inner_x * 0.8:
                            color = tuple(int(c * fade_intensity) for c in self.colors['rings_light'])
                        
                        self.safe_set_pixel(x, y, color)
            
            # Draw ring shadow on planet with fade-out
            for y in range(self.height):
                for x in range(self.width):
                    dx = (x - center_x) / planet_radius_x
                    dy = (y - center_y) / planet_radius_y
                    if dx*dx + dy*dy <= 1:
                        shadow_x = x - center_x
                        shadow_y = y - center_y
                        rx = shadow_x * cos_a - shadow_y * sin_a
                        ry = shadow_x * sin_a + shadow_y * sin_a
                        shadow_dist = (rx / ring_outer_x)**2 + (ry / ring_outer_y)**2
                        if 0.8 <= shadow_dist <= 1.2:
                            if abs(dy) < 0.3:
                                original = tuple(int(c * fade_intensity) for c in self.colors['saturn_dark'])
                            else:
                                original = tuple(int(c * fade_intensity) for c in self.colors['saturn_body'])
                            shadow = tuple(int(c * fade_intensity) for c in self.colors['shadow'])
                            blended = tuple(int(0.7 * o + 0.3 * s) for o, s in zip(original, shadow))
                            self.safe_set_pixel(x, y, blended)
            
            # Draw stars with fade-out
            star_positions = [
                (5, 5), (25, 8), (8, 15), (28, 12), (3, 25),
                (22, 30), (15, 35), (30, 35), (10, 38), (20, 38)
            ]
            
            for x, y in star_positions:
                if 0 <= x < self.width and 0 <= y < self.height:
                    twinkle = abs(math.sin(self.star_timer * 0.1 + x + y)) * 0.5 + 0.5
                    star_color = tuple(int(c * twinkle * fade_intensity) for c in self.colors['stars'])
                    self.safe_set_pixel(x, y, star_color)
            
            # Update display
            self.led.show()
            
            # Continue updating animation parameters during fade-out
            self.ring_rotation += 0.1
            self.sparkle_timer += 1
            self.star_timer += 1
            
            time.sleep(0.1)  # 10 FPS for smooth fade-out
        
        print("🪐 Saturn animation completed!")
        
        # Clear display completely
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run Saturn animation."""
    try:
        saturn = SaturnAnimation()
        saturn.run_animation()
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