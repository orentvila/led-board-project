#!/usr/bin/env python3
"""
Portrait Tree Animation for LED Display
Tree growing animation in portrait orientation (32x48) for real LED display
"""

import time
import random
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Try to import LED controller
try:
    from led_controller import LEDController
    import config
    LED_AVAILABLE = True
    print("✅ LED controller available")
except ImportError:
    print("⚠️  LED controller not available - using mock display")
    LED_AVAILABLE = False
    
    # Mock configuration
    class MockConfig:
        TOTAL_WIDTH = 32
        TOTAL_HEIGHT = 48
    
    config = MockConfig()
    
    # Mock LED controller
    class MockLEDController:
        def __init__(self):
            self.pixels = [[(0, 0, 0) for _ in range(config.TOTAL_WIDTH)] for _ in range(config.TOTAL_HEIGHT)]
        
        def set_pixel(self, x, y, color):
            if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                self.pixels[y][x] = color
        
        def clear(self):
            for y in range(config.TOTAL_HEIGHT):
                for x in range(config.TOTAL_WIDTH):
                    self.pixels[y][x] = (0, 0, 0)
        
        def show(self):
            # Print a simple ASCII representation
            print("\n" + "="*50)
            for y in range(config.TOTAL_HEIGHT):
                line = ""
                for x in range(config.TOTAL_WIDTH):
                    pixel = self.pixels[y][x]
                    if pixel == (0, 0, 0):  # Black
                        line += " "
                    elif pixel == (139, 69, 19):  # Brown (trunk)
                        line += "█"
                    elif pixel == (34, 139, 34):  # Green (leaves/ground)
                        line += "●"
                    else:
                        line += "·"
                print(line)
            print("="*50)
        
        def cleanup(self):
            pass

class PortraitTreeAnimation:
    def __init__(self):
        """Initialize the portrait tree animation."""
        if LED_AVAILABLE:
            self.led = LEDController()
        else:
            self.led = MockLEDController()
        self.running = False
        
        # Animation settings
        self.max_height = config.TOTAL_HEIGHT - 2  # Leave space for ground
        self.growth_speed = 0.3  # seconds between growth steps
        
        # Colors (RGB)
        self.trunk_color = (139, 69, 19)  # Brown
        self.leaf_color = (34, 139, 34)   # Green
        self.ground_color = (34, 139, 34) # Green
        self.black_color = (0, 0, 0)      # Black
        
        # Tree structure
        self.tree_pixels = set()  # Set of (x, y) coordinates for tree
        self.leaves = set()  # Set of (x, y) coordinates for leaves
        
    def _draw_pixel(self, x, y, color):
        """Draw a pixel if it's within bounds."""
        if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
            self.led.set_pixel(x, y, color)
    
    def _draw_ground(self):
        """Draw the ground at the bottom."""
        for x in range(config.TOTAL_WIDTH):
            self._draw_pixel(x, config.TOTAL_HEIGHT - 1, self.ground_color)
    
    def _grow_trunk(self, height):
        """Grow the main trunk to the specified height."""
        center_x = config.TOTAL_WIDTH // 2
        
        for y in range(config.TOTAL_HEIGHT - 1, config.TOTAL_HEIGHT - 1 - height, -1):
            # Draw trunk with varying width
            trunk_width = 3
            if height > 20:  # Make trunk wider at the base
                trunk_width = 5
            
            for dx in range(-trunk_width//2, trunk_width//2 + 1):
                x = center_x + dx
                if 0 <= x < config.TOTAL_WIDTH:
                    self._draw_pixel(x, y, self.trunk_color)
                    self.tree_pixels.add((x, y))
    
    def _create_leaves(self, x, y, size=2):
        """Create leaves around a position."""
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                if abs(dx) + abs(dy) <= size:  # Diamond shape
                    leaf_x = x + dx
                    leaf_y = y + dy
                    if (0 <= leaf_x < config.TOTAL_WIDTH and 
                        0 <= leaf_y < config.TOTAL_HEIGHT and
                        (leaf_x, leaf_y) not in self.tree_pixels):
                        self._draw_pixel(leaf_x, leaf_y, self.leaf_color)
                        self.leaves.add((leaf_x, leaf_y))
    
    def _add_random_leaves(self):
        """Add random leaves to the tree."""
        if len(self.tree_pixels) > 0:
            # Pick a random tree pixel and add leaves nearby
            tree_pixel = random.choice(list(self.tree_pixels))
            if random.random() < 0.3:  # 30% chance
                self._create_leaves(tree_pixel[0], tree_pixel[1], size=1)
    
    def _animate_growth(self):
        """Animate the tree growing."""
        self.running = True
        
        # Clear display
        self.led.clear()
        
        # Draw ground
        self._draw_ground()
        self.led.show()
        time.sleep(0.5)
        
        # Grow the tree step by step
        for height in range(1, self.max_height + 1):
            if not self.running:
                break
            
            # Clear previous frame
            self.led.clear()
            self._draw_ground()
            
            # Grow trunk to current height
            self._grow_trunk(height)
            
            # Add leaves at the top
            if height > 3:
                center_x = config.TOTAL_WIDTH // 2
                top_y = config.TOTAL_HEIGHT - 1 - height
                self._create_leaves(center_x, top_y, size=2)
            
            # Add random leaves
            self._add_random_leaves()
            
            # Show the current state
            self.led.show()
            time.sleep(self.growth_speed)
        
        # Final flourish - add more leaves
        print("🌳 Tree growth complete! Adding final leaves...")
        for _ in range(10):
            if not self.running:
                break
            self._add_random_leaves()
            self.led.show()
            time.sleep(0.2)
        
        # Keep the final tree displayed for a moment
        if self.running:
            print("🌳 Final tree display...")
            time.sleep(3)
    
    def run_animation(self, duration=None):
        """Run the tree growing animation."""
        print("🌱 Starting Portrait Tree Animation...")
        print(f"📏 Display size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print(f"🌳 Max tree height: {self.max_height}")
        
        try:
            self._animate_growth()
        except KeyboardInterrupt:
            print("\n🛑 Animation stopped by user")
        except Exception as e:
            print(f"❌ Animation error: {e}")
        finally:
            self.running = False
            print("🌳 Tree growth animation completed!")
    
    def stop(self):
        """Stop the animation."""
        self.running = False
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Run the portrait tree animation."""
    try:
        # Create and run the animation
        animation = PortraitTreeAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
