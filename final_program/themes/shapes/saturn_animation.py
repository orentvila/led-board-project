#!/usr/bin/env python3
"""
Saturn Circling Animation for Shapes Theme
Pin 18 - Shapes Theme
"""

import time
import math
import sys
import os

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from led_controller import LEDController
import config

class SaturnAnimation:
    def __init__(self, led_controller):
        """Initialize Saturn animation."""
        self.led = led_controller
        self.running = False
        self.duration = 30  # 30 seconds default
        
    def run(self, duration=30):
        """Run the Saturn circling animation."""
        self.duration = duration
        self.running = True
        start_time = time.time()
        
        print(f"🪐 Starting Saturn animation for {duration} seconds...")
        
        # Animation parameters
        center_x = config.TOTAL_WIDTH // 2
        center_y = config.TOTAL_HEIGHT // 2
        saturn_radius = 8
        ring_radius = 12
        orbit_radius = min(center_x - 15, center_y - 10)
        
        angle = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Clear display
            self.led.clear()
            
            # Calculate Saturn position in orbit
            orbit_x = center_x + orbit_radius * math.cos(angle)
            orbit_y = center_y + orbit_radius * math.sin(angle)
            
            # Draw Saturn
            self.draw_saturn(int(orbit_x), int(orbit_y), saturn_radius, ring_radius, angle)
            
            # Draw stars in background
            self.draw_stars(angle)
            
            # Update display
            self.led.show()
            
            # Increment angle for smooth rotation
            angle += 0.1
            
            # Small delay for smooth animation
            time.sleep(0.05)
        
        # Clear at end
        self.led.clear()
        self.led.show()
        print("🪐 Saturn animation completed")
    
    def draw_saturn(self, x, y, planet_radius, ring_radius, rotation_angle):
        """Draw Saturn with rings at position (x, y)."""
        # Draw planet body (circle)
        self.draw_circle(x, y, planet_radius, config.COLORS['YELLOW'])
        
        # Draw rings (ellipse)
        self.draw_ring(x, y, ring_radius, rotation_angle)
    
    def draw_circle(self, center_x, center_y, radius, color):
        """Draw a filled circle."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    x = center_x + dx
                    y = center_y + dy
                    if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                        self.led.set_pixel(x, y, color)
    
    def draw_ring(self, center_x, center_y, radius, rotation_angle):
        """Draw Saturn's rings."""
        ring_color = config.COLORS['ORANGE']
        
        # Draw outer ring
        for angle in range(0, 360, 5):
            rad = math.radians(angle + rotation_angle)
            x = center_x + radius * math.cos(rad)
            y = center_y + radius * math.sin(rad) * 0.3  # Flatten the ring
            
            if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                self.led.set_pixel(int(x), int(y), ring_color)
        
        # Draw inner ring
        inner_radius = radius * 0.7
        for angle in range(0, 360, 8):
            rad = math.radians(angle + rotation_angle)
            x = center_x + inner_radius * math.cos(rad)
            y = center_y + inner_radius * math.sin(rad) * 0.3
            
            if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                self.led.set_pixel(int(x), int(y), ring_color)
    
    def draw_stars(self, angle):
        """Draw twinkling stars in background."""
        star_positions = [
            (5, 5), (25, 8), (8, 20), (28, 15), (12, 35),
            (30, 25), (3, 30), (20, 40), (15, 10), (35, 35)
        ]
        
        for x, y in star_positions:
            # Twinkling effect
            twinkle = math.sin(angle * 2 + x + y) * 0.5 + 0.5
            if twinkle > 0.7:  # Only show bright stars
                brightness = int(255 * twinkle)
                star_color = (brightness, brightness, brightness)
                if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                    self.led.set_pixel(x, y, star_color)
    
    def stop(self):
        """Stop the animation."""
        self.running = False

def main():
    """Test the Saturn animation."""
    print("🪐 Testing Saturn Animation")
    
    try:
        led = LEDController()
        saturn = SaturnAnimation(led)
        saturn.run(duration=10)  # Test for 10 seconds
        led.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
