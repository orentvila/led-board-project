#!/usr/bin/env python3
"""
Rainbow Animation for LED Board
Simple, reliable rainbow effect that looks great
"""

import time
import math
from .base_animation import BaseAnimation
import config

class RainbowAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the rainbow animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Animation parameters
        self.hue_offset = 0
        self.speed = 0.02
        
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB."""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def create_rainbow_frame(self):
        """Create a rainbow frame."""
        # Clear the display
        self.led.clear()
        
        # Create rainbow pattern
        for y in range(self.height):
            for x in range(self.width):
                # Calculate hue based on position and time
                hue = (x * 10 + y * 5 + self.hue_offset) % 360
                color = self.hsv_to_rgb(hue, 1.0, 1.0)
                self.led.set_pixel(x, y, color)
    
    def run(self, duration=30):
        """Run the rainbow animation."""
        print(f"🌈 Starting Rainbow animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            # Create frame
            self.create_rainbow_frame()
            self.led.show()
            
            # Update hue offset
            self.hue_offset += self.speed
            
            frame_count += 1
            time.sleep(0.05)  # 20 FPS
        
        print(f"🌈 Rainbow animation completed ({frame_count} frames)")
        self.cleanup()
