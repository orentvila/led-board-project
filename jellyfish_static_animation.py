#!/usr/bin/env python3
"""
Jellyfish Static Image for LED Board
Displays a static jellyfish image for 5 seconds
"""

import time
from led_controller_exact import LEDControllerExact
import config

class JellyfishStaticAnimation:
    def __init__(self):
        """Initialize the jellyfish static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.jellyfish_color = (255, 255, 255)  # White for jellyfish outline
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_jellyfish(self):
        """Draw a simple jellyfish - bell at top, tentacles below."""
        self.led.clear()  # Black background
        
        center_x = self.width // 2
        bell_y = 10
        
        # Bell - dome shape, wider than tall
        import math
        bell_radius_x = 8
        bell_radius_y = 6
        
        for angle in range(0, 180, 3):  # Top half of ellipse
            rad = math.radians(angle)
            x = int(center_x + bell_radius_x * math.cos(rad))
            y = int(bell_y + bell_radius_y * math.sin(rad))
            self.safe_set_pixel(x, y, self.jellyfish_color)
        
        # Bell bottom curve
        for x in range(center_x - bell_radius_x, center_x + bell_radius_x + 1):
            y = bell_y + bell_radius_y
            self.safe_set_pixel(x, y, self.jellyfish_color)
        
        # Internal curved line in bell
        inner_y = bell_y + 2
        for x in range(center_x - 5, center_x + 6):
            self.safe_set_pixel(x, inner_y, self.jellyfish_color)
        
        # Tentacles - four wavy lines
        tentacle_start_y = bell_y + bell_radius_y + 1
        tentacle_xs = [center_x - 4, center_x - 1, center_x + 2, center_x + 5]
        
        for tentacle_x in tentacle_xs:
            current_y = tentacle_start_y
            current_x = tentacle_x
            wave_offset = 0
            
            for i in range(12):
                self.safe_set_pixel(current_x, current_y, self.jellyfish_color)
                current_y += 1
                # Wave effect
                wave_offset += 0.3
                current_x = tentacle_x + int(math.sin(wave_offset) * 1.5)
                if current_x < 0 or current_x >= self.width:
                    current_x = tentacle_x
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the jellyfish static image.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 5  # 5 seconds
        start_time = time.time()
        
        print("🪼 Starting jellyfish static image...")
        
        self.draw_jellyfish()
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🪼 Jellyfish image stopped by user")
                break
            time.sleep(0.1)
        
        print("🪼 Jellyfish image completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

