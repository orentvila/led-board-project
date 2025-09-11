#!/usr/bin/env python3
"""
Tree Growing Portrait Animation for LED Display
Creates a tree growing animation in portrait orientation (32x48)
Tree grows from bottom to top with branches and leaves
"""

import time
import random
import math
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from led_controller import LEDController
import config

class TreeGrowingPortraitAnimation:
    def __init__(self, led_controller):
        """Initialize the tree growing animation."""
        self.led = led_controller
        self.running = False
        
        # Animation settings
        self.growth_speed = 0.3  # seconds between growth steps
        self.branch_probability = 0.3  # probability of creating a branch
        self.leaf_probability = 0.4  # probability of creating leaves
        
        # Tree structure
        self.tree_pixels = set()  # Set of (x, y) coordinates for tree
        self.branches = []  # List of branch segments
        self.leaves = set()  # Set of (x, y) coordinates for leaves
        
        # Colors
        self.trunk_color = (139, 69, 19)  # Brown trunk
        self.branch_color = (101, 67, 33)  # Darker brown branches
        self.leaf_color = (34, 139, 34)  # Green leaves
        self.ground_color = (34, 139, 34)  # Green ground
        
        # Tree growth parameters
        self.max_height = config.TOTAL_HEIGHT - 2  # Leave space for ground
        self.trunk_width = 2
        self.branch_length = 3
        
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
            trunk_width = self.trunk_width
            if height > 10:  # Make trunk wider at the base
                trunk_width = 3
            
            for dx in range(-trunk_width//2, trunk_width//2 + 1):
                x = center_x + dx
                if 0 <= x < config.TOTAL_WIDTH:
                    self._draw_pixel(x, y, self.trunk_color)
                    self.tree_pixels.add((x, y))
    
    def _create_branch(self, start_x, start_y, direction, length):
        """Create a branch from the given position."""
        branch_pixels = []
        
        for i in range(length):
            if direction == 'left':
                x = start_x - i
                y = start_y - i
            elif direction == 'right':
                x = start_x + i
                y = start_y - i
            else:  # up
                x = start_x
                y = start_y - i
            
            if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
                self._draw_pixel(x, y, self.branch_color)
                branch_pixels.append((x, y))
                self.tree_pixels.add((x, y))
        
        return branch_pixels
    
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
    
    def _grow_branches(self, trunk_height):
        """Grow branches from the trunk."""
        if trunk_height < 5:  # Don't create branches too early
            return
        
        center_x = config.TOTAL_WIDTH // 2
        
        # Create branches at different heights
        branch_heights = [trunk_height - 3, trunk_height - 6, trunk_height - 9]
        
        for branch_y in branch_heights:
            if branch_y > 0:
                # Randomly decide to create branches
                if random.random() < self.branch_probability:
                    # Left branch
                    if random.random() < 0.5:
                        branch_length = random.randint(2, self.branch_length)
                        self._create_branch(center_x - 1, branch_y, 'left', branch_length)
                        
                        # Add leaves to branch tip
                        tip_x = center_x - 1 - branch_length
                        tip_y = branch_y - branch_length
                        if random.random() < self.leaf_probability:
                            self._create_leaves(tip_x, tip_y)
                    
                    # Right branch
                    if random.random() < 0.5:
                        branch_length = random.randint(2, self.branch_length)
                        self._create_branch(center_x + 1, branch_y, 'right', branch_length)
                        
                        # Add leaves to branch tip
                        tip_x = center_x + 1 + branch_length
                        tip_y = branch_y - branch_length
                        if random.random() < self.leaf_probability:
                            self._create_leaves(tip_x, tip_y)
    
    def _add_random_leaves(self):
        """Add random leaves to the tree."""
        if len(self.tree_pixels) > 0:
            # Pick a random tree pixel and add leaves nearby
            tree_pixel = random.choice(list(self.tree_pixels))
            if random.random() < self.leaf_probability:
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
            
            # Add branches
            self._grow_branches(height)
            
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
        print("🌱 Starting tree growing animation...")
        print(f"📏 Display size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print(f"🌳 Max tree height: {self.max_height}")
        
        start_time = time.time()
        
        try:
            self._animate_growth()
        except KeyboardInterrupt:
            print("\n🛑 Animation stopped by user")
        except Exception as e:
            print(f"❌ Animation error: {e}")
        finally:
            self.running = False
            print("🌳 Tree growing animation completed!")
    
    def stop(self):
        """Stop the animation."""
        self.running = False

def main():
    """Test the tree growing animation."""
    try:
        # Initialize LED controller
        led = LEDController()
        
        # Create and run the animation
        animation = TreeGrowingPortraitAnimation(led)
        animation.run_animation()
        
        # Cleanup
        led.cleanup()
        
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
