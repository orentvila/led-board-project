#!/usr/bin/env python3
"""
Deer Animation for LED Board
Pixel art style running deer animation adapted for portrait orientation
Based on Christmas reindeer animation concept
"""

import time
import random
import math
from led_controller_exact import LEDControllerExact
import config

class DeerAnimation:
    def __init__(self):
        """Initialize the deer animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Deer colors - brown tones with white accents
        self.deer_colors = {
            'body': (139, 69, 19),      # Saddle brown
            'belly': (160, 82, 45),     # Saddle brown (lighter)
            'antlers': (101, 67, 33),   # Dark brown
            'nose': (0, 0, 0),          # Black
            'eyes': (0, 0, 0),          # Black
            'hooves': (0, 0, 0),        # Black
            'white_patch': (255, 255, 255),  # White
            'background': (34, 139, 34)  # Forest green
        }
        
        # Animation parameters
        self.total_duration = 30.0  # 30 seconds
        self.animation_speed = 0.1  # Frame delay
        
        # Deer position and movement
        self.deer_x = 16  # Center horizontally
        self.deer_y = 35  # Start near bottom
        self.running_phase = 0
        self.leg_phase = 0
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_deer(self, x, y, running_phase, leg_phase):
        """Draw a pixel art deer at the given position."""
        # Deer body (main oval shape)
        for dy in range(-6, 7):
            for dx in range(-4, 5):
                distance = math.sqrt((dx*dx) + (dy*dy*0.6))  # Oval shape
                if distance <= 4:
                    self.safe_set_pixel(x + dx, y + dy, self.deer_colors['body'])
        
        # Deer belly (lighter oval)
        for dy in range(-4, 5):
            for dx in range(-3, 4):
                distance = math.sqrt((dx*dx) + (dy*dy*0.7))
                if distance <= 3:
                    self.safe_set_pixel(x + dx, y + dy, self.deer_colors['belly'])
        
        # Deer head
        head_x = x + 3
        head_y = y - 2
        for dy in range(-3, 4):
            for dx in range(-2, 3):
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= 2:
                    self.safe_set_pixel(head_x + dx, head_y + dy, self.deer_colors['body'])
        
        # Antlers (branched)
        antler_offset = math.sin(running_phase * 2) * 0.5  # Slight sway
        # Left antler
        for i in range(3):
            self.safe_set_pixel(head_x - 1, head_y - 3 - i, self.deer_colors['antlers'])
        self.safe_set_pixel(head_x - 2, head_y - 4, self.deer_colors['antlers'])
        
        # Right antler
        for i in range(3):
            self.safe_set_pixel(head_x + 1, head_y - 3 - i, self.deer_colors['antlers'])
        self.safe_set_pixel(head_x + 2, head_y - 4, self.deer_colors['antlers'])
        
        # Eyes
        self.safe_set_pixel(head_x - 1, head_y - 1, self.deer_colors['eyes'])
        self.safe_set_pixel(head_x + 1, head_y - 1, self.deer_colors['eyes'])
        
        # Nose
        self.safe_set_pixel(head_x, head_y + 1, self.deer_colors['nose'])
        
        # White patch on chest
        self.safe_set_pixel(x - 2, y + 2, self.deer_colors['white_patch'])
        self.safe_set_pixel(x - 1, y + 2, self.deer_colors['white_patch'])
        self.safe_set_pixel(x - 2, y + 3, self.deer_colors['white_patch'])
        
        # Legs with running animation
        leg_offset = math.sin(leg_phase * 4) * 1.5  # Running motion
        
        # Front legs
        front_leg_x = x + 2
        back_leg_x = x - 2
        
        # Front left leg
        for i in range(4):
            leg_y = y + 3 + i + int(leg_offset)
            self.safe_set_pixel(front_leg_x, leg_y, self.deer_colors['body'])
        self.safe_set_pixel(front_leg_x, y + 7 + int(leg_offset), self.deer_colors['hooves'])
        
        # Front right leg
        for i in range(4):
            leg_y = y + 3 + i - int(leg_offset)
            self.safe_set_pixel(front_leg_x + 1, leg_y, self.deer_colors['body'])
        self.safe_set_pixel(front_leg_x + 1, y + 7 - int(leg_offset), self.deer_colors['hooves'])
        
        # Back legs
        for i in range(4):
            leg_y = y + 3 + i + int(leg_offset * 0.5)
            self.safe_set_pixel(back_leg_x, leg_y, self.deer_colors['body'])
            self.safe_set_pixel(back_leg_x + 1, leg_y, self.deer_colors['body'])
        self.safe_set_pixel(back_leg_x, y + 7 + int(leg_offset * 0.5), self.deer_colors['hooves'])
        self.safe_set_pixel(back_leg_x + 1, y + 7 + int(leg_offset * 0.5), self.deer_colors['hooves'])
        
        # Tail
        tail_x = x - 4
        tail_y = y - 1
        for i in range(3):
            self.safe_set_pixel(tail_x - i, tail_y, self.deer_colors['body'])
    
    def create_forest_background(self):
        """Create a forest green background with some texture."""
        for y in range(self.height):
            for x in range(self.width):
                # Base forest green
                base_green = self.deer_colors['background']
                
                # Add some texture variation
                noise = random.randint(-10, 10)
                r = max(0, min(255, base_green[0] + noise))
                g = max(0, min(255, base_green[1] + noise))
                b = max(0, min(255, base_green[2] + noise))
                
                self.safe_set_pixel(x, y, (r, g, b))
    
    def run_animation(self):
        """Run the deer animation."""
        print("🦌 Starting deer animation...")
        
        start_time = time.time()
        
        while time.time() - start_time < self.total_duration:
            # Clear display
            self.led.clear()
            
            # Create forest background
            self.create_forest_background()
            
            # Update animation phases
            self.running_phase += 0.3
            self.leg_phase += 0.4
            
            # Move deer upward (running up the screen)
            self.deer_y -= 0.3
            if self.deer_y < -10:  # Reset when off screen
                self.deer_y = self.height + 5
            
            # Add slight horizontal sway
            sway_x = math.sin(self.running_phase * 0.5) * 1
            deer_x = self.deer_x + int(sway_x)
            
            # Draw the deer
            self.draw_deer(deer_x, int(self.deer_y), self.running_phase, self.leg_phase)
            
            # Add some sparkle effects (like Christmas magic)
            if random.random() < 0.1:
                sparkle_x = random.randint(0, self.width - 1)
                sparkle_y = random.randint(0, self.height - 1)
                self.safe_set_pixel(sparkle_x, sparkle_y, (255, 255, 255))
            
            self.led.show()
            time.sleep(self.animation_speed)
        
        print("🦌 Deer animation completed!")

def main():
    """Main function to run the deer animation."""
    try:
        deer = DeerAnimation()
        deer.run_animation()
    except KeyboardInterrupt:
        print("\n🦌 Deer animation interrupted by user")
    except Exception as e:
        print(f"❌ Error in deer animation: {e}")
    finally:
        print("🦌 Cleaning up...")

if __name__ == "__main__":
    main()
