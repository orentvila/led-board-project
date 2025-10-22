#!/usr/bin/env python3
"""
Final LED Program Main Controller
4-Button LED Controller with Theme Animations
"""

import time
import signal
import sys
import os
import threading
import pygame
import random
import math

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from button_controller import ButtonController
from led_controller import LEDController
import config

class FinalLEDController:
    def __init__(self):
        """Initialize the final LED controller."""
        self.led = LEDController()
        self.button_controller = ButtonController()
        self.running = True
        self.current_animation = None
        
        # Initialize pygame for audio
        try:
            pygame.mixer.init()
            print("🔊 Audio system initialized")
        except Exception as e:
            print(f"⚠️ Audio system not available: {e}")
            self.audio_available = False
        else:
            self.audio_available = True
        
        # Theme configurations
        self.themes = {
            0: {  # Pin 18 - Colors
                'name': 'Colors',
                'animations': [
                    {'name': 'Rainbow', 'method': 'run_rainbow_animation', 'audio': 'rainbow_theme.wav'},
                    {'name': 'Fire', 'method': 'run_fire_animation', 'audio': 'fire_theme.wav'}
                ]
            },
            1: {  # Pin 17 - Nature
                'name': 'Nature',
                'animations': [
                    {'name': 'Bubbles', 'method': 'run_bubbles_animation', 'audio': 'bubbles_theme.wav'}
                ]
            },
            2: {  # Pin 27 - Shapes
                'name': 'Shapes',
                'animations': [
                    {'name': 'Spiral', 'method': 'run_spiral_animation', 'audio': 'spiral_theme.wav'}
                ]
            },
            3: {  # Pin 22 - Shooting Star
                'name': 'Shooting Star',
                'animations': [
                    {'name': 'Shooting Star', 'method': 'run_shooting_star_animation', 'audio': 'star_theme.wav'}
                ]
            }
        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for all 4 buttons."""
        for i in range(4):
            self.button_controller.register_callback(i, self.button_pressed)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down final LED controller...")
        self.cleanup()
        sys.exit(0)
    
    def button_pressed(self):
        """Called when any button is pressed."""
        # Get the button ID that was pressed
        button_id = None
        for i in range(4):
            if self.button_controller.get_button_state(i):
                button_id = i
                break
        
        if button_id is not None:
            pin_number = config.BUTTON_PINS[button_id]
            theme_name = self.themes[button_id]['name']
            print(f"🎉 Button pressed! Pin: {pin_number} - {theme_name} Theme")
            
            # Start theme animation
            self.start_theme_animation(button_id)
    
    def start_theme_animation(self, theme_id):
        """Start a random animation from the specified theme."""
        theme = self.themes[theme_id]
        
        if not theme['animations']:
            print(f"⚠️ No animations available for {theme['name']} theme")
            return
        
        # Stop current animation
        self.stop_current_animation()
        
        # Select random animation from theme
        animation_info = random.choice(theme['animations'])
        animation_name = animation_info['name']
        
        print(f"🎬 Starting {theme['name']} animation: {animation_name}")
        
        # Play audio if available
        if self.audio_available and 'audio' in animation_info:
            self.play_audio(animation_info['audio'])
        
        # Start animation
        animation_method = animation_info['method']
        method = getattr(self, animation_method)
        
        self.current_animation = threading.Thread(
            target=method,
            args=(30,)  # 30 seconds duration
        )
        self.current_animation.daemon = True
        self.current_animation.start()
    
    def play_audio(self, audio_file):
        """Play audio file if available."""
        if not self.audio_available:
            return
        
        try:
            audio_path = os.path.join('audio', audio_file)
            if os.path.exists(audio_path):
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                print(f"🔊 Playing audio: {audio_file}")
            else:
                print(f"⚠️ Audio file not found: {audio_file}")
        except Exception as e:
            print(f"⚠️ Error playing audio: {e}")
    
    def stop_current_animation(self):
        """Stop the currently running animation."""
        if self.current_animation and self.current_animation.is_alive():
            # Stop any playing audio
            if self.audio_available:
                pygame.mixer.music.stop()
            
            # Wait for animation to finish
            self.current_animation.join(timeout=1.0)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB."""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))
    
    def run_rainbow_animation(self, duration=30):
        """Run rainbow animation."""
        print(f"🌈 Starting Rainbow animation for {duration} seconds...")
        
        start_time = time.time()
        hue_offset = 0
        speed = 0.02
        
        while self.running and (time.time() - start_time) < duration:
            # Clear and create rainbow
            self.led.clear()
            
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    hue = (x * 10 + y * 5 + hue_offset) % 360
                    color = self.hsv_to_rgb(hue, 1.0, 1.0)
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            hue_offset += speed
            time.sleep(0.05)  # 20 FPS
        
        print(f"🌈 Rainbow animation completed")
    
    def run_fire_animation(self, duration=30):
        """Run fire animation."""
        print(f"🔥 Starting Fire animation for {duration} seconds...")
        
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            # Clear and create fire
            self.led.clear()
            
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    # Fire intensity decreases with height
                    height_factor = y / config.TOTAL_HEIGHT
                    intensity = 0.8 * (1 - height_factor)
                    
                    # Add randomness
                    noise = random.random() * 0.3
                    total_intensity = intensity + noise
                    
                    # Choose color based on intensity
                    if total_intensity > 0.8:
                        color = (255, 100, 0)  # Hot orange
                    elif total_intensity > 0.6:
                        color = (255, 150, 0)  # Orange
                    elif total_intensity > 0.4:
                        color = (255, 200, 100)  # Yellow-orange
                    elif total_intensity > 0.2:
                        color = (100, 50, 0)  # Dark red
                    else:
                        color = (0, 0, 0)  # Black
                    
                    # Add sparks occasionally
                    if random.random() < 0.1:
                        color = (255, 255, 255)  # White spark
                    
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print(f"🔥 Fire animation completed")
    
    def run_spiral_animation(self, duration=30):
        """Run spiral animation."""
        print(f"🌀 Starting Spiral animation for {duration} seconds...")
        
        start_time = time.time()
        angle = 0
        radius = 0
        max_radius = min(config.TOTAL_WIDTH, config.TOTAL_HEIGHT) // 2
        
        while self.running and (time.time() - start_time) < duration:
            # Clear and create spiral
            self.led.clear()
            
            center_x = config.TOTAL_WIDTH // 2
            center_y = config.TOTAL_HEIGHT // 2
            
            # Create spiral
            for i in range(100):
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                
                if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                    # Create trail effect
                    for trail in range(3):
                        trail_x = x + trail
                        trail_y = y + trail
                        if 0 <= trail_x < config.TOTAL_WIDTH and 0 <= trail_y < config.TOTAL_HEIGHT:
                            if trail == 0:
                                self.led.set_pixel(trail_x, trail_y, (0, 255, 255))  # Cyan
                            else:
                                self.led.set_pixel(trail_x, trail_y, (0, 200, 200))  # Light cyan
                
                angle += 0.2
                radius += 0.1
                
                if radius > max_radius:
                    radius = 0
                    angle = 0
            
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print(f"🌀 Spiral animation completed")
    
    def run_bubbles_animation(self, duration=30):
        """Run bubbles animation."""
        print(f"🫧 Starting Bubbles animation for {duration} seconds...")
        
        start_time = time.time()
        bubbles = []
        
        # Initialize some bubbles
        for _ in range(3):
            bubble = {
                'position': (random.randint(2, config.TOTAL_WIDTH-2), random.randint(0, config.TOTAL_HEIGHT)),
                'radius': random.randint(2, 4),
                'speed': random.uniform(0.5, 1.5),
                'opacity': random.uniform(0.6, 1.0),
                'age': random.randint(0, 50),
                'active': True
            }
            bubbles.append(bubble)
        
        while self.running and (time.time() - start_time) < duration:
            # Clear and create bubbles
            self.led.clear()
            
            # Update bubbles
            for bubble in bubbles:
                if bubble['active']:
                    x, y = bubble['position']
                    y -= bubble['speed']
                    x += random.uniform(-0.2, 0.2)
                    
                    bubble['position'] = (x, y)
                    bubble['age'] += 1
                    
                    if y < -bubble['radius'] or bubble['age'] > 200:
                        bubble['active'] = False
            
            # Add new bubbles
            if random.random() < 0.1 and len(bubbles) < 8:
                new_bubble = {
                    'position': (random.randint(2, config.TOTAL_WIDTH-2), config.TOTAL_HEIGHT + 5),
                    'radius': random.randint(2, 4),
                    'speed': random.uniform(0.5, 1.5),
                    'opacity': random.uniform(0.6, 1.0),
                    'age': 0,
                    'active': True
                }
                bubbles.append(new_bubble)
            
            # Remove inactive bubbles
            bubbles = [bubble for bubble in bubbles if bubble['active']]
            
            # Draw bubbles
            for bubble in bubbles:
                if bubble['active']:
                    x, y = bubble['position']
                    radius = bubble['radius']
                    opacity = bubble['opacity']
                    
                    # Draw bubble
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if dx * dx + dy * dy <= radius * radius:
                                pixel_x = int(x + dx)
                                pixel_y = int(y + dy)
                                
                                if 0 <= pixel_x < config.TOTAL_WIDTH and 0 <= pixel_y < config.TOTAL_HEIGHT:
                                    color = (150, 200, 255)  # Light blue
                                    final_color = tuple(int(c * opacity) for c in color)
                                    self.led.set_pixel(pixel_x, pixel_y, final_color)
            
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print(f"🫧 Bubbles animation completed")
    
    def run_shooting_star_animation(self, duration=30):
        """Run shooting star animation."""
        print(f"⭐ Starting Shooting Star animation for {duration} seconds...")
        
        start_time = time.time()
        cycle_time = 0
        cycle_duration = 2.0  # 2 seconds per cycle
        
        while self.running and (time.time() - start_time) < duration:
            current_time = time.time() - start_time
            cycle_time = current_time % cycle_duration
            
            # Clear the display
            self.led.clear()
            
            # Calculate star position (diagonal from top-left to bottom-right)
            progress = cycle_time / cycle_duration
            
            # Start position (top-left)
            start_x = 0
            start_y = 0
            
            # End position (bottom-right)
            end_x = config.TOTAL_WIDTH - 1
            end_y = config.TOTAL_HEIGHT - 1
            
            # Current star position
            star_x = int(start_x + (end_x - start_x) * progress)
            star_y = int(start_y + (end_y - start_y) * progress)
            
            # Draw the star and trail
            if 0 <= star_x < config.TOTAL_WIDTH and 0 <= star_y < config.TOTAL_HEIGHT:
                # Draw bright white star
                self.led.set_pixel(star_x, star_y, (255, 255, 255))
                
                # Draw blue trail behind the star
                trail_length = 8
                for i in range(1, trail_length + 1):
                    # Calculate trail position (behind the star)
                    trail_x = star_x - i
                    trail_y = star_y - i
                    
                    if 0 <= trail_x < config.TOTAL_WIDTH and 0 <= trail_y < config.TOTAL_HEIGHT:
                        # Fade the trail (brighter closer to star)
                        fade = 1.0 - (i / trail_length)
                        blue_intensity = int(255 * fade)
                        
                        # Blue trail with fade
                        trail_color = (0, 0, blue_intensity)
                        self.led.set_pixel(trail_x, trail_y, trail_color)
                
                # Add some sparkle effects around the star
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue  # Skip the star itself
                        
                        sparkle_x = star_x + dx
                        sparkle_y = star_y + dy
                        
                        if 0 <= sparkle_x < config.TOTAL_WIDTH and 0 <= sparkle_y < config.TOTAL_HEIGHT:
                            if random.random() < 0.3:  # 30% chance for sparkle
                                self.led.set_pixel(sparkle_x, sparkle_y, (200, 200, 255))  # Light blue sparkle
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS for smooth motion
        
        print(f"⭐ Shooting Star animation completed")
    
    def run(self):
        """Main application loop."""
        print("🎮 Final LED Controller Started")
        print("=" * 50)
        print("Hardware Configuration:")
        print(f"  LED Pin: {config.LED_PIN}")
        print(f"  Button Pins: {config.BUTTON_PINS}")
        print(f"  Total LEDs: {config.TOTAL_LEDS}")
        print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print("=" * 50)
        print()
        print("🎯 Theme Configuration:")
        for i, theme in self.themes.items():
            pin = config.BUTTON_PINS[i]
            anim_count = len(theme['animations'])
            print(f"  Pin {pin}: {theme['name']} ({anim_count} animations)")
        print()
        print("🎯 Instructions:")
        print("  - Press ANY of the 4 buttons to start a theme animation")
        print("  - Each animation runs for 30 seconds")
        print("  - Press Ctrl+C to exit")
        print()
        
        # Start button monitoring
        self.button_controller.start_monitoring()
        
        # Initial display
        self.led.fill_display(config.COLORS['BLUE'])
        self.led.show()
        time.sleep(1)
        self.led.clear()
        self.led.show()
        
        print("✅ Ready! Press any button to start...")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up...")
        self.running = False
        self.stop_current_animation()
        self.button_controller.cleanup()
        self.led.cleanup()
        if self.audio_available:
            pygame.mixer.quit()
        print("✅ Cleanup completed.")

def main():
    """Main entry point."""
    try:
        print("🚀 Starting Final LED Controller...")
        app = FinalLEDController()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
