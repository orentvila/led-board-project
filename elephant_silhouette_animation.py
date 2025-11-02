#!/usr/bin/env python3
"""
Elephant Silhouette Animation for LED Board
Shows a large, simple elephant silhouette
"""

import time
from led_controller_exact import LEDControllerExact
import config

class ElephantSilhouetteAnimation:
    def __init__(self):
        """Initialize the elephant silhouette animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors - simple silhouette
        self.elephant_color = (255, 255, 255)  # Bright white for maximum visibility
        self.bg_color = (0, 0, 0)  # Black background
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def create_elephant_silhouette(self):
        """Create a large elephant silhouette (up to 30x46 pixels)."""
        # Clear display
        self.led.clear()
        
        # Elephant silhouette pattern (30x46 pixels max)
        # Using pixel art approach for cleaner, solid silhouette
        # Center at (16, 24) with pattern starting at (1, 1) to use up to 30x46
        
        # Define the elephant as a series of filled horizontal bands
        # This ensures a solid, clean silhouette
        
        center_x = self.width // 2  # 16
        start_y = 1  # Top of elephant
        
        # Head and ears section (rows 1-14, ~46 pixels tall total)
        # Top of ears (rows 1-3)
        for y in range(start_y, start_y + 3):
            # Left ear
            for x in range(center_x - 13, center_x - 9):
                self.safe_set_pixel(x, y, self.elephant_color)
            # Right ear
            for x in range(center_x + 9, center_x + 13):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Ears getting wider (rows 4-8)
        for y in range(start_y + 3, start_y + 8):
            # Left ear expanding
            ear_width = min(7, (y - start_y - 2))
            for x in range(center_x - 13, center_x - 13 + ear_width):
                self.safe_set_pixel(x, y, self.elephant_color)
            # Right ear expanding
            for x in range(center_x + 13 - ear_width, center_x + 13):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Head section (rows 9-12)
        for y in range(start_y + 8, start_y + 12):
            # Head width about 18 pixels
            for x in range(center_x - 9, center_x + 9):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Body section - largest part (rows 13-28, width ~24-28 pixels)
        for y in range(start_y + 12, start_y + 28):
            # Body widest in middle
            if y < start_y + 20:
                body_width = 26 + (y - start_y - 12) // 2  # Expanding
            else:
                body_width = 28 - (y - start_y - 20) // 2  # Tapering
            body_width = min(28, max(24, body_width))
            start_x = center_x - body_width // 2
            for x in range(start_x, start_x + body_width):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Trunk section (rows 12-32, extending down from head)
        trunk_start_y = start_y + 10
        trunk_end_y = start_y + 32
        for y in range(trunk_start_y, trunk_end_y + 1):
            progress = (y - trunk_start_y) / (trunk_end_y - trunk_start_y)
            # Trunk starts wide (5 pixels) and tapers to 2 pixels
            trunk_width = max(2, int(5 - progress * 3))
            # Trunk curves slightly left at bottom
            trunk_offset = int(-progress * 3)  # Curves left
            trunk_x = center_x + trunk_offset
            for x in range(trunk_x - trunk_width // 2, trunk_x + trunk_width // 2 + 1):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Legs section (rows 28-44)
        leg_y_start = start_y + 28
        leg_y_end = min(start_y + 44, self.height - 2)
        leg_width = 4
        
        # Front left leg
        for y in range(leg_y_start, leg_y_end + 1):
            for x in range(center_x - 9, center_x - 9 + leg_width):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Front right leg (between front and back)
        for y in range(leg_y_start, leg_y_end + 1):
            for x in range(center_x - 4, center_x - 4 + leg_width):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Back left leg
        for y in range(leg_y_start, leg_y_end + 1):
            for x in range(center_x + 1, center_x + 1 + leg_width):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Back right leg
        for y in range(leg_y_start, leg_y_end + 1):
            for x in range(center_x + 6, center_x + 6 + leg_width):
                self.safe_set_pixel(x, y, self.elephant_color)
        
        # Tail (rows 20-25, on right side)
        tail_y_start = start_y + 20
        tail_y_end = start_y + 25
        tail_base_x = center_x + 12
        for y in range(tail_y_start, tail_y_end + 1):
            tail_width = max(2, 4 - (y - tail_y_start))
            for x in range(tail_base_x, tail_base_x + tail_width):
                self.safe_set_pixel(x, y, self.elephant_color)
    
    def run_animation(self, should_stop=None):
        """Run the elephant silhouette animation.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐘 Starting elephant silhouette animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🐘 Elephant animation stopped by user")
                break
            
            self.create_elephant_silhouette()
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print("🐘 Elephant animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run elephant silhouette animation."""
    try:
        animation = ElephantSilhouetteAnimation()
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

