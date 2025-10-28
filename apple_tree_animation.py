#!/usr/bin/env python3
"""
Apple Tree Animation
A beautiful apple tree with falling apple animation
"""

import time
import math
from led_controller_exact import LEDControllerExact

class AppleTreeAnimation:
    def __init__(self):
        """Initialize the apple tree animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        self.duration = 20  # 20 seconds total
        
        # Colors
        self.brown_trunk = (139, 69, 19)  # Dark brown for trunk
        self.brown_soil = (101, 67, 33)  # Brown soil color
        self.green_leaves = (34, 139, 34)  # Forest green for leaves
        self.red_apple = (255, 0, 0)  # Bright red for apples
        self.apple_stem = (101, 67, 33)  # Brown for apple stems
        
        # Tree structure
        self.trunk_width = 6
        self.trunk_height = 16
        self.trunk_x = 13  # Centered trunk
        self.trunk_y = 40  # Bottom of trunk
        
        # Apple positions (7 apples) - better distributed
        self.apple_positions = [
            (16, 6),   # Top center
            (9, 10),   # Upper left
            (23, 10),  # Upper right
            (6, 16),   # Mid left
            (26, 16),  # Mid right
            (11, 22),  # Lower left
            (21, 22),  # Lower right
        ]
        
        # Falling apple (starts at position 0 - top center)
        self.falling_apple_start_pos = (16, 6)
        self.falling_apple_current_pos = [16, 6]
        self.falling_apple_start_time = 10  # Start falling after 10 seconds
        self.falling_apple_fall_duration = 3  # Takes 3 seconds to fall
        
        # Ground level
        self.ground_y = 44
        
    def draw_trunk(self):
        """Draw the tree trunk."""
        # Main trunk (wider and taller)
        for y in range(self.trunk_height):
            for x in range(self.trunk_width):
                pixel_x = self.trunk_x + x
                pixel_y = self.trunk_y - y
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    self.led.set_pixel(pixel_x, pixel_y, self.brown_trunk)
        
        # Branches (more realistic)
        # Left branch
        for i in range(8):
            pixel_x = self.trunk_x - 1 - i
            pixel_y = self.trunk_y - 10 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                self.led.set_pixel(pixel_x, pixel_y, self.brown_trunk)
        
        # Right branch
        for i in range(8):
            pixel_x = self.trunk_x + self.trunk_width + i
            pixel_y = self.trunk_y - 10 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                self.led.set_pixel(pixel_x, pixel_y, self.brown_trunk)
        
        # Additional smaller branches
        # Left small branch
        for i in range(4):
            pixel_x = self.trunk_x - 3 - i
            pixel_y = self.trunk_y - 15 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                self.led.set_pixel(pixel_x, pixel_y, self.brown_trunk)
        
        # Right small branch
        for i in range(4):
            pixel_x = self.trunk_x + self.trunk_width + 2 + i
            pixel_y = self.trunk_y - 15 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                self.led.set_pixel(pixel_x, pixel_y, self.brown_trunk)
    
    def draw_trunk_with_fade(self, fade_intensity):
        """Draw the tree trunk with fade intensity."""
        # Main trunk (wider and taller)
        for y in range(self.trunk_height):
            for x in range(self.trunk_width):
                pixel_x = self.trunk_x + x
                pixel_y = self.trunk_y - y
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    # Apply fade intensity to trunk color
                    faded_color = (
                        int(self.brown_trunk[0] * fade_intensity),
                        int(self.brown_trunk[1] * fade_intensity),
                        int(self.brown_trunk[2] * fade_intensity)
                    )
                    self.led.set_pixel(pixel_x, pixel_y, faded_color)
        
        # Branches (more realistic)
        # Left branch
        for i in range(8):
            pixel_x = self.trunk_x - 1 - i
            pixel_y = self.trunk_y - 10 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                faded_color = (
                    int(self.brown_trunk[0] * fade_intensity),
                    int(self.brown_trunk[1] * fade_intensity),
                    int(self.brown_trunk[2] * fade_intensity)
                )
                self.led.set_pixel(pixel_x, pixel_y, faded_color)
        
        # Right branch
        for i in range(8):
            pixel_x = self.trunk_x + self.trunk_width + i
            pixel_y = self.trunk_y - 10 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                faded_color = (
                    int(self.brown_trunk[0] * fade_intensity),
                    int(self.brown_trunk[1] * fade_intensity),
                    int(self.brown_trunk[2] * fade_intensity)
                )
                self.led.set_pixel(pixel_x, pixel_y, faded_color)
        
        # Additional smaller branches
        # Left small branch
        for i in range(4):
            pixel_x = self.trunk_x - 3 - i
            pixel_y = self.trunk_y - 15 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                faded_color = (
                    int(self.brown_trunk[0] * fade_intensity),
                    int(self.brown_trunk[1] * fade_intensity),
                    int(self.brown_trunk[2] * fade_intensity)
                )
                self.led.set_pixel(pixel_x, pixel_y, faded_color)
        
        # Right small branch
        for i in range(4):
            pixel_x = self.trunk_x + self.trunk_width + 2 + i
            pixel_y = self.trunk_y - 15 - i
            if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                faded_color = (
                    int(self.brown_trunk[0] * fade_intensity),
                    int(self.brown_trunk[1] * fade_intensity),
                    int(self.brown_trunk[2] * fade_intensity)
                )
                self.led.set_pixel(pixel_x, pixel_y, faded_color)
    
    def draw_leaves(self):
        """Draw the tree canopy/leaves."""
        # Main canopy area - larger and more realistic
        center_x = 16
        center_y = 18
        radius = 14
        
        for y in range(self.height):
            for x in range(self.width):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Draw leaves in circular area with some variation
                if distance <= radius and y >= 4 and y <= 30:
                    # Add some texture variation
                    if (x + y) % 3 == 0:  # Skip some pixels for texture
                        continue
                    self.led.set_pixel(x, y, self.green_leaves)
    
    def draw_leaves_with_fade(self, fade_intensity):
        """Draw the tree canopy/leaves with fade intensity."""
        # Main canopy area
        center_x = 16
        center_y = 20
        radius = 12
        
        for y in range(self.height):
            for x in range(self.width):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Draw leaves in circular area with fade intensity
                if distance <= radius and y >= 8 and y <= 32:
                    faded_color = (
                        int(self.green_leaves[0] * fade_intensity),
                        int(self.green_leaves[1] * fade_intensity),
                        int(self.green_leaves[2] * fade_intensity)
                    )
                    self.led.set_pixel(x, y, faded_color)
    
    def draw_apples(self, exclude_falling=False):
        """Draw all apples except the falling one if specified."""
        for i, (apple_x, apple_y) in enumerate(self.apple_positions):
            # Skip the falling apple (first apple) if exclude_falling is True
            if exclude_falling and i == 0:
                continue
                
            # Draw apple
            self.led.set_pixel(apple_x, apple_y, self.red_apple)
            # Draw stem
            if apple_y > 0:
                self.led.set_pixel(apple_x, apple_y - 1, self.apple_stem)
    
    def draw_apples_with_fade(self, exclude_falling=False, fade_intensity=1.0):
        """Draw all apples except the falling one if specified, with fade intensity."""
        for i, (apple_x, apple_y) in enumerate(self.apple_positions):
            # Skip the falling apple (first apple) if exclude_falling is True
            if exclude_falling and i == 0:
                continue
                
            # Draw apple with fade intensity
            faded_apple_color = (
                int(self.red_apple[0] * fade_intensity),
                int(self.red_apple[1] * fade_intensity),
                int(self.red_apple[2] * fade_intensity)
            )
            self.led.set_pixel(apple_x, apple_y, faded_apple_color)
            
            # Draw stem with fade intensity
            if apple_y > 0:
                faded_stem_color = (
                    int(self.apple_stem[0] * fade_intensity),
                    int(self.apple_stem[1] * fade_intensity),
                    int(self.apple_stem[2] * fade_intensity)
                )
                self.led.set_pixel(apple_x, apple_y - 1, faded_stem_color)
    
    def draw_falling_apple(self, progress):
        """Draw the falling apple with gravity effect."""
        # Calculate falling position with gravity
        fall_distance = progress * 20  # Total fall distance
        gravity_effect = progress * progress * 0.5  # Gravity acceleration
        
        current_x = self.falling_apple_start_pos[0]
        current_y = self.falling_apple_start_pos[1] + fall_distance + gravity_effect
        
        # Keep apple within bounds
        current_x = max(0, min(self.width - 1, int(current_x)))
        current_y = max(0, min(self.height - 1, int(current_y)))
        
        # Draw falling apple
        if 0 <= current_x < self.width and 0 <= current_y < self.height:
            self.led.set_pixel(current_x, current_y, self.red_apple)
            # Draw stem
            if current_y > 0:
                self.led.set_pixel(current_x, current_y - 1, self.apple_stem)
    
    def draw_falling_apple_with_fade(self, progress, fade_intensity):
        """Draw the falling apple with gravity effect and fade intensity."""
        # Calculate falling position with gravity
        fall_distance = progress * 20  # Total fall distance
        gravity_effect = progress * progress * 0.5  # Gravity acceleration
        
        current_x = self.falling_apple_start_pos[0]
        current_y = self.falling_apple_start_pos[1] + fall_distance + gravity_effect
        
        # Keep apple within bounds
        current_x = max(0, min(self.width - 1, int(current_x)))
        current_y = max(0, min(self.height - 1, int(current_y)))
        
        # Draw falling apple with fade intensity
        if 0 <= current_x < self.width and 0 <= current_y < self.height:
            faded_apple_color = (
                int(self.red_apple[0] * fade_intensity),
                int(self.red_apple[1] * fade_intensity),
                int(self.red_apple[2] * fade_intensity)
            )
            self.led.set_pixel(current_x, current_y, faded_apple_color)
            
            # Draw stem with fade intensity
            if current_y > 0:
                faded_stem_color = (
                    int(self.apple_stem[0] * fade_intensity),
                    int(self.apple_stem[1] * fade_intensity),
                    int(self.apple_stem[2] * fade_intensity)
                )
                self.led.set_pixel(current_x, current_y - 1, faded_stem_color)
    
    def draw_ground(self):
        """Draw brown soil ground."""
        for x in range(self.width):
            for y in range(self.ground_y, self.height):
                self.led.set_pixel(x, y, self.brown_soil)
    
    def run_animation(self):
        """Run the complete apple tree animation."""
        print("🌳 Starting Apple Tree Animation...")
        print(f"Duration: {self.duration} seconds")
        print(f"Apple will fall after {self.falling_apple_start_time} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < self.duration:
            elapsed = time.time() - start_time
            progress = elapsed / self.duration
            
            # Clear display
            self.led.clear()
            
            # Draw ground first (background)
            self.draw_ground()
            
            # Draw tree trunk
            self.draw_trunk()
            
            # Draw leaves
            self.draw_leaves()
            
            # Handle falling apple
            if elapsed >= self.falling_apple_start_time:
                # Apple is falling
                fall_progress = (elapsed - self.falling_apple_start_time) / self.falling_apple_fall_duration
                fall_progress = min(1.0, fall_progress)  # Clamp to 1.0
                
                # Draw all apples except the falling one
                self.draw_apples(exclude_falling=True)
                
                # Draw falling apple
                self.draw_falling_apple(fall_progress)
            else:
                # All apples are on the tree
                self.draw_apples(exclude_falling=False)
            
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

def main():
    """Main function to run the apple tree animation."""
    try:
        animation = AppleTreeAnimation()
        animation.run_animation()
    except KeyboardInterrupt:
        print("\n🌳 Animation interrupted by user")
    except Exception as e:
        print(f"❌ Error running animation: {e}")

if __name__ == "__main__":
    main()
