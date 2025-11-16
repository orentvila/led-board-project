#!/usr/bin/env python3
"""
Truck Animation for LED Board
Displays a truck bitmap on ground
"""

import time
from led_controller_exact import LEDControllerExact
import config

class TruckAnimation:
    def __init__(self):
        """Initialize the truck animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Truck bitmap data (32x48 pixels)
        # Format: 0x00 = background, non-zero bits = truck pixels
        bitmap_hex = [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x0f, 0xff, 0xc0, 0x00, 0x1f, 0xff, 0xf0, 0x00, 0x3f, 0xff, 0xf0, 0x00, 0x3f, 0xff, 0xff, 0x80,
            0x3f, 0xff, 0xff, 0xc0, 0x3f, 0xff, 0xf8, 0x60, 0x3f, 0xff, 0xf8, 0x30, 0x3f, 0xff, 0xf8, 0x18,
            0x3f, 0xff, 0xf8, 0x18, 0x3f, 0xff, 0xf8, 0x1c, 0x3f, 0xff, 0xff, 0xfc, 0x3f, 0xff, 0xff, 0xfc,
            0x3f, 0xff, 0xff, 0xfc, 0x3f, 0xff, 0xff, 0xfc, 0x3c, 0x1f, 0xf8, 0x3c, 0x3b, 0xcf, 0xf3, 0x98,
            0x13, 0xcf, 0xe7, 0xd0, 0x03, 0xe0, 0x07, 0xc0, 0x03, 0xe0, 0x07, 0xc0, 0x03, 0xc0, 0x03, 0x80,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to pixel array
        # 1 = truck pixel, 0 = background
        # Skip rows 0-7 (not part of truck), start from row 8
        self.truck_pixels = []
        for row in range(48):
            # Skip rows 0-7
            if row < 8:
                # Add empty row for skipped rows
                self.truck_pixels.append([0] * 32)
            else:
                row_data = []
                byte_start = row * 4
                for col in range(32):
                    byte_index = byte_start + (col // 8)
                    bit_index = 7 - (col % 8)
                    byte_value = bitmap_hex[byte_index]
                    pixel = (byte_value >> bit_index) & 1
                    row_data.append(pixel)
                self.truck_pixels.append(row_data)
        
        # Colors
        self.wheel_color = (255, 255, 255)  # White wheels
        self.box_color = (231, 77, 73)  # #E74D49 - Red box
        self.front_color = (248, 147, 18)  # #F89312 - Orange front
        self.ground_color = (34, 139, 34)  # Forest green ground
        self.ground_height = 4  # Height of ground at bottom
        
        # Identify truck parts based on vertical position
        # Wheels are at the bottom (last row)
        # Front is on the left side (lower x values)
        # Box is the main body (middle/right area)
        self.wheel_row_start = 47  # Last row is wheels
        self.front_x_max = 12  # Front part is roughly x < 12
        
        # Find truck dimensions (exclude rows 0-7 and bottom row 47)
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(8, 47):  # Only check rows 8-46, exclude rows 0-7 and row 47
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
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def get_truck_color(self, x, y):
        """Determine the color for a truck pixel based on its position."""
        # Wheels are at the bottom row of actual truck (row 46, not 47)
        # Since we exclude rows 0-7 and row 47, the bottom row is row 46
        if y == 46:  # Bottom row of actual truck
            return self.wheel_color
        
        # Front of truck is on the left side (lower x values)
        if x < self.front_x_max:
            return self.front_color
        
        # Box is the rest (middle/right area)
        return self.box_color
    
    def draw_truck(self):
        """Draw the truck bitmap centered on the screen."""
        # Center the truck horizontally
        center_x = self.width // 2
        x_pos = center_x - (self.truck_actual_width // 2) - self.truck_offset_x
        
        # Position truck vertically (wheels touching ground) - same logic as horse
        ground_y = self.height - self.ground_height
        truck_bottom_y = ground_y  # Wheels on ground line
        vertical_offset = truck_bottom_y - (self.truck_offset_y + self.truck_actual_height)
        
        # Draw truck pixels (exclude rows 0-7 and bottom row 47)
        for y in range(8, 47):  # Only draw rows 8-46, exclude rows 0-7 and row 47
            for x in range(32):
                if self.truck_pixels[y][x] == 1:  # Truck pixel
                    screen_x = x + x_pos
                    screen_y = y + vertical_offset
                    
                    # Only draw if truck is on or above ground and within screen bounds
                    # Allow drawing at ground level (screen_y <= ground_y) so truck touches ground
                    if 0 <= screen_x < self.width and 0 <= screen_y <= ground_y:
                        # Get appropriate color for this pixel
                        color = self.get_truck_color(x, y)
                        self.safe_set_pixel(screen_x, screen_y, color)
    
    def run_animation(self, should_stop=None):
        """Display the truck as a static image centered on the screen."""
        duration = 15  # 15 seconds
        start_time = time.time()
        
        print("🚚 Starting truck display...")
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("🚚 Truck animation stopped by user")
                break
            
            # Draw static truck centered on screen
            self.led.clear()
            self.draw_ground()
            self.draw_truck()
            self.led.show()
            
            time.sleep(0.1)  # Update every 0.1 seconds (static display)
        
        print("🚚 Truck display completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

