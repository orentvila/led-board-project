#!/usr/bin/env python3
"""
Tree Growth Animation for LED Board
A calm 20-second animation showing natural tree growth from sprout to fruit-bearing tree
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
        
        # Colors - more natural and calming palette
        self.colors = {
            'background': (15, 25, 10),      # Dark forest green background
            'soil': (45, 25, 15),            # Rich brown soil
            'soil_light': (60, 35, 20),      # Lighter soil variation
            'sprout': (20, 120, 20),         # Fresh green sprout
            'trunk': (70, 45, 25),           # Natural brown trunk
            'trunk_dark': (50, 30, 15),      # Darker trunk variation
            'branches': (60, 40, 20),        # Branch color
            'leaves': (30, 140, 30),         # Vibrant green leaves
            'leaves_light': (50, 160, 50),   # Lighter leaf variation
            'apples': (180, 20, 20),         # Rich red apples
            'apples_highlight': (220, 40, 40), # Brighter apple highlights
            'ground': (25, 35, 15)           # Ground color
        }
        
        # Animation timing (20 seconds total)
        self.total_duration = 20.0
        self.sprout_start = 1.0      # Sprout appears at 1 second
        self.growth_duration = 10.0  # Tree grows from 1s to 11s
        self.leaves_start = 8.0      # Leaves start appearing at 8s
        self.leaves_duration = 8.0   # Leaves grow from 8s to 16s
        self.apples_start = 16.0     # Apples start appearing at 16s
        self.apples_duration = 4.0   # Apples grow from 16s to 20s
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        
    def create_soil_background(self):
        """Create a natural soil background with texture."""
        soil = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create soil in the bottom portion
        soil_start_y = int(self.height * 0.65)
        
        for y in range(soil_start_y, self.height):
            for x in range(self.width):
                # Add natural soil texture variation
                if np.random.random() < 0.3:
                    soil[y, x] = self.colors['soil_light']
                else:
                    soil[y, x] = self.colors['soil']
                
                # Add some darker spots for realism
                if np.random.random() < 0.1:
                    soil[y, x] = tuple(max(0, c - 15) for c in soil[y, x])
        
        return soil
    
    def create_sprout(self, growth_progress):
        """Create a growing sprout with natural movement."""
        sprout = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Sprout position (center of display)
        center_x = self.width // 2
        ground_y = int(self.height * 0.7)
        
        # Calculate sprout height with easing
        max_sprout_height = 12
        eased_progress = self.ease_in_out(growth_progress)
        sprout_height = int(max_sprout_height * eased_progress)
        
        if sprout_height > 0:
            # Draw main sprout stem
            for y in range(ground_y - sprout_height, ground_y):
                self.safe_set_pixel(sprout, center_x, y, self.colors['sprout'])
                
                # Add small leaves as sprout grows taller
                if growth_progress > 0.4 and y < ground_y - 3:
                    leaf_offset = int(3 * (1 - (y - (ground_y - sprout_height)) / sprout_height))
                    if leaf_offset > 0:
                        self.safe_set_pixel(sprout, center_x - leaf_offset, y, self.colors['sprout'])
                        self.safe_set_pixel(sprout, center_x + leaf_offset, y, self.colors['sprout'])
        
        return sprout
    
    def create_tree(self, growth_progress, leaves_progress=0.0, apples_progress=0.0):
        """Create a natural-looking tree with trunk, branches, leaves, and apples."""
        tree = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Tree position
        center_x = self.width // 2
        ground_y = int(self.height * 0.7)
        
        # Calculate tree dimensions with easing
        max_trunk_height = 30
        eased_growth = self.ease_in_out(growth_progress)
        trunk_height = int(max_trunk_height * eased_growth)
        trunk_width = max(1, int(4 * eased_growth))
        
        if trunk_height > 0:
            # Draw trunk with natural taper
            trunk_start_y = ground_y - trunk_height
            for y in range(trunk_start_y, ground_y):
                # Trunk gets narrower toward the top
                current_width = max(1, trunk_width - (ground_y - y) // 8)
                for x in range(center_x - current_width, center_x + current_width + 1):
                    # Add trunk texture variation
                    if (x + y) % 3 == 0:
                        self.safe_set_pixel(tree, x, y, self.colors['trunk_dark'])
                    else:
                        self.safe_set_pixel(tree, x, y, self.colors['trunk'])
            
            # Draw branches when tree is tall enough
            if growth_progress > 0.5:
                self.add_branches(tree, center_x, trunk_start_y, trunk_height, growth_progress)
            
            # Add leaves when leaves_progress > 0
            if leaves_progress > 0:
                self.add_leaves(tree, center_x, trunk_start_y, trunk_height, leaves_progress)
                
                # Add apples when apples_progress > 0
                if apples_progress > 0:
                    self.add_apples(tree, center_x, trunk_start_y, trunk_height, apples_progress)
        
        return tree
    
    def add_branches(self, tree, center_x, trunk_start_y, trunk_height, growth_progress):
        """Add natural-looking branches to the tree."""
        branch_levels = 4
        for i in range(branch_levels):
            branch_y = trunk_start_y + int(trunk_height * (0.4 + i * 0.15))
            branch_length = int(10 * growth_progress)
            
            # Left branch
            for x in range(center_x - branch_length, center_x):
                self.safe_set_pixel(tree, x, branch_y, self.colors['branches'])
                # Small vertical branch
                if x < center_x - 3:
                    self.safe_set_pixel(tree, x, branch_y - 1, self.colors['branches'])
                    self.safe_set_pixel(tree, x, branch_y - 2, self.colors['branches'])
            
            # Right branch
            for x in range(center_x, center_x + branch_length):
                self.safe_set_pixel(tree, x, branch_y, self.colors['branches'])
                # Small vertical branch
                if x > center_x + 3:
                    self.safe_set_pixel(tree, x, branch_y - 1, self.colors['branches'])
                    self.safe_set_pixel(tree, x, branch_y - 2, self.colors['branches'])
    
    def add_leaves(self, tree, center_x, trunk_start_y, trunk_height, leaves_progress):
        """Add leaves to the tree branches with natural distribution."""
        # Define leaf positions around branches
        leaf_positions = []
        
        # Main canopy area
        canopy_start_y = trunk_start_y + int(trunk_height * 0.3)
        canopy_end_y = trunk_start_y + int(trunk_height * 0.9)
        
        for y in range(canopy_start_y, canopy_end_y):
            # Calculate leaf spread based on height (wider in middle, narrower at top)
            height_ratio = (y - canopy_start_y) / (canopy_end_y - canopy_start_y)
            max_spread = int(15 * (1 - abs(height_ratio - 0.5) * 1.5))
            
            for x in range(center_x - max_spread, center_x + max_spread + 1):
                # Add some randomness to leaf placement for natural look
                if np.random.random() < 0.6:
                    leaf_positions.append((x, y))
        
        # Show leaves based on progress with easing
        eased_progress = self.ease_in_out(leaves_progress)
        num_leaves_to_show = int(len(leaf_positions) * eased_progress)
        
        for i in range(num_leaves_to_show):
            if i < len(leaf_positions):
                x, y = leaf_positions[i]
                # Add leaf color variation
                if np.random.random() < 0.3:
                    self.safe_set_pixel(tree, x, y, self.colors['leaves_light'])
                else:
                    self.safe_set_pixel(tree, x, y, self.colors['leaves'])
    
    def add_apples(self, tree, center_x, trunk_start_y, trunk_height, apples_progress):
        """Add apples to the tree branches."""
        # Define apple positions on branches
        apple_positions = []
        
        # Apple positions on main branches
        branch_positions = [
            (center_x - 8, trunk_start_y + int(trunk_height * 0.4)),
            (center_x + 8, trunk_start_y + int(trunk_height * 0.4)),
            (center_x - 6, trunk_start_y + int(trunk_height * 0.55)),
            (center_x + 6, trunk_start_y + int(trunk_height * 0.55)),
            (center_x - 4, trunk_start_y + int(trunk_height * 0.7)),
            (center_x + 4, trunk_start_y + int(trunk_height * 0.7)),
            (center_x - 2, trunk_start_y + int(trunk_height * 0.5)),
            (center_x + 2, trunk_start_y + int(trunk_height * 0.5)),
            (center_x, trunk_start_y + int(trunk_height * 0.8)),
        ]
        
        for x, y in branch_positions:
            apple_positions.append((x, y))
            # Add some variation in apple positions
            apple_positions.append((x + 1, y))
            apple_positions.append((x, y + 1))
        
        # Show apples based on progress with easing
        eased_progress = self.ease_in_out(apples_progress)
        num_apples_to_show = int(len(apple_positions) * eased_progress)
        
        for i in range(num_apples_to_show):
            if i < len(apple_positions):
                x, y = apple_positions[i]
                # Add highlight to some apples for depth
                if np.random.random() < 0.4:
                    self.safe_set_pixel(tree, x, y, self.colors['apples_highlight'])
                else:
                    self.safe_set_pixel(tree, x, y, self.colors['apples'])
    
    def ease_in_out(self, t):
        """Smooth easing function for natural movement."""
        return t * t * (3.0 - 2.0 * t)
    
    def run_animation(self):
        """Run the complete tree growth animation."""
        print("🌱🌳🍎 Calm Tree Growth Animation 🌱🌳🍎")
        print("Duration: 20 seconds")
        print("Sequence: Soil → Sprout → Tree → Leaves → Apples")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Calculate progress for each phase
                if current_time < self.sprout_start:
                    # Phase 1: Just soil
                    frame = self.create_soil_background()
                elif current_time < self.sprout_start + self.growth_duration:
                    # Phase 2: Sprout growing into tree
                    growth_progress = (current_time - self.sprout_start) / self.growth_duration
                    frame = self.create_soil_background()
                    sprout = self.create_sprout(growth_progress)
                    
                    # Combine soil and sprout
                    for y in range(self.height):
                        for x in range(self.width):
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
                
                time.sleep(0.04)  # 25 FPS for smoother animation
                
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