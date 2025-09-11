#!/usr/bin/env python3
"""
Portrait Tree Animation for LED Display
Simple tree growing animation in portrait orientation (32x48)
"""

import time
import random
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    """Run the portrait tree animation."""
    print("🌱 Starting Portrait Tree Animation...")
    print("📏 Display size: 32x48 pixels")
    print("🌳 Tree growing from bottom to top...")
    
    # Animation settings
    max_height = 46  # Leave space for ground
    growth_speed = 0.2
    
    # Colors (RGB)
    trunk_color = (139, 69, 19)  # Brown
    leaf_color = (34, 139, 34)   # Green
    ground_color = (34, 139, 34) # Green
    
    # Simulate the animation
    for height in range(1, max_height + 1):
        print(f"\n🌳 Growing tree... Height: {height}/{max_height}")
        
        # Simulate tree growth
        center_x = 16  # Center of 32-pixel width
        
        # Draw trunk (3 pixels wide)
        trunk_width = 3
        if height > 20:
            trunk_width = 5  # Wider at base
        
        # Draw ground
        print("Ground: " + "█" * 32)
        
        # Draw tree
        for y in range(max_height - height, max_height):
            line = " " * 32
            if y == max_height - 1:  # Ground
                line = "█" * 32
            else:
                # Trunk
                start_x = center_x - trunk_width // 2
                end_x = center_x + trunk_width // 2
                for x in range(start_x, end_x + 1):
                    if 0 <= x < 32:
                        line = line[:x] + "█" + line[x+1:]
                
                # Add leaves at the top
                if y == max_height - height and height > 3:
                    # Add leaves around the trunk
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            if abs(dx) + abs(dy) <= 2:  # Diamond shape
                                leaf_x = center_x + dx
                                if 0 <= leaf_x < 32:
                                    line = line[:leaf_x] + "●" + line[leaf_x+1:]
            
            print(f"Row {y:2d}: {line}")
        
        time.sleep(growth_speed)
    
    # Final tree
    print("\n🌳 Final Tree Display:")
    print("=" * 50)
    
    # Draw the complete tree
    for y in range(max_height):
        line = " " * 32
        if y == max_height - 1:  # Ground
            line = "█" * 32
        else:
            # Trunk
            center_x = 16
            trunk_width = 5
            start_x = center_x - trunk_width // 2
            end_x = center_x + trunk_width // 2
            for x in range(start_x, end_x + 1):
                if 0 <= x < 32:
                    line = line[:x] + "█" + line[x+1:]
            
            # Add leaves
            if y < max_height - 10:  # Add leaves to upper part
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if abs(dx) + abs(dy) <= 3:
                            leaf_x = center_x + dx
                            if 0 <= leaf_x < 32 and random.random() < 0.3:
                                line = line[:leaf_x] + "●" + line[leaf_x+1:]
        
        print(f"Row {y:2d}: {line}")
    
    print("=" * 50)
    print("🌳 Tree growth animation completed!")
    print("✨ Portrait tree animation finished!")

if __name__ == "__main__":
    main()
