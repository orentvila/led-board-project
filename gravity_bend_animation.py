#!/usr/bin/env python3
"""
Gravity Bend Animation for LED Board
Creates a 2D space-time visualization showing gravitational bending
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class GravityBendAnimation:
    def __init__(self):
        """Initialize the gravity bend animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'space': (5, 5, 20),         # Dark blue space
            'grid': (50, 100, 200),      # Light blue grid lines
            'gravity_well': (255, 0, 0), # Red gravitational source
            'bent_grid': (100, 150, 255), # Bright blue bent grid
            'particles': (255, 255, 0),  # Yellow particles
            'event_horizon': (255, 100, 0), # Orange event horizon
            'warp_field': (150, 50, 255) # Purple warp field
        }
        
        # Animation parameters
        self.gravity_strength = 0
        self.particle_positions = []
        self.grid_spacing = 4
        
    def create_gravity_frame(self, time_step):
        """Create a single frame of the gravity bend animation."""
        # Create base frame with space background
        frame = np.full((self.height, self.width, 3), self.colors['space'], dtype=np.uint8)
        
        # Calculate animation parameters
        self.gravity_strength = 2 + math.sin(time_step * 0.3) * 1.5
        gravity_center_x = self.width // 2
        gravity_center_y = self.height // 2
        
        # Draw gravitational source
        self._draw_gravity_source(frame, gravity_center_x, gravity_center_y, time_step)
        
        # Draw bent grid
        self._draw_bent_grid(frame, gravity_center_x, gravity_center_y, time_step)
        
        # Draw particles falling into gravity well
        self._draw_falling_particles(frame, gravity_center_x, gravity_center_y, time_step)
        
        # Draw event horizon
        self._draw_event_horizon(frame, gravity_center_x, gravity_center_y, time_step)
        
        # Add space-time distortion effects
        self._add_warp_effects(frame, gravity_center_x, gravity_center_y, time_step)
        
        return frame
    
    def _draw_gravity_source(self, frame, center_x, center_y, time_step):
        """Draw the gravitational source (black hole/star)."""
        # Pulsing gravitational source
        pulse = 0.5 + 0.3 * math.sin(time_step * 0.8)
        radius = int(3 * pulse)
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if distance <= radius:
                    # Create glowing effect
                    intensity = int(255 * (1 - distance / radius) * pulse)
                    frame[y, x] = (intensity, 0, 0)
                
                elif distance <= radius + 2:
                    # Outer glow
                    glow_intensity = int(100 * (1 - (distance - radius) / 2) * pulse)
                    frame[y, x] = (glow_intensity, 0, glow_intensity // 2)
    
    def _draw_bent_grid(self, frame, center_x, center_y, time_step):
        """Draw the bent space-time grid."""
        # Draw vertical grid lines
        for x in range(0, self.width, self.grid_spacing):
            self._draw_bent_line(frame, x, 0, x, self.height, center_x, center_y, time_step, 'vertical')
        
        # Draw horizontal grid lines
        for y in range(0, self.height, self.grid_spacing):
            self._draw_bent_line(frame, 0, y, self.width, y, center_x, center_y, time_step, 'horizontal')
    
    def _draw_bent_line(self, frame, x1, y1, x2, y2, center_x, center_y, time_step, direction):
        """Draw a bent line that curves around the gravitational source."""
        steps = max(abs(x2 - x1), abs(y2 - y1)) * 2
        
        for i in range(steps + 1):
            t = i / steps
            
            if direction == 'vertical':
                # Vertical line
                x = x1
                y = y1 + (y2 - y1) * t
            else:
                # Horizontal line
                x = x1 + (x2 - x1) * t
                y = y1
            
            # Calculate gravitational bending
            dx = x - center_x
            dy = y - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Calculate bending effect
                bend_strength = self.gravity_strength / (distance + 1)
                bend_strength = min(bend_strength, 3.0)  # Limit maximum bending
                
                # Apply bending
                if direction == 'vertical':
                    x_bent = x + bend_strength * math.sin(time_step * 0.5 + distance * 0.1)
                    y_bent = y
                else:
                    x_bent = x
                    y_bent = y + bend_strength * math.sin(time_step * 0.5 + distance * 0.1)
                
                # Draw the bent point
                x_int = int(x_bent)
                y_int = int(y_bent)
                
                if 0 <= x_int < self.width and 0 <= y_int < self.height:
                    # Color based on bending strength
                    if bend_strength > 1.0:
                        frame[y_int, x_int] = self.colors['bent_grid']
                    else:
                        frame[y_int, x_int] = self.colors['grid']
    
    def _draw_falling_particles(self, frame, center_x, center_y, time_step):
        """Draw particles falling into the gravity well."""
        num_particles = 8
        
        for i in range(num_particles):
            # Calculate particle orbit
            angle = (i / num_particles) * 2 * math.pi + time_step * 0.3
            base_radius = 15 + 5 * math.sin(time_step * 0.2 + i)
            
            # Spiral inward effect
            spiral_factor = math.exp(-time_step * 0.1) * 0.8 + 0.2
            radius = base_radius * spiral_factor
            
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            if 0 <= x < self.width and 0 <= y < self.height:
                # Particle with trail
                intensity = int(200 + 55 * math.sin(time_step * 2 + i))
                frame[y, x] = (intensity, intensity, 0)
                
                # Add trail
                for trail in range(1, 4):
                    trail_angle = angle - trail * 0.1
                    trail_radius = radius + trail * 0.5
                    trail_x = int(center_x + trail_radius * math.cos(trail_angle))
                    trail_y = int(center_y + trail_radius * math.sin(trail_angle))
                    
                    if 0 <= trail_x < self.width and 0 <= trail_y < self.height:
                        trail_intensity = max(0, intensity - trail * 50)
                        frame[trail_y, trail_x] = (trail_intensity, trail_intensity, 0)
    
    def _draw_event_horizon(self, frame, center_x, center_y, time_step):
        """Draw the event horizon around the gravitational source."""
        event_radius = 6 + math.sin(time_step * 0.4) * 1
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if event_radius - 1 <= distance <= event_radius + 1:
                    # Event horizon ring
                    ring_intensity = int(150 + 100 * math.sin(time_step * 0.6 + distance * 0.5))
                    frame[y, x] = (ring_intensity, ring_intensity // 2, 0)
    
    def _add_warp_effects(self, frame, center_x, center_y, time_step):
        """Add space-time warp effects."""
        warp_radius = 20
        
        for y in range(self.height):
            for x in range(self.width):
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if 8 <= distance <= warp_radius:
                    # Calculate warp distortion
                    angle = math.atan2(y - center_y, x - center_x)
                    warp_strength = 0.5 * math.sin(time_step * 0.3 + angle * 3)
                    
                    # Create ripple effect
                    ripple = math.sin(distance * 0.3 - time_step * 0.5) * 0.3
                    
                    # Apply subtle color shift
                    original_color = frame[y, x]
                    if not np.array_equal(original_color, self.colors['space']):
                        warp_intensity = int(50 * (warp_strength + ripple))
                        frame[y, x] = tuple(min(255, c + warp_intensity) for c in original_color)
    
    def display_gravity_bend(self, duration=25):
        """Display the gravity bend animation."""
        print("Displaying Gravity Bend Animation...")
        print("Features: Bent space-time grid, falling particles, gravitational source")
        
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            # Create frame
            frame = self.create_gravity_frame(frame_count * 0.1)
            
            # Display frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.06)  # 16 FPS for smooth animation
            frame_count += 1
        
        print("Gravity bend animation completed!")
    
    def display_gravity_bend_loop(self, loops=3):
        """Display the gravity bend animation in a loop."""
        print(f"Displaying Gravity Bend Animation - {loops} loops...")
        
        for loop in range(loops):
            print(f"Loop {loop + 1}/{loops}")
            self.display_gravity_bend(duration=20)
            
            if loop < loops - 1:
                print("Restarting gravity simulation...")
                time.sleep(2)
        
        print("Gravity bend loop completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run gravity bend animation."""
    try:
        gravity = GravityBendAnimation()
        
        print("🌌 Gravity Bend Animation 🌌")
        print("1. Single gravity simulation")
        print("2. Multiple gravity loops")
        
        choice = input("Choose animation type (1 or 2): ").strip()
        
        if choice == "2":
            loops = int(input("Number of loops (default 3): ") or "3")
            gravity.display_gravity_bend_loop(loops=loops)
        else:
            gravity.display_gravity_bend(duration=25)
        
        # Clean up
        gravity.cleanup()
        
    except KeyboardInterrupt:
        print("\nGravity bend animation interrupted by user")
        gravity.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        gravity.cleanup()

if __name__ == "__main__":
    main() 