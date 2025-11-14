#!/usr/bin/env python3
"""
Horse Animation for LED Board
Displays a brown horse moving from left to right across green ground
"""

import time
from led_controller_exact import LEDControllerExact
import config

class HorseStaticAnimationBitmap:
    def __init__(self):
        """Initialize the horse animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Horse bitmap data (32x48 pixels) - base pose
        bitmap_hex = [
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x1f, 0xff, 0xff, 0xfc, 0x0f,
            0xff, 0xff, 0xf8, 0x0f, 0xff, 0xff, 0xf8, 0x0f, 0xff, 0xff, 0xf0, 0x0f, 0xff, 0xff, 0xe0, 0xcf,
            0xff, 0x80, 0x80, 0xcf, 0xfc, 0x00, 0x00, 0xff, 0xf8, 0x00, 0x00, 0xff, 0xf2, 0x00, 0x00, 0xff,
            0xf2, 0x00, 0x00, 0xff, 0xf2, 0x00, 0x00, 0xff, 0xf6, 0x00, 0x00, 0xff, 0xf6, 0x07, 0x00, 0xff,
            0xfe, 0x67, 0xf6, 0x7f, 0xfc, 0xe7, 0xf7, 0x7f, 0xfd, 0xef, 0xe7, 0x7f, 0xfb, 0xef, 0xe7, 0x7f,
            0xfb, 0xef, 0xef, 0xff, 0xfb, 0xf7, 0xec, 0xff, 0xfb, 0xf3, 0xef, 0xff, 0xfb, 0xf9, 0xe7, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
            0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        ]
        
        # Convert bitmap to pixel array
        self.horse_base_pixels = []
        for row in range(48):
            row_data = []
            byte_start = row * 4
            for col in range(32):
                byte_index = byte_start + (col // 8)
                bit_index = 7 - (col % 8)
                byte_value = bitmap_hex[byte_index]
                pixel = (byte_value >> bit_index) & 1
                row_data.append(1 - pixel)  # Invert: 0 = horse, 1 = background
            self.horse_base_pixels.append(row_data)
        
        # Colors
        self.horse_color = (139, 69, 19)  # Brown horse (saddle brown)
        self.ground_color = (34, 139, 34)  # Forest green ground
        self.ground_height = 4  # Height of ground at bottom
        
        # Find horse dimensions
        self.horse_width = 32
        self.horse_height = 48
        
        # Find actual horse bounds (non-empty pixels)
        min_x, max_x, min_y, max_y = 32, 0, 48, 0
        for y in range(48):
            for x in range(32):
                if self.horse_base_pixels[y][x] == 1:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_y = min(min_y, y)
                    max_y = max(max_y, y)
        
        self.horse_actual_width = max_x - min_x + 1
        self.horse_actual_height = max_y - min_y + 1
        self.horse_offset_x = min_x
        self.horse_offset_y = min_y
        
        print(f"Horse dimensions: {self.horse_actual_width}x{self.horse_actual_height}, offset: ({self.horse_offset_x}, {self.horse_offset_y})")
        
        # Identify leg regions for animation
        # Legs are in the lower portion of the bitmap (rows ~30-47)
        # Front legs are typically on the left (x < 16), back legs on right (x >= 16)
        self.leg_y_start = 30  # Legs start around row 30
        self.leg_y_end = 48    # Legs go to bottom
        
        # Separate legs: Front Left, Front Right, Back Left, Back Right
        # We'll identify legs by their X position ranges
        self.front_leg_x_range = (0, 15)   # Front legs on left side
        self.back_leg_x_range = (16, 31)   # Back legs on right side
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def get_running_frame(self, frame_index):
        """Get horse frame with animated legs for running.
        
        Running pattern (4 phases):
        Phase 0: Front Left & Back Right down, Front Right & Back Left up
        Phase 1: Front Right & Back Left down, Front Left & Back Right up
        Phase 2: Transition (all legs moving)
        Phase 3: Transition (all legs moving)
        """
        phase = frame_index % 4
        
        # Create modified frame
        frame_pixels = [[0 for _ in range(32)] for _ in range(48)]
        
        # Copy body pixels (everything above legs) - body stays constant
        body_y_end = self.leg_y_start
        for y in range(body_y_end):
            for x in range(32):
                frame_pixels[y][x] = self.horse_base_pixels[y][x]
        
        # Animate legs based on phase
        # Leg movement: lift legs up by shifting pixels vertically
        leg_lift_amount = 4  # Pixels to lift legs
        
        for y in range(self.leg_y_start, self.leg_y_end):
            for x in range(32):
                if self.horse_base_pixels[y][x] == 1:
                    # Determine which leg this pixel belongs to
                    is_front = x < 16
                    is_left = (x < 8) if is_front else (x < 24)
                    
                    # Determine leg state based on phase
                    if phase == 0:
                        # FL & BR down, FR & BL up
                        leg_up = (is_front and not is_left) or (not is_front and is_left)
                    elif phase == 1:
                        # FR & BL down, FL & BR up
                        leg_up = (is_front and is_left) or (not is_front and not is_left)
                    elif phase == 2:
                        # Transition - FL & BR lifting, FR & BL lowering
                        leg_up = (is_front and is_left) or (not is_front and not is_left)
                    else:  # phase == 3
                        # Transition - FR & BL lifting, FL & BR lowering
                        leg_up = (is_front and not is_left) or (not is_front and is_left)
                    
                    # Calculate new position
                    if leg_up:
                        new_y = y - leg_lift_amount
                        new_x = x + 1 if is_front else x - 1  # Slight forward/back movement
                    else:
                        new_y = y
                        new_x = x
                    
                    # Place pixel if within bounds
                    if 0 <= new_y < 48 and 0 <= new_x < 32:
                        frame_pixels[new_y][new_x] = 1
        
        return frame_pixels
    
    def draw_horse(self, x_pos, frame_index=0):
        """Draw the horse bitmap at position x_pos with running leg animation."""
        # Position horse vertically (feet on ground)
        ground_y = self.height - self.ground_height
        horse_bottom_y = ground_y - 1  # Feet just above ground
        vertical_offset = horse_bottom_y - (self.horse_offset_y + self.horse_actual_height)
        
        # Get animated frame with leg movement
        frame_pixels = self.get_running_frame(frame_index)
        
        # Draw horse pixels from animated frame
        for y in range(48):
            for x in range(32):
                if frame_pixels[y][x] == 1:  # Horse pixel
                    screen_x = x + x_pos - self.horse_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if horse is on or above ground and within screen bounds
                    if 0 <= screen_x < self.width and screen_y < self.height - self.ground_height:
                        self.safe_set_pixel(screen_x, screen_y, self.horse_color)
    
    def run_animation(self, should_stop=None):
        """Run the horse animation - moves from left to right with running leg animation."""
        duration = 30  # 30 seconds
        start_time = time.time()
        frame = 0
        
        print("🐴 Starting horse running animation...")
        
        # Animation parameters
        speed = 8.0  # pixels per second (horizontal speed)
        leg_animation_fps = 10  # Frames per leg cycle (faster leg movement)
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse animation stopped by user")
                break
            
            # Calculate horizontal position (horse moves from left to right, looping)
            # Start off-screen left, move across, then loop
            total_distance = self.width + self.horse_actual_width
            x_pos = int((elapsed * speed) % total_distance) - self.horse_actual_width
            
            # Calculate leg animation frame (4 phases for running)
            frame_index = int((frame / leg_animation_fps) % 4)
            
            # Clear and draw
            self.led.clear()
            self.draw_ground()
            self.draw_horse(x_pos, frame_index)
            self.led.show()
            
            frame += 1
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐴 Horse animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
