#!/usr/bin/env python3
"""
Elephant Bitmap Animation for LED Board
Displays an elephant image from binary bitmap data
"""

import time
from led_controller_exact import LEDControllerExact
import config

class ElephantBitmapAnimation:
    def __init__(self):
        """Initialize the elephant bitmap animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Elephant bitmap data (32x48 pixels)
        # Format: 0xff = background, 0x00 = elephant pixels (inverted)
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xcf, 0xff,
            0xff, 0xff, 0x00, 0xff, 0xff, 0xe2, 0x00, 0x3f, 0xff, 0xc6, 0x00, 0x0f, 0xff, 0x86, 0x00, 0x07,
            0xff, 0x06, 0x04, 0x07, 0xfe, 0x02, 0x04, 0x07, 0xfe, 0x03, 0x04, 0x87, 0xfc, 0x01, 0x0c, 0x03,
            0xfc, 0x01, 0x88, 0x03, 0xfc, 0x00, 0xd8, 0x03, 0xfc, 0x00, 0x60, 0x03, 0xfc, 0x00, 0x00, 0x03,
            0xfe, 0x00, 0x03, 0x83, 0xfe, 0x00, 0x07, 0x83, 0xff, 0x00, 0x07, 0x87, 0xff, 0x00, 0x06, 0x07,
            0xff, 0x80, 0x0c, 0x07, 0xff, 0x87, 0x08, 0x0f, 0xff, 0x87, 0x0c, 0x1f, 0xff, 0x87, 0x0f, 0xff,
            0xff, 0x87, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to pixel array
        # This bitmap is inverted: 0xff = background, 0x00 = elephant pixel
        self.elephant_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                # Inverted: if bit is 0, pixel = 1 (elephant), if bit is 1, pixel = 0 (background)
                pixel = 1 if pixel_bit == 0 else 0
                row_data.append(pixel)
            self.elephant_pixels.append(row_data)
        
        # Colors
        self.elephant_color = (150, 150, 150)  # Grey for elephant
        self.ground_color = (34, 139, 34)  # Forest green ground (same as horse)
        
        # Animation settings
        self.ground_height = 4  # Height of ground at bottom (same as horse)
        self.ground_y = self.height - self.ground_height
        
        # Find elephant dimensions for proper positioning
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.elephant_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.elephant_actual_width = max_x - min_x + 1
        self.elephant_actual_height = max_y - min_y + 1
        self.elephant_offset_x = min_x
        self.elephant_offset_y = min_y
        
        print(f"🐘 Elephant dimensions: {self.elephant_actual_width}x{self.elephant_actual_height}, offset: ({self.elephant_offset_x}, {self.elephant_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_elephant(self, x_pos):
        """Draw the elephant bitmap at horizontal position x_pos."""
        # Position elephant vertically (feet touching ground) - same logic as horse
        ground_y = self.height - self.ground_height
        elephant_bottom_y = ground_y  # Feet on ground line
        vertical_offset = elephant_bottom_y - (self.elephant_offset_y + self.elephant_actual_height)
        
        # Draw elephant pixels
        for y in range(48):
            for x in range(32):
                if self.elephant_pixels[y][x] == 1:  # Elephant pixel
                    screen_x = x + x_pos - self.elephant_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if elephant is on or above ground and within screen bounds
                    # Allow drawing at ground level (screen_y <= ground_y) so elephant touches ground
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        self.safe_set_pixel(screen_x, screen_y, self.elephant_color)
    
    def run_animation(self, should_stop=None):
        """Run the elephant animation - moves from left to center, then stops."""
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🐘 Starting elephant animation...")
        
        # Animation parameters
        # Calculate center position: elephant should be centered when its center is at screen center
        center_x = self.width // 2
        target_x_pos = center_x - (self.elephant_actual_width // 2) - self.elephant_offset_x
        
        # Start position: off-screen left
        start_x_pos = -self.elephant_actual_width
        
        # Distance to travel to reach center
        travel_distance = target_x_pos - start_x_pos
        
        # Time to reach center (use first 8 seconds to move, then stay for remaining 12 seconds)
        move_duration = 8.0  # seconds to reach center
        speed = travel_distance / move_duration  # pixels per second
        
        # Draw first frame immediately to prevent blinking
        elapsed = 0
        if elapsed < move_duration:
            x_pos = int(start_x_pos + elapsed * speed)
        else:
            x_pos = target_x_pos
        
        self.led.clear()
        self.draw_ground()
        self.draw_elephant(x_pos)
        self.led.show()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐘 Elephant animation stopped by user")
                break
            
            # Calculate horizontal position
            # Move from left to center during first move_duration seconds
            # Then stay at center for the rest of the duration
            if elapsed < move_duration:
                # Moving phase: calculate position based on elapsed time
                x_pos = int(start_x_pos + elapsed * speed)
                # Clamp to target position to ensure we don't overshoot
                if x_pos > target_x_pos:
                    x_pos = target_x_pos
            else:
                # Stopped phase: stay at center
                x_pos = target_x_pos
            
            # Draw frame
            self.led.clear()
            self.draw_ground()
            self.draw_elephant(x_pos)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐘 Elephant animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run elephant bitmap animation."""
    try:
        animation = ElephantBitmapAnimation()
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

