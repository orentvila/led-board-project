#!/usr/bin/env python3
"""
Birds Bitmap Animation for LED Board
Displays birds with animated wing flapping motion
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class BirdsStaticAnimationBitmap:
    def __init__(self):
        """Initialize the birds bitmap static animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH
        self.height = config.TOTAL_HEIGHT
        
        # Birds bitmap data (32x48 pixels)
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf8, 0xff, 0xff, 0xff, 0xfe, 0x3f, 0xff,
            0xff, 0xff, 0x9e, 0x3f, 0xff, 0xff, 0xc1, 0xff, 0xff, 0xff, 0xe3, 0xff, 0xff, 0xfd, 0xf7, 0xff,
            0xff, 0xf3, 0xff, 0xff, 0xff, 0xef, 0xff, 0xff, 0xff, 0xdf, 0xff, 0xff, 0xf8, 0x9f, 0xff, 0xff,
            0xfe, 0x3f, 0xff, 0xff, 0xff, 0x3c, 0xff, 0xff, 0xff, 0xfe, 0x7f, 0xff, 0xff, 0xff, 0x3b, 0xff,
            0xff, 0xff, 0x87, 0xff, 0xff, 0xff, 0xcf, 0xff, 0xff, 0xff, 0xdf, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xc7, 0xff, 0xff, 0xff, 0xef, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        self.birds_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                row_data.append(1 - pixel)
            self.birds_pixels.append(row_data)
        
        self.birds_color = (255, 255, 255)
        
        # Find bird body center and wing regions
        # Analyze pixels to identify body vs wings
        self.body_center_x = 16  # Approximate center of 32-wide display
        self.wing_animation_amplitude = 1  # Pixels to move wings up/down
        self.wing_flap_speed = 4.0  # Flaps per second
        
    def safe_set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def is_wing_pixel(self, x, y):
        """Determine if a pixel is part of a wing (not body).
        Wings are typically pixels on the sides, away from center."""
        # Calculate distance from center
        center_x = self.body_center_x
        distance_from_center = abs(x - center_x)
        
        # Pixels far from center are likely wings
        # Also check if pixel is in upper/middle region (where wings typically are)
        if y < 30:  # Upper/middle region where wings are
            # If pixel is more than 3 pixels from center, it's likely a wing
            if distance_from_center > 3:
                return True
        return False
    
    def draw_birds(self, wing_phase=0.0):
        """Draw birds with animated wing flapping.
        
        Args:
            wing_phase: Animation phase (0.0 to 1.0) for wing flapping
        """
        self.led.clear()
        
        # Calculate wing offset based on phase
        # Use sine wave: -1 to +1, so wings go up and down
        wing_offset = math.sin(wing_phase * 2 * math.pi) * self.wing_animation_amplitude
        
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.birds_pixels[y][x] == 1:
                    # Check if this is a wing pixel
                    if self.is_wing_pixel(x, y):
                        # Apply vertical offset to wing pixels
                        wing_y = int(y + wing_offset)
                        if 0 <= wing_y < self.height:
                            self.safe_set_pixel(x, wing_y, self.birds_color)
                    else:
                        # Body pixel - draw at original position
                        self.safe_set_pixel(x, y, self.birds_color)
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        duration = 5
        start_time = time.time()
        print("🐦 Starting birds animation with wing flapping...")
        
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("🐦 Birds animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            
            # Calculate wing flapping phase (0.0 to 1.0 cycles)
            wing_phase = (elapsed * self.wing_flap_speed) % 1.0
            
            # Draw birds with animated wings
            self.draw_birds(wing_phase)
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐦 Birds animation completed!")
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        self.led.cleanup()

