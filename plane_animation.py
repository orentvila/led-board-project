#!/usr/bin/env python3
"""
Plane Animation for LED Board
Displays a plane image from binary bitmap data
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class PlaneAnimation:
    def __init__(self):
        """Initialize the plane animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Plane bitmap data (32x48 pixels)
        # Each byte represents 8 horizontal pixels (MSB first)
        # 32 pixels per row = 4 bytes per row
        # 48 rows total = 192 bytes
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xfd, 0xff, 0xff, 0x32, 0xf6, 0xff, 0xff, 0xf9, 0x6b, 0xff, 0xfe, 0x1f, 0xdd, 0xff,
            0xff, 0xc7, 0xbb, 0xff, 0xff, 0xf1, 0x77, 0xff, 0xff, 0xfc, 0xe7, 0xff, 0xff, 0xff, 0xdb, 0xff,
            0xff, 0xff, 0xbd, 0xff, 0xff, 0xff, 0x9b, 0xff, 0xff, 0x7f, 0xdd, 0xff, 0xfe, 0xeb, 0xcd, 0xff,
            0xff, 0x97, 0xed, 0xff, 0xff, 0xef, 0xe5, 0xff, 0xff, 0xef, 0xf7, 0xff, 0xff, 0x7b, 0xf3, 0xff,
            0xfe, 0xf7, 0xf9, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to 32x48 pixel array (INVERTED)
        # Each byte has 8 bits, MSB first (bit 7 is leftmost pixel)
        # 32 pixels per row = 4 bytes per row
        self.plane_pixels = []
        
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
            self.plane_pixels.append(row_data)
        
        # Colors - improved color scheme
        self.plane_color = (255, 255, 255)  # Bright white for plane body
        self.plane_accent = (200, 220, 255)  # Light blue for highlights
        self.sky_color = (30, 60, 100)  # Dark blue sky background
        self.cloud_color = (40, 80, 120)  # Slightly lighter for subtle sky gradient
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_plane(self, brightness=1.0, frame=0):
        """Draw the plane from the bitmap data with improved visuals.
        
        Args:
            brightness: Brightness multiplier (0.0 to 1.0)
            frame: Animation frame number for subtle effects
        """
        self.led.clear()
        
        # Draw sky background with subtle gradient
        for y in range(self.height):
            # Sky gradient: darker at top, slightly lighter at bottom
            gradient_factor = y / self.height
            sky_r = int(self.sky_color[0] * (1.0 + gradient_factor * 0.2))
            sky_g = int(self.sky_color[1] * (1.0 + gradient_factor * 0.2))
            sky_b = int(self.sky_color[2] * (1.0 + gradient_factor * 0.2))
            for x in range(self.width):
                self.safe_set_pixel(x, y, (sky_r, sky_g, sky_b))
        
        # Draw plane with enhanced appearance
        plane_y_offset = 0  # Can animate this later if needed
        for y in range(min(self.height, 48)):
            for x in range(min(self.width, 32)):
                if self.plane_pixels[y][x] == 1:
                    # Main plane body
                    px = x
                    py = y + plane_y_offset
                    
                    if 0 <= px < self.width and 0 <= py < self.height:
                        # Determine color based on position (subtle variation)
                        # Center/main body gets brightest white
                        # Edges get slightly tinted for depth
                        dist_from_center_x = abs(px - self.width // 2)
                        dist_from_center_y = abs(py - self.height // 2)
                        
                        # Bright white for main body, slight blue tint for edges
                        if dist_from_center_x < 12 and dist_from_center_y < 20:
                            # Main body - bright white
                            color = self.plane_color
                        else:
                            # Edges/wings - subtle blue tint
                            color = self.plane_accent
                        
                        # Apply brightness
                        r = int(color[0] * brightness)
                        g = int(color[1] * brightness)
                        b = int(color[2] * brightness)
                        
                        self.safe_set_pixel(px, py, (r, g, b))
                        
                        # Add subtle outline/glow effect for better visibility
                        # Draw slightly dimmed pixels around the plane edges
                        for dy in [-1, 0, 1]:
                            for dx in [-1, 0, 1]:
                                if dx == 0 and dy == 0:
                                    continue
                                nx, ny = px + dx, py + dy
                                if 0 <= nx < self.width and 0 <= ny < self.height:
                                    # Check if this is just outside the plane
                                    check_y = ny - plane_y_offset
                                    if check_y < 0 or check_y >= 48 or nx >= 32:
                                        # Outside bitmap bounds, add subtle glow
                                        glow_r = min(255, int(self.sky_color[0] + r * 0.15))
                                        glow_g = min(255, int(self.sky_color[1] + g * 0.15))
                                        glow_b = min(255, int(self.sky_color[2] + b * 0.15))
                                        self.safe_set_pixel(nx, ny, (glow_r, glow_g, glow_b))
                                    elif self.plane_pixels[check_y][nx] == 0:
                                        # This is sky next to plane, add subtle glow
                                        glow_r = min(255, int(self.sky_color[0] + r * 0.15))
                                        glow_g = min(255, int(self.sky_color[1] + g * 0.15))
                                        glow_b = min(255, int(self.sky_color[2] + b * 0.15))
                                        self.safe_set_pixel(nx, ny, (glow_r, glow_g, glow_b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the plane animation with subtle effects.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("✈️ Starting plane animation...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("✈️ Plane animation stopped by user")
                break
            
            # Subtle pulsing brightness effect (very gentle)
            elapsed = time.time() - start_time
            pulse = 0.9 + 0.1 * (1.0 + math.sin(elapsed * 2.0)) / 2.0  # 0.9 to 1.0
            
            self.draw_plane(brightness=pulse, frame=frame)
            frame += 1
            time.sleep(0.1)  # 10 FPS
        
        print("✈️ Plane animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run plane animation."""
    try:
        animation = PlaneAnimation()
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

