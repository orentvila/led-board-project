#!/usr/bin/env python3
"""
Horse Animation for LED Board
Shows a horse animation based on pixel art pattern
"""

import time
from led_controller_exact import LEDControllerExact
import config

class HorseAnimation:
    def __init__(self):
        """Initialize the horse animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Simple pixel-art horse pattern (approx. 16x16 centered on screen)
        # 0 = background, 1 = body, 2 = mane
        self.horse_pattern = [
            "0000000111000000",
            "0000001111100000",
            "0000011111110000",
            "0000111111111000",
            "0001111111111100",
            "0001111111111100",
            "0011111111111110",
            "0011111111111110",
            "0011111111111110",
            "0001111111111100",
            "0000111111111000",
            "0000111111111000",
            "0000011111110000",
            "0000001111100000",
            "0000000111000000",
            "0000000010000000",
        ]
        
        # Define horse colors
        self.body_color = (255, 180, 40)  # Soft yellow-orange
        self.mane_color = (255, 230, 120)  # Light yellow
        self.bg_color = (0, 0, 0)  # Black background
    
    def draw_horse(self, brightness_scale=1.0):
        """Draw the horse pattern with optional brightness scaling."""
        # Clear background
        self.led.clear()
        
        # Center horse
        start_x = (self.width - len(self.horse_pattern[0])) // 2
        start_y = (self.height - len(self.horse_pattern)) // 2
        
        for y, row in enumerate(self.horse_pattern):
            for x, pixel in enumerate(row):
                if pixel == "1":
                    r, g, b = self.body_color
                elif pixel == "2":
                    r, g, b = self.mane_color
                else:
                    continue
                
                # Apply brightness scaling
                r = int(r * brightness_scale)
                g = int(g * brightness_scale)
                b = int(b * brightness_scale)
                
                # Set pixel
                pixel_x = start_x + x
                pixel_y = start_y + y
                
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    self.led.set_pixel(pixel_x, pixel_y, (r, g, b))
        
        self.led.show()
    
    def fade_in_out(self, should_stop=None):
        """Fade in, hold, then fade out the horse."""
        steps = 50
        
        # Fade in (2 seconds)
        for i in range(steps):
            if should_stop and should_stop():
                print("🐴 Horse animation stopped during fade in")
                return
            
            brightness = i / steps
            self.draw_horse(brightness)
            time.sleep(2.0 / steps)
        
        # Hold 3 seconds
        hold_start = time.time()
        while time.time() - hold_start < 3.0:
            if should_stop and should_stop():
                print("🐴 Horse animation stopped during hold")
                return
            time.sleep(0.1)
        
        # Fade out (2 seconds)
        for i in range(steps, -1, -1):
            if should_stop and should_stop():
                print("🐴 Horse animation stopped during fade out")
                return
            
            brightness = i / steps
            self.draw_horse(brightness)
            time.sleep(2.0 / steps)
    
    def run_animation(self, should_stop=None):
        """Run the horse animation with fade in/out cycle.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds total
        start_time = time.time()
        
        print("🐴 Starting horse animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse animation stopped by user")
                break
            
            # Run fade in/out cycle
            self.fade_in_out(should_stop)
            
            # Small pause between cycles
            if should_stop and should_stop():
                break
            time.sleep(0.5)
        
        print("🐴 Horse animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run horse animation."""
    try:
        animation = HorseAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()

