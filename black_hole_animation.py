#!/usr/bin/env python3
"""
Black Hole Animation for LED Board
Creates a mesmerizing black hole with swirling particles and gravitational effects
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class BlackHoleAnimation:
    def __init__(self):
        """Initialize the black hole animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Black hole colors
        self.colors = {
            'void': (0, 0, 0),           # Pure black center
            'event_horizon': (20, 0, 40), # Dark purple glow
            'accretion_disk': (255, 100, 0), # Orange/red hot gas
            'particles': (0, 255, 255),   # Cyan particles
            'background': (5, 5, 15)      # Dark blue space
        }
        
        # Animation parameters
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.black_hole_radius = 3
        self.event_horizon_radius = 8
        self.accretion_disk_radius = 15
        
    def create_black_hole_frame(self, time_step):
        """Create a single frame of the black hole animation."""
        # Create base frame with space background
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Calculate animation parameters
        swirl_angle = time_step * 0.3
        pulse_intensity = 0.5 + 0.3 * math.sin(time_step * 0.5)
        particle_phase = time_step * 0.8
        
        # Draw black hole center (void)
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
                
                if distance <= self.black_hole_radius:
                    # Pure black void
                    frame[y, x] = self.colors['void']
                
                elif distance <= self.event_horizon_radius:
                    # Event horizon glow
                    intensity = int(40 * pulse_intensity * (1 - distance / self.event_horizon_radius))
                    frame[y, x] = (intensity, 0, intensity * 2)
                
                elif distance <= self.accretion_disk_radius:
                    # Accretion disk with swirling effect
                    angle = math.atan2(y - self.center_y, x - self.center_x)
                    swirl_offset = math.sin(angle * 3 + swirl_angle) * 2
                    distance_with_swirl = distance + swirl_offset
                    
                    if distance_with_swirl <= self.accretion_disk_radius:
                        # Create swirling hot gas effect
                        intensity = int(255 * (1 - distance_with_swirl / self.accretion_disk_radius))
                        red = min(255, intensity + 50)
                        green = max(0, intensity - 100)
                        blue = max(0, intensity - 150)
                        frame[y, x] = (red, green, blue)
        
        # Add swirling particles
        self._add_swirling_particles(frame, particle_phase)
        
        # Add gravitational lensing effect
        self._add_gravitational_lensing(frame, time_step)
        
        return frame
    
    def _add_swirling_particles(self, frame, phase):
        """Add swirling particles around the black hole."""
        num_particles = 12
        
        for i in range(num_particles):
            # Calculate particle position in spiral
            angle = (i / num_particles) * 2 * math.pi + phase
            radius = 12 + 3 * math.sin(phase * 2 + i)
            
            x = int(self.center_x + radius * math.cos(angle))
            y = int(self.center_y + radius * math.sin(angle))
            
            # Ensure particle is within bounds
            if 0 <= x < self.width and 0 <= y < self.height:
                # Create particle with trail effect
                intensity = int(200 + 55 * math.sin(phase * 3 + i))
                frame[y, x] = (0, intensity, intensity)
                
                # Add smaller trail particles
                for trail in range(1, 3):
                    trail_angle = angle - trail * 0.2
                    trail_radius = radius - trail * 1.5
                    trail_x = int(self.center_x + trail_radius * math.cos(trail_angle))
                    trail_y = int(self.center_y + trail_radius * math.sin(trail_angle))
                    
                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        trail_intensity = max(0, intensity - trail * 80)
                        frame[trail_y, trail_x] = (0, trail_intensity, trail_intensity)
    
    def _add_gravitational_lensing(self, frame, time_step):
        """Add gravitational lensing effect (light bending around black hole)."""
        lensing_radius = 20
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
                
                if self.accretion_disk_radius < distance <= lensing_radius:
                    # Calculate lensing effect
                    angle = math.atan2(y - self.center_y, x - self.center_x)
                    lensing_strength = 0.3 * math.sin(time_step * 0.4 + angle * 2)
                    
                    # Distort the background slightly
                    distortion_x = int(x + lensing_strength * math.cos(angle))
                    distortion_y = int(y + lensing_strength * math.sin(angle))
                    
                    if 0 <= distortion_x < self.width and 0 <= distortion_y < self.height:
                        # Blend with original pixel
                        original = frame[y, x]
                        distorted = frame[distortion_y, distortion_x]
                        blend_factor = 0.7
                        
                        frame[y, x] = tuple(int(original[i] * blend_factor + distorted[i] * (1 - blend_factor)) 
                                          for i in range(3))
    
    def display_black_hole(self, duration=20):
        """Display the black hole animation."""
        print("Displaying Black Hole Animation...")
        print("Features: Swirling particles, gravitational lensing, event horizon glow")
        
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            # Create frame
            frame = self.create_black_hole_frame(frame_count * 0.1)
            
            # Display frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS for smooth animation
            frame_count += 1
        
        print("Black hole animation completed!")
    
    def display_black_hole_with_sound_effects(self, duration=30):
        """Display black hole with varying intensity (simulating sound effects)."""
        print("Displaying Black Hole with Dynamic Effects...")
        
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            # Add some random intensity variations
            time_step = frame_count * 0.1
            intensity_mod = 1.0 + 0.3 * math.sin(time_step * 0.7) + 0.1 * math.sin(time_step * 2.3)
            
            # Create frame with intensity modulation
            frame = self.create_black_hole_frame(time_step)
            
            # Apply intensity modulation
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    modulated_color = tuple(min(255, int(c * intensity_mod)) for c in color)
                    self.led.set_pixel(x, y, modulated_color)
            
            self.led.show()
            time.sleep(0.04)  # 25 FPS
            frame_count += 1
        
        print("Dynamic black hole animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run black hole animation."""
    try:
        black_hole = BlackHoleAnimation()
        
        print("🌌 Black Hole Animation 🌌")
        print("1. Standard black hole animation")
        print("2. Dynamic black hole with intensity variations")
        
        choice = input("Choose animation type (1 or 2): ").strip()
        
        if choice == "2":
            black_hole.display_black_hole_with_sound_effects(duration=25)
        else:
            black_hole.display_black_hole(duration=20)
        
        # Clean up
        black_hole.cleanup()
        
    except KeyboardInterrupt:
        print("\nBlack hole animation interrupted by user")
        black_hole.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        black_hole.cleanup()

if __name__ == "__main__":
    main() 