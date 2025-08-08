#!/usr/bin/env python3
"""
Shark Animation for LED Board
Features a realistic shark swimming through underwater scenes
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class SharkAnimation:
    def __init__(self):
        """Initialize the shark animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'ocean_deep': (0, 50, 100),     # Deep ocean blue
            'ocean_light': (0, 100, 150),   # Light ocean blue
            'ocean_surface': (0, 150, 200), # Surface water
            'shark_body': (64, 64, 64),     # Dark gray shark
            'shark_belly': (128, 128, 128), # Light gray belly
            'shark_fin': (32, 32, 32),      # Dark fin
            'shark_eye': (255, 255, 255),   # White eye
            'shark_pupil': (0, 0, 0),       # Black pupil
            'bubble': (200, 220, 255),      # Light blue bubbles
            'bubble_small': (220, 240, 255), # Smaller bubbles
            'seaweed': (34, 139, 34),       # Green seaweed
            'coral': (255, 127, 80),        # Orange coral
            'sand': (238, 203, 173),        # Sandy bottom
            'fish': (255, 215, 0),          # Golden fish
            'fish_silver': (192, 192, 192), # Silver fish
            'shark_teeth': (255, 255, 255), # White teeth
            'shark_gills': (100, 100, 100)  # Shark gills
        }
        
        # Animation parameters
        self.shark_x = -10  # Start off-screen
        self.shark_y = self.height // 2
        self.shark_direction = 1  # 1 for right, -1 for left
        self.bubble_timer = 0
        self.fish_timer = 0
        self.water_timer = 0
        
    def create_ocean_background(self, frame):
        """Create ocean background with depth gradient."""
        for y in range(self.height):
            for x in range(self.width):
                # Ocean depth gradient
                depth_factor = y / self.height
                
                if depth_factor < 0.3:  # Surface
                    frame[y, x] = self.colors['ocean_surface']
                elif depth_factor < 0.7:  # Mid-depth
                    frame[y, x] = self.colors['ocean_light']
                else:  # Deep ocean
                    frame[y, x] = self.colors['ocean_deep']
                
                # Add subtle water movement
                water_wave = math.sin((x + self.water_timer * 0.3) * 0.2) * 0.1
                current_color = frame[y, x]
                frame[y, x] = tuple(int(c * (1 + water_wave)) for c in current_color)
    
    def create_sand_bottom(self, frame):
        """Create sandy ocean floor."""
        for y in range(int(self.height * 0.8), self.height):
            for x in range(self.width):
                # Sandy bottom with texture
                sand_texture = math.sin(x * 0.3) * 0.1 + math.sin(y * 0.2) * 0.1
                sand_color = tuple(int(c * (0.8 + sand_texture)) for c in self.colors['sand'])
                
                # Blend with ocean
                ocean_color = frame[y, x]
                frame[y, x] = tuple(int(0.7 * o + 0.3 * s) for o, s in zip(ocean_color, sand_color))
    
    def create_seaweed(self, frame):
        """Create swaying seaweed."""
        seaweed_positions = [5, 12, 20, 27]
        
        for x in seaweed_positions:
            # Seaweed swaying
            sway = math.sin(self.water_timer * 0.2 + x * 0.5) * 0.3
            sway_x = x + int(sway)
            
            # Draw seaweed
            for y in range(int(self.height * 0.7), self.height):
                seaweed_y = y - int(self.height * 0.7)
                if seaweed_y < 8:  # Limit seaweed height
                    if 0 <= sway_x < self.width and 0 <= y < self.height:
                        # Seaweed color variation
                        seaweed_color = tuple(int(c * (0.8 + seaweed_y * 0.1)) for c in self.colors['seaweed'])
                        frame[y, sway_x] = seaweed_color
    
    def create_coral(self, frame):
        """Create coral formations."""
        coral_positions = [(8, int(self.height * 0.75)), (24, int(self.height * 0.78))]
        
        for cx, cy in coral_positions:
            # Coral swaying
            coral_sway = math.sin(self.water_timer * 0.15 + cx * 0.3) * 0.2
            coral_x = cx + int(coral_sway)
            
            # Draw coral
            for y in range(cy, min(cy + 6, self.height)):
                for x in range(coral_x - 1, coral_x + 2):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        coral_color = tuple(int(c * (0.9 + (y - cy) * 0.05)) for c in self.colors['coral'])
                        frame[y, x] = coral_color
    
    def create_bubbles(self, frame):
        """Create rising bubbles."""
        # Static bubbles
        bubble_positions = [
            (3, 35), (7, 32), (15, 38), (22, 35), (28, 30),
            (5, 25), (18, 28), (25, 25), (10, 20), (30, 22)
        ]
        
        for x, y in bubble_positions:
            # Bubble rising animation
            rise_y = int(y - (self.bubble_timer * 0.1) % 20)
            if 0 <= x < self.width and 0 <= rise_y < self.height:
                # Bubble pulsing
                pulse = math.sin(self.bubble_timer * 0.3 + x + y) * 0.3 + 0.7
                bubble_color = tuple(int(c * pulse) for c in self.colors['bubble'])
                frame[rise_y, x] = bubble_color
        
        # Small bubbles from shark
        if self.shark_x > 0 and self.shark_x < self.width:
            for i in range(3):
                bubble_x = int(self.shark_x + math.sin(self.bubble_timer * 0.5 + i) * 2)
                bubble_y = int(self.shark_y + 3 - (self.bubble_timer * 0.2 + i * 2) % 10)
                if 0 <= bubble_x < self.width and 0 <= bubble_y < self.height:
                    frame[bubble_y, bubble_x] = self.colors['bubble_small']
    
    def create_fish(self, frame):
        """Create small fish swimming."""
        fish_positions = [
            (int(self.width * 0.2), int(self.height * 0.3)),
            (int(self.width * 0.7), int(self.height * 0.6)),
            (int(self.width * 0.4), int(self.height * 0.4))
        ]
        
        for i, (fx, fy) in enumerate(fish_positions):
            # Fish swimming motion
            fish_x = int(fx + math.sin(self.fish_timer * 0.1 + i) * 3)
            fish_y = int(fy + math.cos(self.fish_timer * 0.15 + i) * 2)
            
            if 0 <= fish_x < self.width and 0 <= fish_y < self.height:
                # Fish color
                fish_color = self.colors['fish'] if i % 2 == 0 else self.colors['fish_silver']
                frame[fish_y, fish_x] = fish_color
                
                # Fish tail
                tail_x = fish_x - 1 if fish_x > 0 else fish_x
                if 0 <= tail_x < self.width and 0 <= fish_y < self.height:
                    frame[fish_y, tail_x] = fish_color
    
    def create_shark(self, frame):
        """Create the shark swimming."""
        if self.shark_x < -15:  # Reset shark position
            self.shark_x = -10
            self.shark_direction = 1
        elif self.shark_x > self.width + 15:  # Shark exits screen
            self.shark_x = self.width + 10
            self.shark_direction = -1
        
        # Move shark
        self.shark_x += self.shark_direction * 0.8
        
        # Shark body (main body)
        shark_length = 12
        shark_height = 4
        
        for y in range(self.height):
            for x in range(self.width):
                # Shark body position
                shark_center_x = int(self.shark_x)
                shark_center_y = int(self.shark_y)
                
                # Check if pixel is within shark body
                dx = abs(x - shark_center_x)
                dy = abs(y - shark_center_y)
                
                if dx <= shark_length // 2 and dy <= shark_height // 2:
                    # Shark body shape (elliptical)
                    if (dx / (shark_length // 2))**2 + (dy / (shark_height // 2))**2 <= 1:
                        # Belly (lighter)
                        if dy > 0 and y > shark_center_y:
                            frame[y, x] = self.colors['shark_belly']
                        else:
                            frame[y, x] = self.colors['shark_body']
        
        # Shark tail
        tail_x = shark_center_x + (shark_length // 2 + 2) * self.shark_direction
        tail_y = shark_center_y
        if 0 <= tail_x < self.width and 0 <= tail_y < self.height:
            frame[tail_y, tail_x] = self.colors['shark_body']
            # Tail fin
            for dy in range(-2, 3):
                tail_fin_y = tail_y + dy
                if 0 <= tail_fin_y < self.height:
                    frame[tail_fin_y, tail_x] = self.colors['shark_fin']
        
        # Shark dorsal fin
        fin_x = shark_center_x
        fin_y = shark_center_y - shark_height // 2 - 2
        if 0 <= fin_x < self.width and 0 <= fin_y < self.height:
            frame[fin_y, fin_x] = self.colors['shark_fin']
            # Fin shape
            for dx in range(-1, 2):
                fin_side_x = fin_x + dx
                if 0 <= fin_side_x < self.width and 0 <= fin_y < self.height:
                    frame[fin_y, fin_side_x] = self.colors['shark_fin']
        
        # Shark head
        head_x = shark_center_x - (shark_length // 2 + 1) * self.shark_direction
        head_y = shark_center_y
        if 0 <= head_x < self.width and 0 <= head_y < self.height:
            frame[head_y, head_x] = self.colors['shark_body']
        
        # Shark eyes
        eye_x = head_x + self.shark_direction
        eye_y = head_y - 1
        if 0 <= eye_x < self.width and 0 <= eye_y < self.height:
            frame[eye_y, eye_x] = self.colors['shark_eye']
            # Pupil
            frame[eye_y, eye_x] = self.colors['shark_pupil']
        
        # Shark gills
        gill_x = head_x + 2 * self.shark_direction
        gill_y = head_y
        if 0 <= gill_x < self.width and 0 <= gill_y < self.height:
            frame[gill_y, gill_x] = self.colors['shark_gills']
    
    def create_frame(self):
        """Create a complete shark animation frame."""
        frame = np.full((self.height, self.width, 3), self.colors['ocean_deep'], dtype=np.uint8)
        
        # Create scene elements
        self.create_ocean_background(frame)
        self.create_sand_bottom(frame)
        self.create_seaweed(frame)
        self.create_coral(frame)
        self.create_bubbles(frame)
        self.create_fish(frame)
        self.create_shark(frame)
        
        return frame
    
    def display_shark_animation(self, duration=25):
        """Display the shark animation."""
        print("🦈 Shark Animation 🦈")
        print(f"Displaying for {duration} seconds...")
        print("Features: Swimming shark, underwater scene, bubbles, fish, seaweed")
        
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
            self.bubble_timer += 1
            self.fish_timer += 1
            self.water_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Shark animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run shark animation."""
    try:
        shark = SharkAnimation()
        shark.display_shark_animation(25)
        shark.cleanup()
        
    except KeyboardInterrupt:
        print("\nShark animation interrupted by user")
        shark.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        shark.cleanup()

if __name__ == "__main__":
    main() 