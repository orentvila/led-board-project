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
        
        # Convert bitmap to 32x48 pixel array
        # Each byte has 8 bits, MSB first (bit 7 is leftmost pixel)
        # 32 pixels per row = 4 bytes per row
        # Bit value 1 = balloon pixel (draw), Bit value 0 = background (don't draw)
        self.balloon_pixels = []
        
        for row in range(48):
            row_data = []
            byte_start = row * 4  # 4 bytes per row
            for col in range(32):
                byte_index = byte_start + (col // 8)  # Which byte in the row
                bit_index = 7 - (col % 8)  # MSB first (bit 7 is leftmost pixel)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                # NO INVERSION: 1 = balloon pixel, 0 = background
                row_data.append(pixel)
            self.balloon_pixels.append(row_data)
        
        # Colors - match the image design
        self.teal_color = (100, 200, 180)  # Light teal/turquoise for outer panels
        self.pale_yellow = (255, 255, 200)  # Pale yellow/cream for center panel and basket
        self.black_outline = (0, 0, 0)  # Black for outlines (handled by bitmap)
        self.basket_color = (255, 255, 200)  # Pale yellow/cream basket (same as center)
        
        # Scaling factor - make balloon smaller (0.75 = 75% size)
        self.scale_factor = 0.75
        self.scaled_width = int(32 * self.scale_factor)  # 24 pixels
        self.scaled_height = int(48 * self.scale_factor)  # 36 pixels
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def get_balloon_color(self, x, y, original_y, original_x):
        """Get color for balloon pixel based on position (three vertical panels).
        
        Args:
            x: Scaled x coordinate
            y: Scaled y coordinate (for display)
            original_y: Original y coordinate from bitmap (for color selection)
            original_x: Original x coordinate from bitmap (for panel selection)
        """
        # Three vertical panels: left (teal), center (pale yellow), right (teal)
        # Center panel is wider - roughly 12 pixels, side panels are ~10 pixels each
        left_panel_width = 10
        center_panel_width = 12
        
        # Determine which panel based on original_x position
        if original_x < left_panel_width:
            # Left panel - teal
            return self.teal_color
        elif original_x < left_panel_width + center_panel_width:
            # Center panel - pale yellow
            return self.pale_yellow
        else:
            # Right panel - teal
            return self.teal_color
    
    def draw_balloon(self, brightness=1.0, y_offset=0):
        """Draw the balloon from the bitmap data - scaled down and positioned.
        
        Args:
            brightness: Brightness multiplier (0.0 to 1.0)
            y_offset: Vertical offset for flying animation (negative moves up)
        """
        self.led.clear()  # Black background
        
        # Calculate center position
        center_x = self.width // 2
        balloon_left = center_x - self.scaled_width // 2
        
        # Track the actual maximum x coordinate we draw to
        max_display_x = -1
        
        # Draw scaled balloon - only draw pixels that exist in the bitmap
        for orig_y in range(48):
            for orig_x in range(32):
                if self.balloon_pixels[orig_y][orig_x] == 1:
                    # Calculate scaled position
                    scaled_x = int(orig_x * self.scale_factor)
                    scaled_y = int(orig_y * self.scale_factor)
                    
                    # Center horizontally and apply y_offset for flying
                    display_x = balloon_left + scaled_x
                    display_y = scaled_y + y_offset
                    
                    # Track maximum x for cleanup
                    if display_x > max_display_x:
                        max_display_x = display_x
                    
                    # Only draw if within screen bounds
                    if 0 <= display_x < self.width and 0 <= display_y < self.height:
                        # Determine color based on position
                        # For basket/ropes area (rows 28-48), use pale yellow
                        if orig_y >= 28:
                            color = self.pale_yellow
                        else:
                            # Get color based on three-panel design
                            color = self.get_balloon_color(scaled_x, scaled_y, orig_y, orig_x)
                        
                        # Apply brightness
                        r = int(color[0] * brightness)
                        g = int(color[1] * brightness)
                        b = int(color[2] * brightness)
                        
                        self.safe_set_pixel(display_x, display_y, (r, g, b))
        
        # Explicitly turn off all pixels to the right of the balloon
        # Use the maximum x we actually drew, plus a small margin for safety
        right_boundary = max_display_x + 1 if max_display_x >= 0 else balloon_left + self.scaled_width
        
        # Clear everything to the right of the balloon
        for y in range(self.height):
            for x in range(right_boundary, self.width):
                self.safe_set_pixel(x, y, (0, 0, 0))
        
        # Also clear everything to the left of the balloon
        for y in range(self.height):
            for x in range(balloon_left):
                self.safe_set_pixel(x, y, (0, 0, 0))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the balloon animation flying upward.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("🎈 Starting balloon animation...")
        
        # Animation: balloon starts at bottom, flies up once over 20 seconds
        # Start from bottom (completely below screen) to top (completely above screen)
        start_y_offset = self.height + self.scaled_height  # Start below screen
        end_y_offset = -self.scaled_height  # End above screen
        total_distance = start_y_offset - end_y_offset
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🎈 Balloon animation stopped by user")
                break
            
            elapsed = time.time() - start_time
            
            # Calculate y_offset for flying up - single cycle over full duration
            # Progress from 0.0 (start) to 1.0 (end)
            progress = min(1.0, elapsed / duration)
            
            # Linear interpolation from start to end
            y_offset = int(start_y_offset - progress * total_distance)
            
            # Subtle brightness pulse
            pulse = 0.9 + 0.1 * (1.0 + math.sin(elapsed * 1.5)) / 2.0  # 0.9 to 1.0
            
            self.draw_balloon(brightness=pulse, y_offset=y_offset)
            frame += 1
            time.sleep(0.05)  # 20 FPS for smoother animation
        
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

