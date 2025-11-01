#!/usr/bin/env python3
"""
Main application for Raspberry Pi LED Display Project
Controls 6 LED panels (32x8 each) to create a 48x32 display
"""

import time
import signal
import sys
import threading
import subprocess
import os
import random
import math
# from led_controller import LEDController  # Using LEDControllerExact instead
from display_patterns import DisplayPatterns
from button_controller import ButtonController
# from squares_animation import SquaresAnimation  # File not found
from led_controller_exact import LEDControllerExact
import config

# Try to import pygame for audio support
try:
    import pygame
    AUDIO_AVAILABLE = True
except ImportError:
    print("⚠️ Pygame not available, audio will be disabled")
    AUDIO_AVAILABLE = False
    pygame = None

class LEDDisplayApp:
    def __init__(self):
        """Initialize the LED display application."""
        print("🔧 Initializing LED controller...")
        self.led = LEDControllerExact()
        
        # Test LED controller immediately   
        print("🔧 Testing LED controller...")
        self.led.clear()
        self.led.show()
        time.sleep(0.2)
        
        self.patterns = DisplayPatterns(self.led)
        # self.squares_animation = SquaresAnimation(self.led)  # File not found
        print("🔧 Initializing button controller...")
        self.button_controller = ButtonController()
        
        # Test button controller
        time.sleep(0.2)
        
        self.current_pattern = None
        self.running = True
        
        # Shape animation system - 4 animations cycling
        self.shape_animations = [
            "squares", "triangles", "bubbles", "stars"
        ]
        self.current_shape_index = 0
        self.current_shape_process = None
        self.shape_animation_running = False
        
        # Nature animation system
        self.nature_animations = [
            "floating_clouds_animation.py",
            "rain_animation.py",
            "growing_flowers_animation.py",
            "apple_tree_animation.py"
        ]
        self.current_nature_index = 0
        self.nature_animation_running = False
        
        # Objects animation system
        self.objects_animations = [
            "house", "clock", "traffic_lights", "umbrella"
        ]
        self.current_object_index = 0
        self.objects_animation_running = False
        
        # Clock/House animation cycling for Button 27
        self.show_clock_first = True
        self.clock_animation_running = False
        self.house_animation_running = False
        
        # Initialize audio system
        self.audio_available = False
        if AUDIO_AVAILABLE:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.audio_available = True
                print("🔊 Audio system initialized")
            except Exception as e:
                print(f"⚠️ Audio system not available: {e}")
                self.audio_available = False
        
        # Audio file mapping for animations
        # Place audio files in an 'audio' folder in the project directory
        self.animation_audio = {
            'big_rectangle': 'big_rectangle.wav',
            'floating_clouds': 'floating_clouds.wav',
            'rain': 'rain.wav',
            'growing_flowers': 'growing_flowers.wav',
            'apple_tree': 'apple_tree.wav',
            'squares': 'squares.wav',
            'triangles': 'triangles.wav',
            'bubbles': 'bubbles.wav',
            'stars': 'stars.wav',
            'house': 'house.wav',
            'clock': 'clock.wav',
            'traffic_lights': 'traffic_lights.wav',
            'umbrella': 'umbrella.wav',
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for the 4 buttons."""
        # Button 18 (index 0) - Shapes
        self.button_controller.register_callback(0, self.start_shapes_animation)
        # Button 17 (index 1) - Nature animations
        self.button_controller.register_callback(1, self.start_nature_animation)
        # Button 27 (index 2) - Clock/House animation (cycle between them)
        self.button_controller.register_callback(2, self.start_clock_or_house_animation)
        # Button 22 (index 3) - Objects animations
        self.button_controller.register_callback(3, self.start_objects_animation)
    
    def play_animation_audio(self, animation_name):
        """Play audio for the specified animation."""
        if not self.audio_available:
            return
        
        if animation_name in self.animation_audio:
            audio_file = self.animation_audio[animation_name]
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            audio_path = os.path.join(script_dir, 'audio', audio_file)
            
            if os.path.exists(audio_path):
                try:
                    pygame.mixer.music.load(audio_path)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    print(f"🔊 Playing audio for {animation_name}: {audio_file}")
                except Exception as e:
                    print(f"⚠️ Error playing audio {audio_file}: {e}")
            else:
                print(f"⚠️ Audio file not found: {audio_path}")
                print(f"   Looking for: {audio_path}")
        else:
            print(f"⚠️ No audio mapped for animation: {animation_name}")
    
    def stop_animation_audio(self):
        """Stop any currently playing animation audio."""
        if not self.audio_available:
            return
        
        try:
            pygame.mixer.music.stop()
            print("🔇 Stopped animation audio")
        except Exception as e:
            print(f"⚠️ Error stopping audio: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down LED display...")
        self.cleanup()
        sys.exit(0)
    
    def stop_current_shape_animation(self):
        """Stop the currently running shape animation."""
        if self.current_shape_process and self.current_shape_process.poll() is None:
            print("🛑 Stopping current shape animation...")
            self.current_shape_process.terminate()
            self.current_shape_process.wait()
            self.current_shape_process = None
            print("✅ Shape animation stopped")
    
    def start_shapes_animation(self):
        """Start shapes animation - cycles through different shapes."""
        print("🔷 Starting shapes animation...")
        self.stop_current_pattern()
        
        # Small delay to ensure everything is stopped
        time.sleep(0.1)
        
        # Ensure we have animations available
        if not self.shape_animations:
            print("⚠️ No shape animations available")
            return
        
        # Cycle to next shape with bounds checking
        self.current_shape_index = (self.current_shape_index + 1) % len(self.shape_animations)
        
        shape_names = ["Squares", "Triangles", "Bubbles", "Stars"]
        
        # Ensure index is within bounds
        if self.current_shape_index >= len(shape_names):
            self.current_shape_index = 0
        
        shape_name = shape_names[self.current_shape_index]
        
        print(f"🎬 Starting {shape_name} animation...")
        
        # Start the shape animation as a thread
        self.current_pattern = threading.Thread(target=self.run_shape_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print(f"✅ Started {shape_name} animation")
    
    def start_nature_animation(self):
        """Start nature animation - cycles through different nature scenes."""
        print("🌿 Starting nature animation...")
        print(f"🔧 Current state - flag: {self.nature_animation_running}, index: {self.current_nature_index}")
        
        # Stop any current animation and wait for it to fully stop
        self.stop_current_pattern()
        time.sleep(0.3)  # Even longer wait to ensure everything is stopped
        
        # Ensure the flag is False before starting new animation
        self.nature_animation_running = False
        time.sleep(0.2)  # Longer pause
        
        # Cycle to next nature animation
        self.current_nature_index = (self.current_nature_index + 1) % len(self.nature_animations)
        nature_file = self.nature_animations[self.current_nature_index]
        nature_name = nature_file.replace('_animation.py', '').replace('_', ' ').title()
        
        print(f"🌿 Starting {nature_name}...")
        print(f"🔧 About to set flag to True")
        
        # Set the flag BEFORE starting the thread
        self.nature_animation_running = True
        print(f"🔧 Flag set to: {self.nature_animation_running}")
        
        # Additional verification
        if not self.nature_animation_running:
            print("❌ CRITICAL ERROR: Flag is still False after setting!")
            return
        
        # Start the nature animation as a thread
        self.current_pattern = threading.Thread(target=self.run_nature_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print(f"✅ Started {nature_name}")
        print(f"🔧 Thread started, flag should be: {self.nature_animation_running}")
        
        # FALLBACK: If thread doesn't work, try direct call
        time.sleep(0.1)  # Brief wait to see if thread starts
        if not self.current_pattern.is_alive():
            print("⚠️ Thread not alive, trying direct call...")
            self.run_nature_animation()
    
    def run_nature_animation(self):
        """Run the current nature animation."""
        print(f"🔧 run_nature_animation called, flag: {self.nature_animation_running}, index: {self.current_nature_index}")
        try:
            if self.current_nature_index == 0:
                self.run_floating_clouds()
            elif self.current_nature_index == 1:
                self.run_rain_animation()
            elif self.current_nature_index == 2:
                self.run_growing_flowers_animation()
            elif self.current_nature_index == 3:
                self.run_apple_tree_animation()
        finally:
            self.nature_animation_running = False
            print(f"🔧 Animation finished, flag set to: {self.nature_animation_running}")
    
    def run_floating_clouds(self):
        """Run floating clouds animation."""
        import math
        # Play audio for this animation
        self.play_animation_audio('floating_clouds')
        
        duration = 30
        start_time = time.time()
        
        print(f"🌤️ Floating clouds animation started (flag: {self.nature_animation_running})")
        
        # Double-check the flag is still True
        if not self.nature_animation_running:
            print("❌ Animation flag is False, stopping clouds")
            return
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Initialize clouds
        clouds = []
        for _ in range(4):
            cloud = {
                'x': random.randint(-10, width + 10),
                'y': random.randint(10, height - 10),
                'size': random.randint(8, 15),
                'speed': random.uniform(0.3, 0.8),
                'drift_phase': random.uniform(0, 2 * math.pi)
            }
            clouds.append(cloud)
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display
            self.led.clear()
            
            # Create sky background with gradient blue (like the image)
            for y in range(height):
                # Gradient from darker blue at top to lighter blue at bottom
                sky_intensity = 1.0 - (y / height) * 0.3
                # Sky blue gradient: darker at top, lighter at bottom
                sky_color = (int(80 * sky_intensity), int(120 * sky_intensity), int(180 * sky_intensity))
                
                for x in range(width):
                    self.led.set_pixel(x, y, sky_color)
            
            # Draw clouds
            for cloud in clouds:
                center_x = int(cloud['x'])
                center_y = int(cloud['y'])
                size = cloud['size']
                
                # Add gentle drift
                drift_x = math.sin(cloud['drift_phase'] + (time.time() - start_time) * 0.02) * 2
                drift_y = math.cos(cloud['drift_phase'] + (time.time() - start_time) * 0.015) * 1
                
                center_x += int(drift_x)
                center_y += int(drift_y)
                
                # Draw cloud with image-style colors and shape
                for y in range(max(0, center_y - size), min(height, center_y + size)):
                    for x in range(max(0, center_x - size), min(width, center_x + size)):
                        dx = x - center_x
                        dy = y - center_y
                        distance = math.sqrt(dx*dx + dy*dy)
                        
                        # Create organic cloud shape (not perfect circle)
                        cloud_radius = size * (0.7 + math.sin(x * 0.3 + y * 0.2) * 0.3)
                        
                        if distance <= cloud_radius:
                            # Calculate position within cloud for color variation
                            cloud_progress = distance / cloud_radius
                            
                            # Main cloud body: creamy yellow/off-white (#FFFDD0)
                            if dy < center_y - size * 0.2:  # Top part of cloud
                                cloud_color = (255, 253, 208)  # Creamy yellow-white
                            # Cloud underside: warm peach shadow (#E0B0A0)
                            elif dy > center_y + size * 0.1:  # Bottom part of cloud
                                cloud_color = (224, 176, 160)  # Warm peach
                            # Middle transition area
                            else:
                                # Blend between creamy and peach
                                blend = (dy - (center_y - size * 0.2)) / (size * 0.3)
                                blend = max(0, min(1, blend))
                                cloud_color = (
                                    int(255 * (1 - blend) + 224 * blend),
                                    int(253 * (1 - blend) + 176 * blend),
                                    int(208 * (1 - blend) + 160 * blend)
                                )
                            
                            # Add soft edge fade
                            edge_fade = 1.0 - cloud_progress * 0.3
                            cloud_color = tuple(int(c * edge_fade) for c in cloud_color)
                            
                            self.led.set_pixel(x, y, cloud_color)
            
            # Update cloud positions
            for cloud in clouds:
                cloud['x'] += cloud['speed']
                cloud['y'] += math.sin((time.time() - start_time) * 0.01 + cloud['drift_phase']) * 0.2
                
                if cloud['x'] > width + 20:
                    cloud['x'] = -20
                    cloud['y'] = random.randint(10, height - 10)
            
                self.led.show()
                time.sleep(0.1)  # 10 FPS for gentle movement
    
    def run_rain_animation(self):
        """Run rain animation with gentle drops and soft colors."""
        import math
        # Play audio for this animation
        self.play_animation_audio('rain')
        
        duration = 30
        start_time = time.time()
        
        print(f"🌧️ Rain animation started (flag: {self.nature_animation_running})")
        
        # Double-check the flag is still True
        if not self.nature_animation_running:
            print("❌ Animation flag is False, stopping rain")
            return
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Initialize rain drops
        rain_drops = []
        for _ in range(25):  # 25 rain drops
            drop = {
                'x': random.randint(0, width - 1),
                'y': random.randint(-10, height + 10),
                'speed': random.uniform(1.5, 3.0),
                'intensity': random.uniform(0.3, 1.0),
                'length': random.randint(3, 8)
            }
            rain_drops.append(drop)
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display
            self.led.clear()
            
            # Create black background
            for y in range(height):
                for x in range(width):
                    self.led.set_pixel(x, y, (0, 0, 0))  # Pure black background
            
            # Draw rain drops
            for drop in rain_drops:
                # Draw the rain drop as a vertical line
                for i in range(drop['length']):
                    y_pos = int(drop['y']) - i
                    if 0 <= y_pos < height:
                        # Rain drop color: white to yellow gradient
                        intensity = drop['intensity'] * (1.0 - (i / drop['length']) * 0.3)
                        
                        # Mix white and yellow based on drop position
                        white_amount = random.uniform(0.3, 0.8)  # Vary between drops
                        yellow_amount = 1.0 - white_amount
                        
                        rain_color = (
                            int(255 * intensity * white_amount + 255 * intensity * yellow_amount),
                            int(255 * intensity * white_amount + 200 * intensity * yellow_amount),
                            int(255 * intensity * white_amount + 0 * intensity * yellow_amount)
                        )
                        self.led.set_pixel(int(drop['x']), y_pos, rain_color)
            
            # Update rain drop positions
            for drop in rain_drops:
                drop['y'] += drop['speed']
                
                # Reset drop when it goes off screen
                if drop['y'] > height + 10:
                    drop['y'] = random.randint(-10, -5)
                    drop['x'] = random.randint(0, width - 1)
                    drop['speed'] = random.uniform(1.5, 3.0)
                    drop['intensity'] = random.uniform(0.3, 1.0)
            
            # Lightning flash removed to prevent flickering
            
            self.led.show()
            time.sleep(0.08)  # 12.5 FPS for smooth rain
    
    def run_growing_flowers_animation(self):
        """Run growing flowers animation with gentle swaying and blooming."""
        import math
        # Play audio for this animation
        self.play_animation_audio('growing_flowers')
        
        duration = 30
        start_time = time.time()
        
        print(f"🌸 Growing flowers animation started (flag: {self.nature_animation_running})")
        
        # Double-check the flag is still True
        if not self.nature_animation_running:
            print("❌ Animation flag is False, stopping flowers")
            return
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Initialize single flower
        flower_colors = [
            (255, 182, 193),  # Pink
            (255, 192, 203),  # Light pink
            (255, 255, 224),  # Light yellow
            (255, 218, 185),  # Peach
            (221, 160, 221),  # Plum
            (255, 228, 196),   # Bisque
            (255, 239, 213)   # Papaya whip
        ]
        
        # Create single flower in the center
        flower = {
            'x': width // 2,  # Center of display
            'y': height - 8,  # Start from ground
            'stem_height': 0,  # Will grow
            'max_stem_height': 20,  # Increased height (was 12)
            'petal_size': 0,  # Will grow
            'max_petal_size': 5,  # Fixed size
            'color': random.choice(flower_colors),
            'bloom_progress': 0,  # 0 to 1
            'sway_phase': 0,  # Start phase
            'sway_amount': 1.0  # Gentle sway
        }
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display (dark background)
            self.led.clear()
            
            # Background is now dark (black) - no sky gradient
            
            # Draw ground
            for x in range(width):
                for y in range(height - 3, height):
                    ground_color = (139, 69, 19)  # Brown ground
                    self.led.set_pixel(x, y, ground_color)
            
            # Draw single flower
            # Draw stem (with one extra column for thickness)
            stem_color = (34, 139, 34)  # Forest green
            for i in range(int(flower['stem_height'])):
                y_pos = height - 1 - i
                # Draw main stem column
                if 0 <= y_pos < height and 0 <= flower['x'] < width:
                    self.led.set_pixel(flower['x'], y_pos, stem_color)
                # Draw additional column to make stalk wider
                if 0 <= y_pos < height and 0 <= flower['x'] + 1 < width:
                    self.led.set_pixel(flower['x'] + 1, y_pos, stem_color)
            
            # Draw flower petals if bloomed (with gentle sway)
            if flower['bloom_progress'] > 0.3:
                # Calculate gentle sway for petals only
                sway_x = math.sin(flower['sway_phase'] + (time.time() - start_time) * 0.3) * flower['sway_amount']
                petal_x = int(flower['x'] + sway_x)
                petal_size = int(flower['petal_size'] * flower['bloom_progress'])
                flower_y = height - 1 - int(flower['stem_height'])
                
                # Safety check for petal_size
                if petal_size > 0:
                    # Draw petals in a circle
                    for dy in range(-petal_size, petal_size + 1):
                        for dx in range(-petal_size, petal_size + 1):
                            distance = math.sqrt(dx*dx + dy*dy)
                            if distance <= petal_size:
                                x = petal_x + dx
                                y = flower_y + dy
                                if 0 <= x < width and 0 <= y < height:
                                    # Add some petal variation
                                    petal_intensity = 1.0 - (distance / petal_size) * 0.3
                                    petal_color = (
                                        int(flower['color'][0] * petal_intensity),
                                        int(flower['color'][1] * petal_intensity),
                                        int(flower['color'][2] * petal_intensity)
                                    )
                                    self.led.set_pixel(x, y, petal_color)
            
            # Update single flower growth
            # Grow stem
            if flower['stem_height'] < flower['max_stem_height']:
                flower['stem_height'] += 0.1
            
            # Start blooming when stem is ready
            if flower['stem_height'] >= flower['max_stem_height'] * 0.8:
                flower['bloom_progress'] = min(1.0, flower['bloom_progress'] + 0.02)
                flower['petal_size'] = flower['max_petal_size'] * flower['bloom_progress']
            
            # Update sway phase for petals only
            flower['sway_phase'] += 0.05
            
            self.led.show()
            time.sleep(0.1)  # 10 FPS for gentle movement
    
    def run_bubbles_animation(self):
        """Run bubbles animation with colorful bubbles rising from bottom."""
        import math
        # Play audio for this animation
        self.play_animation_audio('bubbles')
        
        duration = 30
        start_time = time.time()
        
        print(f"🫧 Bubbles animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Bubble colors - soft, translucent colors
        bubble_colors = [
            (100, 200, 255),  # Light blue
            (255, 150, 200),  # Pink
            (200, 255, 150),  # Light green
            (255, 200, 100),  # Orange
            (200, 150, 255),  # Purple
            (150, 255, 200),  # Mint green
            (255, 100, 150),  # Rose
            (100, 255, 255),  # Cyan
        ]
        
        # Animation parameters
        bubble_spawn_rate = 0.3  # New bubble every 0.3 seconds
        max_bubbles = 15  # Maximum number of bubbles on screen
        bubble_sizes = [2, 3, 4, 5]  # Different bubble sizes
        rise_speeds = [0.5, 0.8, 1.2, 1.5]  # Different rise speeds
        
        # Bubble storage
        bubbles = []
        last_spawn_time = 0
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display with black background
            self.led.clear()
            
            current_time = time.time() - start_time
            
            # Spawn new bubbles
            if current_time - last_spawn_time >= bubble_spawn_rate and len(bubbles) < max_bubbles:
                bubble = {
                    'x': random.randint(2, width - 3),
                    'y': height - 1,  # Start at bottom
                    'size': random.choice(bubble_sizes),
                    'speed': random.choice(rise_speeds),
                    'color': random.choice(bubble_colors),
                    'wobble_phase': random.uniform(0, 2 * math.pi),
                    'wobble_amplitude': random.uniform(0.5, 1.5)
                }
                bubbles.append(bubble)
                last_spawn_time = current_time
            
            # Update and draw bubbles
            bubbles_to_remove = []
            for i, bubble in enumerate(bubbles):
                # Update bubble position - only upward movement
                bubble['y'] -= bubble['speed']
                
                # No horizontal movement - bubbles move straight up
                bubble_x = int(bubble['x'])
                bubble_y = int(bubble['y'])
                
                # Remove bubbles that have risen off screen
                if bubble_y < -bubble['size']:
                    bubbles_to_remove.append(i)
                    continue
                
                # Draw bubble with soft, translucent effect
                size = bubble['size']
                color = bubble['color']
                
                # Draw bubble with soft edges
                for dy in range(-size, size + 1):
                    for dx in range(-size, size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        if distance <= size:
                            x = bubble_x + dx
                            y = bubble_y + dy
                            
                            if 0 <= x < width and 0 <= y < height:
                                # Create translucent effect
                                intensity = 1.0 - (distance / size) * 0.5
                                r = int(color[0] * intensity)
                                g = int(color[1] * intensity)
                                b = int(color[2] * intensity)
                                
                                # Add some sparkle effect
                                if random.random() < 0.1:
                                    r = min(255, r + 50)
                                    g = min(255, g + 50)
                                    b = min(255, b + 50)
                                
                                self.led.set_pixel(x, y, (r, g, b))
            
            # Remove bubbles that are off screen
            for i in reversed(bubbles_to_remove):
                bubbles.pop(i)
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS for smooth bubble movement
        
        # Cleanup when animation ends
        self.nature_animation_running = False
        print("🫧 Bubbles animation finished")
    
    def run_apple_tree_animation(self):
        """Run apple tree animation with falling apple."""
        import math
        # Play audio for this animation
        self.play_animation_audio('apple_tree')
        
        start_time = time.time()
        
        print(f"🌳 Apple Tree animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Colors
        brown_trunk = (139, 69, 19)  # Dark brown for trunk
        brown_soil = (101, 67, 33)  # Brown soil color
        green_leaves = (34, 139, 34)  # Forest green for leaves
        red_apple = (255, 0, 0)  # Bright red for apples
        apple_stem = (101, 67, 33)  # Brown for apple stems
        
        # Tree structure
        trunk_width = 6
        trunk_height = 16
        trunk_x = 13  # Centered trunk
        trunk_y = 47  # Bottom of trunk (touching ground)
        
        # Apple positions (7 apples) - better distributed
        apple_positions = [
            (16, 6),   # Top center
            (9, 10),   # Upper left
            (23, 10),  # Upper right
            (6, 16),   # Mid left
            (26, 16),  # Mid right
            (11, 22),  # Lower left
            (21, 22),  # Lower right
        ]
        
        # Each apple starts falling 3 seconds after the previous one
        falling_apple_start_delay = 3  # First apple starts after 3 seconds
        seconds_between_apples = 3  # 3 seconds between each apple
        falling_apple_fall_duration = 3  # Takes 3 seconds to fall
        
        # Calculate animation duration: last apple finishes + 3 seconds
        num_apples = len(apple_positions)
        last_apple_index = num_apples - 1
        last_apple_start_time = falling_apple_start_delay + (last_apple_index * seconds_between_apples)
        last_apple_finish_time = last_apple_start_time + falling_apple_fall_duration
        duration = last_apple_finish_time + 3  # Add 3 seconds after last apple falls
        
        # Ground level
        ground_y = 44
        
        def draw_trunk():
            """Draw the tree trunk (no branches)."""
            # Main trunk only (no branches)
            for y in range(trunk_height):
                for x in range(trunk_width):
                    pixel_x = trunk_x + x
                    pixel_y = trunk_y - y
                    if 0 <= pixel_x < width and 0 <= pixel_y < height:
                        # Only draw trunk pixels that are above ground level
                        if pixel_y < ground_y:
                            self.led.set_pixel(pixel_x, pixel_y, brown_trunk)
        
        def draw_leaves():
            """Draw the tree canopy/leaves."""
            # Main canopy area - larger and more realistic
            center_x = 16
            center_y = 18
            radius = 14
            
            for y in range(height):
                for x in range(width):
                    # Calculate distance from center
                    dx = x - center_x
                    dy = y - center_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    # Draw leaves in circular area with some variation
                    if distance <= radius and y >= 4 and y <= 30:
                        # Add some texture variation
                        if (x + y) % 3 == 0:  # Skip some pixels for texture
                            continue
                        self.led.set_pixel(x, y, green_leaves)
        
        def draw_apples(exclude_falling_indices=None):
            """Draw all apples except the ones that are falling."""
            if exclude_falling_indices is None:
                exclude_falling_indices = set()
            
            for i, (apple_x, apple_y) in enumerate(apple_positions):
                # Skip apples that are falling
                if i in exclude_falling_indices:
                    continue
                    
                # Draw apple
                self.led.set_pixel(apple_x, apple_y, red_apple)
                # Draw stem
                if apple_y > 0:
                    self.led.set_pixel(apple_x, apple_y - 1, apple_stem)
        
        def draw_falling_apple(apple_index, progress):
            """Draw a falling apple with gravity effect."""
            # Get the starting position of this apple
            start_pos = apple_positions[apple_index]
            start_x, start_y = start_pos
            
            # Calculate falling position with gravity
            # Apple starts at start_y, ground is at y=44, so need to fall (44 - start_y) pixels
            fall_distance = progress * (ground_y - start_y)  # Total fall distance to ground
            gravity_effect = progress * progress * 0.5  # Gravity acceleration
            
            current_x = start_x
            current_y = start_y + fall_distance + gravity_effect
            
            # Keep apple within bounds
            current_x = max(0, min(width - 1, int(current_x)))
            current_y = max(0, min(height - 1, int(current_y)))
            
            # Draw falling apple
            if 0 <= current_x < width and 0 <= current_y < height:
                self.led.set_pixel(current_x, current_y, red_apple)
                # Draw stem
                if current_y > 0:
                    self.led.set_pixel(current_x, current_y - 1, apple_stem)
            
            return current_x  # Return x position for ground placement
        
        def draw_apple_on_ground(apple_x):
            """Draw an apple on the ground at the specified x position."""
            # Draw apple at ground level
            ground_apple_y = ground_y  # Ground level
            if 0 <= apple_x < width and 0 <= ground_apple_y < height:
                self.led.set_pixel(apple_x, ground_apple_y, red_apple)
                # Draw stem above the apple
                if ground_apple_y > 0:
                    self.led.set_pixel(apple_x, ground_apple_y - 1, apple_stem)
        
        def draw_ground():
            """Draw brown soil ground."""
            for x in range(width):
                for y in range(ground_y, height):
                    self.led.set_pixel(x, y, brown_soil)
        
        # Track apples that have fallen to the ground (apple_index: ground_x_position)
        fallen_apples = {}
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Draw ground first (background)
            draw_ground()
            
            # Draw tree trunk
            draw_trunk()
            
            # Draw leaves
            draw_leaves()
            
            # Handle falling apples - each starts 3 seconds after the previous one
            falling_indices = set()
            for i in range(len(apple_positions)):
                # Skip apples that have already fallen
                if i in fallen_apples:
                    continue
                
                # Calculate when this apple should start falling
                apple_start_time = falling_apple_start_delay + (i * seconds_between_apples)
                
                if elapsed >= apple_start_time:
                    # This apple is falling or has fallen
                    fall_progress = (elapsed - apple_start_time) / falling_apple_fall_duration
                    fall_progress = min(1.0, fall_progress)  # Clamp to 1.0
                    
                    if fall_progress < 1.0:
                        # Apple is still falling
                        falling_indices.add(i)
                        apple_x = draw_falling_apple(i, fall_progress)
                    else:
                        # Apple has finished falling - add to fallen apples
                        start_pos = apple_positions[i]
                        apple_x = start_pos[0]  # Use original x position
                        fallen_apples[i] = apple_x
            
            # Draw all apples that are still on the tree (not falling and not fallen)
            all_removed_indices = falling_indices | set(fallen_apples.keys())
            draw_apples(exclude_falling_indices=all_removed_indices)
            
            # Draw fallen apples on the ground
            for apple_index, ground_x in fallen_apples.items():
                draw_apple_on_ground(ground_x)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Keep final frame for a moment
        print("🌳 Apple Tree Animation completed!")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
        print("🌳 Animation finished")
    
    def start_house_animation(self):
        """Start house animation."""
        print("🏠 Starting house animation...")
        self.stop_current_pattern()
        time.sleep(0.3)  # Longer wait to ensure everything is stopped
        
        # Set flags
        self.animation_stop_flag = False
        self.house_animation_running = True
        
        # Start the house animation as a thread
        self.current_pattern = threading.Thread(target=self.run_house_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print("✅ Started house animation")
    
    def run_house_animation(self):
        """Run house animation with smoke rising from chimney."""
        import math
        import random
        # Play audio for this animation
        self.play_animation_audio('house')
        
        duration = 20
        start_time = time.time()
        
        print(f"🏠 House animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Colors from the image
        orange_house = (255, 165, 0)  # Orange house body
        red_roof = (236, 99, 88)      # #EC6358 - red roof
        brown_chimney = (139, 69, 19) # Brown chimney
        light_gray_window_frame = (180, 180, 180)  # Light gray window frame
        blue_window = (0, 100, 200)   # Bright blue window panes
        white_smoke = (255, 255, 255) # White smoke
        light_smoke = (240, 240, 240) # Light gray smoke
        
        # House dimensions and position
        house_x = 8   # Left edge of house
        house_y = 40  # Bottom of house
        house_width = 16
        house_height = 20
        
        # Roof dimensions - triangular roof with wider base
        roof_base_width = house_width + 4  # Roof base is wider than house
        roof_height = 12
        roof_top_y = house_y - house_height  # Roof bottom sits ON TOP of house
        
        # Chimney dimensions - sits on top of roof
        chimney_x = 20
        chimney_y = house_y - house_height - 2  # Chimney sits on top of roof
        chimney_width = 3
        chimney_height = 6
        
        # Window dimensions - centered inside house
        window_x = house_x + (house_width - 4) // 2  # Center window in house
        window_y = house_y - house_height + 8  # Position window inside house
        window_size = 4
        
        # Smoke particles
        smoke_particles = []
        smoke_start_time = 2  # Start smoke after 2 seconds
        
        def draw_house_body():
            """Draw the main house body (orange rectangle)."""
            for y in range(house_height):
                for x in range(house_width):
                    pixel_x = house_x + x
                    pixel_y = house_y - y
                    if 0 <= pixel_x < width and 0 <= pixel_y < height:
                        self.led.set_pixel(pixel_x, pixel_y, orange_house)
        
        def draw_roof():
            """Draw the triangular roof sitting properly on the house."""
            # House top is at: house_y - house_height
            # Roof base sits on house top
            roof_base_y = house_y - house_height
            
            # Draw a simple triangle pointing UP
            # Start from the base (house top) and go up to the apex
            for row in range(roof_height):
                y_pos = roof_base_y - row  # Go UP from base
                
                # Calculate how many pixels to draw on this row
                # Base row has full width, apex has 1 pixel
                pixels_to_draw = roof_base_width - (row * 2)
                
                if pixels_to_draw > 0:
                    # Center the pixels over the house
                    # The roof base is wider than the house, so center it properly
                    roof_offset = (roof_base_width - house_width) // 2
                    start_x = house_x - roof_offset + row
                    
                    # Draw the pixels for this row
                    for i in range(pixels_to_draw):
                        x_pos = start_x + i
                        if 0 <= x_pos < width and 0 <= y_pos < height:
                            self.led.set_pixel(x_pos, y_pos, red_roof)
        
        def draw_chimney():
            """Draw the brown chimney sitting on top of roof."""
            for y in range(chimney_height):
                for x in range(chimney_width):
                    pixel_x = chimney_x + x
                    pixel_y = chimney_y - y
                    if 0 <= pixel_x < width and 0 <= pixel_y < height:
                        self.led.set_pixel(pixel_x, pixel_y, brown_chimney)
        
        def draw_window():
            """Draw the window with frame and panes."""
            # Draw window frame
            for y in range(window_size + 2):
                for x in range(window_size + 2):
                    pixel_x = window_x - 1 + x
                    pixel_y = window_y - 1 + y
                    if 0 <= pixel_x < width and 0 <= pixel_y < height:
                        # Frame
                        if x == 0 or x == window_size + 1 or y == 0 or y == window_size + 1:
                            self.led.set_pixel(pixel_x, pixel_y, light_gray_window_frame)
                        # Window panes
                        else:
                            self.led.set_pixel(pixel_x, pixel_y, blue_window)
            
            # Draw cross frame
            center_x = window_x + window_size // 2
            center_y = window_y + window_size // 2
            
            # Vertical line
            for y in range(window_y, window_y + window_size):
                if 0 <= center_x < width and 0 <= y < height:
                    self.led.set_pixel(center_x, y, light_gray_window_frame)
            
            # Horizontal line
            for x in range(window_x, window_x + window_size):
                if 0 <= x < width and 0 <= center_y < height:
                    self.led.set_pixel(x, center_y, light_gray_window_frame)
        
        def add_smoke_particle():
            """Add a new smoke particle at the chimney top."""
            particle = {
                'x': chimney_x + chimney_width // 2 + random.uniform(-0.5, 0.5),
                'y': chimney_y - chimney_height + 1,  # Start from chimney top
                'life': 1.0,
                'speed': random.uniform(0.3, 0.6),
                'drift': random.uniform(-0.2, 0.2)
            }
            smoke_particles.append(particle)
        
        def update_smoke(elapsed):
            """Update smoke particles."""
            # Add new smoke particles
            if elapsed >= smoke_start_time:
                if random.random() < 0.3:  # 30% chance each frame
                    add_smoke_particle()
            
            # Update existing particles
            particles_to_remove = []
            for i, particle in enumerate(smoke_particles):
                # Move particle up and drift sideways
                particle['y'] -= particle['speed']
                particle['x'] += particle['drift']
                particle['life'] -= 0.02  # Fade out
                
                # Remove particles that are off-screen or faded
                if (particle['y'] < 0 or particle['life'] <= 0 or 
                    particle['x'] < 0 or particle['x'] >= width):
                    particles_to_remove.append(i)
            
            # Remove dead particles (in reverse order to maintain indices)
            for i in reversed(particles_to_remove):
                smoke_particles.pop(i)
        
        def draw_smoke():
            """Draw all smoke particles."""
            for particle in smoke_particles:
                x = int(particle['x'])
                y = int(particle['y'])
                
                if 0 <= x < width and 0 <= y < height:
                    # Fade smoke based on life
                    if particle['life'] > 0.7:
                        color = white_smoke
                    else:
                        color = light_smoke
                    
                    self.led.set_pixel(x, y, color)
                    
                    # Draw a small smoke puff (2x2 pixels)
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            smoke_x = x + dx
                            smoke_y = y + dy
                            if (0 <= smoke_x < width and 0 <= smoke_y < height and
                                random.random() < 0.6):  # Random smoke texture
                                self.led.set_pixel(smoke_x, smoke_y, color)
        
        while time.time() - start_time < duration and (self.objects_animation_running or self.house_animation_running) and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Draw house components
            draw_house_body()
            draw_roof()
            draw_chimney()
            draw_window()
            
            # Update and draw smoke
            update_smoke(elapsed)
            draw_smoke()
            
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
    
    def start_clock_animation(self):
        """Start clock animation."""
        print("🕐 Starting clock animation...")
        self.stop_current_pattern()
        time.sleep(0.3)  # Longer wait to ensure everything is stopped
        
        # Set flags
        self.animation_stop_flag = False
        self.clock_animation_running = True
        
        # Start the clock animation as a thread
        self.current_pattern = threading.Thread(target=self.run_clock_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print("✅ Started clock animation")
    
    def run_clock_animation(self):
        """Run clock animation with static hand pointing upward."""
        import math
        # Play audio for this animation
        self.play_animation_audio('clock')
        
        duration = 20
        start_time = time.time()
        
        print(f"🕐 Clock animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Colors from the image
        dark_teal = (0, 128, 128)  # Dark teal for ring and hand
        white_face = (255, 255, 255)  # White clock face
        yellow_markers = (255, 255, 0)  # Yellow hour markers
        
        # Clock dimensions and position
        clock_center_x = width // 2  # Center horizontally
        clock_center_y = height // 2  # Center vertically
        clock_radius = 12  # Clock radius
        
        def draw_clock():
            """Draw the complete clock."""
            # Draw outer ring (bezel)
            for angle in range(0, 360, 1):
                rad = math.radians(angle)
                x = int(clock_center_x + clock_radius * math.cos(rad))
                y = int(clock_center_y + clock_radius * math.sin(rad))
                if 0 <= x < width and 0 <= y < height:
                    self.led.set_pixel(x, y, dark_teal)
            
            # Draw white clock face
            for y in range(clock_center_y - clock_radius + 2, clock_center_y + clock_radius - 1):
                for x in range(clock_center_x - clock_radius + 2, clock_center_x + clock_radius - 1):
                    # Check if pixel is inside the circle
                    dx = x - clock_center_x
                    dy = y - clock_center_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= clock_radius - 2:
                        self.led.set_pixel(x, y, white_face)
            
            # Draw hour markers
            for hour in range(12):
                angle = hour * 30  # 30 degrees per hour
                rad = math.radians(angle)
                
                # Calculate marker position
                marker_radius = clock_radius - 3
                marker_x = int(clock_center_x + marker_radius * math.cos(rad))
                marker_y = int(clock_center_y + marker_radius * math.sin(rad))
                
                # Draw marker (longer for 12 o'clock)
                marker_length = 3 if hour == 0 else 2
                
                # Draw horizontal marker
                for i in range(-marker_length//2, marker_length//2 + 1):
                    marker_pixel_x = marker_x + i
                    marker_pixel_y = marker_y
                    if 0 <= marker_pixel_x < width and 0 <= marker_pixel_y < height:
                        self.led.set_pixel(marker_pixel_x, marker_pixel_y, yellow_markers)
            
            # Draw clock hand pointing upward (12 o'clock)
            hand_length = clock_radius - 4
            hand_x = clock_center_x
            hand_y = clock_center_y - hand_length
            
            # Draw hand base (small circle at center)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    base_x = clock_center_x + dx
                    base_y = clock_center_y + dy
                    if 0 <= base_x < width and 0 <= base_y < height:
                        self.led.set_pixel(base_x, base_y, dark_teal)
            
            # Draw hand line pointing upward
            for i in range(hand_length):
                hand_pixel_y = clock_center_y - i
                if 0 <= hand_x < width and 0 <= hand_pixel_y < height:
                    self.led.set_pixel(hand_x, hand_pixel_y, dark_teal)
        
        while time.time() - start_time < duration and self.clock_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Draw clock
            draw_clock()
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Keep final frame for a moment
        print("🕐 Clock Animation completed!")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
        print("🕐 Animation finished")
    
    def start_clock_or_house_animation(self):
        """Start clock or house animation based on cycling flag."""
        if self.show_clock_first:
            self.show_clock_first = False  # Next time show house
            self.start_clock_animation()
        else:
            self.show_clock_first = True  # Next time show clock
            self.start_house_animation()
    
    def start_lion_animation(self):
        """Start lion animation."""
        print("🦁 Starting lion animation...")
        self.stop_current_pattern()
        time.sleep(0.3)  # Longer wait to ensure everything is stopped
        
        # Set flags
        self.animation_stop_flag = False
        self.lion_animation_running = True
        
        # Start the lion animation as a thread
        self.current_pattern = threading.Thread(target=self.run_lion_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print("✅ Started lion animation")
    
    def run_lion_animation(self):
        """Run lion animation with gentle movement."""
        import math
        duration = 30
        start_time = time.time()
        
        print(f"🦁 Lion animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Lion colors (matching image)
        lion_colors = {
            'body': (255, 200, 0),      # Golden yellow body
            'mane': (139, 69, 19),      # Brown mane
            'mane_outline': (101, 50, 14),  # Darker brown outline
            'face': (255, 255, 0),      # Yellow face
            'eyes': (0, 0, 0),          # Black eyes
            'nose': (0, 0, 0),          # Black nose
            'whiskers': (0, 0, 0),      # Black whiskers
            'mouth': (0, 0, 0),         # Black mouth
            'blush': (255, 182, 193),   # Pink blush
            'tail_tuft': (101, 50, 14),  # Dark brown tail tuft
            'background': (245, 245, 220)  # Light cream background
        }
        
        while time.time() - start_time < duration and self.lion_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display
            self.led.clear()
            
            # Create light cream background
            for y in range(height):
                for x in range(width):
                    self.led.set_pixel(x, y, lion_colors['background'])
            
            # Calculate gentle movement
            sway_offset = math.sin((time.time() - start_time) * 0.5) * 1  # Gentle swaying
            
            # Lion center position
            center_x = width // 2 + int(sway_offset)
            center_y = height // 2
            
            # Draw lion mane (brown, wavy edge)
            for dy in range(-8, 9):
                for dx in range(-8, 9):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if 6 <= distance <= 8:  # Mane ring
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < width and 0 <= y < height:
                            self.led.set_pixel(x, y, lion_colors['mane'])
            
            # Draw mane outline
            for dy in range(-9, 10):
                for dx in range(-9, 10):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if 8 < distance <= 9:  # Mane outline
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < width and 0 <= y < height:
                            self.led.set_pixel(x, y, lion_colors['mane_outline'])
            
            # Draw lion body (golden yellow)
            for dy in range(-4, 5):
                for dx in range(-3, 4):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= 4:  # Body
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < width and 0 <= y < height:
                            self.led.set_pixel(x, y, lion_colors['body'])
            
            # Draw lion face (yellow)
            for dy in range(-3, 4):
                for dx in range(-2, 3):
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= 3:  # Face
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < width and 0 <= y < height:
                            self.led.set_pixel(x, y, lion_colors['face'])
            
            # Draw eyes (black dots)
            if 0 <= center_x - 1 < width and 0 <= center_y - 1 < height:
                self.led.set_pixel(center_x - 1, center_y - 1, lion_colors['eyes'])
            if 0 <= center_x + 1 < width and 0 <= center_y - 1 < height:
                self.led.set_pixel(center_x + 1, center_y - 1, lion_colors['eyes'])
            
            # Draw nose (black triangle)
            if 0 <= center_x < width and 0 <= center_y < height:
                self.led.set_pixel(center_x, center_y, lion_colors['nose'])
            
            # Draw whiskers (black lines)
            for i in range(-2, 3):
                if 0 <= center_x - 3 < width and 0 <= center_y + i < height:
                    self.led.set_pixel(center_x - 3, center_y + i, lion_colors['whiskers'])
                if 0 <= center_x + 3 < width and 0 <= center_y + i < height:
                    self.led.set_pixel(center_x + 3, center_y + i, lion_colors['whiskers'])
            
            # Draw mouth (curved line)
            if 0 <= center_x - 1 < width and 0 <= center_y + 2 < height:
                self.led.set_pixel(center_x - 1, center_y + 2, lion_colors['mouth'])
            if 0 <= center_x < width and 0 <= center_y + 2 < height:
                self.led.set_pixel(center_x, center_y + 2, lion_colors['mouth'])
            if 0 <= center_x + 1 < width and 0 <= center_y + 2 < height:
                self.led.set_pixel(center_x + 1, center_y + 2, lion_colors['mouth'])
            
            # Draw blush (pink cheeks)
            if 0 <= center_x - 2 < width and 0 <= center_y + 1 < height:
                self.led.set_pixel(center_x - 2, center_y + 1, lion_colors['blush'])
            if 0 <= center_x + 2 < width and 0 <= center_y + 1 < height:
                self.led.set_pixel(center_x + 2, center_y + 1, lion_colors['blush'])
            
            # Draw tail (curved)
            tail_x = center_x + 4
            tail_y = center_y + 2
            if 0 <= tail_x < width and 0 <= tail_y < height:
                self.led.set_pixel(tail_x, tail_y, lion_colors['body'])
            if 0 <= tail_x + 1 < width and 0 <= tail_y + 1 < height:
                self.led.set_pixel(tail_x + 1, tail_y + 1, lion_colors['body'])
            if 0 <= tail_x + 2 < width and 0 <= tail_y < height:
                self.led.set_pixel(tail_x + 2, tail_y, lion_colors['body'])
            
            # Draw tail tuft
            if 0 <= tail_x + 2 < width and 0 <= tail_y - 1 < height:
                self.led.set_pixel(tail_x + 2, tail_y - 1, lion_colors['tail_tuft'])
            
            self.led.show()
            time.sleep(0.2)  # Gentle animation speed
        
        # Cleanup when animation ends
        self.lion_animation_running = False
        print("🦁 Lion animation finished")
    
    def run_shape_animation(self):
        """Run the current shape animation."""
        self.shape_animation_running = True
        
        try:
            # Ensure index is within bounds
            if self.current_shape_index >= len(self.shape_animations):
                self.current_shape_index = 0
                print("⚠️ Shape index out of bounds, resetting to 0")
            
            if self.current_shape_index == 0:
                self.run_squares_animation()
            elif self.current_shape_index == 1:
                self.run_triangles_animation()
            elif self.current_shape_index == 2:
                self.run_bubbles_shape_animation()
            elif self.current_shape_index == 3:
                self.run_stars_animation()
            else:
                print(f"⚠️ Unknown shape index: {self.current_shape_index}")
        finally:
            self.shape_animation_running = False
    
    def run_squares_animation(self):
        """Run squares animation - squares appear randomly, fade in, fill screen."""
        import math
        # Play audio for this animation
        self.play_animation_audio('squares')
        
        width = 32
        height = 48
        
        # Square size: 1/16 of screen = 8x12 pixels (32/4 = 8, 48/4 = 12)
        square_width = 8
        square_height = 12
        
        # Colors - original plus additional
        colors = [
            (240, 135, 135),  # #F08787
            (255, 199, 167),  # #FFC7A7
            (254, 226, 173),  # #FEE2AD
            (248, 250, 180),  # #F8FAB4
            (78, 215, 241),   # #4ED7F1
            (111, 230, 252),  # #6FE6FC
            (168, 241, 255),  # #A8F1FF
            (255, 250, 141),  # #FFFA8D
            (117, 106, 182),  # #756AB6
            (172, 135, 197),  # #AC87C5
            (224, 174, 208),  # #E0AED0
            (255, 229, 229),  # #FFE5E5
        ]
        
        # Calculate grid positions for squares
        grid_cols = width // square_width  # 4 columns
        grid_rows = height // square_height  # 4 rows
        total_squares = grid_cols * grid_rows  # 16 squares
        
        # Calculate timing: enough time for all squares to appear + fade-in, then fade-out separately
        # 16 squares * 2 seconds = 32 seconds for all to appear
        # Plus 1 second fade-in for last square = 33 seconds main animation
        squares_appear_time = total_squares * 2  # 32 seconds for all squares
        fade_in_time = 1  # 1 second fade-in for last square
        main_animation_duration = squares_appear_time + fade_in_time  # 33 seconds
        fade_out_duration = 3  # 3 seconds fade-out after main animation
        
        start_time = time.time()
        
        # Track which squares have appeared
        appeared_squares = {}  # {(grid_x, grid_y): (appear_time, color)}
        
        print(f"🔲 Squares animation started")
        
        # Main animation: squares appear and fade in
        while time.time() - start_time < main_animation_duration and self.shape_animation_running:
            elapsed = time.time() - start_time
            
            # Add a new square every 2 seconds
            if elapsed > 0 and len(appeared_squares) < total_squares:
                next_square_time = len(appeared_squares) * 2
                if elapsed >= next_square_time:
                    # Find a random position that hasn't appeared yet
                    available_positions = []
                    for row in range(grid_rows):
                        for col in range(grid_cols):
                            if (col, row) not in appeared_squares:
                                available_positions.append((col, row))
                    
                    if available_positions:
                        pos = random.choice(available_positions)
                        color = random.choice(colors)
                        appeared_squares[pos] = (elapsed, color)
            
            # Clear display
            self.led.clear()
            
            # Draw all appeared squares with fade-in
            for (grid_x, grid_y), (appear_time, color) in appeared_squares.items():
                # Calculate fade-in progress (0 to 1 over 1 second)
                square_age = elapsed - appear_time
                fade_progress = min(1.0, square_age / 1.0)  # Fade in over 1 second
                fade_intensity = 1.0 - (1.0 - fade_progress) ** 2  # Ease-out
                
                # Calculate pixel position
                pixel_x_start = grid_x * square_width
                pixel_y_start = grid_y * square_height
                
                # Draw square
                for x in range(square_width):
                    for y in range(square_height):
                        px = pixel_x_start + x
                        py = pixel_y_start + y
                        if 0 <= px < width and 0 <= py < height:
                            final_color = (
                                int(color[0] * fade_intensity),
                                int(color[1] * fade_intensity),
                                int(color[2] * fade_intensity)
                            )
                            self.led.set_pixel(px, py, final_color)
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS
        
        # Fade out all squares smoothly (only after main animation completes)
        print("🔲 Fading out squares...")
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration and self.shape_animation_running:
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_out_intensity = 1.0 - (fade_progress ** 2)  # Ease-out
            
            # Clear display
            self.led.clear()
            
            # Draw all squares with fade-out intensity
            for (grid_x, grid_y), (_, color) in appeared_squares.items():
                pixel_x_start = grid_x * square_width
                pixel_y_start = grid_y * square_height
                
                for x in range(square_width):
                    for y in range(square_height):
                        px = pixel_x_start + x
                        py = pixel_y_start + y
                        if 0 <= px < width and 0 <= py < height:
                            final_color = (
                                int(color[0] * fade_out_intensity),
                                int(color[1] * fade_out_intensity),
                                int(color[2] * fade_out_intensity)
                            )
                            self.led.set_pixel(px, py, final_color)
            
            self.led.show()
            time.sleep(0.05)
    
        # Clear display completely
        self.led.clear()
        self.led.show()
        print("🔲 Squares animation finished")
    
    def run_triangles_animation(self):
        """Run triangles animation - 12 equal triangles appear one by one, filling screen."""
        import math
        # Play audio for this animation
        self.play_animation_audio('triangles')
        
        width = 32
        height = 48
        
        # Divide screen into 12 equal triangles
        # Each section: 16 pixels wide × 16 pixels tall
        section_width = 16
        section_height = 16
        
        # Calculate grid: 32 pixels wide / 16 = 2 columns, 48 pixels tall / 16 = 3 rows
        grid_cols = width // section_width  # 2 columns
        grid_rows = height // section_height  # 3 rows
        total_triangles = grid_cols * grid_rows  # 2 × 3 = 6 triangles
        
        # But we need 12 triangles total, so we'll create 2 triangles per section
        # Each 16×16 section will be divided into 2 right-angled triangles
        # Total: 6 sections × 2 triangles = 12 triangles
        triangles_per_section = 2
        total_triangles = (grid_cols * grid_rows) * triangles_per_section  # 12 triangles
        
        # Colors (8 colors total, will cycle through them)
        colors = [
            (235, 90, 60),   # #EB5A3C
            (223, 151, 85),  # #DF9755
            (231, 210, 131), # #E7D283
            (237, 244, 194), # #EDF4C2
            (124, 68, 79),   # #7C444F
            (159, 82, 85),   # #9F5255
            (225, 106, 84),  # #E16A54
            (243, 158, 96),  # #F39E60
        ]
        
        # Calculate timing: enough time for all triangles to appear + fade-in + fade-out
        # 12 triangles * 2 seconds = 24 seconds for all to appear
        # Plus 1 second fade-in for last triangle + 3 seconds fade-out = 28 seconds total
        time_between_triangles = 2  # 2 seconds between each triangle
        triangles_appear_time = total_triangles * time_between_triangles  # 24 seconds for all triangles
        fade_in_time = 1  # 1 second fade-in for last triangle
        fade_out_duration = 3
        main_animation_duration = triangles_appear_time + fade_in_time  # 25 seconds
        
        start_time = time.time()
        
        # Generate triangle positions in grid (2×3 sections, each with 2 triangles = 12 total)
        # Each 16×16 section is divided diagonally into 2 right-angled triangles
        triangle_positions = []
        for row in range(grid_rows):
            for col in range(grid_cols):
                x_start = col * section_width
                y_start = row * section_height
                # Each section has 2 triangles split diagonally
                # Triangle 1: top-left to bottom-right diagonal (top-left triangle)
                triangle_positions.append((x_start, y_start, 'top-left'))
                # Triangle 2: bottom-left to top-right diagonal (bottom-right triangle)
                triangle_positions.append((x_start, y_start, 'bottom-right'))
        
        # Track which triangles have appeared: {triangle_index: (appear_time, color)}
        appeared_triangles = {}
        
        print(f"△ Triangles animation started")
        
        def draw_triangle_in_section(section_x, section_y, triangle_type, color, intensity):
            """Draw a right-angled triangle in a 16×16 section."""
            # Each 16×16 section is divided diagonally into 2 right-angled triangles
            # Diagonal goes from top-left (0,0) to bottom-right (15,15)
            # Since section_width == section_height == 16, diagonal is y = x
            if triangle_type == 'top-left':
                # Top-left triangle: pixels on or above the diagonal (y <= x)
                # Right angle at top-left, hypotenuse along diagonal to bottom-right
                for y in range(section_height):
                    for x in range(section_width):
                        # Check if pixel is in top-left triangle (above or on diagonal)
                        # For square, diagonal is y = x, so top-left triangle is where y <= x
                        if y <= x:
                            px = section_x + x
                            py = section_y + y
                            if 0 <= px < width and 0 <= py < height:
                                final_color = (
                                    int(color[0] * intensity),
                                    int(color[1] * intensity),
                                    int(color[2] * intensity)
                                )
                                self.led.set_pixel(px, py, final_color)
            
            else:  # triangle_type == 'bottom-right'
                # Bottom-right triangle: pixels below the diagonal (y > x)
                # Right angle at bottom-right, hypotenuse along diagonal to top-left
                for y in range(section_height):
                    for x in range(section_width):
                        # Check if pixel is in bottom-right triangle (below diagonal)
                        # For square, diagonal is y = x, so bottom-right triangle is where y > x
                        if y > x:
                            px = section_x + x
                            py = section_y + y
                            if 0 <= px < width and 0 <= py < height:
                                final_color = (
                                    int(color[0] * intensity),
                                    int(color[1] * intensity),
                                    int(color[2] * intensity)
                                )
                                self.led.set_pixel(px, py, final_color)
        
        # Main animation: triangles appear and fade in
        while time.time() - start_time < main_animation_duration and self.shape_animation_running:
            elapsed = time.time() - start_time
            
            # Add a new triangle at regular intervals
            if elapsed > 0 and len(appeared_triangles) < total_triangles:
                next_triangle_time = len(appeared_triangles) * time_between_triangles
                if elapsed >= next_triangle_time:
                    # Find a random triangle position that hasn't appeared yet
                    available_indices = [i for i in range(total_triangles) if i not in appeared_triangles]
                    
                    if available_indices:
                        triangle_idx = random.choice(available_indices)
                        # Cycle through colors
                        color = colors[triangle_idx % len(colors)]
                        appeared_triangles[triangle_idx] = (elapsed, color)
            
            # Clear display
            self.led.clear()
            
            # Draw all appeared triangles with fade-in
            for triangle_idx, (appear_time, color) in appeared_triangles.items():
                triangle_age = elapsed - appear_time
                fade_progress = min(1.0, triangle_age / 1.0)
                fade_intensity = 1.0 - (1.0 - fade_progress) ** 2  # Ease-out
                
                # Get triangle position
                section_x, section_y, triangle_type = triangle_positions[triangle_idx]
                draw_triangle_in_section(section_x, section_y, triangle_type, color, fade_intensity)
            
            self.led.show()
            time.sleep(0.05)
        
        # Fade out all triangles smoothly
        print("△ Fading out triangles...")
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration and self.shape_animation_running:
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_out_intensity = 1.0 - (fade_progress ** 2)  # Ease-out
            
            self.led.clear()
            for triangle_idx, (_, color) in appeared_triangles.items():
                section_x, section_y, triangle_type = triangle_positions[triangle_idx]
                draw_triangle_in_section(section_x, section_y, triangle_type, color, fade_out_intensity)
            
            self.led.show()
            time.sleep(0.05)
        
        self.led.clear()
        self.led.show()
        print("△ Triangles animation finished")
    
    def run_bubbles_shape_animation(self):
        """Run bubbles animation - using the nature bubbles animation."""
        import math
        # Play audio for this animation
        self.play_animation_audio('bubbles')
        
        duration = 30
        start_time = time.time()
        width = 32
        height = 48
        
        print(f"🫧 Bubbles animation started")
        
        # Bubble colors - soft, translucent colors
        bubble_colors = [
            (100, 200, 255),  # Light blue
            (255, 150, 200),  # Pink
            (200, 255, 150),  # Light green
            (255, 200, 100),  # Orange
            (200, 150, 255),  # Purple
            (150, 255, 200),  # Mint green
            (255, 100, 150),  # Rose
            (100, 255, 255),  # Cyan
        ]
        
        # Animation parameters
        bubble_spawn_rate = 0.3  # New bubble every 0.3 seconds
        max_bubbles = 15  # Maximum number of bubbles on screen
        bubble_sizes = [2, 3, 4, 5]  # Different bubble sizes
        rise_speeds = [0.3, 0.5, 0.7, 0.9]  # Slower rise speeds
        
        # Bubble storage
        bubbles = []
        last_spawn_time = 0
        
        while time.time() - start_time < duration and self.shape_animation_running:
            # Clear display with black background
            self.led.clear()
            
            current_time = time.time() - start_time
            
            # Spawn new bubbles
            if current_time - last_spawn_time >= bubble_spawn_rate and len(bubbles) < max_bubbles:
                bubble = {
                    'x': random.randint(2, width - 3),
                    'y': height - 1,  # Start at bottom
                    'size': random.choice(bubble_sizes),
                    'speed': random.choice(rise_speeds),
                    'color': random.choice(bubble_colors),
                    'wobble_phase': random.uniform(0, 2 * math.pi),
                    'wobble_amplitude': random.uniform(0.5, 1.5)
                }
                bubbles.append(bubble)
                last_spawn_time = current_time
            
            # Update and draw bubbles
            bubbles_to_remove = []
            for i, bubble in enumerate(bubbles):
                # Update bubble position - only upward movement
                bubble['y'] -= bubble['speed']
                
                # No horizontal movement - bubbles move straight up
                bubble_x = int(bubble['x'])
                bubble_y = int(bubble['y'])
                
                # Remove bubbles that have risen off screen
                if bubble_y < -bubble['size']:
                    bubbles_to_remove.append(i)
                    continue
                
                # Draw bubble with soft, translucent effect
                size = bubble['size']
                color = bubble['color']
                
                # Draw bubble with soft edges
                for dy in range(-size, size + 1):
                    for dx in range(-size, size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        if distance <= size:
                            x = bubble_x + dx
                            y = bubble_y + dy
                            
                            if 0 <= x < width and 0 <= y < height:
                                # Create translucent effect
                                intensity = 1.0 - (distance / size) * 0.5
                                r = int(color[0] * intensity)
                                g = int(color[1] * intensity)
                                b = int(color[2] * intensity)
                                
                                # Add some sparkle effect
                                if random.random() < 0.1:
                                    r = min(255, r + 50)
                                    g = min(255, g + 50)
                                    b = min(255, b + 50)
                                
                                self.led.set_pixel(x, y, (r, g, b))
            
            # Remove bubbles that are off screen
            for i in reversed(bubbles_to_remove):
                bubbles.pop(i)
            
            self.led.show()
            time.sleep(0.05)  # 20 FPS for smooth bubble movement
        
        # Fade out all bubbles smoothly
        print("🫧 Fading out bubbles...")
        fade_out_duration = 3
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration and self.shape_animation_running:
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_out_intensity = 1.0 - (fade_progress ** 2)  # Ease-out
            
            self.led.clear()
            
            # Draw all remaining bubbles with fade-out
            for bubble in bubbles:
                bubble_x = int(bubble['x'])
                bubble_y = int(bubble['y'])
                size = bubble['size']
                color = bubble['color']
                
                for dy in range(-size, size + 1):
                    for dx in range(-size, size + 1):
                        distance = math.sqrt(dx*dx + dy*dy)
                        if distance <= size:
                            x = bubble_x + dx
                            y = bubble_y + dy
                            
                            if 0 <= x < width and 0 <= y < height:
                                # Combine fade-out with translucent effect
                                intensity = (1.0 - (distance / size) * 0.5) * fade_out_intensity
                                r = int(color[0] * intensity)
                                g = int(color[1] * intensity)
                                b = int(color[2] * intensity)
                                self.led.set_pixel(x, y, (r, g, b))
            
            self.led.show()
            time.sleep(0.05)
        
        self.led.clear()
        self.led.show()
        print("🫧 Bubbles animation finished")
    
    def run_stars_animation(self):
        """Run stars animation - 8 stars appear one by one."""
        import math
        # Play audio for this animation
        self.play_animation_audio('stars')
        
        duration = 30
        start_time = time.time()
        width = 32
        height = 48
        
        # Colors
        colors = [
            (195, 255, 147),  # #C3FF93
            (255, 219, 92),   # #FFDB5C
            (255, 175, 97),   # #FFAF61
            (255, 112, 171),  # #FF70AB
            (255, 118, 206),  # #FF76CE
            (253, 255, 194),  # #FDFFC2
            (148, 255, 216),  # #94FFD8
            (163, 216, 255),  # #A3D8FF
        ]
        
        # 8 stars total
        num_stars = 8
        star_positions = []  # Will store (x, y, color, appear_time)
        
        # Generate random positions for stars (not filling entire screen)
        star_radius = 4  # Size of star
        min_distance = 8  # Minimum distance between stars
        
        print(f"⭐ Stars animation started")
        
        while time.time() - start_time < duration and self.shape_animation_running:
            elapsed = time.time() - start_time
            
            # Add a new star every 3 seconds
            if elapsed > 0 and len(star_positions) < num_stars:
                next_star_time = len(star_positions) * 3
                if elapsed >= next_star_time:
                    # Find a valid position (not too close to other stars)
                    attempts = 0
                    while attempts < 50:
                        x = random.randint(star_radius, width - star_radius - 1)
                        y = random.randint(star_radius, height - star_radius - 1)
                        
                        # Check distance from other stars
                        too_close = False
                        for sx, sy, _, _ in star_positions:
                            dist = math.sqrt((x - sx)**2 + (y - sy)**2)
                            if dist < min_distance:
                                too_close = True
                                break
                        
                        if not too_close:
                            color = colors[len(star_positions)]
                            star_positions.append((x, y, color, elapsed))
                            break
                        attempts += 1
            
            # Clear display
            self.led.clear()
            
            # Draw all appeared stars with fade-in
            for x, y, color, appear_time in star_positions:
                star_age = elapsed - appear_time
                fade_progress = min(1.0, star_age / 1.0)
                fade_intensity = 1.0 - (1.0 - fade_progress) ** 2  # Ease-out
                
                # Draw star shape (cross/plus shape)
                star_size = 4
                final_color = (
                    int(color[0] * fade_intensity),
                    int(color[1] * fade_intensity),
                    int(color[2] * fade_intensity)
                )
                
                # Horizontal line
                for dx in range(-star_size, star_size + 1):
                    px = x + dx
                    py = y
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                
                # Vertical line
                for dy in range(-star_size, star_size + 1):
                    px = x
                    py = y + dy
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                
                # Diagonal lines (simple X)
                for i in range(-star_size // 2, star_size // 2 + 1):
                    # Top-left to bottom-right
                    px = x + i
                    py = y + i
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                    
                    # Top-right to bottom-left
                    px = x + i
                    py = y - i
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
            
            self.led.show()
            time.sleep(0.05)
        
        # Fade out
        print("⭐ Fading out stars...")
        fade_out_duration = 3
        fade_out_start = time.time()
        
        while time.time() - fade_out_start < fade_out_duration and self.shape_animation_running:
            elapsed_fade = time.time() - fade_out_start
            fade_progress = elapsed_fade / fade_out_duration
            fade_out_intensity = 1.0 - (fade_progress ** 2)
            
            self.led.clear()
            for x, y, color, _ in star_positions:
                star_size = 4
                final_color = (
                    int(color[0] * fade_out_intensity),
                    int(color[1] * fade_out_intensity),
                    int(color[2] * fade_out_intensity)
                )
                
                # Draw star
                for dx in range(-star_size, star_size + 1):
                    px = x + dx
                    py = y
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                
                for dy in range(-star_size, star_size + 1):
                    px = x
                    py = y + dy
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                
                for i in range(-star_size // 2, star_size // 2 + 1):
                    px = x + i
                    py = y + i
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
                    px = x + i
                    py = y - i
                    if 0 <= px < width and 0 <= py < height:
                        self.led.set_pixel(px, py, final_color)
            
            self.led.show()
            time.sleep(0.05)
        
        self.led.clear()
        self.led.show()
        print("⭐ Stars animation finished")
    
    def start_rainbow_pattern(self):
        """Start rainbow wave pattern."""
        print("Starting rainbow pattern")
        self.stop_current_pattern()
        time.sleep(0.1)  # Ensure everything is stopped
        self.current_pattern = threading.Thread(target=self.patterns.rainbow_wave)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
    
    def start_wave_pattern(self):
        """Start color wave pattern."""
        print("Starting wave pattern")
        self.stop_current_pattern()
        time.sleep(0.1)  # Ensure everything is stopped
        self.current_pattern = threading.Thread(
            target=self.patterns.color_wave, 
            args=(config.COLORS['BLUE'],)
        )
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
    
    def start_text_scroll(self):
        """Start text scrolling pattern."""
        print("Starting text scroll")
        self.stop_current_pattern()
        time.sleep(0.1)  # Ensure everything is stopped
        self.current_pattern = threading.Thread(
            target=self.patterns.scrolling_text,
            args=("HELLO RASPBERRY PI!", config.COLORS['GREEN'])
        )
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
    
    def start_objects_animation(self):
        """Start objects animation - cycles through different objects."""
        print("🎯 Starting objects animation...")
        self.stop_current_pattern()
        
        # Small delay to ensure everything is stopped
        time.sleep(0.1)
        
        # Ensure we have animations available
        if not self.objects_animations:
            print("⚠️ No object animations available")
            return
        
        # Cycle to next object with bounds checking
        self.current_object_index = (self.current_object_index + 1) % len(self.objects_animations)
        
        object_names = ["House", "Clock", "Traffic Lights", "Umbrella"]
        
        # Ensure index is within bounds
        if self.current_object_index >= len(object_names):
            self.current_object_index = 0
        
        object_name = object_names[self.current_object_index]
        
        print(f"🎬 Starting {object_name} animation...")
        
        # Start the object animation as a thread
        self.current_pattern = threading.Thread(target=self.run_objects_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print(f"✅ Started {object_name} animation")
    
    def run_objects_animation(self):
        """Run the current object animation."""
        self.objects_animation_running = True
        
        try:
            # Ensure index is within bounds
            if self.current_object_index >= len(self.objects_animations):
                self.current_object_index = 0
                print("⚠️ Object index out of bounds, resetting to 0")
            
            if self.current_object_index == 0:
                self.run_house_animation()
            elif self.current_object_index == 1:
                self.run_clock_objects_animation()
            elif self.current_object_index == 2:
                self.run_traffic_lights_animation()
            elif self.current_object_index == 3:
                self.run_umbrella_animation()
            else:
                print(f"⚠️ Unknown object index: {self.current_object_index}")
        finally:
            self.objects_animation_running = False
    
    def run_clock_objects_animation(self):
        """Run clock animation with moving hands in a circle."""
        import math
        # Play audio for this animation
        self.play_animation_audio('clock')
        
        duration = 20
        start_time = time.time()
        width = 32
        height = 48
        
        # Colors
        clock_fill = (108, 36, 152)  # #6C2498
        white = (255, 255, 255)      # White border and hands
        
        # Clock dimensions - radius of 30 LEDs (but limited by screen size)
        # Screen is 32×48, so max radius is 16 (width) or 24 (height)
        # Use 24 to get as close to 30 as possible while fitting on screen
        clock_center_x = width // 2
        clock_center_y = height // 2
        clock_radius = 24  # Maximum radius that fits on 48px tall screen
        
        # Hand parameters - don't touch border
        hand_inner_radius = 3  # Small center circle
        hand_outer_radius = clock_radius - 4  # Hands stop before border
        
        print(f"🕐 Clock animation started")
        
        def draw_clock(elapsed_time):
            """Draw the complete clock with moving hands."""
            # Draw white border (outer ring)
            for angle in range(0, 360, 1):
                rad = math.radians(angle)
                x = int(clock_center_x + clock_radius * math.cos(rad))
                y = int(clock_center_y + clock_radius * math.sin(rad))
                if 0 <= x < width and 0 <= y < height:
                    self.led.set_pixel(x, y, white)
            
            # Draw filled clock face (#6C2498)
            for y in range(height):
                for x in range(width):
                    dx = x - clock_center_x
                    dy = y - clock_center_y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance < clock_radius:
                        self.led.set_pixel(x, y, clock_fill)
            
            # Redraw white border on top of fill
            for angle in range(0, 360, 1):
                rad = math.radians(angle)
                x = int(clock_center_x + clock_radius * math.cos(rad))
                y = int(clock_center_y + clock_radius * math.sin(rad))
                if 0 <= x < width and 0 <= y < height:
                    self.led.set_pixel(x, y, white)
            
            # Calculate hand positions based on elapsed time
            # Minutes hand: full rotation in 60 seconds
            minutes_angle = (elapsed_time * 360 / 60) % 360
            # Hours hand: full rotation in 12 * 60 = 720 seconds
            hours_angle = (elapsed_time * 360 / 720) % 360
            
            # Draw minute hand (longer)
            minutes_rad = math.radians(minutes_angle - 90)  # -90 to start at 12 o'clock
            for r in range(hand_inner_radius, int(hand_outer_radius * 0.9)):  # Minutes hand is 90% of max
                px = int(clock_center_x + r * math.cos(minutes_rad))
                py = int(clock_center_y + r * math.sin(minutes_rad))
                if 0 <= px < width and 0 <= py < height:
                    # Check distance from center to ensure it's inside the circle
                    dist_from_center = math.sqrt((px - clock_center_x)**2 + (py - clock_center_y)**2)
                    if dist_from_center < clock_radius:
                        self.led.set_pixel(px, py, white)
            
            # Draw hour hand (shorter)
            hours_rad = math.radians(hours_angle - 90)  # -90 to start at 12 o'clock
            for r in range(hand_inner_radius, int(hand_outer_radius * 0.6)):  # Hours hand is 60% of max
                px = int(clock_center_x + r * math.cos(hours_rad))
                py = int(clock_center_y + r * math.sin(hours_rad))
                if 0 <= px < width and 0 <= py < height:
                    # Check distance from center to ensure it's inside the circle
                    dist_from_center = math.sqrt((px - clock_center_x)**2 + (py - clock_center_y)**2)
                    if dist_from_center < clock_radius:
                        self.led.set_pixel(px, py, white)
            
            # Draw center circle (white)
            for dy in range(-hand_inner_radius, hand_inner_radius + 1):
                for dx in range(-hand_inner_radius, hand_inner_radius + 1):
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= hand_inner_radius:
                        px = clock_center_x + dx
                        py = clock_center_y + dy
                        if 0 <= px < width and 0 <= py < height:
                            self.led.set_pixel(px, py, white)
        
        while time.time() - start_time < duration and self.objects_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Draw clock with moving hands
            draw_clock(elapsed)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Keep final frame for a moment
        print("🕐 Clock animation finished")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def run_traffic_lights_animation(self):
        """Run traffic lights animation - different lights turn on every 5 seconds."""
        import math
        # Play audio for this animation
        self.play_animation_audio('traffic_lights')
        
        duration = 20
        start_time = time.time()
        width = 32
        height = 48
        
        print(f"🚦 Traffic lights animation started")
        
        # Traffic light fixture size: 40×24 (but screen is 32×48, so scale to fit)
        # Scale proportionally: 40×24 -> 32×19 (maintains aspect ratio)
        # But let's use 32×24 to make it more visible (stretches slightly)
        fixture_width = 32  # Full width of screen
        fixture_height = 24  # Half height of screen
        
        # Position traffic lights in center
        fixture_x = 0  # Start at left edge
        fixture_y = (height - fixture_height) // 2  # Center vertically
        
        # Light colors
        red_light = (255, 0, 0)
        yellow_light = (255, 255, 0)
        green_light = (0, 255, 0)
        off_color = (40, 40, 40)  # Dark gray when off
        fixture_color = (60, 60, 60)  # Dark gray for fixture
        
        # Light positions within fixture (3 lights: red on top, yellow middle, green bottom)
        light_size = 8  # Each light is 8 pixels in diameter
        light_spacing = 8
        fixture_center_x = fixture_x + fixture_width // 2
        
        red_light_y = fixture_y + light_size // 2
        yellow_light_y = fixture_y + fixture_height // 2
        green_light_y = fixture_y + fixture_height - light_size // 2
        
        # Track which lights are on
        current_light = None  # 'red', 'yellow', 'green', or None
        
        def draw_traffic_lights(active_light):
            """Draw traffic light fixture with active light."""
            # Draw fixture background
            for y in range(fixture_y, fixture_y + fixture_height):
                for x in range(fixture_x, fixture_x + fixture_width):
                    if 0 <= x < width and 0 <= y < height:
                        self.led.set_pixel(x, y, fixture_color)
            
            # Draw red light
            light_color = red_light if active_light == 'red' else off_color
            for dy in range(-light_size//2, light_size//2 + 1):
                for dx in range(-light_size//2, light_size//2 + 1):
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= light_size // 2:
                        px = fixture_center_x + dx
                        py = red_light_y + dy
                        if 0 <= px < width and 0 <= py < height:
                            self.led.set_pixel(px, py, light_color)
            
            # Draw yellow light
            light_color = yellow_light if active_light == 'yellow' else off_color
            for dy in range(-light_size//2, light_size//2 + 1):
                for dx in range(-light_size//2, light_size//2 + 1):
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= light_size // 2:
                        px = fixture_center_x + dx
                        py = yellow_light_y + dy
                        if 0 <= px < width and 0 <= py < height:
                            self.led.set_pixel(px, py, light_color)
            
            # Draw green light
            light_color = green_light if active_light == 'green' else off_color
            for dy in range(-light_size//2, light_size//2 + 1):
                for dx in range(-light_size//2, light_size//2 + 1):
                    dist = math.sqrt(dx*dx + dy*dy)
                    if dist <= light_size // 2:
                        px = fixture_center_x + dx
                        py = green_light_y + dy
                        if 0 <= px < width and 0 <= py < height:
                            self.led.set_pixel(px, py, light_color)
        
        while time.time() - start_time < duration and self.objects_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Determine which light should be on based on elapsed time
            # Every 5 seconds, a different light turns on
            light_phase = int(elapsed / 5) % 4  # 0=none, 1=red, 2=yellow, 3=green
            
            if light_phase == 0:
                current_light = None  # No lights
            elif light_phase == 1:
                current_light = 'red'
            elif light_phase == 2:
                current_light = 'yellow'
            else:
                current_light = 'green'
            
            # Clear display
            self.led.clear()
            
            # Draw traffic lights
            draw_traffic_lights(current_light)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        print("🚦 Traffic lights animation finished")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def run_umbrella_animation(self):
        """Run umbrella animation - starts closed and opens over 20 seconds."""
        import math
        # Play audio for this animation
        self.play_animation_audio('umbrella')
        
        open_duration = 20  # Opening animation
        static_duration = 5  # Stay open static
        total_duration = open_duration + static_duration
        start_time = time.time()
        width = 32
        height = 48
        
        print(f"☂️ Umbrella animation started")
        
        # Colors
        colors = [
            (119, 190, 240),  # #77BEF0
            (255, 203, 97),   # #FFCB61
            (255, 137, 79),   # #FF894F
            (234, 91, 111),   # #EA5B6F
        ]
        
        # Umbrella dimensions
        umbrella_center_x = width // 2
        umbrella_center_y = height // 4  # Top quarter of screen
        max_radius = 16  # Maximum open radius
        handle_length = 20  # Length of handle
        
        def draw_umbrella(open_progress):
            """Draw umbrella with opening animation."""
            # open_progress: 0 (closed) to 1 (fully open)
            
            # Calculate current radius based on opening progress
            current_radius = max_radius * open_progress
            
            # Draw handle (vertical line from umbrella center down)
            handle_start_y = umbrella_center_y
            handle_end_y = umbrella_center_y + handle_length
            
            for y in range(handle_start_y, min(handle_end_y, height)):
                if 0 <= umbrella_center_x < width and 0 <= y < height:
                    self.led.set_pixel(umbrella_center_x, y, (100, 100, 100))  # Dark gray handle
            
            # Draw umbrella canopy
            if open_progress > 0:
                # Create segments (8 segments for umbrella)
                num_segments = 8
                for segment in range(num_segments):
                    # Each segment gets a different color
                    segment_color = colors[segment % len(colors)]
                    
                    # Calculate segment angles
                    start_angle = (segment * 360 / num_segments) - 90  # Start at top (-90 degrees)
                    end_angle = ((segment + 1) * 360 / num_segments) - 90
                    
                    # Draw segment as a pie slice
                    for y in range(height):
                        for x in range(width):
                            dx = x - umbrella_center_x
                            dy = y - umbrella_center_y
                            distance = math.sqrt(dx*dx + dy*dy)
                            
                            # Check if pixel is within current radius
                            if distance <= current_radius:
                                # Calculate angle of this pixel
                                angle = math.degrees(math.atan2(dy, dx))
                                # Normalize angle to 0-360
                                if angle < 0:
                                    angle += 360
                                
                                # Check if angle is within segment range
                                if start_angle <= angle < end_angle or (start_angle > end_angle and (angle >= start_angle or angle < end_angle)):
                                    # Only draw if above the handle (in the canopy area)
                                    if y < umbrella_center_y:
                                        self.led.set_pixel(x, y, segment_color)
            
            # Draw handle tip (small circle at bottom)
            handle_tip_y = min(umbrella_center_y + handle_length, height - 1)
            if 0 <= umbrella_center_x < width and 0 <= handle_tip_y < height:
                self.led.set_pixel(umbrella_center_x, handle_tip_y, (100, 100, 100))
                if umbrella_center_x - 1 >= 0:
                    self.led.set_pixel(umbrella_center_x - 1, handle_tip_y, (100, 100, 100))
                if umbrella_center_x + 1 < width:
                    self.led.set_pixel(umbrella_center_x + 1, handle_tip_y, (100, 100, 100))
        
        # Opening phase
        while time.time() - start_time < open_duration and self.objects_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            open_progress = min(1.0, elapsed / open_duration)
            
            # Clear display
            self.led.clear()
            
            # Draw umbrella with current opening progress
            draw_umbrella(open_progress)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Static open phase - keep umbrella fully open for 5 seconds
        static_start = time.time()
        while time.time() - static_start < static_duration and self.objects_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display
            self.led.clear()
            
            # Draw fully open umbrella
            draw_umbrella(1.0)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        print("☂️ Umbrella animation finished")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def stop_current_pattern(self):
        """Stop the currently running pattern."""
        print("🛑 Stopping all animations...")
        
        # Stop audio
        self.stop_animation_audio()
        
        # Stop pattern animations
        if hasattr(self, 'patterns'):
            self.patterns.stop()
        # if hasattr(self, 'squares_animation'):
        #     self.squares_animation.stop()  # File not found
        
        # Stop thread patterns
        if self.current_pattern and hasattr(self.current_pattern, 'is_alive') and self.current_pattern.is_alive():
            print("Stopping thread pattern...")
            self.current_pattern.join(timeout=1.0)  # Longer timeout
            # Force kill if still alive
            if self.current_pattern.is_alive():
                print("⚠️ Force stopping thread...")
                # Set a flag to stop the animation
                if hasattr(self, 'animation_stop_flag'):
                    self.animation_stop_flag = True
        
        # Stop shape animations
        self.stop_current_shape_animation()
        self.shape_animation_running = False
        
        # Stop nature animations
        self.nature_animation_running = False
        
        # Stop lion animations
        self.lion_animation_running = False
        
        # Add animation stop flag
        self.animation_stop_flag = True
        
        # Clear the display
        if hasattr(self, 'led'):
            self.led.clear()
            self.led.show()
        
        # Reset the flag after clearing
        self.animation_stop_flag = False
        
        print("✅ All animations stopped")
    
    def demo_sequence(self):
        """Run a demo sequence of various patterns."""
        print("Starting demo sequence...")
        
        # Demo 1: Mushroom display
        print("Demo 1: Mushroom display")
        from mushroom_display import MushroomDisplay
        mushroom = MushroomDisplay()
        mushroom.display_mushroom(duration=5)
        mushroom.display_mushroom_animation(duration=5)
        mushroom.cleanup()
        
        # Demo 2: Panel sequence
        print("Demo 2: Panel sequence")
        colors = [config.COLORS['RED'], config.COLORS['GREEN'], config.COLORS['BLUE'], 
                 config.COLORS['YELLOW'], config.COLORS['MAGENTA']]
        self.patterns.panel_sequence(colors, duration=3)
        
        # Demo 3: Rainbow wave
        print("Demo 3: Rainbow wave")
        self.patterns.rainbow_wave(duration=3)
        
        # Demo 4: Text scroll
        print("Demo 4: Text scroll")
        self.patterns.scrolling_text("MUSHROOM LED DISPLAY", config.COLORS['WHITE'], duration=3)
        
        # Demo 5: Squares animation
        print("Demo 5: Squares animation")
        # self.squares_animation.run_animation()  # File not found
        print("⚠️ Squares animation not available - file not found")
        
        print("Demo sequence completed!")
    
    def run(self):
        """Main application loop."""
        print("LED Display Application Started")
        print("Display Configuration:")
        print(f"  Total LEDs: {config.TOTAL_LEDS}")
        print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print(f"  Panels: {config.PANELS_COUNT} ({config.PANEL_WIDTH}x{config.PANEL_HEIGHT} each)")
        print(f"  LED Pin: {config.LED_PIN}")
        print(f"  Brightness: {config.BRIGHTNESS}")
        print()
        
        # Start button monitoring
        self.button_controller.start_monitoring()
        
        # Skip demo sequence - go straight to button monitoring
        print("Skipping demo sequence - waiting for button presses...")
        
        # Keep the application running
        print("Application running. Press Ctrl+C to exit.")
        print("Button controls (when connected):")
        print("  Button 18: Shapes animation")
        print("  Button 17: Nature animations")
        print("  Button 27: Lion animation")
        print("  Button 22: Objects animation")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.stop_current_pattern()
        self.stop_current_shape_animation()
        self.button_controller.cleanup()
        self.led.cleanup()
        print("Cleanup completed.")

def git_pull_update():
    """Pull latest changes from git repository."""
    import subprocess
    import os
    
    try:
        print("Checking for updates...")
        
        # Get the current directory
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        
        # Check if this is a git repository
        if not os.path.exists('.git'):
            print("Not a git repository, skipping update check")
            return False
        
        # Fetch latest changes
        print("Fetching latest changes...")
        result = subprocess.run(['git', 'fetch'], 
                              capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode != 0:
            print(f"Git fetch failed: {result.stderr}")
            return False
        
        # Check if there are any changes to pull
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=current_dir)
        
        # Check if we're behind the remote
        result_behind = subprocess.run(['git', 'rev-list', 'HEAD..origin/main', '--count'], 
                                     capture_output=True, text=True, cwd=current_dir)
        
        if result_behind.returncode == 0 and result_behind.stdout.strip() != '0':
            commits_behind = int(result_behind.stdout.strip())
            print(f"Found {commits_behind} new commits, pulling updates...")
            
            # Pull the changes
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  capture_output=True, text=True, cwd=current_dir)
            
            if result.returncode == 0:
                print("✅ Successfully updated from git repository!")
                print("Changes pulled:")
                print(result.stdout)
                return True
            else:
                print(f"❌ Git pull failed: {result.stderr}")
                return False
        else:
            print("✅ Already up to date!")
            return False
            
    except Exception as e:
        print(f"❌ Error during git update: {e}")
        return False

def main():
    """Main entry point."""
    try:
        # Set up signal handlers for proper cleanup
        import signal
        def signal_handler(signum, frame):
            print("\n🛑 Shutting down gracefully...")
            try:
                import sys
                if not sys.platform.startswith('win'):
                    import RPi.GPIO as GPIO
                    GPIO.cleanup()
                    print("✅ GPIO cleaned up on exit")
            except:
                pass
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Check for git updates first
        updated = git_pull_update()
        
        if updated:
            print("🔄 Restarting application with updated code...")
            # Clean up GPIO and LED resources before restart
            try:
                # Try to cleanup GPIO if we're on Raspberry Pi
                import sys
                if not sys.platform.startswith('win'):
                    import RPi.GPIO as GPIO
                    GPIO.cleanup()
                    print("✅ GPIO cleaned up before restart")
                else:
                    print("✅ Mock GPIO - no cleanup needed")
            except Exception as e:
                print(f"Warning: Error during GPIO cleanup: {e}")
            
            # Add a longer delay to ensure proper cleanup, module unloading, and hardware reset
            import time
            print("⏳ Waiting for modules to fully unload before restart...")
            time.sleep(5)  # Longer wait to ensure all modules are released and hardware is ready
            print("🔄 Restarting now...")
            # Restart the application to load new code
            import os
            import sys
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # Add longer delays to ensure LED controller is fully ready
        import time
        print("🔧 Initializing LED display system...")
        time.sleep(2.0)  # Increased delay for GPIO cleanup
        
        # Additional GPIO cleanup attempt before starting
        try:
            import sys
            if not sys.platform.startswith('win'):
                import RPi.GPIO as GPIO
                GPIO.cleanup()
                print("✅ Additional GPIO cleanup completed")
                time.sleep(1.0)  # Wait after cleanup
        except Exception as e:
            print(f"Note: Additional GPIO cleanup: {e}")
        
        # Start the application
        app = LEDDisplayApp()
        
        # Additional initialization delay to ensure everything is ready
        print("🔧 Finalizing initialization...")
        time.sleep(1.0)  # Increased from 0.5s
        
        # Clear the display to ensure it's ready
        print("🔧 Clearing display and testing...")
        app.led.clear()
        app.led.show()
        time.sleep(0.5)
        
        # Test button controller initialization
        print("🔧 Testing button controller...")
        time.sleep(0.5)
        
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main() 