#!/usr/bin/env python3
"""
Beating Heart Animation for LED Board
Soft red heart that slowly beats with no background
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class BeatingHeartAnimation:
    def __init__(self):
        """Initialize the beating heart animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Soft red colors for the heart
        self.heart_colors = {
            'main': (255, 100, 100),      # Soft red
            'bright': (255, 150, 150),    # Brighter red for beat
            'dim': (200, 80, 80),         # Dimmer red
        }
        
        # Animation parameters
        self.total_duration = 30.0  # 30 seconds
        self.animation_speed = 0.15  # Frame delay for slow beating
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_heart(self, center_x, center_y, size, beat_intensity=1.0):
        """Draw a heart shape at the given position with beat intensity."""
        # Calculate heart color based on beat intensity
        base_color = self.heart_colors['main']
        if beat_intensity > 0.8:
            color = self.heart_colors['bright']
        elif beat_intensity < 0.3:
            color = self.heart_colors['dim']
        else:
            # Interpolate between main and bright/dim
            if beat_intensity > 0.5:
                factor = (beat_intensity - 0.5) * 2
                color = (
                    int(base_color[0] + (self.heart_colors['bright'][0] - base_color[0]) * factor),
                    int(base_color[1] + (self.heart_colors['bright'][1] - base_color[1]) * factor),
                    int(base_color[2] + (self.heart_colors['bright'][2] - base_color[2]) * factor)
                )
            else:
                factor = beat_intensity * 2
                color = (
                    int(base_color[0] + (self.heart_colors['dim'][0] - base_color[0]) * (1 - factor)),
                    int(base_color[1] + (self.heart_colors['dim'][1] - base_color[1]) * (1 - factor)),
                    int(base_color[2] + (self.heart_colors['dim'][2] - base_color[2]) * (1 - factor))
                )
        
        # Draw heart shape using mathematical heart equation
        for dy in range(-int(size * 1.2), int(size * 1.2) + 1):
            for dx in range(-int(size * 1.2), int(size * 1.2) + 1):
                # Heart equation: (x² + y² - 1)³ - x²y³ ≤ 0
                x_norm = dx / size
                y_norm = dy / size
                
                # Heart equation
                heart_eq = (x_norm*x_norm + y_norm*y_norm - 1)**3 - x_norm*x_norm * y_norm*y_norm*y_norm
                
                if heart_eq <= 0:
                    self.safe_set_pixel(center_x + dx, center_y + dy, color)
    
    def run_animation(self):
        """Run the beating heart animation."""
        print("❤️ Starting beating heart animation...")
        
        start_time = time.time()
        
        # Heart position (center of screen)
        heart_x = self.width // 2
        heart_y = self.height // 2
        
        while time.time() - start_time < self.total_duration:
            # Clear display (no background)
            self.led.clear()
            
            # Calculate beat cycle (slow beating)
            beat_cycle = (time.time() - start_time) * 0.8  # Slow beat
            beat_intensity = (math.sin(beat_cycle) + 1) / 2  # 0 to 1
            
            # Calculate heart size with beat
            base_size = 8
            size_variation = math.sin(beat_cycle * 2) * 1.5  # Size changes with beat
            current_size = base_size + size_variation
            
            # Draw the beating heart
            self.draw_heart(heart_x, heart_y, current_size, beat_intensity)
            
            self.led.show()
            time.sleep(self.animation_speed)
        
        print("❤️ Beating heart animation completed!")

def main():
    """Main function to run the beating heart animation."""
    try:
        heart = BeatingHeartAnimation()
        heart.run_animation()
    except KeyboardInterrupt:
        print("\n❤️ Beating heart animation interrupted by user")
    except Exception as e:
        print(f"❌ Error in beating heart animation: {e}")
    finally:
        print("❤️ Cleaning up...")

if __name__ == "__main__":
    main()
