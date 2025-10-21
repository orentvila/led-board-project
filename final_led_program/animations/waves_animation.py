#!/usr/bin/env python3
"""
Waves Animation for LED Board
Features animated waves with flowing water effects
"""

import time
import numpy as np
import math
from .base_animation import BaseAnimation
import config

class WavesAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the waves animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'background': (0, 20, 40),        # Dark blue background
            'wave_crest': (100, 200, 255),    # Light blue wave crests
            'wave_body': (50, 150, 255),      # Medium blue wave body
            'wave_trough': (20, 80, 200),     # Dark blue wave troughs
            'foam': (200, 220, 255),          # White foam
            'sparkle': (255, 255, 255),       # White sparkles
        }
        
        # Wave parameters
        self.wave_amplitude = 8
        self.wave_frequency = 0.1
        self.wave_speed = 0.05
        self.time_offset = 0
        
        # Multiple wave layers
        self.waves = [
            {'amplitude': 6, 'frequency': 0.08, 'speed': 0.03, 'phase': 0},
            {'amplitude': 4, 'frequency': 0.12, 'speed': 0.05, 'phase': math.pi/3},
            {'amplitude': 3, 'frequency': 0.15, 'speed': 0.04, 'phase': math.pi/2},
        ]
        
        # Sparkle effects
        self.sparkles = []
        self.sparkle_timer = 0
    
    def generate_wave_height(self, x, t, wave_params):
        """Generate wave height at position x and time t."""
        amplitude = wave_params['amplitude']
        frequency = wave_params['frequency']
        speed = wave_params['speed']
        phase = wave_params['phase']
        
        # Sine wave with phase offset
        wave = amplitude * math.sin(frequency * x + speed * t + phase)
        return wave
    
    def get_wave_color(self, height, max_height):
        """Get color based on wave height."""
        if height > max_height * 0.8:
            return self.colors['wave_crest']
        elif height > max_height * 0.4:
            return self.colors['wave_body']
        else:
            return self.colors['wave_trough']
    
    def add_sparkles(self, frame, t):
        """Add sparkle effects to wave crests."""
        # Add new sparkles occasionally
        if len(self.sparkles) < 20 and np.random.random() < 0.1:
            x = np.random.randint(0, self.width)
            y = np.random.randint(self.height//2, self.height)
            self.sparkles.append({
                'x': x,
                'y': y,
                'life': 1.0,
                'brightness': np.random.uniform(0.5, 1.0)
            })
        
        # Update and draw sparkles
        for sparkle in self.sparkles[:]:
            sparkle['life'] -= 0.02
            if sparkle['life'] <= 0:
                self.sparkles.remove(sparkle)
            else:
                x, y = int(sparkle['x']), int(sparkle['y'])
                if 0 <= x < self.width and 0 <= y < self.height:
                    brightness = sparkle['brightness'] * sparkle['life']
                    color = tuple(int(c * brightness) for c in self.colors['sparkle'])
                    frame[y, x] = color
    
    def add_foam(self, frame, wave_heights):
        """Add foam effects to wave crests."""
        for x in range(self.width):
            if wave_heights[x] > 0:
                # Add foam at wave crests
                crest_y = int(self.height//2 + wave_heights[x])
                if 0 <= crest_y < self.height:
                    # Main foam
                    frame[crest_y, x] = self.colors['foam']
                    
                    # Additional foam particles
                    for dy in range(1, 3):
                        foam_y = crest_y - dy
                        if 0 <= foam_y < self.height and np.random.random() < 0.3:
                            frame[foam_y, x] = self.colors['foam']
    
    def create_waves_frame(self, t):
        """Create a single frame of the waves animation."""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Calculate combined wave heights
        wave_heights = np.zeros(self.width)
        for wave in self.waves:
            for x in range(self.width):
                height = self.generate_wave_height(x, t, wave)
                wave_heights[x] += height
        
        # Draw waves
        for x in range(self.width):
            wave_height = wave_heights[x]
            center_y = self.height // 2
            
            # Draw wave from center to top
            for y in range(center_y, self.height):
                # Calculate distance from wave center
                distance_from_center = y - center_y
                
                # Get color based on wave height and position
                if distance_from_center <= wave_height:
                    # Inside the wave
                    if distance_from_center > wave_height * 0.8:
                        color = self.colors['wave_crest']
                    elif distance_from_center > wave_height * 0.4:
                        color = self.colors['wave_body']
                    else:
                        color = self.colors['wave_trough']
                    
                    frame[y, x] = color
        
        # Add foam effects
        self.add_foam(frame, wave_heights)
        
        # Add sparkles
        self.add_sparkles(frame, t)
        
        return frame
    
    def run(self, duration=30):
        """Run the waves animation."""
        print(f"🌊 Starting Waves animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Calculate animation time
            t = time.time() - start_time
            
            # Create frame
            frame = self.create_waves_frame(t)
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            frame_count += 1
            time.sleep(0.1)  # 10 FPS
        
        print(f"🌊 Waves animation completed ({frame_count} frames)")
        self.cleanup()
