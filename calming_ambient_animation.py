#!/usr/bin/env python3
"""
Calming Ambient Animation for LED Board
Features soft colors, gentle flowing shapes, and peaceful visual effects
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class CalmingAmbientAnimation:
    def __init__(self):
        """Initialize the calming ambient animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Soft, calming color palette
        self.colors = {
            'background': (10, 15, 25),      # Deep blue-black
            'lavender': (230, 230, 250),     # Soft lavender
            'sage': (200, 220, 200),         # Gentle sage green
            'peach': (255, 218, 185),        # Soft peach
            'mint': (180, 220, 200),         # Mint green
            'rose': (255, 192, 203),         # Soft rose pink
            'cream': (255, 253, 240),        # Warm cream
            'sky_blue': (176, 196, 222),     # Light sky blue
            'purple_mist': (221, 160, 221),  # Soft purple
            'golden_hour': (255, 228, 196),  # Golden hour light
            'twilight': (119, 136, 153),     # Twilight blue-gray
            'moonlight': (248, 248, 255),    # Moonlight white
            'aurora_green': (152, 251, 152), # Aurora green
            'aurora_blue': (173, 216, 230),  # Aurora blue
            'aurora_purple': (221, 160, 221) # Aurora purple
        }
        
        # Animation parameters
        self.time = 0
        self.flow_timer = 0
        self.pulse_timer = 0
        self.aurora_timer = 0
        
    def create_flowing_shapes(self, frame):
        """Create gentle flowing organic shapes."""
        for y in range(self.height):
            for x in range(self.width):
                # Create flowing wave patterns
                wave1 = math.sin((x + self.flow_timer * 0.3) * 0.2) * 0.5
                wave2 = math.sin((y + self.flow_timer * 0.2) * 0.15) * 0.5
                wave3 = math.sin((x + y + self.flow_timer * 0.1) * 0.1) * 0.3
                
                combined_wave = wave1 + wave2 + wave3
                
                # Create organic blob shapes
                center_x = self.width // 2
                center_y = self.height // 2
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                # Soft circular gradient
                radius = 15 + math.sin(self.time * 0.05) * 3
                if distance < radius:
                    intensity = 1 - (distance / radius)
                    intensity = max(0, intensity)
                    
                    # Blend colors based on position and time
                    color_mix = (math.sin(self.time * 0.02 + x * 0.1) + 1) / 2
                    
                    if color_mix < 0.33:
                        color = self.colors['lavender']
                    elif color_mix < 0.66:
                        color = self.colors['sage']
                    else:
                        color = self.colors['peach']
                    
                    # Apply wave distortion
                    wave_offset = combined_wave * 0.3
                    final_intensity = max(0, intensity + wave_offset)
                    
                    # Blend with background
                    bg_color = self.colors['background']
                    final_color = tuple(int(bg + (c - bg) * final_intensity * 0.7) 
                                      for bg, c in zip(bg_color, color))
                    frame[y, x] = final_color
    
    def create_aurora_effect(self, frame):
        """Create aurora-like flowing light effects."""
        for y in range(self.height):
            for x in range(self.width):
                # Aurora wave patterns
                aurora1 = math.sin((x + self.aurora_timer * 0.4) * 0.3) * 0.6
                aurora2 = math.sin((y + self.aurora_timer * 0.3) * 0.2) * 0.4
                aurora3 = math.sin((x - y + self.aurora_timer * 0.2) * 0.15) * 0.3
                
                aurora_intensity = (aurora1 + aurora2 + aurora3) / 3
                
                if aurora_intensity > 0.2:
                    # Aurora colors
                    color_phase = (self.aurora_timer * 0.1 + x * 0.1) % (2 * math.pi)
                    
                    if color_phase < math.pi / 3:
                        aurora_color = self.colors['aurora_green']
                    elif color_phase < 2 * math.pi / 3:
                        aurora_color = self.colors['aurora_blue']
                    else:
                        aurora_color = self.colors['aurora_purple']
                    
                    # Blend with existing frame
                    current = frame[y, x]
                    blend_factor = (aurora_intensity - 0.2) * 0.4
                    frame[y, x] = tuple(int(c + (a - c) * blend_factor) 
                                      for c, a in zip(current, aurora_color))
    
    def create_breathing_circles(self, frame):
        """Create breathing circle effects."""
        # Multiple breathing circles
        circle_centers = [
            (self.width // 4, self.height // 3),
            (3 * self.width // 4, 2 * self.height // 3),
            (self.width // 2, self.height // 4),
            (self.width // 3, 3 * self.height // 4)
        ]
        
        for i, (cx, cy) in enumerate(circle_centers):
            # Breathing cycle
            breath_cycle = math.sin(self.pulse_timer * 0.1 + i * math.pi / 2)
            radius = 3 + breath_cycle * 2
            
            # Circle colors
            circle_colors = [self.colors['mint'], self.colors['rose'], 
                           self.colors['sky_blue'], self.colors['purple_mist']]
            color = circle_colors[i % len(circle_colors)]
            
            # Draw breathing circle
            for y in range(self.height):
                for x in range(self.width):
                    distance = math.sqrt((x - cx)**2 + (y - cy)**2)
                    if distance < radius:
                        intensity = 1 - (distance / radius)
                        intensity = max(0, intensity)
                        
                        # Blend with existing frame
                        current = frame[y, x]
                        frame[y, x] = tuple(int(c + (col - c) * intensity * 0.3) 
                                          for c, col in zip(current, color))
    
    def create_floating_particles(self, frame):
        """Create gentle floating particles."""
        num_particles = 8
        for i in range(num_particles):
            # Particle movement
            particle_x = (self.width // 2 + 
                         math.sin(self.time * 0.02 + i * 0.8) * self.width * 0.3)
            particle_y = (self.height // 2 + 
                         math.cos(self.time * 0.015 + i * 0.6) * self.height * 0.3)
            
            # Particle pulsing
            pulse = math.sin(self.time * 0.1 + i) * 0.5 + 0.5
            
            # Particle colors
            particle_colors = [self.colors['moonlight'], self.colors['cream'], 
                             self.colors['golden_hour']]
            color = particle_colors[i % len(particle_colors)]
            
            # Draw particle
            px, py = int(particle_x), int(particle_y)
            if 0 <= px < self.width and 0 <= py < self.height:
                # Soft particle glow
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        glow_x, glow_y = px + dx, py + dy
                        if 0 <= glow_x < self.width and 0 <= glow_y < self.height:
                            glow_intensity = pulse * (1 - (abs(dx) + abs(dy)) * 0.3)
                            glow_intensity = max(0, glow_intensity)
                            
                            current = frame[glow_y, glow_x]
                            frame[glow_y, glow_x] = tuple(int(c + (col - c) * glow_intensity * 0.4) 
                                                        for c, col in zip(current, color))
    
    def create_gradient_background(self, frame):
        """Create a subtle gradient background."""
        for y in range(self.height):
            for x in range(self.width):
                # Vertical gradient
                vertical_gradient = y / self.height
                
                # Horizontal gradient
                horizontal_gradient = x / self.width
                
                # Combine gradients
                gradient = (vertical_gradient + horizontal_gradient) / 2
                
                # Subtle color variation
                color_variation = math.sin(self.time * 0.01 + x * 0.1 + y * 0.1) * 0.1
                
                # Base background color
                base_color = self.colors['background']
                
                # Add subtle variation
                frame[y, x] = tuple(int(c * (0.8 + gradient * 0.2 + color_variation)) 
                                  for c in base_color)
    
    def create_frame(self):
        """Create a complete calming ambient frame."""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create scene elements
        self.create_gradient_background(frame)
        self.create_flowing_shapes(frame)
        self.create_aurora_effect(frame)
        self.create_breathing_circles(frame)
        self.create_floating_particles(frame)
        
        return frame
    
    def display_calming_animation(self, duration=30):
        """Display the calming ambient animation."""
        print("🧘‍♀️ Calming Ambient Animation 🧘‍♀️")
        print(f"Displaying for {duration} seconds...")
        print("Features: Soft colors, flowing shapes, breathing circles, aurora effects")
        
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
            self.time += 1
            self.flow_timer += 1
            self.pulse_timer += 1
            self.aurora_timer += 1
            
            time.sleep(0.08)  # ~12 FPS for smooth, calming motion
        
        print("Calming ambient animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run calming ambient animation."""
    try:
        ambient = CalmingAmbientAnimation()
        ambient.display_calming_animation(30)
        ambient.cleanup()
        
    except KeyboardInterrupt:
        print("\nCalming animation interrupted by user")
        ambient.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        ambient.cleanup()

if __name__ == "__main__":
    main() 