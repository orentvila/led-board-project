#!/usr/bin/env python3
"""
Butterfly Animation for LED Board
Displays a colorful butterfly with fluttering motion
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class ButterflyAnimation:
    def __init__(self):
        """Initialize the butterfly animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Butterfly colors
        # #EC6290 = RGB(236, 98, 144) - Pink
        # #9B42B3 = RGB(155, 66, 179) - Purple
        self.color1 = (236, 98, 144)  # Pink
        self.color2 = (155, 66, 179)  # Purple
        
        # Butterfly dimensions
        self.butterfly_width = 8
        self.butterfly_height = 6
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_butterfly(self, x, y, wing_phase=0):
        """Draw a butterfly at position (x, y) with wing fluttering animation.
        
        Args:
            x, y: Center position of butterfly body
            wing_phase: Phase for wing animation (0-2*pi)
        """
        # Wing fluttering effect (wings move up/down)
        wing_offset = math.sin(wing_phase) * 1.5
        
        # Butterfly body (vertical line in center) - dark brown
        body_color = (80, 40, 40)  # Dark brown body
        for i in range(5):
            body_y = int(y + i - 2)
            if 0 <= body_y < self.height:
                self.safe_set_pixel(int(x), body_y, body_color)
        
        # Top wings (left and right) - larger wings
        # Left top wing - pink (#EC6290)
        left_top_wing = [
            (x - 2, y - 3 + int(wing_offset)),
            (x - 3, y - 2 + int(wing_offset)),
            (x - 4, y - 1 + int(wing_offset)),
            (x - 4, y + int(wing_offset)),
            (x - 3, y + 1 + int(wing_offset)),
            (x - 2, y + int(wing_offset)),
            (x - 1, y - 1 + int(wing_offset)),
        ]
        for px, py in left_top_wing:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.color1)
        
        # Right top wing - purple (#9B42B3)
        right_top_wing = [
            (x + 2, y - 3 + int(wing_offset)),
            (x + 3, y - 2 + int(wing_offset)),
            (x + 4, y - 1 + int(wing_offset)),
            (x + 4, y + int(wing_offset)),
            (x + 3, y + 1 + int(wing_offset)),
            (x + 2, y + int(wing_offset)),
            (x + 1, y - 1 + int(wing_offset)),
        ]
        for px, py in right_top_wing:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.color2)
        
        # Bottom wings (left and right) - smaller wings
        # Left bottom wing - purple (#9B42B3)
        left_bottom_wing = [
            (x - 2, y + 1 - int(wing_offset)),
            (x - 3, y + 2 - int(wing_offset)),
            (x - 4, y + 3 - int(wing_offset)),
            (x - 3, y + 4 - int(wing_offset)),
            (x - 2, y + 3 - int(wing_offset)),
            (x - 1, y + 2 - int(wing_offset)),
        ]
        for px, py in left_bottom_wing:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.color2)
        
        # Right bottom wing - pink (#EC6290)
        right_bottom_wing = [
            (x + 2, y + 1 - int(wing_offset)),
            (x + 3, y + 2 - int(wing_offset)),
            (x + 4, y + 3 - int(wing_offset)),
            (x + 3, y + 4 - int(wing_offset)),
            (x + 2, y + 3 - int(wing_offset)),
            (x + 1, y + 2 - int(wing_offset)),
        ]
        for px, py in right_bottom_wing:
            if 0 <= px < self.width and 0 <= py < self.height:
                self.safe_set_pixel(px, py, self.color1)
    
    def run_animation(self, should_stop=None):
        """Run the butterfly animation with fluttering motion."""
        duration = 30  # 30 seconds
        start_time = time.time()
        
        print("🦋 Starting butterfly animation...")
        
        # Animation parameters
        flutter_speed = 8.0  # Wing flutter cycles per second
        horizontal_speed = 2.0  # Horizontal drift speed (pixels per second)
        vertical_speed = 1.5  # Vertical flutter speed (pixels per second)
        
        # Start position
        start_x = self.width // 4
        start_y = self.height // 2
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Check stop flag
            if should_stop and should_stop():
                print("🦋 Butterfly animation stopped by user")
                break
            
            # Calculate butterfly position with gentle drift
            # Horizontal: gentle drift across screen
            x_pos = (start_x + elapsed * horizontal_speed) % (self.width + 10) - 5
            
            # Vertical: fluttering up and down motion
            vertical_flutter = math.sin(elapsed * vertical_speed * 2 * math.pi) * 3
            y_pos = start_y + int(vertical_flutter)
            
            # Wing fluttering phase
            wing_phase = elapsed * flutter_speed * 2 * math.pi
            
            # Clear and draw
            self.led.clear()
            self.draw_butterfly(int(x_pos), int(y_pos), wing_phase)
            self.led.show()
            
            time.sleep(0.05)  # 20 FPS for smooth animation
        
        print("🦋 Butterfly animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()
