#!/usr/bin/env python3
"""
Fire Animation for LED Board
Simple fire effect that looks great
"""

import time
import random
from .base_animation import BaseAnimation
import config

class FireAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the fire animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Fire colors
        self.colors = {
            'hot': (255, 100, 0),      # Orange-red
            'warm': (255, 150, 0),     # Orange
            'cool': (255, 200, 100),   # Yellow-orange
            'ember': (100, 50, 0),     # Dark red
            'spark': (255, 255, 255),  # White spark
        }
        
        # Fire parameters
        self.fire_intensity = 0.8
        self.spark_chance = 0.1
        
    def create_fire_frame(self):
        """Create a fire frame."""
        # Clear the display
        self.led.clear()
        
        # Create fire from bottom to top
        for y in range(self.height):
            for x in range(self.width):
                # Fire intensity decreases with height
                height_factor = y / self.height
                intensity = self.fire_intensity * (1 - height_factor)
                
                # Add randomness
                noise = random.random() * 0.3
                total_intensity = intensity + noise
                
                # Choose color based on intensity
                if total_intensity > 0.8:
                    color = self.colors['hot']
                elif total_intensity > 0.6:
                    color = self.colors['warm']
                elif total_intensity > 0.4:
                    color = self.colors['cool']
                elif total_intensity > 0.2:
                    color = self.colors['ember']
                else:
                    color = (0, 0, 0)  # Black
                
                # Add sparks occasionally
                if random.random() < self.spark_chance:
                    color = self.colors['spark']
                
                self.led.set_pixel(x, y, color)
    
    def run(self, duration=30):
        """Run the fire animation."""
        print(f"🔥 Starting Fire animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Create frame
            self.create_fire_frame()
            self.led.show()
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🔥 Fire animation completed ({frame_count} frames)")
        self.cleanup()
