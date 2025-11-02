#!/usr/bin/env python3
"""
Animals Pastel Animation for LED Board
Displays 8 animals with smooth fade transitions in soft pastel colors.
Each animal is shown for 7.5 seconds with 1 second fade in/out.
Total duration: 60 seconds
"""

import time
import math
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class AnimalsPastelAnimation:
    def __init__(self):
        """Initialize the animals pastel animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Soft pastel colors
        self.colors = {
            'background': (10, 10, 15),  # Very dark blue-gray background
            
            # Dog - soft beige/tan
            'dog_body': (255, 220, 180),  # Soft beige
            'dog_ears': (230, 200, 160),  # Slightly darker beige
            'dog_nose': (200, 180, 200),  # Soft gray-purple
            
            # Cat - soft peach
            'cat_body': (255, 200, 180),  # Soft peach
            'cat_ears': (255, 180, 150),  # Deeper peach
            'cat_whiskers': (255, 240, 220),  # Very light cream
            
            # Horse - soft tan/brown
            'horse_body': (220, 200, 170),  # Soft tan
            'horse_mane': (180, 160, 140),  # Darker tan
            'horse_legs': (190, 170, 150),  # Medium tan
            
            # Fish - soft blue/teal
            'fish_body': (150, 220, 240),  # Soft sky blue
            'fish_fins': (120, 200, 230),  # Deeper blue
            'fish_eye': (100, 150, 200),  # Deep blue
            
            # Zebra - soft gray with white
            'zebra_white': (240, 240, 240),  # Soft white
            'zebra_black': (100, 100, 100),  # Soft gray (instead of harsh black)
            
            # Cow - soft cream with gray
            'cow_body': (250, 245, 235),  # Cream white
            'cow_spots': (180, 170, 160),  # Soft gray-brown
            'cow_horns': (200, 190, 180),  # Light gray
            
            # Frog - soft green
            'frog_body': (180, 230, 180),  # Soft mint green
            'frog_eyes': (150, 200, 150),  # Deeper green
            'frog_pupils': (80, 120, 80),  # Dark green
            
            # Rooster - soft red/orange/yellow
            'rooster_body': (255, 220, 180),  # Soft orange
            'rooster_comb': (255, 180, 160),  # Soft red
            'rooster_tail': (255, 240, 180),  # Soft yellow
            'rooster_beak': (230, 200, 150),  # Soft orange-brown
        }
        
        # Animation parameters
        self.animal_duration = 7.5  # seconds per animal
        self.fade_in_duration = 1.0  # seconds for fade in
        self.fade_out_duration = 1.0  # seconds for fade out
        self.total_duration = 60.0  # total animation duration
        
    def apply_fade(self, color, fade_intensity):
        """Apply fade intensity to a color (0.0 to 1.0)."""
        return tuple(int(c * fade_intensity) for c in color)
    
    def blend_colors(self, color1, color2, blend_factor):
        """Blend two colors together (0.0 = color1, 1.0 = color2)."""
        return tuple(
            int(c1 * (1 - blend_factor) + c2 * blend_factor)
            for c1, c2 in zip(color1, color2)
        )
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def draw_dog(self, fade_intensity=1.0):
        """Draw a minimalist dog with ears and tail."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Dog body (oval)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 7
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['dog_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Floppy ears
        # Left ear
        for y in range(max(0, center_y - 10), min(self.height, center_y)):
            for x in range(max(0, center_x - 8), min(self.width, center_x - 1)):
                if y <= center_y - 2 and x <= center_x - 2:
                    color = self.apply_fade(self.colors['dog_ears'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        # Right ear
        for y in range(max(0, center_y - 10), min(self.height, center_y)):
            for x in range(max(0, center_x + 1), min(self.width, center_x + 8)):
                if y <= center_y - 2:
                    color = self.apply_fade(self.colors['dog_ears'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Nose
        self.safe_set_pixel(center_x, center_y, 
                          self.apply_fade(self.colors['dog_nose'], fade_intensity))
        
        # Tail (curved, wagging style)
        tail_points = [(center_x + 6, center_y + 8), (center_x + 8, center_y + 6),
                       (center_x + 10, center_y + 4), (center_x + 11, center_y + 2)]
        for px, py in tail_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                color = self.apply_fade(self.colors['dog_body'], fade_intensity)
                self.safe_set_pixel(px, py, color)
    
    def draw_cat(self, fade_intensity=1.0):
        """Draw a minimalist cat with pointed ears and whiskers."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Cat head (smaller, rounder)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 8
                dy = (y - center_y) / 6
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['cat_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Pointed triangular ears
        # Left ear
        for y in range(max(0, center_y - 9), min(self.height, center_y - 1)):
            for x in range(max(0, center_x - 6), min(self.width, center_x)):
                if y - (center_y - 9) <= (center_x - x) * 1.2:
                    color = self.apply_fade(self.colors['cat_ears'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        # Right ear
        for y in range(max(0, center_y - 9), min(self.height, center_y - 1)):
            for x in range(max(0, center_x), min(self.width, center_x + 6)):
                if y - (center_y - 9) <= (x - center_x) * 1.2:
                    color = self.apply_fade(self.colors['cat_ears'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Whiskers (horizontal lines)
        for i in range(4):
            # Left whiskers
            if center_x - 6 - i >= 0:
                self.safe_set_pixel(center_x - 6 - i, center_y, 
                                  self.apply_fade(self.colors['cat_whiskers'], fade_intensity))
            # Right whiskers
            if center_x + 6 + i < self.width:
                self.safe_set_pixel(center_x + 6 + i, center_y, 
                                  self.apply_fade(self.colors['cat_whiskers'], fade_intensity))
    
    def draw_horse(self, fade_intensity=1.0):
        """Draw a minimalist horse with mane and long legs."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Horse body (elongated oval)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 12
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['horse_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Mane (flowing down the neck)
        for y in range(max(0, center_y - 8), min(self.height, center_y - 2)):
            for x in range(max(0, center_x - 2), min(self.width, center_x + 3)):
                color = self.apply_fade(self.colors['horse_mane'], fade_intensity)
                self.safe_set_pixel(x, y, color)
        
        # Long legs (four legs)
        leg_y_start = center_y + 6
        leg_y_end = min(self.height, center_y + 15)
        for y in range(max(0, leg_y_start), leg_y_end):
            # Front left
            if center_x - 4 >= 0:
                self.safe_set_pixel(center_x - 4, y, 
                                  self.apply_fade(self.colors['horse_legs'], fade_intensity))
            # Front right
            if center_x - 1 < self.width:
                self.safe_set_pixel(center_x - 1, y, 
                                  self.apply_fade(self.colors['horse_legs'], fade_intensity))
            # Back left
            if center_x + 2 < self.width:
                self.safe_set_pixel(center_x + 2, y, 
                                  self.apply_fade(self.colors['horse_legs'], fade_intensity))
            # Back right
            if center_x + 5 < self.width:
                self.safe_set_pixel(center_x + 5, y, 
                                  self.apply_fade(self.colors['horse_legs'], fade_intensity))
    
    def draw_fish(self, fade_intensity=1.0):
        """Draw a minimalist fish with fins and tail."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Fish body (oval, horizontal)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 5
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['fish_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Top fin
        for x in range(max(0, center_x - 4), min(self.width, center_x + 5)):
            for y in range(max(0, center_y - 6), min(self.height, center_y - 4)):
                color = self.apply_fade(self.colors['fish_fins'], fade_intensity)
                self.safe_set_pixel(x, y, color)
        
        # Bottom fin
        for x in range(max(0, center_x - 4), min(self.width, center_x + 5)):
            for y in range(max(0, center_y + 4), min(self.height, center_y + 6)):
                color = self.apply_fade(self.colors['fish_fins'], fade_intensity)
                self.safe_set_pixel(x, y, color)
        
        # Tail (fan shape)
        tail_x = center_x + 8
        for y in range(max(0, center_y - 4), min(self.height, center_y + 5)):
            if tail_x < self.width:
                color = self.apply_fade(self.colors['fish_fins'], fade_intensity)
                self.safe_set_pixel(tail_x, y, color)
                if abs(y - center_y) > 2 and tail_x + 1 < self.width:
                    self.safe_set_pixel(tail_x + 1, y, color)
        
        # Eye
        self.safe_set_pixel(center_x - 3, center_y, 
                          self.apply_fade(self.colors['fish_eye'], fade_intensity))
    
    def draw_zebra(self, fade_intensity=1.0):
        """Draw a minimalist zebra with distinctive stripes."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Zebra body (oval)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 11
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    # Base white color
                    color = self.apply_fade(self.colors['zebra_white'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Vertical stripes (characteristic of zebra)
        stripe_width = 2
        for x in range(max(0, center_x - 9), min(self.width, center_x + 10), 4):
            for y in range(max(0, center_y - 7), min(self.height, center_y + 8)):
                # Check if this point is within the body
                dx = (x - center_x) / 11
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['zebra_black'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
                    if x + 1 < self.width:
                        self.safe_set_pixel(x + 1, y, color)
    
    def draw_cow(self, fade_intensity=1.0):
        """Draw a minimalist cow with spots and horns."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Cow body (rounded rectangle)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 11
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['cow_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Random spots (characteristic of cow)
        spots = [
            (center_x - 6, center_y - 3), (center_x + 5, center_y - 2),
            (center_x - 4, center_y + 2), (center_x + 6, center_y + 4)
        ]
        for spot_x, spot_y in spots:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = spot_x + dx, spot_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if dx*dx + dy*dy <= 4:
                            color = self.apply_fade(self.colors['cow_spots'], fade_intensity)
                            self.safe_set_pixel(x, y, color)
        
        # Horns (two curved horns)
        # Left horn
        horn_points = [(center_x - 5, center_y - 8), (center_x - 6, center_y - 9),
                       (center_x - 5, center_y - 10)]
        for px, py in horn_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                color = self.apply_fade(self.colors['cow_horns'], fade_intensity)
                self.safe_set_pixel(px, py, color)
        # Right horn
        horn_points = [(center_x + 5, center_y - 8), (center_x + 6, center_y - 9),
                       (center_x + 5, center_y - 10)]
        for px, py in horn_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                color = self.apply_fade(self.colors['cow_horns'], fade_intensity)
                self.safe_set_pixel(px, py, color)
    
    def draw_frog(self, fade_intensity=1.0):
        """Draw a minimalist frog with big eyes and folded legs."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Frog body (wide oval)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 6
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['frog_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Big eyes (characteristic of frog)
        # Left eye
        eye_x, eye_y = center_x - 5, center_y - 4
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                x, y = eye_x + dx, eye_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if dx*dx + dy*dy <= 4:
                        color = self.apply_fade(self.colors['frog_eyes'], fade_intensity)
                        self.safe_set_pixel(x, y, color)
        # Right eye
        eye_x, eye_y = center_x + 5, center_y - 4
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                x, y = eye_x + dx, eye_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if dx*dx + dy*dy <= 4:
                        color = self.apply_fade(self.colors['frog_eyes'], fade_intensity)
                        self.safe_set_pixel(x, y, color)
        
        # Pupils
        self.safe_set_pixel(center_x - 5, center_y - 4, 
                          self.apply_fade(self.colors['frog_pupils'], fade_intensity))
        self.safe_set_pixel(center_x + 5, center_y - 4, 
                          self.apply_fade(self.colors['frog_pupils'], fade_intensity))
        
        # Folded legs (positioned to sides)
        # Left leg
        for dx in range(-2, 3):
            for dy in range(-1, 3):
                x, y = center_x - 6 + dx, center_y + 5 + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if dx*dx + dy*dy <= 3:
                        color = self.apply_fade(self.colors['frog_body'], fade_intensity)
                        self.safe_set_pixel(x, y, color)
        # Right leg
        for dx in range(-2, 3):
            for dy in range(-1, 3):
                x, y = center_x + 6 + dx, center_y + 5 + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    if dx*dx + dy*dy <= 3:
                        color = self.apply_fade(self.colors['frog_body'], fade_intensity)
                        self.safe_set_pixel(x, y, color)
    
    def draw_rooster(self, fade_intensity=1.0):
        """Draw a minimalist rooster with comb and tail feathers."""
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Rooster body (rounded)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 9
                dy = (y - center_y) / 7
                if dx*dx + dy*dy <= 1:
                    color = self.apply_fade(self.colors['rooster_body'], fade_intensity)
                    self.safe_set_pixel(x, y, color)
        
        # Comb (red crown on top of head)
        comb_points = [
            (center_x - 2, center_y - 9), (center_x - 1, center_y - 10),
            (center_x, center_y - 11), (center_x + 1, center_y - 10),
            (center_x + 2, center_y - 9)
        ]
        for px, py in comb_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                color = self.apply_fade(self.colors['rooster_comb'], fade_intensity)
                self.safe_set_pixel(px, py, color)
        
        # Tail feathers (fan-shaped, colorful)
        tail_x = center_x + 7
        for i in range(5):
            y_offset = -2 + i
            y_pos = center_y + y_offset
            if 0 <= tail_x < self.width and 0 <= y_pos < self.height:
                # Use yellow color for tail
                color = self.apply_fade(self.colors['rooster_tail'], fade_intensity)
                self.safe_set_pixel(tail_x, y_pos, color)
                if tail_x + 1 < self.width:
                    self.safe_set_pixel(tail_x + 1, y_pos, color)
                    if abs(y_offset) <= 1 and tail_x + 2 < self.width:
                        self.safe_set_pixel(tail_x + 2, y_pos, color)
        
        # Beak (small triangular beak)
        beak_points = [(center_x, center_y - 2), (center_x - 1, center_y - 1),
                       (center_x + 1, center_y - 1)]
        for px, py in beak_points:
            if 0 <= px < self.width and 0 <= py < self.height:
                color = self.apply_fade(self.colors['rooster_beak'], fade_intensity)
                self.safe_set_pixel(px, py, color)
    
    def render_animal_to_buffer(self, draw_func, fade_intensity):
        """Render an animal to a buffer and return the buffer."""
        buffer = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Temporary LED controller to capture the drawing
        class TempLED:
            def __init__(self, buf):
                self.buffer = buf
                self.width = buf.shape[1]
                self.height = buf.shape[0]
            
            def set_pixel(self, x, y, color):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.buffer[y, x] = color
        
        temp_led = TempLED(buffer)
        original_led = self.led
        self.led = temp_led
        
        # Draw the animal (this will write to buffer)
        draw_func(fade_intensity)
        
        # Restore original LED controller
        self.led = original_led
        
        return buffer
    
    def blend_buffers(self, buffer1, buffer2, blend_factor):
        """Blend two buffers together (0.0 = buffer1, 1.0 = buffer2)."""
        result = np.zeros_like(buffer1)
        for y in range(self.height):
            for x in range(self.width):
                c1 = buffer1[y, x]
                c2 = buffer2[y, x]
                blended = tuple(
                    int(c1[i] * (1 - blend_factor) + c2[i] * blend_factor)
                    for i in range(3)
                )
                result[y, x] = blended
        return result
    
    def run_animation(self):
        """Run the complete 60-second animal animation with smooth blending."""
        animals = [
            ("dog", self.draw_dog),
            ("cat", self.draw_cat),
            ("horse", self.draw_horse),
            ("fish", self.draw_fish),
            ("zebra", self.draw_zebra),
            ("cow", self.draw_cow),
            ("frog", self.draw_frog),
            ("rooster", self.draw_rooster)
        ]
        
        print("🐾 Starting Animals Pastel Animation (60 seconds)")
        print("Animals: Dog → Cat → Horse → Fish → Zebra → Cow → Frog → Rooster")
        
        start_time = time.time()
        frame_time = 1.0 / 30.0  # 30 FPS for smooth animation
        
        # Pre-render all animals at full intensity for blending
        print("🎨 Pre-rendering animals...")
        animal_buffers = []
        for animal_name, draw_func in animals:
            buffer = self.render_animal_to_buffer(draw_func, 1.0)
            animal_buffers.append(buffer)
            print(f"  ✓ {animal_name.capitalize()} rendered")
        
        print("▶️ Starting animation loop...")
        
        # Single unified loop for smooth transitions
        while True:
            elapsed_total = time.time() - start_time
            
            if elapsed_total >= self.total_duration:
                break
            
            # Determine which animal(s) to show
            animal_index = int(elapsed_total / self.animal_duration)
            
            if animal_index >= len(animals):
                break
            
            # Calculate position within current animal's timeframe
            animal_start_time = animal_index * self.animal_duration
            elapsed_animal = elapsed_total - animal_start_time
            
            # Clear display
            self.led.clear()
            
            current_buffer = animal_buffers[animal_index]
            prev_buffer = animal_buffers[animal_index - 1] if animal_index > 0 else None
            next_buffer = animal_buffers[animal_index + 1] if animal_index < len(animals) - 1 else None
            
            # Fade in (first 1 second of current animal)
            if elapsed_animal < self.fade_in_duration:
                fade_progress = elapsed_animal / self.fade_in_duration
                # Smooth ease-out fade in
                fade_in_intensity = 1.0 - (1.0 - fade_progress) ** 2
                
                # During fade in, blend with previous animal if it exists
                if prev_buffer is not None:
                    # Previous animal fades out as current fades in
                    prev_fade = 1.0 - fade_in_intensity
                    blended = self.blend_buffers(prev_buffer, current_buffer, fade_in_intensity)
                    
                    # Draw blended result
                    for y in range(self.height):
                        for x in range(self.width):
                            color = blended[y, x]
                            self.led.set_pixel(x, y, tuple(int(c) for c in color))
                else:
                    # First animal, just fade in
                    for y in range(self.height):
                        for x in range(self.width):
                            color = current_buffer[y, x]
                            faded_color = tuple(int(c * fade_in_intensity) for c in color)
                            self.led.set_pixel(x, y, faded_color)
            
            # Fade out (last 1 second) - blend with next animal if it exists
            elif elapsed_animal >= self.animal_duration - self.fade_out_duration:
                fade_out_elapsed = elapsed_animal - (self.animal_duration - self.fade_out_duration)
                fade_progress = fade_out_elapsed / self.fade_out_duration
                fade_out_intensity = fade_progress ** 2
                current_fade = 1.0 - fade_out_intensity
                
                if next_buffer is not None:
                    # Next animal starts fading in as current fades out
                    # Both fades happen simultaneously over the 1-second transition
                    next_fade_intensity = 1.0 - (1.0 - fade_progress) ** 2
                    
                    # Blend current (fading out) and next (fading in)
                    blended = self.blend_buffers(current_buffer, next_buffer, next_fade_intensity)
                    
                    # Draw blended result
                    for y in range(self.height):
                        for x in range(self.width):
                            color = blended[y, x]
                            self.led.set_pixel(x, y, tuple(int(c) for c in color))
                else:
                    # Last animal, just fade out
                    for y in range(self.height):
                        for x in range(self.width):
                            color = current_buffer[y, x]
                            faded_color = tuple(int(c * current_fade) for c in color)
                            self.led.set_pixel(x, y, faded_color)
            
            # Full display (middle period)
            else:
                # Draw current animal at full intensity
                for y in range(self.height):
                    for x in range(self.width):
                        color = current_buffer[y, x]
                        self.led.set_pixel(x, y, tuple(int(c) for c in color))
            
            # Show frame
            self.led.show()
            
            # Frame timing
            time.sleep(frame_time)
        
        # Final clear
        self.led.clear()
        self.led.show()
        
        print("🎉 Animals Pastel Animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run the animals animation."""
    try:
        animation = AnimalsPastelAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()

