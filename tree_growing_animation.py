#!/usr/bin/env python3
"""
Tree Growing Animation for LED Board
Features a big tree growing from the ground up with branches and leaves
"""

import time
import numpy as np
import math
from led_controller_fixed import LEDControllerFixed
import config

class TreeGrowingAnimation:
    def __init__(self):
        """Initialize the tree growing animation."""
        self.led = LEDControllerFixed()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 40
        
        # Colors
        self.colors = {
            'sky': (135, 206, 235),        # Light blue sky
            'ground': (139, 69, 19),       # Brown ground
            'trunk': (101, 67, 33),        # Dark brown trunk
            'trunk_light': (139, 69, 19),  # Lighter brown trunk
            'branch': (101, 67, 33),       # Brown branches
            'leaves_dark': (34, 139, 34),  # Dark green leaves
            'leaves_light': (50, 205, 50), # Light green leaves
            'leaves_yellow': (255, 255, 0), # Yellow leaves
            'leaves_orange': (255, 165, 0), # Orange leaves
            'leaves_red': (255, 0, 0),     # Red leaves
            'roots': (101, 67, 33),        # Brown roots
            'grass': (34, 139, 34),        # Green grass
            'sun': (255, 255, 0),          # Yellow sun
            'cloud': (255, 255, 255),      # White clouds
            'soil': (160, 82, 45)          # Soil color
        }
        
        # Animation parameters
        self.growth_stage = 0
        self.growth_timer = 0
        self.leaf_timer = 0
        self.season_timer = 0
        self.max_height = self.height * 0.8  # Maximum tree height
        
    def create_sky_and_ground(self, frame):
        """Create sky and ground background."""
        # Sky (upper 70% of display)
        sky_height = int(self.height * 0.7)
        for y in range(sky_height):
            for x in range(self.width):
                frame[y, x] = self.colors['sky']
        
        # Ground (lower 30% of display)
        for y in range(sky_height, self.height):
            for x in range(self.width):
                frame[y, x] = self.colors['ground']
        
        # Add some grass texture
        for y in range(sky_height, sky_height + 3):
            for x in range(self.width):
                if np.random.random() < 0.3:  # 30% chance for grass
                    frame[y, x] = self.colors['grass']
    
    def create_sun_and_clouds(self, frame):
        """Create sun and moving clouds."""
        # Sun
        sun_x = int(self.width * 0.8)
        sun_y = int(self.height * 0.15)
        for y in range(sun_y - 2, sun_y + 3):
            for x in range(sun_x - 2, sun_x + 3):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['sun']
        
        # Moving clouds
        cloud_positions = [
            (int(self.width * 0.2 + self.growth_timer * 0.1) % self.width, int(self.height * 0.1)),
            (int(self.width * 0.6 + self.growth_timer * 0.15) % self.width, int(self.height * 0.08))
        ]
        
        for cx, cy in cloud_positions:
            for y in range(cy - 1, cy + 2):
                for x in range(cx - 3, cx + 4):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        frame[y, x] = self.colors['cloud']
    
    def create_roots(self, frame):
        """Create tree roots in the ground."""
        root_base_x = self.width // 2
        root_base_y = int(self.height * 0.7)  # Ground level
        
        # Main root
        for y in range(root_base_y, self.height):
            for x in range(root_base_x - 1, root_base_x + 2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    frame[y, x] = self.colors['roots']
        
        # Side roots
        root_positions = [
            (root_base_x - 3, root_base_y + 2),
            (root_base_x + 3, root_base_y + 2),
            (root_base_x - 2, root_base_y + 4),
            (root_base_x + 2, root_base_y + 4)
        ]
        
        for rx, ry in root_positions:
            for y in range(ry, min(ry + 3, self.height)):
                for x in range(rx - 1, rx + 2):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        frame[y, x] = self.colors['roots']
    
    def create_trunk(self, frame, current_height):
        """Create the growing tree trunk."""
        trunk_x = self.width // 2
        trunk_width = 3
        
        # Calculate current trunk height based on growth stage
        trunk_height = int(current_height * self.max_height)
        
        # Draw trunk
        for y in range(int(self.height * 0.7), int(self.height * 0.7) + trunk_height):
            for x in range(trunk_x - trunk_width // 2, trunk_x + trunk_width // 2 + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Add some trunk texture variation
                    if (x + y) % 2 == 0:
                        frame[y, x] = self.colors['trunk']
                    else:
                        frame[y, x] = self.colors['trunk_light']
    
    def create_branches(self, frame, current_height):
        """Create branches on the growing tree."""
        trunk_x = self.width // 2
        trunk_height = int(current_height * self.max_height)
        
        # Only create branches if trunk is tall enough
        if trunk_height < 10:
            return
        
        # Branch positions (relative to trunk height)
        branch_positions = [
            (0.3, 0.4),  # Lower branches
            (0.5, 0.6),  # Middle branches
            (0.7, 0.8),  # Upper branches
        ]
        
        for branch_ratio, branch_length_ratio in branch_positions:
            branch_y = int(self.height * 0.7) + int(trunk_height * branch_ratio)
            
            # Only draw branch if it's within current growth
            if branch_y < int(self.height * 0.7) + trunk_height:
                branch_length = int(8 * branch_length_ratio)
                
                # Left branch
                for i in range(branch_length):
                    branch_x = trunk_x - i
                    branch_y_pos = branch_y - i // 2
                    if 0 <= branch_x < self.width and 0 <= branch_y_pos < self.height:
                        frame[branch_y_pos, branch_x] = self.colors['branch']
                
                # Right branch
                for i in range(branch_length):
                    branch_x = trunk_x + i
                    branch_y_pos = branch_y - i // 2
                    if 0 <= branch_x < self.width and 0 <= branch_y_pos < self.height:
                        frame[branch_y_pos, branch_x] = self.colors['branch']
    
    def create_leaves(self, frame, current_height):
        """Create leaves on the growing tree."""
        trunk_x = self.width // 2
        trunk_height = int(current_height * self.max_height)
        
        # Only create leaves if trunk is tall enough
        if trunk_height < 8:
            return
        
        # Leaf clusters at different heights
        leaf_positions = [
            (0.4, 0.3),  # Lower leaves
            (0.6, 0.4),  # Middle leaves
            (0.8, 0.5),  # Upper leaves
            (0.9, 0.3),  # Top leaves
        ]
        
        for leaf_ratio, leaf_size_ratio in leaf_positions:
            leaf_center_y = int(self.height * 0.7) + int(trunk_height * leaf_ratio)
            
            # Only draw leaves if they're within current growth
            if leaf_center_y < int(self.height * 0.7) + trunk_height:
                leaf_size = int(6 * leaf_size_ratio)
                
                # Create leaf cluster
                for y in range(leaf_center_y - leaf_size, leaf_center_y + leaf_size):
                    for x in range(trunk_x - leaf_size, trunk_x + leaf_size + 1):
                        if 0 <= x < self.width and 0 <= y < self.height:
                            distance = math.sqrt((x - trunk_x)**2 + (y - leaf_center_y)**2)
                            
                            if distance <= leaf_size:
                                # Seasonal leaf colors
                                season = (self.season_timer * 0.01) % 4
                                
                                if season < 1:  # Spring - light green
                                    leaf_color = self.colors['leaves_light']
                                elif season < 2:  # Summer - dark green
                                    leaf_color = self.colors['leaves_dark']
                                elif season < 3:  # Fall - yellow/orange/red
                                    fall_phase = (season - 2) * 3
                                    if fall_phase < 1:
                                        leaf_color = self.colors['leaves_yellow']
                                    elif fall_phase < 2:
                                        leaf_color = self.colors['leaves_orange']
                                    else:
                                        leaf_color = self.colors['leaves_red']
                                else:  # Winter - no leaves (will be handled by growth)
                                    leaf_color = self.colors['leaves_dark']
                                
                                # Add some variation
                                variation = math.sin(x * 0.2 + y * 0.2 + self.leaf_timer * 0.1) * 0.2 + 0.8
                                final_color = tuple(int(c * variation) for c in leaf_color)
                                frame[y, x] = final_color
    
    def create_growing_animation(self, frame):
        """Create the growing animation frame."""
        # Calculate current growth stage (0 to 1)
        growth_duration = 200  # frames for full growth
        current_growth = min(1.0, self.growth_timer / growth_duration)
        
        # Create background
        self.create_sky_and_ground(frame)
        self.create_sun_and_clouds(frame)
        
        # Create roots (always visible)
        self.create_roots(frame)
        
        # Create trunk (grows from ground up)
        self.create_trunk(frame, current_growth)
        
        # Create branches (appear as trunk grows)
        self.create_branches(frame, current_growth)
        
        # Create leaves (appear after branches)
        self.create_leaves(frame, current_growth)
    
    def display_tree_growing(self, duration=25):
        """Display the tree growing animation."""
        print("🌳 Tree Growing Animation 🌳")
        print(f"Displaying for {duration} seconds...")
        print("Features: Tree growing from ground, branches, seasonal leaves")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create the frame
            frame = np.full((self.height, self.width, 3), self.colors['sky'], dtype=np.uint8)
            self.create_growing_animation(frame)
            
            # Display the frame
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            # Update animation parameters
            self.growth_timer += 1
            self.leaf_timer += 1
            self.season_timer += 1
            
            time.sleep(0.1)  # 10 FPS
        
        print("Tree growing animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run tree growing animation."""
    try:
        tree = TreeGrowingAnimation()
        tree.display_tree_growing(25)
        tree.cleanup()
        
    except KeyboardInterrupt:
        print("\nTree growing animation interrupted by user")
        tree.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        tree.cleanup()

if __name__ == "__main__":
    main() 