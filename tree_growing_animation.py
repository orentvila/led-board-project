#!/usr/bin/env python3
"""
Tree Growing Animation for LED Board
Features a single, well-formed tree growing from the ground up
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
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors matching the described tree
        self.colors = {
            'background': (255, 255, 255),  # White background like the image
            'ground': (240, 240, 240),      # Light gray ground
            'trunk': (139, 69, 19),         # Brown trunk
            'trunk_dark': (101, 67, 33),    # Darker brown for trunk variation
            'leaves': (34, 139, 34),        # Vibrant green leaves
            'leaves_light': (50, 205, 50),  # Lighter green for variation
            'shadow': (200, 200, 200),      # Light gray shadow
            'soil': (160, 82, 45)           # Soil color
        }
        
        # Animation parameters
        self.growth_timer = 0
        self.leaf_timer = 0
        self.max_height = self.height * 0.75  # Tree height
        
    def create_background(self, frame):
        """Create white background with light gray ground."""
        # White background
        frame[:] = self.colors['background']
        
        # Light gray ground (lower 25% of display)
        ground_start = int(self.height * 0.75)
        for y in range(ground_start, self.height):
            for x in range(self.width):
                frame[y, x] = self.colors['ground']
    
    def create_tree_shadow(self, frame):
        """Create a subtle shadow beneath the tree."""
        shadow_x = self.width // 2
        shadow_y = int(self.height * 0.78)
        
        # Create oval shadow
        for y in range(shadow_y, min(shadow_y + 4, self.height)):
            for x in range(shadow_x - 6, shadow_x + 7):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Calculate shadow intensity based on distance from center
                    distance = math.sqrt((x - shadow_x)**2 + (y - shadow_y)**2)
                    if distance <= 6:
                        intensity = 1 - (distance / 6) * 0.3
                        shadow_color = tuple(int(c * intensity) for c in self.colors['shadow'])
                        frame[y, x] = shadow_color
    
    def create_trunk(self, frame, current_height):
        """Create a sturdy, well-formed trunk."""
        trunk_x = self.width // 2
        trunk_height = int(current_height * self.max_height)
        
        # Only draw if trunk has started growing
        if trunk_height < 2:
            return
        
        # Draw trunk with some width variation
        for y in range(int(self.height * 0.75), int(self.height * 0.75) + trunk_height):
            # Trunk gets slightly narrower toward the top
            trunk_width = max(2, 4 - (y - int(self.height * 0.75)) // 8)
            
            for x in range(trunk_x - trunk_width // 2, trunk_x + trunk_width // 2 + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Add trunk texture variation
                    if (x + y) % 2 == 0:
                        frame[y, x] = self.colors['trunk']
                    else:
                        frame[y, x] = self.colors['trunk_dark']
    
    def create_canopy(self, frame, current_height):
        """Create a dense, full canopy of leaves."""
        trunk_x = self.width // 2
        trunk_height = int(current_height * self.max_height)
        
        # Only create canopy if trunk is tall enough
        if trunk_height < 8:
            return
        
        # Canopy center (above trunk)
        canopy_center_y = int(self.height * 0.75) + trunk_height - 4
        canopy_radius = min(12, int(trunk_height * 0.8))
        
        # Create dense canopy
        for y in range(canopy_center_y - canopy_radius, canopy_center_y + canopy_radius):
            for x in range(trunk_x - canopy_radius, trunk_x + canopy_radius + 1):
                if 0 <= x < self.width and 0 <= y < self.height:
                    distance = math.sqrt((x - trunk_x)**2 + (y - canopy_center_y)**2)
                    
                    if distance <= canopy_radius:
                        # Create natural canopy shape (slightly oval)
                        canopy_shape = ((x - trunk_x) / canopy_radius)**2 + ((y - canopy_center_y) / (canopy_radius * 0.8))**2
                        
                        if canopy_shape <= 1:
                            # Add leaf variation
                            leaf_variation = math.sin(x * 0.3 + y * 0.2 + self.leaf_timer * 0.1) * 0.3 + 0.7
                            
                            # Choose leaf color based on position
                            if leaf_variation > 0.8:
                                leaf_color = self.colors['leaves_light']
                            else:
                                leaf_color = self.colors['leaves']
                            
                            # Blend with existing frame
                            current = frame[y, x]
                            frame[y, x] = tuple(int(c + (l - c) * 0.8) for c, l in zip(current, leaf_color))
    
    def create_branches(self, frame, current_height):
        """Create main branches supporting the canopy."""
        trunk_x = self.width // 2
        trunk_height = int(current_height * self.max_height)
        
        # Only create branches if trunk is tall enough
        if trunk_height < 10:
            return
        
        # Main branches
        branch_positions = [
            (0.6, 0.3),  # Lower branches
            (0.8, 0.4),  # Upper branches
        ]
        
        for branch_ratio, branch_length_ratio in branch_positions:
            branch_y = int(self.height * 0.75) + int(trunk_height * branch_ratio)
            
            # Only draw branch if it's within current growth
            if branch_y < int(self.height * 0.75) + trunk_height:
                branch_length = int(6 * branch_length_ratio)
                
                # Left branch
                for i in range(branch_length):
                    branch_x = trunk_x - i
                    branch_y_pos = branch_y - i // 3
                    if 0 <= branch_x < self.width and 0 <= branch_y_pos < self.height:
                        frame[branch_y_pos, branch_x] = self.colors['trunk']
                
                # Right branch
                for i in range(branch_length):
                    branch_x = trunk_x + i
                    branch_y_pos = branch_y - i // 3
                    if 0 <= branch_x < self.width and 0 <= branch_y_pos < self.height:
                        frame[branch_y_pos, branch_x] = self.colors['trunk']
    
    def create_growing_animation(self, frame):
        """Create the growing animation frame."""
        # Calculate current growth stage (0 to 1)
        growth_duration = 150  # frames for full growth
        current_growth = min(1.0, self.growth_timer / growth_duration)
        
        # Create background
        self.create_background(frame)
        
        # Create shadow (always visible)
        self.create_tree_shadow(frame)
        
        # Create trunk (grows from ground up)
        self.create_trunk(frame, current_growth)
        
        # Create branches (appear as trunk grows)
        self.create_branches(frame, current_growth)
        
        # Create canopy (appears after trunk and branches)
        self.create_canopy(frame, current_growth)
    
    def display_tree_growing(self, duration=20):
        """Display the tree growing animation."""
        print("🌳 Tree Growing Animation 🌳")
        print(f"Displaying for {duration} seconds...")
        print("Features: Single tree with dense canopy growing from ground")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Create the frame
            frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
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
            
            time.sleep(0.1)  # 10 FPS
        
        print("Tree growing animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run tree growing animation."""
    try:
        tree = TreeGrowingAnimation()
        tree.display_tree_growing(20)
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