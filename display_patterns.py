import time
import math
import random
import numpy as np
from led_controller import LEDController
import config

class DisplayPatterns:
    def __init__(self, led_controller):
        """Initialize display patterns with LED controller."""
        self.led = led_controller
        self.running = False
    
    def stop(self):
        """Stop all running patterns."""
        self.running = False
    
    def rainbow_wave(self, duration=None):
        """Create a rainbow wave effect across the display."""
        self.running = True
        start_time = time.time()
        offset = 0
        
        while self.running and (duration is None or time.time() - start_time < duration):
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    # Create rainbow effect
                    hue = (x + y + offset) / (config.TOTAL_WIDTH + config.TOTAL_HEIGHT) * 360
                    color = self._hsv_to_rgb(hue, 1.0, 1.0)
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            offset += 5
            time.sleep(config.RAINBOW_SPEED)
    
    def color_wave(self, color, duration=None):
        """Create a wave effect with a specific color."""
        self.running = True
        start_time = time.time()
        offset = 0
        
        while self.running and (duration is None or time.time() - start_time < duration):
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    # Create wave effect
                    wave = math.sin((x + offset) * 0.2) * 0.5 + 0.5
                    brightness = int(wave * 255)
                    wave_color = tuple(int(c * wave) for c in color)
                    self.led.set_pixel(x, y, wave_color)
            
            self.led.show()
            offset += 2
            time.sleep(config.WAVE_SPEED)
    
    def scrolling_text(self, text, color, duration=None):
        """Scroll text across the display."""
        self.running = True
        start_time = time.time()
        text_width = len(text) * 6  # Approximate character width
        x_offset = config.TOTAL_WIDTH
        
        while self.running and (duration is None or time.time() - start_time < duration):
            self.led.clear()
            self.led.draw_text(text, x_offset, 1, color)
            self.led.show()
            
            x_offset -= 1
            if x_offset < -text_width:
                x_offset = config.TOTAL_WIDTH
            
            time.sleep(config.SCROLL_SPEED)
    
    def matrix_rain(self, duration=None):
        """Create a Matrix-style falling rain effect."""
        self.running = True
        start_time = time.time()
        drops = []
        
        # Initialize drops
        for x in range(config.TOTAL_WIDTH):
            drops.append(random.randint(-config.TOTAL_HEIGHT, 0))
        
        while self.running and (duration is None or time.time() - start_time < duration):
            self.led.clear()
            
            for x in range(config.TOTAL_WIDTH):
                # Move drops down
                drops[x] += 1
                if drops[x] >= config.TOTAL_HEIGHT:
                    drops[x] = random.randint(-config.TOTAL_HEIGHT, 0)
                
                # Draw drop trail
                for i in range(config.TOTAL_HEIGHT):
                    y = drops[x] - i
                    if 0 <= y < config.TOTAL_HEIGHT:
                        # Fade effect
                        intensity = max(0, 255 - i * 50)
                        color = (0, intensity, 0)
                        self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.1)
    
    def fire_effect(self, duration=None):
        """Create a fire effect."""
        self.running = True
        start_time = time.time()
        fire_matrix = np.zeros((config.TOTAL_HEIGHT, config.TOTAL_WIDTH), dtype=np.uint8)
        
        while self.running and (duration is None or time.time() - start_time < duration):
            # Generate fire at bottom
            for x in range(config.TOTAL_WIDTH):
                fire_matrix[config.TOTAL_HEIGHT - 1, x] = random.randint(0, 255)
            
            # Propagate fire upward
            for y in range(config.TOTAL_HEIGHT - 1):
                for x in range(config.TOTAL_WIDTH):
                    if fire_matrix[y + 1, x] > 0:
                        # Spread fire
                        spread = random.randint(-1, 1)
                        new_x = max(0, min(config.TOTAL_WIDTH - 1, x + spread))
                        fire_matrix[y, new_x] = max(0, fire_matrix[y + 1, x] - random.randint(0, 30))
            
            # Convert to colors
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    intensity = fire_matrix[y, x]
                    if intensity > 200:
                        color = (255, 255, 0)  # Yellow
                    elif intensity > 100:
                        color = (255, intensity, 0)  # Orange
                    elif intensity > 0:
                        color = (intensity, 0, 0)  # Red
                    else:
                        color = (0, 0, 0)  # Black
                    
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.05)
    
    def panel_sequence(self, colors, duration=None):
        """Light up panels in sequence with different colors."""
        self.running = True
        start_time = time.time()
        panel = 0
        
        while self.running and (duration is None or time.time() - start_time < duration):
            # Clear all panels
            for p in range(config.PANELS_COUNT):
                self.led.fill_panel(p, config.COLORS['BLACK'])
            
            # Light up current panel
            color = colors[panel % len(colors)]
            self.led.fill_panel(panel, color)
            self.led.show()
            
            panel = (panel + 1) % config.PANELS_COUNT
            time.sleep(0.5)
    
    def bouncing_ball(self, color, duration=None):
        """Create a bouncing ball animation."""
        self.running = True
        start_time = time.time()
        ball_x = config.TOTAL_WIDTH // 2
        ball_y = config.TOTAL_HEIGHT // 2
        vel_x = 2
        vel_y = 1
        
        while self.running and (duration is None or time.time() - start_time < duration):
            self.led.clear()
            
            # Update ball position
            ball_x += vel_x
            ball_y += vel_y
            
            # Bounce off walls
            if ball_x <= 0 or ball_x >= config.TOTAL_WIDTH - 1:
                vel_x = -vel_x
                ball_x = max(0, min(config.TOTAL_WIDTH - 1, ball_x))
            
            if ball_y <= 0 or ball_y >= config.TOTAL_HEIGHT - 1:
                vel_y = -vel_y
                ball_y = max(0, min(config.TOTAL_HEIGHT - 1, ball_y))
            
            # Draw ball
            self.led.set_pixel(int(ball_x), int(ball_y), color)
            
            # Draw ball trail
            for i in range(1, 4):
                trail_x = int(ball_x - vel_x * i * 0.5)
                trail_y = int(ball_y - vel_y * i * 0.5)
                if 0 <= trail_x < config.TOTAL_WIDTH and 0 <= trail_y < config.TOTAL_HEIGHT:
                    trail_color = tuple(int(c * (1 - i * 0.3)) for c in color)
                    self.led.set_pixel(trail_x, trail_y, trail_color)
            
            self.led.show()
            time.sleep(0.1)
    
    def spiral_pattern(self, color, duration=None):
        """Create a spiral pattern."""
        self.running = True
        start_time = time.time()
        center_x = config.TOTAL_WIDTH // 2
        center_y = config.TOTAL_HEIGHT // 2
        angle = 0
        
        while self.running and (duration is None or time.time() - start_time < duration):
            self.led.clear()
            
            # Draw spiral
            for i in range(50):
                radius = i * 0.5
                x = int(center_x + radius * math.cos(angle + i * 0.2))
                y = int(center_y + radius * math.sin(angle + i * 0.2))
                
                if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                    intensity = max(0, 255 - i * 5)
                    spiral_color = tuple(int(c * intensity / 255) for c in color)
                    self.led.set_pixel(x, y, spiral_color)
            
            self.led.show()
            angle += 0.1
            time.sleep(0.05)
    
    def _hsv_to_rgb(self, h, s, v):
        """Convert HSV color to RGB."""
        h = h / 360.0
        if s == 0.0:
            return (int(v * 255), int(v * 255), int(v * 255))
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return (int(r * 255), int(g * 255), int(b * 255)) 