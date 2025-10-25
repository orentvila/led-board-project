#!/usr/bin/env python3
"""
Music Instruments Animation for LED Board
Features sousaphone, saxophone, drums, and guitar
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class MusicInstrumentsAnimation:
    def __init__(self):
        """Initialize the music instruments animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'sousaphone_brass': (255, 215, 0), # Golden brass
            'sousaphone_dark': (218, 165, 32), # Darker brass
            'saxophone_brass': (255, 215, 0),  # Golden brass
            'saxophone_keys': (192, 192, 192), # Silver keys
            'drums_wood': (139, 69, 19),       # Brown wood
            'drums_skin': (255, 248, 220),     # Drum skin
            'drums_metal': (192, 192, 192),    # Silver metal
            'guitar_wood': (160, 82, 45),      # Brown wood
            'guitar_neck': (139, 69, 19),      # Darker wood
            'guitar_strings': (255, 255, 255), # White strings
            'guitar_pickguard': (0, 0, 0),     # Black pickguard
            'guitar_bridge': (192, 192, 192),  # Silver bridge
            'guitar_tuners': (192, 192, 192),  # Silver tuners
            'highlight': (255, 255, 255),      # White highlights
            'shadow': (50, 50, 50)             # Dark shadows
        }
        
        # Animation parameters
        self.instrument_timer = 0
        self.highlight_timer = 0
        self.current_instrument = 0
        self.instrument_duration = 6  # seconds per instrument
        
    def create_sousaphone(self, frame):
        """Create a large sousaphone."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Sousaphone body (circular bell)
        bell_radius = 10
        for y in range(self.height):
            for x in range(self.width):
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= bell_radius:
                    # Bell shape
                    frame[y, x] = self.colors['sousaphone_brass']
                    
                    # Add some texture variation
                    if (x + y) % 2 == 0:
                        frame[y, x] = self.colors['sousaphone_dark']
        
        # Sousaphone tubing (curved)
        tubing_points = [
            (center_x - 8, center_y + 8),
            (center_x - 6, center_y + 12),
            (center_x - 4, center_y + 16),
            (center_x - 2, center_y + 20),
            (center_x, center_y + 24),
            (center_x + 2, center_y + 28),
            (center_x + 4, center_y + 32)
        ]
        
        for i, (tx, ty) in enumerate(tubing_points):
            if 0 <= tx < self.width and 0 <= ty < self.height:
                # Tubing thickness
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        tubing_x, tubing_y = tx + dx, ty + dy
                        if 0 <= tubing_x < self.width and 0 <= tubing_y < self.height:
                            frame[tubing_y, tubing_x] = self.colors['sousaphone_brass']
        
        # Sousaphone mouthpiece
        mouth_x = center_x - 6
        mouth_y = center_y + 8
        for y in range(mouth_y - 2, mouth_y + 3):
            for x in range(mouth_x - 2, mouth_x + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['sousaphone_dark']
    
    def create_saxophone(self, frame):
        """Create a large saxophone."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Saxophone body (curved)
        body_points = [
            (center_x - 8, center_y - 4),
            (center_x - 6, center_y),
            (center_x - 4, center_y + 4),
            (center_x - 2, center_y + 8),
            (center_x, center_y + 12),
            (center_x + 2, center_y + 16),
            (center_x + 4, center_y + 20),
            (center_x + 6, center_y + 24),
            (center_x + 8, center_y + 28)
        ]
        
        for i, (bx, by) in enumerate(body_points):
            if 0 <= bx < self.width and 0 <= by < self.height:
                # Body thickness
                for dy in range(-2, 3):
                    for dx in range(-1, 2):
                        body_x, body_y = bx + dx, by + dy
                        if 0 <= body_x < self.width and 0 <= body_y < self.height:
                            frame[body_y, body_x] = self.colors['saxophone_brass']
        
        # Saxophone bell (flared end)
        bell_x = center_x + 8
        bell_y = center_y + 28
        for y in range(bell_y - 4, bell_y + 5):
            for x in range(bell_x - 3, bell_x + 4):
                if 0 <= x < self.width and 0 <= y < self.height:
                    distance = math.sqrt((x - bell_x)**2 + (y - bell_y)**2)
                    if distance <= 4:
                        frame[y, x] = self.colors['saxophone_brass']
        
        # Saxophone keys
        key_positions = [
            (center_x - 4, center_y + 4),
            (center_x - 2, center_y + 8),
            (center_x, center_y + 12),
            (center_x + 2, center_y + 16),
            (center_x + 4, center_y + 20)
        ]
        
        for kx, ky in key_positions:
            if 0 <= kx < self.width and 0 <= ky < self.height:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        key_x, key_y = kx + dx, ky + dy
                        if 0 <= key_x < self.width and 0 <= key_y < self.height:
                            frame[key_y, key_x] = self.colors['saxophone_keys']
        
        # Saxophone mouthpiece
        mouth_x = center_x - 8
        mouth_y = center_y - 4
        for y in range(mouth_y - 2, mouth_y + 3):
            for x in range(mouth_x - 2, mouth_x + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['saxophone_brass']
    
    def create_drums(self, frame):
        """Create a drum set."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Bass drum (large)
        bass_x = center_x
        bass_y = center_y + 8
        bass_radius = 8
        
        for y in range(self.height):
            for x in range(self.width):
                dx = x - bass_x
                dy = y - bass_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= bass_radius:
                    frame[y, x] = self.colors['drums_skin']
                    
                    # Drum rim
                    if distance >= bass_radius - 1:
                        frame[y, x] = self.colors['drums_metal']
        
        # Snare drum (smaller)
        snare_x = center_x - 6
        snare_y = center_y - 4
        snare_radius = 4
        
        for y in range(self.height):
            for x in range(self.width):
                dx = x - snare_x
                dy = y - snare_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= snare_radius:
                    frame[y, x] = self.colors['drums_skin']
                    
                    # Drum rim
                    if distance >= snare_radius - 1:
                        frame[y, x] = self.colors['drums_metal']
        
        # Tom-tom (medium)
        tom_x = center_x + 6
        tom_y = center_y - 2
        tom_radius = 5
        
        for y in range(self.height):
            for x in range(self.width):
                dx = x - tom_x
                dy = y - tom_y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance <= tom_radius:
                    frame[y, x] = self.colors['drums_skin']
                    
                    # Drum rim
                    if distance >= tom_radius - 1:
                        frame[y, x] = self.colors['drums_metal']
        
        # Drum stands
        stand_positions = [
            (bass_x, bass_y + bass_radius + 2),
            (snare_x, snare_y + snare_radius + 2),
            (tom_x, tom_y + tom_radius + 2)
        ]
        
        for sx, sy in stand_positions:
            for y in range(sy, min(sy + 4, self.height)):
                for x in range(sx - 1, sx + 2):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        frame[y, x] = self.colors['drums_metal']
    
    def create_guitar(self, frame):
        """Create a large guitar."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Guitar body (acoustic shape)
        body_radius_x = 10
        body_radius_y = 8
        
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / body_radius_x
                dy = (y - center_y) / body_radius_y
                
                # Guitar body shape
                if dx*dx + dy*dy <= 1:
                    frame[y, x] = self.colors['guitar_wood']
                    
                    # Sound hole
                    hole_distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if hole_distance <= 3:
                        frame[y, x] = self.colors['guitar_pickguard']
        
        # Guitar neck
        neck_x = center_x
        neck_y = center_y - 8
        
        for y in range(neck_y, neck_y + 16):
            for x in range(neck_x - 1, neck_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['guitar_neck']
        
        # Guitar headstock
        head_x = center_x
        head_y = neck_y - 4
        
        for y in range(head_y - 3, head_y + 3):
            for x in range(head_x - 4, head_x + 5):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['guitar_neck']
        
        # Guitar strings
        string_positions = [
            (neck_x - 1, neck_y, head_y - 2),
            (neck_x, neck_y, head_y - 1),
            (neck_x + 1, neck_y, head_y),
            (neck_x - 1, neck_y, head_y + 1),
            (neck_x, neck_y, head_y + 2),
            (neck_x + 1, neck_y, head_y + 3)
        ]
        
        for sx, sy, ey in string_positions:
            for y in range(sy, ey):
                if 0 <= sx < self.width and 0 <= y < self.height:
                    frame[y, sx] = self.colors['guitar_strings']
        
        # Guitar tuners
        tuner_positions = [
            (head_x - 3, head_y - 2),
            (head_x - 2, head_y - 1),
            (head_x - 1, head_y),
            (head_x + 1, head_y + 1),
            (head_x + 2, head_y + 2),
            (head_x + 3, head_y + 3)
        ]
        
        for tx, ty in tuner_positions:
            if 0 <= tx < self.width and 0 <= ty < self.height:
                frame[ty, tx] = self.colors['guitar_tuners']
        
        # Guitar bridge
        bridge_x = center_x
        bridge_y = center_y + 2
        
        for y in range(bridge_y - 1, bridge_y + 2):
            for x in range(bridge_x - 3, bridge_x + 4):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['guitar_bridge']
    
    def add_highlights(self, frame):
        """Add highlights to make instruments shine."""
        highlight_positions = []
        
        # Add random highlights
        for _ in range(5):
            hx = np.random.randint(0, self.width)
            hy = np.random.randint(0, self.height)
            highlight_positions.append((hx, hy))
        
        for hx, hy in highlight_positions:
            if 0 <= hx < self.width and 0 <= hy < self.height:
                # Create highlight glow
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        glow_x, glow_y = hx + dx, hy + dy
                        if 0 <= glow_x < self.width and 0 <= glow_y < self.height:
                            glow_intensity = 1 - (abs(dx) + abs(dy)) * 0.3
                            glow_intensity = max(0, glow_intensity)
                            
                            current = frame[glow_y, glow_x]
                            highlight = self.colors['highlight']
                            frame[glow_y, glow_x] = tuple(int(c + (h - c) * glow_intensity * 0.3) 
                                                        for c, h in zip(current, highlight))
    
    def display_instrument(self, instrument_name, instrument_func, duration=6):
        """Display a specific instrument for the given duration."""
        print(f"Displaying {instrument_name.upper()} for {duration} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create frame with current instrument
            frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
            
            # Draw the instrument
            instrument_func(frame)
            
            # Add highlights
            self.add_highlights(frame)
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.instrument_timer += 1
            self.highlight_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print(f"{instrument_name.capitalize()} display completed!")
    
    def display_instruments_sequence(self):
        """Display the sequence of musical instruments."""
        print("🎷🥁🎸🎺 MUSICAL INSTRUMENTS ANIMATION 🎷🥁🎸🎺")
        print("Sequence: Sousaphone → Saxophone → Drums → Guitar")
        print("Each instrument is displayed prominently!")
        
        try:
            # Define instruments and their functions
            instruments = [
                ("sousaphone", self.create_sousaphone),
                ("saxophone", self.create_saxophone),
                ("drums", self.create_drums),
                ("guitar", self.create_guitar)
            ]
            
            for instrument_name, instrument_func in instruments:
                # Display the instrument
                self.display_instrument(instrument_name, instrument_func, self.instrument_duration)
                
                # Brief pause between instruments
                if instrument_name != "guitar":  # Don't pause after the last instrument
                    print("Transitioning to next instrument...")
                    time.sleep(1)
            
            print("Musical instruments animation completed!")
            
        except KeyboardInterrupt:
            print("\nMusical instruments animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run musical instruments animation."""
    try:
        instruments = MusicInstrumentsAnimation()
        instruments.display_instruments_sequence()
        instruments.cleanup()
        
    except KeyboardInterrupt:
        print("\nMusical instruments animation interrupted by user")
        instruments.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        instruments.cleanup()

if __name__ == "__main__":
    main() 