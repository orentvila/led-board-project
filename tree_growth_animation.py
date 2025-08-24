#!/usr/bin/env python3
"""
Tree Growth Animation for LED Board
Shows a peaceful 20-second growth from sprout to fruit-bearing tree
"""

import time
import numpy as np
from led_controller_fixed import LEDControllerFixed
import config

class TreeGrowthAnimation:
    def __init__(self):
        """Initialize the tree growth animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.colors = {
            'background': (20, 40, 10),      # Dark green background (soil/ground)
            'soil': (60, 30, 10),            # Brown soil
            'sprout': (0, 100, 0),           # Bright green sprout
            'trunk': (80, 40, 20),           # Brown trunk
            'branches': (60, 30, 15),        # Darker brown branches
            'leaves': (0, 150, 0),           # Green leaves
            'apples': (200, 0, 0),           # Bright red apples
            'apple_highlight': (255, 50, 50), # Lighter red for apple highlights
            'ground': (40, 60, 20)           # Ground color
        }
        
        # Animation timing (20 seconds total)
        self.total_duration = 20.0
        self.sprout_start = 2.0      # Sprout appears at 2 seconds
        self.growth_duration = 8.0   # Tree grows from 2s to 10s
        self.leaves_start = 10.0     # Leaves start appearing at 10s
        self.leaves_duration = 6.0   # Leaves grow from 10s to 16s
        self.apples_start = 16.0     # Apples start appearing at 16s
        self.apples_duration = 4.0   # Apples grow from 16s to 20s
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        
    def create_ground(self):
        """Create the ground/soil background."""
        ground = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create soil texture in the bottom third
        ground_y_start = int(self.height * 0.7)
        for y in range(ground_y_start, self.height):
            for x in range(self.width):
                # Add some variation to soil color
                variation = np.random.randint(-10, 10)
                soil_color = tuple(max(0, min(255, c + variation)) for c in self.colors['soil'])
                ground[y, x] = soil_color
        
        return ground
    
    def create_sprout(self, growth_progress):
        """Create a growing sprout."""
        sprout = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Sprout position (center of display)
        center_x = self.width // 2
        ground_y = int(self.height * 0.8)
        
        # Calculate sprout height based on growth progress
        max_sprout_height = 8
        sprout_height = int(max_sprout_height * growth_progress)
        
        if sprout_height > 0:
            # Draw sprout stem
            for y in range(ground_y - sprout_height, ground_y):
                self.safe_set_pixel(sprout, center_x, y, self.colors['sprout'])
                # Add small leaves as sprout grows
                if growth_progress > 0.3 and y < ground_y - 2:
                    self.safe_set_pixel(sprout, center_x - 1, y, self.colors['sprout'])
                    self.safe_set_pixel(sprout, center_x + 1, y, self.colors['sprout'])
        
        return sprout
    
    def create_tree(self, growth_progress, leaves_progress=0.0, apples_progress=0.0):
        """Create a growing tree with trunk, branches, leaves, and apples."""
        tree = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Tree position
        center_x = self.width // 2
        ground_y = int(self.height * 0.8)
        
        # Calculate tree dimensions based on growth progress
        max_trunk_height = 25
        trunk_height = int(max_trunk_height * growth_progress)
        trunk_width = max(1, int(3 * growth_progress))
        
        if trunk_height > 0:
            # Draw trunk
            trunk_start_y = ground_y - trunk_height
            for y in range(trunk_start_y, ground_y):
                for x in range(center_x - trunk_width, center_x + trunk_width + 1):
                    self.safe_set_pixel(tree, x, y, self.colors['trunk'])
            
            # Draw branches when tree is tall enough
            if growth_progress > 0.4:
                branch_levels = 3
                for i in range(branch_levels):
                    branch_y = trunk_start_y + int(trunk_height * (0.3 + i * 0.2))
                    branch_length = int(8 * growth_progress)
                    
                    # Left branch
                    for x in range(center_x - branch_length, center_x):
                        self.safe_set_pixel(tree, x, branch_y, self.colors['branches'])
                        # Small vertical branch
                        if x < center_x - 2:
                            self.safe_set_pixel(tree, x, branch_y - 1, self.colors['branches'])
                    
                    # Right branch
                    for x in range(center_x, center_x + branch_length):
                        self.safe_set_pixel(tree, x, branch_y, self.colors['branches'])
                        # Small vertical branch
                        if x > center_x + 2:
                            self.safe_set_pixel(tree, x, branch_y - 1, self.colors['branches'])
            
            # Add leaves when leaves_progress > 0
            if leaves_progress > 0:
                self.add_leaves(tree, center_x, trunk_start_y, trunk_height, leaves_progress)
                
                # Add apples when apples_progress > 0
                if apples_progress > 0:
                    self.add_apples(tree, center_x, trunk_start_y, trunk_height, apples_progress)
        
        return tree
    
    def add_leaves(self, tree, center_x, trunk_start_y, trunk_height, leaves_progress):
        """Add leaves to the tree branches."""
        # Define leaf positions around branches
        leaf_positions = []
        
        # Main canopy area
        canopy_start_y = trunk_start_y + int(trunk_height * 0.3)
        canopy_end_y = trunk_start_y + int(trunk_height * 0.8)
        
        for y in range(canopy_start_y, canopy_end_y):
            # Calculate leaf spread based on height
            max_spread = int(12 * (1 - (y - canopy_start_y) / (canopy_end_y - canopy_start_y)))
            for x in range(center_x - max_spread, center_x + max_spread + 1):
                # Add some randomness to leaf placement
                if np.random.random() < 0.7:
                    leaf_positions.append((x, y))
        
        # Show leaves based on progress
        num_leaves_to_show = int(len(leaf_positions) * leaves_progress)
        for i in range(num_leaves_to_show):
            if i < len(leaf_positions):
                x, y = leaf_positions[i]
                self.safe_set_pixel(tree, x, y, self.colors['leaves'])
    
    def add_apples(self, tree, center_x, trunk_start_y, trunk_height, apples_progress):
        """Add apples to the tree branches."""
        # Define apple positions (fewer than leaves)
        apple_positions = []
        
        # Apple positions on branches
        branch_positions = [
            (center_x - 6, trunk_start_y + int(trunk_height * 0.4)),
            (center_x + 6, trunk_start_y + int(trunk_height * 0.4)),
            (center_x - 4, trunk_start_y + int(trunk_height * 0.6)),
            (center_x + 4, trunk_start_y + int(trunk_height * 0.6)),
            (center_x - 2, trunk_start_y + int(trunk_height * 0.5)),
            (center_x + 2, trunk_start_y + int(trunk_height * 0.5)),
            (center_x, trunk_start_y + int(trunk_height * 0.7)),
        ]
        
        for x, y in branch_positions:
            apple_positions.append((x, y))
            # Add some variation in apple positions
            apple_positions.append((x + 1, y))
            apple_positions.append((x, y + 1))
        
        # Show apples based on progress
        num_apples_to_show = int(len(apple_positions) * apples_progress)
        for i in range(num_apples_to_show):
            if i < len(apple_positions):
                x, y = apple_positions[i]
                # Add highlight to some apples
                if np.random.random() < 0.3:
                    self.safe_set_pixel(tree, x, y, self.colors['apple_highlight'])
                else:
                    self.safe_set_pixel(tree, x, y, self.colors['apples'])
    
    def run_animation(self):
        """Run the complete tree growth animation."""
        print("🌱🌳🍎 Tree Growth Animation 🌱🌳🍎")
        print("Duration: 20 seconds")
        print("Sequence: Ground → Sprout → Tree → Leaves → Apples")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Calculate progress for each phase
                if current_time < self.sprout_start:
                    # Phase 1: Just ground
                    frame = self.create_ground()
                elif current_time < self.sprout_start + self.growth_duration:
                    # Phase 2: Sprout growing
                    growth_progress = (current_time - self.sprout_start) / self.growth_duration
                    frame = self.create_ground()
                    sprout = self.create_sprout(growth_progress)
                    # Combine ground and sprout
                    for y in range(self.height):
                        for x in range(self.width):
                            # Compare RGB values properly
                            if not np.array_equal(sprout[y, x], self.colors['background']):
                                frame[y, x] = sprout[y, x]
                else:
                    # Phase 3: Full tree with leaves and apples
                    leaves_progress = 0.0
                    apples_progress = 0.0
                    
                    if current_time >= self.leaves_start:
                        leaves_progress = min(1.0, (current_time - self.leaves_start) / self.leaves_duration)
                    
                    if current_time >= self.apples_start:
                        apples_progress = min(1.0, (current_time - self.apples_start) / self.apples_duration)
                    
                    frame = self.create_tree(1.0, leaves_progress, apples_progress)
                
                # Display the frame
                for y in range(self.height):
                    for x in range(self.width):
                        self.led.set_pixel(x, y, frame[y, x])
                
                self.led.show()
                
                # Check if animation is complete
                if current_time >= self.total_duration:
                    print("Tree growth animation completed!")
                    break
                
                time.sleep(0.05)  # 20 FPS for smooth animation
                
        except KeyboardInterrupt:
            print("\nTree growth animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run tree growth animation."""
    try:
        tree_growth = TreeGrowthAnimation()
        tree_growth.run_animation()
        tree_growth.cleanup()
        
    except KeyboardInterrupt:
        print("\nTree growth animation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 