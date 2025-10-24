#!/usr/bin/env python3
"""
Floating Clouds Animation for LED Board
Soft, gentle clouds drifting across a peaceful sky
"""

import time
import numpy as np
import math
import random
from led_controller_exact import LEDControllerExact
import config

class FloatingCloudsAnimation:
    def __init__(self):
        """Initialize the floating clouds animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Soft, calming colors
        self.colors = {
            'sky': (135, 206, 235),        # Sky blue
            'cloud_white': (248, 248, 255), # Soft white
            'cloud_light': (240, 248, 255), # Light cloud
            'cloud_shadow': (230, 240, 250), # Cloud shadow
        }
        
        # Animation parameters
        self.animation_timer = 0
        self.duration = 30  # seconds
        self.clouds = []
        
        # Initialize clouds
        self._create_clouds()
        
    def _create_clouds(self):
        """Create initial cloud formations."""
        # Create 3-5 clouds at different positions
        num_clouds = random.randint(3, 5)
        
        for _ in range(num_clouds):
            cloud = {
                'x': random.randint(-10, self.width + 10),  # Start off-screen
                'y': random.randint(10, self.height - 10),  # Different heights
                'size': random.randint(8, 15),              # Cloud size
                'speed': random.uniform(0.3, 0.8),          # Slow drift speed
                'shape_variation': random.uniform(0.5, 1.5), # Shape variation
                'opacity': random.uniform(0.7, 0.9),        # Cloud opacity
                'drift_phase': random.uniform(0, 2 * math.pi) # Drift variation
            }
            self.clouds.append(cloud)
    
    def create_sky_background(self, frame):
        """Create a soft sky background."""
        # Create gradient sky from top to bottom
        for y in range(self.height):
            # Sky gets slightly darker toward the bottom
            sky_intensity = 1.0 - (y / self.height) * 0.2
            sky_color = tuple(int(c * sky_intensity) for c in self.colors['sky'])
            
            for x in range(self.width):
                frame[y, x] = sky_color
    
    def create_cloud(self, frame, cloud):
        """Create a single cloud with soft, organic shape."""
        center_x = int(cloud['x'])
        center_y = int(cloud['y'])
        size = cloud['size']
        
        # Add gentle drift motion
        drift_x = math.sin(cloud['drift_phase'] + self.animation_timer * 0.02) * 2
        drift_y = math.cos(cloud['drift_phase'] + self.animation_timer * 0.015) * 1
        
        center_x += int(drift_x)
        center_y += int(drift_y)
        
        # Create organic cloud shape
        for y in range(max(0, center_y - size), min(self.height, center_y + size)):
            for x in range(max(0, center_x - size), min(self.width, center_x + size)):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Create organic cloud shape with noise
                noise = math.sin(x * 0.3 + y * 0.2 + self.animation_timer * 0.1) * 0.3
                cloud_radius = size * (0.8 + noise)
                
                if distance <= cloud_radius:
                    # Calculate cloud opacity based on distance
                    opacity = 1.0 - (distance / cloud_radius) * 0.5
                    opacity *= cloud['opacity']
                    
                    # Choose cloud color based on position
                    if (x + y) % 3 == 0:
                        base_color = self.colors['cloud_white']
                    elif (x + y) % 3 == 1:
                        base_color = self.colors['cloud_light']
                    else:
                        base_color = self.colors['cloud_shadow']
                    
                    # Apply opacity
                    cloud_color = tuple(int(c * opacity) for c in base_color)
                    
                    # Blend with sky
                    current_sky = frame[y, x]
                    blended_color = tuple(
                        int(s + (c - s) * opacity) 
                        for s, c in zip(current_sky, cloud_color)
                    )
                    frame[y, x] = blended_color
    
    def update_clouds(self):
        """Update cloud positions with gentle movement."""
        for cloud in self.clouds:
            # Move cloud slowly across screen
            cloud['x'] += cloud['speed']
            
            # Add gentle vertical drift
            cloud['y'] += math.sin(self.animation_timer * 0.01 + cloud['drift_phase']) * 0.2
            
            # Reset cloud position when it goes off screen
            if cloud['x'] > self.width + 20:
                cloud['x'] = -20
                cloud['y'] = random.randint(10, self.height - 10)
    
    def create_frame(self):
        """Create a single frame of the floating clouds animation."""
        # Start with sky background
        frame = np.full((self.height, self.width, 3), self.colors['sky'], dtype=np.uint8)
        self.create_sky_background(frame)
        
        # Add clouds
        for cloud in self.clouds:
            self.create_cloud(frame, cloud)
        
        return frame
    
    def display_floating_clouds(self, duration=30):
        """Display the floating clouds animation."""
        print("☁️ Floating Clouds Animation ☁️")
        print(f"Displaying for {duration} seconds...")
        print("Features: Soft clouds, gentle drift, calming sky")
        
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
            
            # Update cloud positions
            self.update_clouds()
            
            # Update animation parameters
            self.animation_timer += 1
            
            time.sleep(0.1)  # 10 FPS for gentle movement
        
        print("Floating clouds animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run floating clouds animation."""
    try:
        clouds = FloatingCloudsAnimation()
        clouds.display_floating_clouds(30)
        clouds.cleanup()
        
    except KeyboardInterrupt:
        print("\nFloating clouds animation interrupted by user")
        clouds.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        clouds.cleanup()

if __name__ == "__main__":
    main()
