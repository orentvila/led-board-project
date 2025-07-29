#!/usr/bin/env python3
"""
Dudi Paddleboarding Animation for LED Board
Features a person paddleboarding in crystal-clear turquoise water
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class DudiPaddleboardingAnimation:
    def __init__(self):
        """Initialize the Dudi paddleboarding animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'sky': (135, 206, 235),        # Light blue sky
            'water_deep': (0, 150, 200),   # Deep turquoise water
            'water_light': (64, 224, 208), # Light turquoise water
            'water_surface': (173, 216, 230), # Surface water reflection
            'sand': (238, 203, 173),       # Sandy bottom
            'board_white': (255, 255, 255), # White paddleboard
            'board_red': (255, 0, 0),      # Red board section
            'board_gray': (128, 128, 128), # Gray board section
            'person_skin': (210, 180, 140), # Person's skin tone
            'person_shorts': (25, 25, 112), # Dark blue shorts
            'person_cap': (0, 0, 0),       # Black cap
            'paddle': (139, 69, 19),       # Brown paddle
            'shadow': (50, 50, 50),        # Shadow on sand
            'sun': (255, 255, 0),          # Yellow sun
            'cloud': (255, 255, 255)       # White clouds
        }
        
        # Animation parameters
        self.water_timer = 0
        self.paddle_timer = 0
        self.cloud_timer = 0
        self.sun_timer = 0
        
    def create_water_ripples(self, frame):
        """Create animated water ripples."""
        for y in range(self.height):
            for x in range(self.width):
                # Water ripple effect
                ripple = math.sin((x + self.water_timer * 0.5) * 0.3) * 0.1
                ripple += math.sin((y + self.water_timer * 0.3) * 0.2) * 0.1
                
                # Base water color
                if y < self.height * 0.7:  # Upper water
                    frame[y, x] = self.colors['water_light']
                else:  # Deeper water
                    frame[y, x] = self.colors['water_deep']
                
                # Add ripple variation
                if ripple > 0:
                    # Blend with lighter water
                    current = frame[y, x]
                    light = self.colors['water_surface']
                    frame[y, x] = tuple(int(0.8 * c + 0.2 * l) for c, l in zip(current, light))
    
    def create_sand_bottom(self, frame):
        """Create sandy bottom visible through clear water."""
        for y in range(int(self.height * 0.7), self.height):
            for x in range(self.width):
                # Sandy bottom pattern
                sand_pattern = math.sin(x * 0.2) * 0.1 + math.sin(y * 0.3) * 0.1
                sand_color = tuple(int(c * (0.8 + sand_pattern)) for c in self.colors['sand'])
                
                # Blend with water for transparency effect
                water_color = frame[y, x]
                frame[y, x] = tuple(int(0.3 * s + 0.7 * w) for s, w in zip(sand_color, water_color))
    
    def create_paddleboard(self, frame, paddle_x_offset=0):
        """Create the paddleboard with person."""
        # Board position (centered horizontally, in water)
        board_x = self.width // 2 + paddle_x_offset
        board_y = self.height // 2
        
        # Paddleboard (white with red nose and gray center)
        board_length = 12
        board_width = 3
        
        for y in range(self.height):
            for x in range(self.width):
                # Check if pixel is on the board
                if (abs(x - board_x) <= board_width // 2 and 
                    abs(y - board_y) <= board_length // 2):
                    
                    # Board sections
                    if y < board_y - 4:  # Nose (red)
                        frame[y, x] = self.colors['board_red']
                    elif abs(y - board_y) <= 2:  # Center (gray)
                        frame[y, x] = self.colors['board_gray']
                    else:  # Main body (white)
                        frame[y, x] = self.colors['board_white']
        
        # Person on the board
        person_x = board_x
        person_y = board_y
        
        # Person's body (standing)
        for y in range(person_y - 6, person_y + 2):
            for x in range(person_x - 1, person_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    if y < person_y - 2:  # Torso (skin)
                        frame[y, x] = self.colors['person_skin']
                    else:  # Shorts
                        frame[y, x] = self.colors['person_shorts']
        
        # Person's head
        for y in range(person_y - 8, person_y - 6):
            for x in range(person_x - 1, person_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['person_skin']
        
        # Cap
        for x in range(person_x - 2, person_x + 3):
            if 0 <= x < self.width and 0 <= person_y - 8 < self.height:
                frame[person_y - 8, x] = self.colors['person_cap']
        
        # Paddle (moving)
        paddle_angle = math.sin(self.paddle_timer * 0.2) * 0.3
        paddle_length = 8
        
        # Paddle handle
        for i in range(paddle_length):
            px = int(person_x + i * math.cos(paddle_angle))
            py = int(person_y - 4 + i * math.sin(paddle_angle))
            if 0 <= px < self.width and 0 <= py < self.height:
                frame[py, px] = self.colors['paddle']
        
        # Paddle blade
        blade_x = int(person_x + paddle_length * math.cos(paddle_angle))
        blade_y = int(person_y - 4 + paddle_length * math.sin(paddle_angle))
        for y in range(blade_y - 2, blade_y + 3):
            for x in range(blade_x - 1, blade_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['paddle']
    
    def create_shadow(self, frame, paddle_x_offset=0):
        """Create shadow of paddleboard and person on sand."""
        shadow_x = self.width // 2 + paddle_x_offset
        shadow_y = int(self.height * 0.8)
        
        # Board shadow
        for y in range(shadow_y - 3, shadow_y + 3):
            for x in range(shadow_x - 2, shadow_x + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Blend with sand
                    current = frame[y, x]
                    shadow = self.colors['shadow']
                    frame[y, x] = tuple(int(0.6 * c + 0.4 * s) for c, s in zip(current, shadow))
        
        # Person shadow
        for y in range(shadow_y, shadow_y + 4):
            for x in range(shadow_x - 1, shadow_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    current = frame[y, x]
                    shadow = self.colors['shadow']
                    frame[y, x] = tuple(int(0.5 * c + 0.5 * s) for c, s in zip(current, shadow))
    
    def create_sky(self, frame):
        """Create sky with sun and clouds."""
        # Sky background
        for y in range(int(self.height * 0.3)):
            for x in range(self.width):
                frame[y, x] = self.colors['sky']
        
        # Sun (moving slightly)
        sun_x = int(self.width * 0.8 + math.sin(self.sun_timer * 0.05) * 2)
        sun_y = int(self.height * 0.15)
        
        for y in range(sun_y - 2, sun_y + 3):
            for x in range(sun_x - 2, sun_x + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['sun']
        
        # Moving clouds
        cloud_positions = [
            (int(self.width * 0.2 + self.cloud_timer * 0.1) % self.width, int(self.height * 0.1)),
            (int(self.width * 0.6 + self.cloud_timer * 0.15) % self.width, int(self.height * 0.08)),
            (int(self.width * 0.4 + self.cloud_timer * 0.08) % self.width, int(self.height * 0.12))
        ]
        
        for cx, cy in cloud_positions:
            for y in range(cy - 1, cy + 2):
                for x in range(cx - 3, cx + 4):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        frame[y, x] = self.colors['cloud']
    
    def create_frame(self):
        """Create a complete frame of the paddleboarding scene."""
        frame = np.full((self.height, self.width, 3), self.colors['sky'], dtype=np.uint8)
        
        # Create scene elements
        self.create_sky(frame)
        self.create_water_ripples(frame)
        self.create_sand_bottom(frame)
        self.create_shadow(frame, int(math.sin(self.paddle_timer * 0.1) * 2))
        self.create_paddleboard(frame, int(math.sin(self.paddle_timer * 0.1) * 2))
        
        return frame
    
    def display_dudi_animation(self, duration=20):
        """Display the Dudi paddleboarding animation."""
        print("🏄‍♂️ Dudi Paddleboarding Animation 🏄‍♂️")
        print(f"Displaying for {duration} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create the frame
            frame = self.create_frame()
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.water_timer += 1
            self.paddle_timer += 1
            self.cloud_timer += 1
            self.sun_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Dudi paddleboarding animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run Dudi paddleboarding animation."""
    try:
        dudi = DudiPaddleboardingAnimation()
        dudi.display_dudi_animation(20)
        dudi.cleanup()
        
    except KeyboardInterrupt:
        print("\nDudi animation interrupted by user")
        dudi.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        dudi.cleanup()

if __name__ == "__main__":
    main() 