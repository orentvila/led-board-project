#!/usr/bin/env python3
"""
Truck Animation for LED Board
Displays a truck bitmap on ground
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class TruckAnimation:
    def __init__(self):
        """Initialize the truck animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Truck bitmap data (32x48 pixels)
        # Format: 0xff = background, 0x00 = truck pixels (inverted)
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xf0, 0x00, 0x3f, 0xff, 0xe0, 0x00, 0x0f, 0xff, 0xc0, 0x00, 0x0f, 0xff, 0xc0, 0x00, 0x00, 0x7f,
            0xc0, 0x00, 0x00, 0x3f, 0xc0, 0x00, 0x07, 0x9f, 0xc0, 0x00, 0x07, 0xcf, 0xc0, 0x00, 0x07, 0xe7,
            0xc0, 0x00, 0x07, 0xe7, 0xc0, 0x00, 0x07, 0xe3, 0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x03,
            0xc0, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x00, 0x03, 0xc3, 0xe0, 0x07, 0xc3, 0xc4, 0x30, 0x0c, 0x67,
            0xec, 0x30, 0x18, 0x2f, 0xfc, 0x1f, 0xf8, 0x3f, 0xfc, 0x1f, 0xf8, 0x3f, 0xfc, 0x3f, 0xfc, 0x7f,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to pixel array
        # This bitmap is inverted: 0xff = background, 0x00 = truck pixel
        # So we check if bit is 0 (not 1) to identify truck pixels
        self.truck_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel_bit = (byte_value >> bit_index) & 1
                # Inverted: 0 = truck pixel, 1 = background
                pixel = 0 if pixel_bit == 0 else 0  # If bit is 0, it's a truck pixel
                # Actually, let's invert: if bit is 0, pixel = 1 (truck), if bit is 1, pixel = 0 (background)
                pixel = 1 if pixel_bit == 0 else 0
                row_data.append(pixel)
            self.truck_pixels.append(row_data)
        
        # Colors
        self.truck_color = (96, 172, 99)  # #60AC63 - Green truck color
        self.ground_color = (123, 123, 123)  # #7B7B7B - Gray ground
        self.sky_color = (10, 15, 25)  # Dimmed blue sky
        self.sun_color = (255, 200, 50)  # Bright yellow sun
        self.ground_height = 4  # Height of ground at bottom
        
        # Identify truck parts based on vertical position
        # Wheels are at the bottom (last row)
        # Front is on the left side (lower x values)
        # Box is the main body (middle/right area)
        self.wheel_row_start = 47  # Last row is wheels
        self.front_x_max = 12  # Front part is roughly x < 12
        
        # Find truck dimensions
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.truck_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.truck_actual_width = max_x - min_x + 1
        self.truck_actual_height = max_y - min_y + 1
        self.truck_offset_x = min_x
        self.truck_offset_y = min_y
        
        print(f"🚚 Truck dimensions: {self.truck_actual_width}x{self.truck_actual_height}, offset: ({self.truck_offset_x}, {self.truck_offset_y})")
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_sky(self):
        """Draw dimmed blue sky background."""
        for y in range(self.height - self.ground_height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.sky_color)
    
    def draw_sun(self):
        """Draw small sun in the sky."""
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
                            int(self.sun_color[0] * intensity),
                            int(self.sun_color[1] * intensity),
                            int(self.sun_color[2] * intensity)
                        )
                        self.safe_set_pixel(x, y, sun_pixel_color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def get_truck_color(self, x, y):
        """Return the truck color - entire truck uses same color."""
        return self.truck_color
    
    def draw_truck(self, x_pos):
        """Draw the truck bitmap at horizontal position x_pos."""
        # Position truck vertically (wheels touching ground) - same logic as horse
        ground_y = self.height - self.ground_height
        truck_bottom_y = ground_y  # Wheels on ground line
        vertical_offset = truck_bottom_y - (self.truck_offset_y + self.truck_actual_height)
        
        # Draw truck pixels
        for y in range(48):
            for x in range(32):
                if self.truck_pixels[y][x] == 1:  # Truck pixel
                    screen_x = x + x_pos - self.truck_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if truck is on or above ground and within screen bounds
                    # Allow drawing at ground level (screen_y <= ground_y) so truck touches ground
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        # Get appropriate color for this pixel
                        color = self.get_truck_color(x, y)
                        self.safe_set_pixel(screen_x, screen_y, color)
    
    def run_animation(self, should_stop=None):
        """Display the truck moving from left to right across the screen."""
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("🚚 Starting truck animation...")
        
        # Animation parameters
        speed = (self.width + self.truck_actual_width) / duration  # pixels per second
        
        # Draw first frame immediately to prevent blinking
        elapsed = 0
        x_pos = int(elapsed * speed) - self.truck_actual_width
        self.led.clear()
        self.draw_sky()
        self.draw_sun()
        self.draw_ground()
        self.draw_truck(x_pos)
        self.led.show()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🚚 Truck animation stopped by user")
                break
            
            # Calculate horizontal position (truck moves from left to right)
            # Start off-screen left, move across, exit off-screen right
            x_pos = int(elapsed * speed) - self.truck_actual_width
            
            # Draw frame
            self.led.clear()
            self.draw_sky()
            self.draw_sun()
            self.draw_ground()
            self.draw_truck(x_pos)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        # Fade out the truck animation smoothly
        print("🚚 Fading out truck animation...")
        fade_out_duration = 2  # 2 seconds fade-out
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🚚 Truck animation stopped during fade-out")
                break
            
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_intensity = 1.0 - fade_progress  # Fade from 1.0 to 0.0
            
            # Calculate truck position (continue moving during fade-out)
            elapsed_total = time.time() - start_time
            x_pos = int(elapsed_total * speed) - self.truck_actual_width
            
            # Clear display
            self.led.clear()
            
            # Draw sky with fade-out
            sky_color_fade = tuple(int(c * fade_intensity) for c in self.sky_color)
            for y in range(self.height - self.ground_height):
                for x in range(self.width):
                    self.safe_set_pixel(x, y, sky_color_fade)
            
            # Draw sun with fade-out
            sun_x = self.width - 8
            sun_y = 5
            sun_size = 3
            for dy in range(-sun_size, sun_size + 1):
                for dx in range(-sun_size, sun_size + 1):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= sun_size:
                        x = sun_x + dx
                        y = sun_y + dy
                        if 0 <= x < self.width and 0 <= y < self.height - self.ground_height:
                            intensity = (1.0 - (distance / sun_size) * 0.3) * fade_intensity
                            sun_pixel_color = (
                                int(self.sun_color[0] * intensity),
                                int(self.sun_color[1] * intensity),
                                int(self.sun_color[2] * intensity)
                            )
                            self.safe_set_pixel(x, y, sun_pixel_color)
            
            # Draw ground with fade-out
            ground_color_fade = tuple(int(c * fade_intensity) for c in self.ground_color)
            for y in range(self.height - self.ground_height, self.height):
                for x in range(self.width):
                    self.safe_set_pixel(x, y, ground_color_fade)
            
            # Draw truck with fade-out
            ground_y = self.height - self.ground_height
            truck_bottom_y = ground_y
            vertical_offset = truck_bottom_y - (self.truck_offset_y + self.truck_actual_height)
            
            truck_color_fade = tuple(int(c * fade_intensity) for c in self.truck_color)
            for y in range(48):
                for x in range(32):
                    if self.truck_pixels[y][x] == 1:
                        screen_x = x + x_pos - self.truck_offset_x
                        screen_y = y + vertical_offset
                        if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                            self.safe_set_pixel(screen_x, screen_y, truck_color_fade)
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS for smooth fade-out
        
        print("🚚 Truck animation completed!")
        
        # Clear display completely
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

