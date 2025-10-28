#!/usr/bin/env python3
"""
House Animation
A pixel-art style house with slowly rising smoke from the chimney
"""

import time
import math
import random
from led_controller_exact import LEDControllerExact

class HouseAnimation:
    def __init__(self):
        """Initialize the house animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        self.duration = 20  # 20 seconds total
        
        # Colors from the image
        self.gray_house = (200, 200, 200)  # Light gray house body
        self.red_roof = (236, 99, 88)      # #EC6358 - red roof
        self.brown_chimney = (139, 69, 19) # Brown chimney
        self.light_gray_window_frame = (180, 180, 180)  # Light gray window frame
        self.blue_window = (0, 100, 200)   # Bright blue window panes
        self.white_smoke = (255, 255, 255) # White smoke
        self.light_smoke = (240, 240, 240) # Light gray smoke
        
        # House dimensions and position
        self.house_x = 8   # Left edge of house
        self.house_y = 30  # Bottom of house
        self.house_width = 16
        self.house_height = 18
        
        # Roof dimensions
        self.roof_height = 8
        
        # Chimney dimensions
        self.chimney_x = 20
        self.chimney_y = 26
        self.chimney_width = 3
        self.chimney_height = 6
        
        # Window dimensions
        self.window_x = 12
        self.window_y = 36
        self.window_size = 4
        
        # Smoke particles
        self.smoke_particles = []
        self.smoke_start_time = 2  # Start smoke after 2 seconds
        
    def draw_house_body(self):
        """Draw the main house body (gray rectangle)."""
        for y in range(self.house_height):
            for x in range(self.house_width):
                pixel_x = self.house_x + x
                pixel_y = self.house_y - y
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    self.led.set_pixel(pixel_x, pixel_y, self.gray_house)
    
    def draw_roof(self):
        """Draw the triangular roof."""
        roof_top_y = self.house_y - self.house_height
        roof_bottom_y = roof_top_y + self.roof_height
        
        for y in range(roof_top_y, roof_bottom_y):
            # Calculate roof width at this height
            height_from_top = y - roof_top_y
            roof_width_at_height = self.house_width - (height_from_top * 2)
            
            if roof_width_at_height > 0:
                roof_start_x = self.house_x + height_from_top
                roof_end_x = roof_start_x + roof_width_at_height
                
                for x in range(roof_start_x, roof_end_x):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.led.set_pixel(x, y, self.red_roof)
    
    def draw_chimney(self):
        """Draw the brown chimney."""
        for y in range(self.chimney_height):
            for x in range(self.chimney_width):
                pixel_x = self.chimney_x + x
                pixel_y = self.chimney_y - y
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    self.led.set_pixel(pixel_x, pixel_y, self.brown_chimney)
    
    def draw_window(self):
        """Draw the window with frame and panes."""
        # Draw window frame
        for y in range(self.window_size + 2):
            for x in range(self.window_size + 2):
                pixel_x = self.window_x - 1 + x
                pixel_y = self.window_y - 1 + y
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    # Frame
                    if x == 0 or x == self.window_size + 1 or y == 0 or y == self.window_size + 1:
                        self.led.set_pixel(pixel_x, pixel_y, self.light_gray_window_frame)
                    # Window panes
                    else:
                        self.led.set_pixel(pixel_x, pixel_y, self.blue_window)
        
        # Draw cross frame
        center_x = self.window_x + self.window_size // 2
        center_y = self.window_y + self.window_size // 2
        
        # Vertical line
        for y in range(self.window_y, self.window_y + self.window_size):
            if 0 <= center_x < self.width and 0 <= y < self.height:
                self.led.set_pixel(center_x, y, self.light_gray_window_frame)
        
        # Horizontal line
        for x in range(self.window_x, self.window_x + self.window_size):
            if 0 <= x < self.width and 0 <= center_y < self.height:
                self.led.set_pixel(x, center_y, self.light_gray_window_frame)
    
    def add_smoke_particle(self):
        """Add a new smoke particle at the chimney top."""
        particle = {
            'x': self.chimney_x + self.chimney_width // 2 + random.uniform(-0.5, 0.5),
            'y': self.chimney_y - self.chimney_height,
            'life': 1.0,
            'speed': random.uniform(0.3, 0.6),
            'drift': random.uniform(-0.2, 0.2)
        }
        self.smoke_particles.append(particle)
    
    def update_smoke(self, elapsed):
        """Update smoke particles."""
        # Add new smoke particles
        if elapsed >= self.smoke_start_time:
            if random.random() < 0.3:  # 30% chance each frame
                self.add_smoke_particle()
        
        # Update existing particles
        particles_to_remove = []
        for i, particle in enumerate(self.smoke_particles):
            # Move particle up and drift sideways
            particle['y'] -= particle['speed']
            particle['x'] += particle['drift']
            particle['life'] -= 0.02  # Fade out
            
            # Remove particles that are off-screen or faded
            if (particle['y'] < 0 or particle['life'] <= 0 or 
                particle['x'] < 0 or particle['x'] >= self.width):
                particles_to_remove.append(i)
        
        # Remove dead particles (in reverse order to maintain indices)
        for i in reversed(particles_to_remove):
            self.smoke_particles.pop(i)
    
    def draw_smoke(self):
        """Draw all smoke particles."""
        for particle in self.smoke_particles:
            x = int(particle['x'])
            y = int(particle['y'])
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Fade smoke based on life
                if particle['life'] > 0.7:
                    color = self.white_smoke
                else:
                    color = self.light_smoke
                
                self.led.set_pixel(x, y, color)
                
                # Draw a small smoke puff (2x2 pixels)
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        smoke_x = x + dx
                        smoke_y = y + dy
                        if (0 <= smoke_x < self.width and 0 <= smoke_y < self.height and
                            random.random() < 0.6):  # Random smoke texture
                            self.led.set_pixel(smoke_x, smoke_y, color)
    
    def run_animation(self):
        """Run the complete house animation."""
        print("🏠 Starting House Animation...")
        print(f"Duration: {self.duration} seconds")
        print("Smoke will start rising after 2 seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < self.duration:
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Draw house components
            self.draw_house_body()
            self.draw_roof()
            self.draw_chimney()
            self.draw_window()
            
            # Update and draw smoke
            self.update_smoke(elapsed)
            self.draw_smoke()
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Keep final frame for a moment
        print("🏠 House Animation completed!")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
        print("🏠 Animation finished")

def main():
    """Main function to run the house animation."""
    try:
        animation = HouseAnimation()
        animation.run_animation()
    except KeyboardInterrupt:
        print("\n🏠 Animation interrupted by user")
    except Exception as e:
        print(f"❌ Error running animation: {e}")

if __name__ == "__main__":
    main()
