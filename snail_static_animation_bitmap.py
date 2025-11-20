#!/usr/bin/env python3
"""
Snail Animation for LED Board
Displays a snail moving from left to right on light green ground with sun and clouds
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class SnailStaticAnimationBitmap:
    def __init__(self):
        """Initialize the snail animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH
        self.height = config.TOTAL_HEIGHT
        
        # Snail bitmap data (32x48 pixels)
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x20, 0x00, 0x00, 0x01, 0x20, 0x00, 0x7f, 0x01, 0x20,
            0x00, 0xe1, 0xc1, 0xe0, 0x01, 0x80, 0x61, 0xc0, 0x03, 0x00, 0x23, 0xe0, 0x06, 0x38, 0x36, 0x20,
            0x04, 0x7c, 0x1e, 0x20, 0x04, 0x46, 0x1c, 0x60, 0x04, 0x42, 0x18, 0x40, 0x04, 0x02, 0x18, 0xc0,
            0x04, 0x07, 0xf0, 0xc0, 0x07, 0xff, 0xe1, 0x80, 0x03, 0x00, 0x01, 0x00, 0x06, 0x00, 0x03, 0x00,
            0x0c, 0x00, 0x06, 0x00, 0x0f, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
        ]
        
        # Convert bitmap to pixel array
        self.snail_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                # 1 = snail pixel, 0 = background
                row_data.append(pixel)
            self.snail_pixels.append(row_data)
        
        # Colors
        # Snail color: #384247 = RGB(56, 66, 71)
        self.snail_color = (56, 66, 71)
        # Ground: same as horse (forest green)
        self.ground_color = (34, 139, 34)  # Forest green ground
        self.sky_color = (5, 8, 12)  # Dramatically dimmed dark blue sky
        self.sun_color = (255, 200, 50)  # Bright yellow sun
        self.cloud_color = (255, 255, 255)  # White clouds
        self.ground_height = 7  # Height of ground at bottom
        
        # Find snail dimensions
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.snail_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.snail_actual_width = max_x - min_x + 1
        self.snail_actual_height = max_y - min_y + 1
        self.snail_offset_x = min_x
        self.snail_offset_y = min_y
        
        print(f"🐌 Snail dimensions: {self.snail_actual_width}x{self.snail_actual_height}, offset: ({self.snail_offset_x}, {self.snail_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_sky(self, fade_alpha=1.0):
        """Draw dark blue sky background."""
        faded_sky = (
            int(self.sky_color[0] * fade_alpha),
            int(self.sky_color[1] * fade_alpha),
            int(self.sky_color[2] * fade_alpha)
        )
        for y in range(self.height - self.ground_height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, faded_sky)
    
    def draw_sun(self, fade_alpha=1.0):
        """Draw sun in the sky."""
        sun_x = self.width - 8  # Position sun on the right side, near top
        sun_y = 5  # Near the top
        sun_size = 3  # Small sun radius
        
        # Draw sun as a circle
        for dy in range(-sun_size, sun_size + 1):
            for dx in range(-sun_size, sun_size + 1):
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= sun_size:
                    x = sun_x + dx
                    y = sun_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height - self.ground_height:
                        # Fade edges for soft sun
                        intensity = 1.0 - (distance / sun_size) * 0.3
                        sun_pixel_color = (
                            int(self.sun_color[0] * intensity * fade_alpha),
                            int(self.sun_color[1] * intensity * fade_alpha),
                            int(self.sun_color[2] * intensity * fade_alpha)
                        )
                        self.safe_set_pixel(x, y, sun_pixel_color)
    
    def draw_clouds(self, phase=0, fade_alpha=1.0):
        """Draw clouds in the sky."""
        faded_cloud = (
            int(self.cloud_color[0] * fade_alpha),
            int(self.cloud_color[1] * fade_alpha),
            int(self.cloud_color[2] * fade_alpha)
        )
        # Create a few clouds at different positions
        cloud_positions = [
            (5 + phase * 0.5, 8),   # Cloud 1 - left side
            (15 + phase * 0.3, 6),  # Cloud 2 - middle-left
            (22 + phase * 0.4, 9),  # Cloud 3 - middle-right
        ]
        
        for cloud_x, cloud_y in cloud_positions:
            cloud_x = int(cloud_x) % (self.width + 10) - 5
            
            if 0 <= cloud_x < self.width:
                # Draw cloud shape (simple puffy cloud)
                for dy in range(-1, 2):
                    for dx in range(-3, 4):
                        x = cloud_x + dx
                        y = cloud_y + dy
                        
                        if 0 <= x < self.width and 0 <= y < self.height - self.ground_height:
                            # Create cloud effect - make it puffy
                            if abs(dx) + abs(dy) <= 2:
                                self.safe_set_pixel(x, y, faded_cloud)
    
    def draw_ground(self, fade_alpha=1.0):
        """Draw forest green ground at the bottom."""
        faded_ground = (
            int(self.ground_color[0] * fade_alpha),
            int(self.ground_color[1] * fade_alpha),
            int(self.ground_color[2] * fade_alpha)
        )
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, faded_ground)
    
    def draw_snail(self, x_pos, fade_alpha=1.0):
        """Draw the snail bitmap at position x_pos, positioned on ground.
        
        Args:
            x_pos: Horizontal position of the snail
            fade_alpha: Fade alpha value (1.0 = fully visible, 0.0 = invisible)
        """
        # Position snail vertically (bottom on ground)
        ground_y = self.height - self.ground_height
        snail_bottom_y = ground_y  # Snail bottom on ground line
        vertical_offset = snail_bottom_y - (self.snail_offset_y + self.snail_actual_height)
        
        # Apply fade to snail color
        faded_color = (
            int(self.snail_color[0] * fade_alpha),
            int(self.snail_color[1] * fade_alpha),
            int(self.snail_color[2] * fade_alpha)
        )
        
        # Draw snail pixels
        for y in range(48):
            for x in range(32):
                if self.snail_pixels[y][x] == 1:  # Snail pixel
                    screen_x = x + x_pos - self.snail_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if snail is on or above ground and within screen bounds
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        self.safe_set_pixel(screen_x, screen_y, faded_color)
    
    def run_animation(self, should_stop=None):
        """Run the snail animation - moves from left to right once, then fades out."""
        duration = 20  # 20 seconds total
        fade_duration = 2  # 2 seconds for fade out
        start_time = time.time()
        
        print("🐌 Starting snail animation...")
        
        # Animation parameters
        # Calculate speed so snail crosses screen in (duration - fade_duration) seconds
        travel_time = duration - fade_duration  # 17 seconds for movement
        total_distance = self.width + self.snail_actual_width
        speed = total_distance / travel_time  # pixels per second
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐌 Snail animation stopped by user")
                break
            
            # Calculate horizontal position (snail moves from left to right once)
            # Start off-screen left, move across screen
            if elapsed < travel_time:
                # Moving phase
                x_pos = int(elapsed * speed) - self.snail_actual_width
                fade_alpha = 1.0
            else:
                # Fade out phase
                # Keep snail at final position
                x_pos = int(travel_time * speed) - self.snail_actual_width
                # Calculate fade alpha (1.0 -> 0.0)
                fade_elapsed = elapsed - travel_time
                fade_alpha = max(0.0, 1.0 - (fade_elapsed / fade_duration))
            
            # Cloud animation phase (for drifting clouds)
            cloud_phase = elapsed * 0.1  # Slow cloud drift
            
            # Clear and draw
            self.led.clear()
            self.draw_sky(fade_alpha)
            self.draw_sun(fade_alpha)
            self.draw_clouds(cloud_phase, fade_alpha)
            self.draw_ground(fade_alpha)
            self.draw_snail(x_pos, fade_alpha)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐌 Snail animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        self.led.cleanup()

