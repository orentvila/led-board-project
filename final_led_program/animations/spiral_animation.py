#!/usr/bin/env python3
"""
Spiral Animation for LED Board
Simple spiral effect that looks great
"""

import time
import math
from .base_animation import BaseAnimation
import config

class SpiralAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the spiral animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black
            'spiral': (0, 255, 255),         # Cyan
            'trail': (0, 200, 200),          # Light cyan
        }
        
        # Animation parameters
        self.angle = 0
        self.radius = 0
        self.max_radius = min(self.width, self.height) // 2
        self.speed = 0.1
        
    def create_spiral_frame(self):
        """Create a spiral frame."""
        # Clear the display
        self.led.clear()
        
        # Calculate center
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Create spiral
        for i in range(100):  # Number of spiral points
            # Calculate spiral coordinates
            x = int(center_x + self.radius * math.cos(self.angle))
            y = int(center_y + self.radius * math.sin(self.angle))
            
            # Check bounds
            if 0 <= x < self.width and 0 <= y < self.height:
                # Create trail effect
                for trail in range(3):
                    trail_x = x + trail
                    trail_y = y + trail
                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        if trail == 0:
                            self.led.set_pixel(trail_x, trail_y, self.colors['spiral'])
                        else:
                            self.led.set_pixel(trail_x, trail_y, self.colors['trail'])
            
            # Update spiral parameters
            self.angle += 0.2
            self.radius += 0.1
            
            # Reset when spiral gets too big
            if self.radius > self.max_radius:
                self.radius = 0
                self.angle = 0
    
    def run(self, duration=30):
        """Run the spiral animation."""
        print(f"🌀 Starting Spiral animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Create frame
            self.create_spiral_frame()
            self.led.show()
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🌀 Spiral animation completed ({frame_count} frames)")
        self.cleanup()
