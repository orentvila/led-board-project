#!/usr/bin/env python3
"""
Ship Sailing Animation for LED Board
Creates a ship sailing across the sea with waves and water effects
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class ShipSailingAnimation:
    def __init__(self):
        """Initialize the ship sailing animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'sky': (10, 20, 50),         # Dark blue sky
            'sea': (0, 50, 100),         # Blue sea
            'wave_crest': (0, 100, 150), # Light blue wave tops
            'ship_hull': (139, 69, 19),  # Brown ship hull
            'ship_sail': (255, 255, 200), # Off-white sails
            'ship_mast': (101, 67, 33),  # Dark brown mast
            'clouds': (100, 100, 120),   # Gray clouds
            'sun': (255, 200, 0),        # Yellow sun
            'foam': (150, 200, 255)      # White foam
        }
        
        # Animation parameters
        self.ship_x = -5  # Start off-screen
        self.ship_y = 25  # Ship's vertical position
        self.wave_offset = 0
        self.cloud_offset = 0
        
    def create_ship_frame(self, time_step):
        """Create a single frame of the ship sailing animation."""
        # Create base frame with sky and sea
        frame = np.full((self.height, self.width, 3), self.colors['sky'], dtype=np.uint8)
        
        # Calculate animation parameters
        self.ship_x = -5 + (time_step * 0.5)  # Ship moves right
        wave_phase = time_step * 0.3
        cloud_phase = time_step * 0.1
        
        # Draw sky gradient
        self._draw_sky_gradient(frame)
        
        # Draw clouds
        self._draw_clouds(frame, cloud_phase)
        
        # Draw sun
        self._draw_sun(frame)
        
        # Draw sea with waves
        self._draw_sea_with_waves(frame, wave_phase)
        
        # Draw ship
        self._draw_ship(frame, time_step)
        
        # Add wave foam effects
        self._add_wave_foam(frame, wave_phase)
        
        return frame
    
    def _draw_sky_gradient(self, frame):
        """Draw sky gradient from top to horizon."""
        horizon_y = 15  # Horizon line
        
        for y in range(horizon_y):
            # Create gradient from dark blue to lighter blue
            intensity = int(10 + (y / horizon_y) * 20)
            color = (intensity, intensity + 10, intensity + 30)
            
            for x in range(self.width):
                frame[y, x] = color
    
    def _draw_clouds(self, frame, phase):
        """Draw moving clouds in the sky."""
        cloud_positions = [
            (5 + phase * 2, 3),
            (15 + phase * 1.5, 5),
            (25 + phase * 2.5, 4),
            (10 + phase * 1.8, 6)
        ]
        
        for cloud_x, cloud_y in cloud_positions:
            cloud_x = int(cloud_x) % (self.width + 10) - 5
            
            if 0 <= cloud_x < self.width:
                # Draw cloud shape
                for dy in range(-1, 2):
                    for dx in range(-2, 3):
                        x = cloud_x + dx
                        y = cloud_y + dy
                        
                        if 0 <= x < self.width and 0 <= y < self.height:
                            # Create cloud effect
                            if abs(dx) + abs(dy) <= 2:
                                frame[y, x] = self.colors['clouds']
    
    def _draw_sun(self, frame):
        """Draw the sun in the sky."""
        sun_x, sun_y = 25, 8
        
        # Draw sun with glow effect
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                x = sun_x + dx
                y = sun_y + dy
                
                if 0 <= x < self.width and 0 <= y < self.height:
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= 2:
                        intensity = int(255 * (1 - distance / 2))
                        frame[y, x] = (intensity, intensity * 0.8, 0)
    
    def _draw_sea_with_waves(self, frame, phase):
        """Draw the sea with animated waves."""
        horizon_y = 15
        
        for y in range(horizon_y, self.height):
            for x in range(self.width):
                # Create wave pattern
                wave_height = math.sin(x * 0.3 + phase) * 2
                wave_y = y + int(wave_height)
                
                if 0 <= wave_y < self.height:
                    # Sea color with depth variation
                    depth_factor = (y - horizon_y) / (self.height - horizon_y)
                    base_blue = int(50 + depth_factor * 50)
                    
                    # Add wave variation
                    wave_variation = math.sin(x * 0.5 + phase * 2) * 20
                    blue = max(0, min(255, base_blue + wave_variation))
                    
                    frame[wave_y, x] = (0, 30, blue)
    
    def _draw_ship(self, frame, time_step):
        """Draw the sailing ship."""
        ship_x = int(self.ship_x)
        ship_y = int(self.ship_y)
        
        # Add gentle rocking motion
        rock_offset = math.sin(time_step * 0.8) * 1
        ship_y += int(rock_offset)
        
        # Only draw if ship is visible
        if ship_x >= -3 and ship_x < self.width + 3:
            # Draw ship hull
            self._draw_ship_hull(frame, ship_x, ship_y)
            
            # Draw ship mast and sails
            self._draw_ship_sails(frame, ship_x, ship_y, time_step)
    
    def _draw_ship_hull(self, frame, x, y):
        """Draw the ship's hull."""
        # Hull shape (boat bottom)
        hull_points = [
            (x, y), (x+1, y), (x+2, y), (x+3, y), (x+4, y), (x+5, y),
            (x+1, y+1), (x+2, y+1), (x+3, y+1), (x+4, y+1),
            (x+2, y+2), (x+3, y+2)
        ]
        
        for px, py in hull_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                frame[py, px] = self.colors['ship_hull']
    
    def _draw_ship_sails(self, frame, x, y, time_step):
        """Draw the ship's mast and sails."""
        mast_x = x + 3
        mast_y = y - 1
        
        # Draw mast
        for my in range(mast_y, mast_y + 8):
            if 0 <= mast_x < self.width and 0 <= my < self.height:
                frame[my, mast_x] = self.colors['ship_mast']
        
        # Draw sails with wind effect
        wind_angle = math.sin(time_step * 0.5) * 0.3
        
        # Main sail
        sail_points = [
            (mast_x, mast_y + 1), (mast_x, mast_y + 2), (mast_x, mast_y + 3),
            (mast_x + 1, mast_y + 1), (mast_x + 1, mast_y + 2), (mast_x + 1, mast_y + 3),
            (mast_x + 2, mast_y + 1), (mast_x + 2, mast_y + 2),
            (mast_x + 3, mast_y + 1)
        ]
        
        for px, py in sail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                frame[py, px] = self.colors['ship_sail']
        
        # Small sail
        small_sail_points = [
            (mast_x, mast_y + 4), (mast_x, mast_y + 5),
            (mast_x + 1, mast_y + 4), (mast_x + 1, mast_y + 5),
            (mast_x + 2, mast_y + 4)
        ]
        
        for px, py in small_sail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                frame[py, px] = self.colors['ship_sail']
    
    def _add_wave_foam(self, frame, phase):
        """Add foam effects to the waves."""
        horizon_y = 15
        
        for x in range(self.width):
            # Create foam at wave crests
            wave_height = math.sin(x * 0.3 + phase) * 2
            foam_y = horizon_y + int(wave_height)
            
            if 0 <= foam_y < self.height:
                # Add foam particles
                for dx in range(-1, 2):
                    foam_x = x + dx
                    if 0 <= foam_x < self.width:
                        frame[foam_y, foam_x] = self.colors['foam']
    
    def display_ship_sailing(self, duration=30):
        """Display the ship sailing animation."""
        print("Displaying Ship Sailing Animation...")
        print("Features: Animated waves, moving clouds, sailing ship")
        
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            # Create frame
            frame = self.create_ship_frame(frame_count * 0.1)
            
            # Display frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.08)  # 12 FPS for smooth sailing
            frame_count += 1
        
        print("Ship sailing animation completed!")
    
    def display_ship_sailing_loop(self, loops=3):
        """Display the ship sailing animation in a loop."""
        print(f"Displaying Ship Sailing Animation - {loops} loops...")
        
        for loop in range(loops):
            print(f"Loop {loop + 1}/{loops}")
            self.display_ship_sailing(duration=25)
            
            if loop < loops - 1:
                print("Restarting ship journey...")
                time.sleep(2)
        
        print("Ship sailing loop completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run ship sailing animation."""
    try:
        ship = ShipSailingAnimation()
        
        print("⛵ Ship Sailing Animation ⛵")
        print("1. Single sailing journey")
        print("2. Multiple sailing loops")
        
        choice = input("Choose animation type (1 or 2): ").strip()
        
        if choice == "2":
            loops = int(input("Number of loops (default 3): ") or "3")
            ship.display_ship_sailing_loop(loops=loops)
        else:
            ship.display_ship_sailing(duration=30)
        
        # Clean up
        ship.cleanup()
        
    except KeyboardInterrupt:
        print("\nShip sailing animation interrupted by user")
        ship.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        ship.cleanup()

if __name__ == "__main__":
    main() 