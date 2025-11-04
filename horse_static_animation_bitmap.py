#!/usr/bin/env python3
"""
Horse Galloping Animation for LED Board
Displays a brown horse galloping on green ground
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class HorseStaticAnimationBitmap:
    def __init__(self):
        """Initialize the horse galloping animation."""
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
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def get_gallop_frame(self, frame_index):
        """Get horse pixels for a specific gallop frame with leg animation.
        
        Gallop cycle has 4 phases:
        0: All legs extended (moment before push) - on ground
        1: Front legs up, back legs pushing - rising
        2: All legs in air (suspension) - peak bounce
        3: Front legs landing, back legs forward - landing
        """
        # Create a copy of base pixels
        frame_pixels = [row[:] for row in self.horse_base_pixels]
        
        # Identify and modify leg positions
        # Legs are in the lower portion of the horse bitmap
        # We'll shift leg pixels vertically based on gallop phase
        
        phase = frame_index % 4
        
        # Define leg areas (approximate Y positions in bitmap)
        front_leg_y_start = 35  # Front legs start around here
        back_leg_y_start = 38   # Back legs start around here
        
        # Create modified frame
        modified_frame = [[0 for _ in range(32)] for _ in range(48)]
        
        # Copy body pixels (everything above legs)
        body_y_end = 32  # Body ends before legs
        for y in range(body_y_end):
            for x in range(32):
                modified_frame[y][x] = frame_pixels[y][x]
        
        # Modify leg positions based on phase
        if phase == 0:  # All legs down
            leg_shift_front = 0
            leg_shift_back = 0
            vertical_bounce = 0
        elif phase == 1:  # Front up, back pushing
            leg_shift_front = -3  # Front legs lifted
            leg_shift_back = 0   # Back legs pushing off
            vertical_bounce = -1  # Rising
        elif phase == 2:  # All legs in air (suspension)
            leg_shift_front = -4  # Front legs high
            leg_shift_back = -4   # Back legs high
            vertical_bounce = -2  # Peak bounce
        else:  # phase == 3: Front landing, back forward
            leg_shift_front = 0   # Front legs landing
            leg_shift_back = -2   # Back legs forward
            vertical_bounce = -1  # Landing
        
        # Copy and shift leg pixels
        for y in range(front_leg_y_start, 48):
            for x in range(32):
                if frame_pixels[y][x] == 1:
                    # Front leg area (left side)
                    if x < 16:
                        new_y = y + leg_shift_front
                        if 0 <= new_y < 48:
                            modified_frame[new_y][x] = 1
                    # Back leg area (right side)
                    else:
                        new_y = y + leg_shift_back
                        if 0 <= new_y < 48:
                            modified_frame[new_y][x] = 1
        
        return modified_frame, vertical_bounce
    
    def draw_ground(self):
        """Draw green ground at the bottom."""
        for y in range(self.height - self.ground_height, self.height):
            for x in range(self.width):
                self.safe_set_pixel(x, y, self.ground_color)
    
    def draw_horse_galloping(self, x_pos, frame_index, vertical_offset=0, frame_pixels=None):
        """Draw the horse at position x_pos with gallop frame."""
        if frame_pixels is None:
            frame_pixels, _ = self.get_gallop_frame(frame_index)
        
        # Draw horse pixels
        for y in range(48):
            for x in range(32):
                if frame_pixels[y][x] == 1:  # Horse pixel
                    screen_x = x + x_pos - self.horse_offset_x
                    screen_y = y + vertical_offset
                    
                    # Only draw if horse is on or above ground
                    if screen_y < self.height - self.ground_height:
                        self.safe_set_pixel(screen_x, screen_y, self.horse_color)
    
    def run_animation(self, should_stop=None):
        """Run the horse galloping animation."""
        duration = 30  # 30 seconds
        start_time = time.time()
        frame = 0
        
        print("🐴 Starting horse galloping animation...")
        
        # Galloping parameters
        gallop_speed = 12.0  # pixels per second (horizontal speed)
        gallop_fps = 8  # frames per gallop cycle (2 per phase)
        ground_y = self.height - self.ground_height
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🐴 Horse animation stopped by user")
                break
            
            # Calculate horizontal position (horse runs from left to right, looping)
            x_pos = int((elapsed * gallop_speed) % (self.width + self.horse_actual_width + 10)) - 5
            
            # Calculate gallop frame (4 phases, cycling)
            frame_index = int((frame / gallop_fps) % 4)
            
            # Get gallop frame with leg animation
            frame_pixels, frame_bounce = self.get_gallop_frame(frame_index)
            
            # Additional smooth bounce for realism
            smooth_bounce = -0.5 * math.sin((frame / gallop_fps) * 2 * math.pi)
            total_bounce = frame_bounce + int(smooth_bounce)
            
            # Position horse vertically (feet on ground)
            horse_bottom_y = ground_y - 1  # Feet just above ground
            vertical_offset = horse_bottom_y - (self.horse_offset_y + self.horse_actual_height) + total_bounce
            
            # Clear and draw
            self.led.clear()
            self.draw_ground()
            self.draw_horse_galloping(x_pos, frame_index, vertical_offset, frame_pixels)
            self.led.show()
            
            frame += 1
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🐴 Horse galloping animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
