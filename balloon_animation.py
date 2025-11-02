#!/usr/bin/env python3
"""
Flying Balloon Animation for LED Board
Displays a hot air balloon image from binary bitmap data
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class BalloonAnimation:
    def __init__(self):
        """Initialize the balloon animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Balloon bitmap data (32x48 pixels)
        # Each byte represents 8 horizontal pixels (MSB first)
        # 32 pixels per row = 4 bytes per row
        # 48 rows total = 192 bytes
        bitmap_hex = [
            0x00, 0x3f, 0xc0, 0x0f, 0x01, 0xf0, 0xf8, 0x0f, 0x07, 0x60, 0x6e, 0x0f, 0x0c, 0xc0, 0x33, 0x0f,
            0x18, 0x80, 0x10, 0x8f, 0x30, 0x80, 0x18, 0x4f, 0x20, 0x80, 0x08, 0x6f, 0x41, 0x80, 0x08, 0x2f,
            0x41, 0x00, 0x08, 0x2f, 0xc1, 0x00, 0x08, 0x3f, 0x81, 0x00, 0x08, 0x1f, 0x81, 0x00, 0x08, 0x1f,
            0x81, 0x00, 0x08, 0x1f, 0x81, 0x00, 0x08, 0x1f, 0x81, 0x00, 0x08, 0x1f, 0x81, 0x00, 0x08, 0x1f,
            0xc1, 0x00, 0x08, 0x3f, 0x41, 0x00, 0x08, 0x3f, 0x41, 0x80, 0x08, 0x2f, 0x61, 0x80, 0x08, 0x2f,
            0x20, 0x80, 0x08, 0x6f, 0x20, 0x80, 0x18, 0x4f, 0x30, 0x80, 0x10, 0x4f, 0x10, 0x80, 0x10, 0x8f,
            0x18, 0xc0, 0x31, 0x8f, 0x0c, 0x40, 0x21, 0x0f, 0x04, 0x40, 0x23, 0x0f, 0x06, 0x60, 0x62, 0x0f,
            0x03, 0x20, 0x4c, 0x0f, 0x01, 0xb0, 0xd8, 0x0f, 0x00, 0xd0, 0x90, 0x0f, 0x00, 0xf9, 0xf0, 0x0f,
            0x00, 0x80, 0x10, 0x0f, 0x00, 0xff, 0xf0, 0x0f, 0x00, 0x00, 0x00, 0x0f, 0x00, 0x00, 0x00, 0x0f,
            0x00, 0x00, 0x00, 0x0f, 0x00, 0xff, 0xf0, 0x0f, 0x01, 0xff, 0xf8, 0x0f, 0x01, 0xff, 0xf8, 0x0f,
            0x00, 0x80, 0x10, 0x0f, 0x00, 0x80, 0x00, 0x0f, 0x00, 0x80, 0x00, 0x0f, 0x00, 0x80, 0x00, 0x0f,
            0x00, 0x80, 0x00, 0x0f, 0x00, 0x80, 0x00, 0x0f, 0x00, 0x80, 0x00, 0x0f, 0x00, 0xff, 0xf0, 0x0f
        ]
        
        # Convert bitmap to 32x48 pixel array (INVERTED for better visibility)
        # Each byte has 8 bits, MSB first (bit 7 is leftmost pixel)
        # 32 pixels per row = 4 bytes per row
        self.balloon_pixels = []
        
        for row in range(48):
            row_data = []
            byte_start = row * 4  # 4 bytes per row
            for col in range(32):
                byte_index = byte_start + (col // 8)  # Which byte in the row
                bit_index = 7 - (col % 8)  # MSB first (bit 7 is leftmost pixel)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                # INVERT: 1 becomes 0, 0 becomes 1
                row_data.append(1 - pixel)
            self.balloon_pixels.append(row_data)
        
        # Colors - vibrant balloon colors
        self.balloon_color_1 = (255, 100, 100)  # Red
        self.balloon_color_2 = (100, 100, 255)  # Blue
        self.balloon_color_3 = (255, 200, 100)  # Orange/Yellow
        self.basket_color = (150, 100, 50)  # Brown basket
        self.ropes_color = (200, 200, 200)  # Gray ropes
        self.sky_color = (135, 206, 250)  # Sky blue background
        self.cloud_color = (255, 255, 255)  # White clouds
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def get_balloon_color(self, x, y):
        """Get color for balloon pixel based on position (striped pattern)."""
        # Top part of balloon (rows 0-20) - colorful stripes
        if y < 20:
            # Vertical stripes pattern
            stripe_width = 4
            stripe_index = (x // stripe_width) % 3
            if stripe_index == 0:
                return self.balloon_color_1  # Red
            elif stripe_index == 1:
                return self.balloon_color_2  # Blue
            else:
                return self.balloon_color_3  # Orange/Yellow
        # Bottom part (rows 20-28) - similar pattern
        elif y < 28:
            stripe_width = 3
            stripe_index = (x // stripe_width) % 3
            if stripe_index == 0:
                return self.balloon_color_1
            elif stripe_index == 1:
                return self.balloon_color_2
            else:
                return self.balloon_color_3
        # Basket area (rows 28-32)
        elif y < 32:
            return self.basket_color
        # Ropes (rows 32-48)
        else:
            return self.ropes_color
    
    def draw_balloon(self, brightness=1.0, frame=0):
        """Draw the balloon from the bitmap data - no background.
        
        Args:
            brightness: Brightness multiplier (0.0 to 1.0)
            frame: Animation frame number for subtle effects
        """
        self.led.clear()  # Black background
        
        # Draw only the balloon - no background
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.balloon_pixels[y][x] == 1:
                    # Get appropriate color for this part of balloon
                    color = self.get_balloon_color(x, y)
                    
                    # Apply brightness
                    r = int(color[0] * brightness)
                    g = int(color[1] * brightness)
                    b = int(color[2] * brightness)
                    
                    self.safe_set_pixel(x, y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the balloon animation with subtle floating effect.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("🎈 Starting balloon animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🎈 Balloon animation stopped by user")
                break
            
            # Subtle floating effect - gentle brightness pulse
            elapsed = time.time() - start_time
            pulse = 0.9 + 0.1 * (1.0 + math.sin(elapsed * 1.5)) / 2.0  # 0.9 to 1.0
            
            self.draw_balloon(brightness=pulse, frame=frame)
            frame += 1
            time.sleep(0.1)  # 10 FPS
        
        print("🎈 Balloon animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run balloon animation."""
    try:
        animation = BalloonAnimation()
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

