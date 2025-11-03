#!/usr/bin/env python3
"""
Balloon Animation for LED Board
Displays a colorful hot air balloon that flies upward
"""

import time
import math
from led_controller_exact import LEDControllerExact
import config

class BalloonAnimation:
    def __init__(self):
        """Initialize the balloon animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Balloon dimensions
        # Width_factor can reach 1.7 at middle, so balloon_width needs to be adjusted
        # To get max rendered width of 30: 30 / 1.7 ≈ 18
        self.balloon_width = 18  # Base width - renders to ~30 pixels at widest point
        self.balloon_height = 30  # Height of balloon envelope
        self.basket_height = 6  # Height of basket
        
        # Colors matching the image
        self.color_green = (150, 255, 150)  # Light green
        self.color_yellow = (255, 255, 100)  # Bright yellow
        self.color_pink = (255, 150, 200)  # Reddish-pink/fuchsia
        self.color_brown_dark = (100, 60, 40)  # Dark brown for transition/ropes
        self.color_basket = (200, 150, 100)  # Light brown for basket
        
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def get_balloon_color(self, x, center_x, y, top_y):
        """Get color for balloon pixel based on vertical panel position.
        
        Args:
            x: X coordinate
            center_x: Center X of balloon
            y: Y coordinate (relative to top_y)
            top_y: Top Y of balloon
        """
        # Calculate relative position from center
        relative_x = x - center_x
        
        # Vertical stripes: green, yellow, pink (repeat)
        stripe_width = self.balloon_width // 3  # About 8 pixels per stripe
        stripe_index = (relative_x + self.balloon_width // 2) // stripe_width
        
        if stripe_index % 3 == 0:
            return self.color_green
        elif stripe_index % 3 == 1:
            return self.color_yellow
        else:
            return self.color_pink
    
    def is_inside_balloon_envelope(self, x, y, center_x, top_y):
        """Check if a point is inside the balloon envelope (circular shape).
        
        Args:
            x, y: Point coordinates
            center_x: X coordinate of balloon center
            top_y: Y coordinate of balloon top
        """
        # Balloon envelope is a perfect circle
        # Radius determines the size - use half of balloon_height for radius
        radius = self.balloon_height // 2  # 15 pixels radius
        
        # Circle center is at (center_x, top_y + radius)
        circle_center_y = top_y + radius
        
        # Check if point is inside the circle using circle equation:
        # (x - center_x)^2 + (y - circle_center_y)^2 <= radius^2
        dx = x - center_x
        dy = y - circle_center_y
        distance_squared = dx * dx + dy * dy
        
        return distance_squared <= radius * radius
    
    def is_inside_basket_area(self, x, y, center_x, envelope_bottom):
        """Check if a point is inside the basket/transition area.
        
        Args:
            x, y: Point coordinates
            center_x: X coordinate of balloon center
            envelope_bottom: Y coordinate where envelope ends
        """
        transition_height = 4
        basket_top = envelope_bottom + transition_height
        basket_bottom = basket_top + self.basket_height
        
        if y < envelope_bottom or y >= basket_bottom:
            return False
        
        # Transition piece: narrows from envelope to basket
        if y < basket_top:
            # Transition area - dark brown
            relative_y = (y - envelope_bottom) / transition_height
            width = int(self.balloon_width * 0.4 * (1 - relative_y * 0.5))
        else:
            # Basket area - wider than transition
            width = int(self.balloon_width * 0.35)
        
        left_edge = center_x - width // 2
        right_edge = center_x + width // 2
        
        return left_edge <= x <= right_edge
    
    def draw_balloon(self, brightness=1.0, y_offset=0):
        """Draw the balloon - colorful striped envelope, basket, with y_offset for animation.
        
        Args:
            brightness: Brightness multiplier (0.0 to 1.0)
            y_offset: Vertical offset for flying animation
        """
        self.led.clear()  # Black background
        
        # Calculate balloon position
        center_x = self.width // 2
        top_y = y_offset
        envelope_bottom = top_y + self.balloon_height
        
        # Draw balloon - envelope first
        for y in range(self.height):
            for x in range(self.width):
                if self.is_inside_balloon_envelope(x, y, center_x, top_y):
                    # Get color based on vertical stripe position
                    color = self.get_balloon_color(x, center_x, y, top_y)
                    
                    # Apply brightness
                    r = int(color[0] * brightness)
                    g = int(color[1] * brightness)
                    b = int(color[2] * brightness)
                    self.safe_set_pixel(x, y, (r, g, b))
                
                elif self.is_inside_basket_area(x, y, center_x, envelope_bottom):
                    # Determine if transition or basket
                    transition_height = 4
                    basket_top = envelope_bottom + transition_height
                    
                    if y < basket_top:
                        # Transition piece - dark brown
                        color = self.color_brown_dark
                    else:
                        # Basket - light brown
                        color = self.color_basket
                    
                    # Apply brightness
                    r = int(color[0] * brightness)
                    g = int(color[1] * brightness)
                    b = int(color[2] * brightness)
                    self.safe_set_pixel(x, y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the balloon animation flying upward.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 20  # 20 seconds
        start_time = time.time()
        frame = 0
        
        print("🎈 Starting balloon animation...")
        
        # Animation: balloon starts at bottom, flies up once over 20 seconds
        # Start from completely below the screen (original animals button version)
        total_balloon_height = self.balloon_height + 4 + self.basket_height  # envelope + transition + basket = 40 pixels
        # Start completely below screen - balloon top starts well below visible area
        start_y_offset = self.height + total_balloon_height  # Start completely below screen
        end_y_offset = -total_balloon_height  # End above screen
        total_distance = start_y_offset - end_y_offset
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Calculate y_offset for flying up - single cycle over full duration
            # Progress from 0.0 (start) to 1.0 (end)
            progress = min(1.0, elapsed / duration)
            
            # Linear interpolation from start to end
            y_offset = int(start_y_offset - progress * total_distance)
            
            # Subtle brightness pulse
            pulse = 0.9 + 0.1 * (1.0 + math.sin(elapsed * 1.5)) / 2.0  # 0.9 to 1.0
            
            # Draw the balloon first, then check stop flag
            self.draw_balloon(brightness=pulse, y_offset=y_offset)
            frame += 1
            
            # Check stop flag AFTER drawing, with a small sleep
            if should_stop and should_stop():
                print("🎈 Balloon animation stopped by user")
                break
            
            time.sleep(0.05)  # 20 FPS for smoother animation
        
        print("🎈 Balloon animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run balloon animation."""
    try:
        animation = BalloonAnimation()
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()

