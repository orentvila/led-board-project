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
        
        # Shape animation system - only big rectangle animation
        self.shape_animations = [
            "big_rectangle_animation.py"
        ]
        self.current_shape_index = 0
        self.current_shape_process = None
        self.shape_animation_running = False
        
        # Nature animation system
        self.nature_animations = [
            "floating_clouds_animation.py",
            "rain_animation.py",
            "growing_flowers_animation.py",
            "bubbles_animation.py",
            "apple_tree_animation.py",
            "butterfly_animation.py"
        ]
        self.current_nature_index = 0
        self.nature_animation_running = False
        
        # House animation system
        self.house_animation_running = False
        
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
        # Button 27 (index 2) - House animation
        self.button_controller.register_callback(2, self.start_house_animation)
        # Button 22 (index 3) - Squares animation
        self.button_controller.register_callback(3, self.start_squares_animation)
    
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
        shape_names = ["Big Rectangle"]
        
        # Ensure index is within bounds
        if self.current_shape_index >= len(shape_names):
            self.current_shape_index = 0
        
        shape_name = shape_names[self.current_shape_index]
        
        print(f"🎬 Starting {shape_name}...")
        
        # Start the shape animation as a thread
        self.current_pattern = threading.Thread(target=self.run_shape_animation)
        self.current_pattern.daemon = False  # Don't use daemon threads
        self.current_pattern.start()
        
        print(f"✅ Started {shape_name}")
    
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
                self.run_bubbles_animation()
            elif self.current_nature_index == 4:
                self.run_apple_tree_animation()
            elif self.current_nature_index == 5:
                self.run_butterfly_animation()
        finally:
            self.nature_animation_running = False
            print(f"🔧 Animation finished, flag set to: {self.nature_animation_running}")
    
    def run_floating_clouds(self):
        """Run floating clouds animation."""
        import math
        duration = 30
        start_time = time.time()
        
        print(f"🌤️ Floating clouds animation started (flag: {self.nature_animation_running})")
        
        # Double-check the flag is still True
        if not self.nature_animation_running:
            print("❌ Animation flag is False, stopping clouds")
            return
        
        # TEST: Clear display and show a simple pattern first
        print("🧪 Testing LED display...")
        self.led.clear()
        for x in range(32):
            for y in range(48):
                if x < 16 and y < 24:
                    self.led.set_pixel(x, y, (255, 0, 0))  # Red quadrant
                elif x >= 16 and y < 24:
                    self.led.set_pixel(x, y, (0, 255, 0))  # Green quadrant
                elif x < 16 and y >= 24:
                    self.led.set_pixel(x, y, (0, 0, 255))  # Blue quadrant
                else:
                    self.led.set_pixel(x, y, (255, 255, 0))  # Yellow quadrant
        self.led.show()
        time.sleep(2)  # Show test pattern for 2 seconds
        print("🧪 Test pattern shown, starting clouds...")
        
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
            'max_stem_height': 12,  # Fixed height
            'petal_size': 0,  # Will grow
            'max_petal_size': 5,  # Fixed size
            'color': random.choice(flower_colors),
            'bloom_progress': 0,  # 0 to 1
            'sway_phase': 0,  # Start phase
            'sway_amount': 1.0  # Gentle sway
        }
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            # Clear display
            self.led.clear()
            
            # Create soft sky background
            for y in range(height):
                sky_intensity = 1.0 - (y / height) * 0.2
                sky_color = (int(135 * sky_intensity), int(206 * sky_intensity), int(235 * sky_intensity))
                
                for x in range(width):
                    self.led.set_pixel(x, y, sky_color)
            
            # Draw ground
            for x in range(width):
                for y in range(height - 3, height):
                    ground_color = (139, 69, 19)  # Brown ground
                    self.led.set_pixel(x, y, ground_color)
            
            # Draw single flower
            # Draw stem (static position)
            stem_color = (34, 139, 34)  # Forest green
            for i in range(int(flower['stem_height'])):
                y_pos = height - 1 - i
                if 0 <= y_pos < height and 0 <= flower['x'] < width:
                    self.led.set_pixel(flower['x'], y_pos, stem_color)
            
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
                # Update bubble position
                bubble['y'] -= bubble['speed']
                
                # Add gentle wobble
                wobble_x = math.sin(bubble['wobble_phase'] + current_time * 2) * bubble['wobble_amplitude']
                bubble_x = int(bubble['x'] + wobble_x)
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
        duration = 20
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
        
        # Falling apple (starts at position 0 - top center)
        falling_apple_start_pos = (16, 6)
        falling_apple_start_time = 10  # Start falling after 10 seconds
        falling_apple_fall_duration = 3  # Takes 3 seconds to fall
        
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
        
        def draw_apples(exclude_falling=False):
            """Draw all apples except the falling one if specified."""
            for i, (apple_x, apple_y) in enumerate(apple_positions):
                # Skip the falling apple (first apple) if exclude_falling is True
                if exclude_falling and i == 0:
                    continue
                    
                # Draw apple
                self.led.set_pixel(apple_x, apple_y, red_apple)
                # Draw stem
                if apple_y > 0:
                    self.led.set_pixel(apple_x, apple_y - 1, apple_stem)
        
        def draw_falling_apple(progress):
            """Draw the falling apple with gravity effect."""
            # Calculate falling position with gravity
            # Apple starts at y=6, ground is at y=44, so need to fall 38 pixels
            fall_distance = progress * 38  # Total fall distance to ground
            gravity_effect = progress * progress * 0.5  # Gravity acceleration
            
            current_x = falling_apple_start_pos[0]
            current_y = falling_apple_start_pos[1] + fall_distance + gravity_effect
            
            # Keep apple within bounds
            current_x = max(0, min(width - 1, int(current_x)))
            current_y = max(0, min(height - 1, int(current_y)))
            
            # Draw falling apple
            if 0 <= current_x < width and 0 <= current_y < height:
                self.led.set_pixel(current_x, current_y, red_apple)
                # Draw stem
                if current_y > 0:
                    self.led.set_pixel(current_x, current_y - 1, apple_stem)
        
        def draw_ground():
            """Draw brown soil ground."""
            for x in range(width):
                for y in range(ground_y, height):
                    self.led.set_pixel(x, y, brown_soil)
        
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
            
            # Handle falling apple
            if elapsed >= falling_apple_start_time:
                # Apple is falling
                fall_progress = (elapsed - falling_apple_start_time) / falling_apple_fall_duration
                fall_progress = min(1.0, fall_progress)  # Clamp to 1.0
                
                # Draw all apples except the falling one
                draw_apples(exclude_falling=True)
                
                # Draw falling apple
                draw_falling_apple(fall_progress)
            else:
                # All apples are on the tree
                draw_apples(exclude_falling=False)
            
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
    
    def run_butterfly_animation(self):
        """Run butterfly animation with flapping wings."""
        import math
        duration = 20
        start_time = time.time()
        
        print(f"🦋 Butterfly animation started")
        
        # Get display dimensions
        width = 32
        height = 48
        
        # Colors from the image
        pink_wings = (240, 128, 128)  # #F08080 - light coral pink
        brown_body = (180, 100, 80)   # Brownish-pink body
        black_antennae = (50, 50, 50)  # Dark antennae
        
        # Butterfly position (centered)
        center_x = 16
        center_y = 24
        
        # Wing dimensions
        upper_wing_radius = 8
        lower_wing_radius = 6
        
        def draw_butterfly(wing_angle):
            """Draw the butterfly with animated wings."""
            # Draw body (vertical oval)
            for dy in range(-6, 7):
                for dx in range(-1, 2):
                    x = center_x + dx
                    y = center_y + dy
                    if 0 <= x < width and 0 <= y < height:
                        # Make body slightly oval
                        if abs(dx) <= 1 and abs(dy) <= 6:
                            self.led.set_pixel(x, y, brown_body)
            
            # Draw antennae
            antennae_length = 4
            for i in range(antennae_length):
                # Left antenna
                antenna_x = center_x - 1 - i
                antenna_y = center_y - 6 - i
                if 0 <= antenna_x < width and 0 <= antenna_y < height:
                    self.led.set_pixel(antenna_x, antenna_y, black_antennae)
                
                # Right antenna
                antenna_x = center_x + 1 + i
                antenna_y = center_y - 6 - i
                if 0 <= antenna_x < width and 0 <= antenna_y < height:
                    self.led.set_pixel(antenna_x, antenna_y, black_antennae)
            
            # Draw wings with flapping animation
            draw_wings(wing_angle)
        
        def draw_wings(wing_angle):
            """Draw the butterfly wings with flapping animation."""
            # Calculate wing positions based on angle
            # wing_angle: 0 = fully open, 1 = fully closed
            
            # Upper wings (larger)
            draw_wing_segment(
                center_x - 2, center_y - 2,  # Left upper wing center
                upper_wing_radius, wing_angle, -1  # Left side
            )
            draw_wing_segment(
                center_x + 2, center_y - 2,  # Right upper wing center
                upper_wing_radius, wing_angle, 1   # Right side
            )
            
            # Lower wings (smaller)
            draw_wing_segment(
                center_x - 1, center_y + 2,  # Left lower wing center
                lower_wing_radius, wing_angle * 0.8, -1  # Left side
            )
            draw_wing_segment(
                center_x + 1, center_y + 2,  # Right lower wing center
                lower_wing_radius, wing_angle * 0.8, 1   # Right side
            )
        
        def draw_wing_segment(center_x, center_y, radius, wing_angle, side):
            """Draw a single wing segment."""
            # Adjust radius based on wing angle (wings get smaller when closed)
            adjusted_radius = int(radius * (1 - wing_angle * 0.3))
            
            for dy in range(-adjusted_radius, adjusted_radius + 1):
                for dx in range(-adjusted_radius, adjusted_radius + 1):
                    # Only draw on the correct side
                    if (side == -1 and dx > 0) or (side == 1 and dx < 0):
                        continue
                    
                    # Calculate distance from center
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    # Draw wing pixels
                    if distance <= adjusted_radius:
                        x = center_x + dx
                        y = center_y + dy
                        if 0 <= x < width and 0 <= y < height:
                            # Add some wing texture variation
                            if (x + y) % 2 == 0:  # Skip some pixels for texture
                                continue
                            self.led.set_pixel(x, y, pink_wings)
        
        while time.time() - start_time < duration and self.nature_animation_running and not getattr(self, 'animation_stop_flag', False):
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Calculate wing flapping angle (slow, gentle flapping)
            # Use sine wave for smooth, natural wing movement
            flap_frequency = 0.8  # Flaps per second (slow)
            wing_angle = abs(math.sin(elapsed * flap_frequency * 2 * math.pi))
            
            # Draw butterfly
            draw_butterfly(wing_angle)
            
            # Show the frame
            self.led.show()
            
            # Frame rate
            time.sleep(0.05)  # 20 FPS
        
        # Keep final frame for a moment
        print("🦋 Butterfly Animation completed!")
        time.sleep(2)
        
        # Clear display
        self.led.clear()
        self.led.show()
        print("🦋 Animation finished")
    
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
                self.run_big_rectangle()
            else:
                print(f"⚠️ Unknown shape index: {self.current_shape_index}")
        finally:
            self.shape_animation_running = False
    
    def run_big_rectangle(self):
        """Run big rectangle animation with soft blue color."""
        import math
        duration = 20  # 20 seconds as requested
        start_time = time.time()
        
        print(f"🔷 Big Rectangle animation started")
        
        # Starting color #73C0E0 and ending color #157BB8
        start_color = (115, 192, 224)  # RGB values for #73C0E0
        end_color = (21, 123, 184)    # RGB values for #157BB8
        
        # Calculate rectangle dimensions (big rectangle)
        margin_x = 2
        margin_y = 4
        rect_width = 32 - (2 * margin_x)  # 28 pixels wide
        rect_height = 48 - (2 * margin_y)  # 40 pixels tall
        
        # Rectangle position (centered)
        rect_x = margin_x
        rect_y = margin_y
        
        while time.time() - start_time < duration and self.shape_animation_running:
            # Calculate progress (0 to 1)
            elapsed = time.time() - start_time
            progress = elapsed / duration
            
            # Calculate fade intensity using smooth easing function (ease-out cubic)
            # This provides a smooth fade-in effect
            fade_intensity = 1.0 - (1.0 - progress) ** 3
            
            # Calculate color transition from start to end color
            current_color = (
                int(start_color[0] + (end_color[0] - start_color[0]) * progress),
                int(start_color[1] + (end_color[1] - start_color[1]) * progress),
                int(start_color[2] + (end_color[2] - start_color[2]) * progress)
            )
            
            # Clear display
            self.led.clear()
            
            # Draw the rectangle with current color and fade intensity
            for y in range(rect_height):
                for x in range(rect_width):
                    # Calculate final color with fade intensity
                    final_color = (
                        int(current_color[0] * fade_intensity),
                        int(current_color[1] * fade_intensity),
                        int(current_color[2] * fade_intensity)
                    )
                    
                    # Set pixel
                    pixel_x = rect_x + x
                    pixel_y = rect_y + y
                    
                    if 0 <= pixel_x < 32 and 0 <= pixel_y < 48:
                        self.led.set_pixel(pixel_x, pixel_y, final_color)
            
            # Show the frame
            self.led.show()
            
            # Higher frame rate for smoother animation
            time.sleep(0.03)  # ~33 FPS for much smoother animation
        
        # Keep the rectangle fully lit for a moment at the end
        print("🔷 Rectangle fully lit, keeping for 2 seconds...")
        time.sleep(2)
        
        # Fade out slowly
        print("🔷 Fading out...")
        fade_out_duration = 3  # 3 seconds fade out
        fade_start = time.time()
        
        while time.time() - fade_start < fade_out_duration and self.shape_animation_running:
            elapsed_fade = time.time() - fade_start
            fade_progress = elapsed_fade / fade_out_duration
            
            # Calculate fade out intensity (1 to 0)
            fade_out_intensity = 1.0 - fade_progress
            
            # Use the final color for fade out
            final_color_for_fade = end_color
            
            # Clear display
            self.led.clear()
            
            # Draw the rectangle with fade out intensity
            for y in range(rect_height):
                for x in range(rect_width):
                    # Calculate final color with fade out intensity
                    final_color = (
                        int(final_color_for_fade[0] * fade_out_intensity),
                        int(final_color_for_fade[1] * fade_out_intensity),
                        int(final_color_for_fade[2] * fade_out_intensity)
                    )
                    
                    # Set pixel
                    pixel_x = rect_x + x
                    pixel_y = rect_y + y
                    
                    if 0 <= pixel_x < 32 and 0 <= pixel_y < 48:
                        self.led.set_pixel(pixel_x, pixel_y, final_color)
            
            # Show the frame
            self.led.show()
            
            # Higher frame rate for smoother animation
            time.sleep(0.03)
        
        # Clear display completely
        self.led.clear()
        self.led.show()
        
        print("🔷 Big Rectangle animation finished")
    
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
    
    def start_squares_animation(self):
        """Start squares animation pattern."""
        print("Starting squares animation")
        self.stop_current_pattern()
        time.sleep(0.1)  # Ensure everything is stopped
        # self.current_pattern = threading.Thread(target=self.squares_animation.run_animation)  # File not found
        # self.current_pattern.daemon = False  # Don't use daemon threads
        # self.current_pattern.start()
        print("⚠️ Squares animation not available - file not found")
    
    def stop_current_pattern(self):
        """Stop the currently running pattern."""
        print("🛑 Stopping all animations...")
        
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
        print("  Button 22: Squares animation")
        
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
        # Check for git updates first
        updated = git_pull_update()
        
        if updated:
            print("🔄 Restarting application with updated code...")
            # Add a longer delay to ensure proper cleanup and hardware reset
            import time
            time.sleep(2)
            # Restart the application to load new code
            import os
            import sys
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # Add longer delays to ensure LED controller is fully ready
        import time
        print("🔧 Initializing LED display system...")
        time.sleep(1.0)  # Increased from 0.5s
        
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