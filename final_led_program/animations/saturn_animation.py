#!/usr/bin/env python3
"""
Saturn Animation for LED Board
Features rotating rings, planet details, and sparkle effects
"""

import time
import numpy as np
import math
from .base_animation import BaseAnimation
import config

class SaturnAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the Saturn animation."""
        super().__init__(led_controller)
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
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                
                # Check if pixel is within Saturn's body
                if (dx * dx) / (planet_radius_x * planet_radius_x) + (dy * dy) / (planet_radius_y * planet_radius_y) <= 1:
                    # Add some banding to Saturn
                    band = int((y - center_y + planet_radius_y) / (2 * planet_radius_y) * 3)
                    if band % 2 == 0:
                        frame[y, x] = self.colors['saturn_body']
                    else:
                        frame[y, x] = self.colors['saturn_dark']
        
        # Draw rings
        self.draw_rings(frame, center_x, center_y, ring_angle)
        
        # Add stars
        self.add_stars(frame)
        
        # Add sparkles
        self.add_sparkles(frame)
        
        return frame
    
    def draw_rings(self, frame, center_x, center_y, angle):
        """Draw Saturn's rings at the given angle."""
        # Ring parameters
        inner_radius = 10
        outer_radius = 16
        
        for y in range(self.height):
            for x in range(self.width):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx * dx + dy * dy)
                
                if inner_radius <= distance <= outer_radius:
                    # Calculate angle for ring position
                    pixel_angle = math.atan2(dy, dx)
                    ring_angle = (pixel_angle - angle) % (2 * math.pi)
                    
                    # Create ring pattern
                    ring_section = int(ring_angle / (math.pi / 4)) % 4
                    
                    if ring_section == 0:
                        frame[y, x] = self.colors['rings_gold']
                    elif ring_section == 1:
                        frame[y, x] = self.colors['rings_light']
                    elif ring_section == 2:
                        frame[y, x] = self.colors['rings_dark']
                    else:
                        frame[y, x] = self.colors['rings_gold']
    
    def add_stars(self, frame):
        """Add twinkling stars to the background."""
        # Create star positions based on time
        star_count = 20
        for i in range(star_count):
            # Use time-based seed for consistent star positions
            seed = (i * 12345 + int(time.time() * 2)) % 10000
            x = seed % self.width
            y = (seed // 100) % self.height
            
            # Only add stars in empty space
            if np.array_equal(frame[y, x], self.colors['space']):
                # Twinkling effect
                twinkle = int(time.time() * 3 + i) % 3
                if twinkle == 0:
                    frame[y, x] = self.colors['stars']
    
    def add_sparkles(self, frame):
        """Add sparkle effects to the rings."""
        sparkle_count = 5
        for i in range(sparkle_count):
            seed = (i * 54321 + int(time.time() * 4)) % 10000
            x = seed % self.width
            y = (seed // 100) % self.height
            
            # Add sparkles near rings
            if 8 <= x <= 24 and 20 <= y <= 28:
                frame[y, x] = self.colors['sparkle']
    
    def run(self, duration=30):
        """Run the Saturn animation."""
        print(f"🪐 Starting Saturn animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Create frame
            frame = self.create_saturn_frame(self.ring_rotation)
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.ring_rotation += 0.1
            if self.ring_rotation >= 2 * math.pi:
                self.ring_rotation = 0
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🪐 Saturn animation completed ({frame_count} frames)")
        self.cleanup()
