#!/usr/bin/env python3
"""
Bubbles Animation for LED Board
Features floating bubbles with realistic physics
"""

import time
import numpy as np
import math
import random
from .base_animation import BaseAnimation
import config

class BubblesAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the bubbles animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'water': (0, 20, 40),         # Dark blue water
            'bubble': (150, 200, 255),    # Light blue bubbles
            'bubble_highlight': (200, 220, 255), # Bubble highlights
            'bubble_shadow': (100, 150, 200), # Bubble shadows
        }
        
        # Animation parameters
        self.bubbles = []
        self.bubble_timer = 0
        
    def create_bubbles_frame(self):
        """Create a frame with floating bubbles."""
        frame = np.full((self.height, self.width, 3), self.colors['water'], dtype=np.uint8)
        
        # Draw bubbles
        for bubble in self.bubbles:
            if bubble['active']:
                x, y = bubble['position']
                radius = bubble['radius']
                
                # Draw bubble
                self.draw_bubble(frame, int(x), int(y), radius, bubble['opacity'])
        
        return frame
    
    def draw_bubble(self, frame, x, y, radius, opacity):
        """Draw a single bubble with highlight and shadow."""
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    pixel_x = x + dx
                    pixel_y = y + dy
                    
                    if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                        # Calculate distance from center
                        distance = math.sqrt(dx * dx + dy * dy)
                        
                        # Create bubble effect with highlight
                        if distance <= radius * 0.3:
                            # Highlight
                            color = self.colors['bubble_highlight']
                        elif distance <= radius * 0.8:
                            # Main bubble
                            color = self.colors['bubble']
                        else:
                            # Edge shadow
                            color = self.colors['bubble_shadow']
                        
                        # Apply opacity
                        final_color = tuple(int(c * opacity) for c in color)
                        frame[pixel_y, pixel_x] = final_color
    
    def update_bubbles(self):
        """Update bubble positions and properties."""
        # Update existing bubbles
        for bubble in self.bubbles:
            if bubble['active']:
                # Move bubble up
                x, y = bubble['position']
                y -= bubble['speed']
                
                # Add slight horizontal drift
                x += random.uniform(-0.2, 0.2)
                
                bubble['position'] = (x, y)
                bubble['age'] += 1
                
                # Remove bubbles that are off screen or too old
                if y < -bubble['radius'] or bubble['age'] > 200:
                    bubble['active'] = False
        
        # Add new bubbles occasionally
        if random.random() < 0.1 and len(self.bubbles) < 8:
            new_bubble = {
                'position': (random.randint(2, self.width-2), self.height + 5),
                'radius': random.randint(2, 4),
                'speed': random.uniform(0.5, 1.5),
                'opacity': random.uniform(0.6, 1.0),
                'age': 0,
                'active': True
            }
            self.bubbles.append(new_bubble)
        
        # Remove inactive bubbles
        self.bubbles = [bubble for bubble in self.bubbles if bubble['active']]
    
    def run(self, duration=30):
        """Run the bubbles animation."""
        print(f"🫧 Starting Bubbles animation for {duration} seconds...")
        
        # Initialize some bubbles
        for _ in range(3):
            bubble = {
                'position': (random.randint(2, self.width-2), random.randint(0, self.height)),
                'radius': random.randint(2, 4),
                'speed': random.uniform(0.5, 1.5),
                'opacity': random.uniform(0.6, 1.0),
                'age': random.randint(0, 50),
                'active': True
            }
            self.bubbles.append(bubble)
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Update animation
            self.update_bubbles()
            
            # Create frame
            frame = self.create_bubbles_frame()
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🫧 Bubbles animation completed ({frame_count} frames)")
        self.cleanup()
