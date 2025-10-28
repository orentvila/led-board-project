#!/usr/bin/env python3
"""
Butterfly Animation
A beautiful pink butterfly with slowly flapping wings
"""

import time
import math
from led_controller_exact import LEDControllerExact

class ButterflyAnimation:
    def __init__(self):
        """Initialize the butterfly animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        self.duration = 20  # 20 seconds total
        
        # Colors from the image
        self.pink_wings = (240, 128, 128)  # #F08080 - light coral pink
        self.brown_body = (180, 100, 80)   # Brownish-pink body
        self.black_antennae = (50, 50, 50)  # Dark antennae
        
        # Butterfly position (centered)
        self.center_x = 16
        self.center_y = 24
        
        # Wing dimensions - much bigger to almost reach screen edges
        self.upper_wing_radius = 14  # Almost half the screen width
        self.lower_wing_radius = 10  # Slightly smaller lower wings
        
    def draw_butterfly(self, wing_angle):
        """Draw the butterfly with animated wings."""
        # Draw body (vertical oval)
        for dy in range(-6, 7):
            for dx in range(-1, 2):
                x = self.center_x + dx
                y = self.center_y + dy
                if 0 <= x < self.width and 0 <= y < self.height:
                    # Make body slightly oval
                    if abs(dx) <= 1 and abs(dy) <= 6:
                        self.led.set_pixel(x, y, self.brown_body)
        
        # Draw antennae
        antennae_length = 4
        for i in range(antennae_length):
            # Left antenna
            antenna_x = self.center_x - 1 - i
            antenna_y = self.center_y - 6 - i
            if 0 <= antenna_x < self.width and 0 <= antenna_y < self.height:
                self.led.set_pixel(antenna_x, antenna_y, self.black_antennae)
            
            # Right antenna
            antenna_x = self.center_x + 1 + i
            antenna_y = self.center_y - 6 - i
            if 0 <= antenna_x < self.width and 0 <= antenna_y < self.height:
                self.led.set_pixel(antenna_x, antenna_y, self.black_antennae)
        
        # Draw wings with flapping animation
        self.draw_wings(wing_angle)
    
    def draw_wings(self, wing_angle):
        """Draw the butterfly wings with flapping animation."""
        # Calculate wing positions based on angle
        # wing_angle: 0 = fully open, 1 = fully closed
        
        # Upper wings (larger) - positioned further apart for bigger wings
        self.draw_wing_segment(
            self.center_x - 3, self.center_y - 3,  # Left upper wing center
            self.upper_wing_radius, wing_angle, -1  # Left side
        )
        self.draw_wing_segment(
            self.center_x + 3, self.center_y - 3,  # Right upper wing center
            self.upper_wing_radius, wing_angle, 1   # Right side
        )
        
        # Lower wings (smaller) - positioned further apart for bigger wings
        self.draw_wing_segment(
            self.center_x - 2, self.center_y + 3,  # Left lower wing center
            self.lower_wing_radius, wing_angle * 0.8, -1  # Left side
        )
        self.draw_wing_segment(
            self.center_x + 2, self.center_y + 3,  # Right lower wing center
            self.lower_wing_radius, wing_angle * 0.8, 1   # Right side
        )
    
    def draw_wing_segment(self, center_x, center_y, radius, wing_angle, side):
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
                    if 0 <= x < self.width and 0 <= y < self.height:
                        # Add some wing texture variation
                        if (x + y) % 2 == 0:  # Skip some pixels for texture
                            continue
                        self.led.set_pixel(x, y, self.pink_wings)
    
    def run_animation(self):
        """Run the complete butterfly animation."""
        print("🦋 Starting Butterfly Animation...")
        print(f"Duration: {self.duration} seconds")
        print("Wings will flap slowly and gracefully")
        
        start_time = time.time()
        
        while time.time() - start_time < self.duration:
            elapsed = time.time() - start_time
            
            # Clear display
            self.led.clear()
            
            # Calculate wing flapping angle (slow, gentle flapping)
            # Use sine wave for smooth, natural wing movement
            flap_frequency = 0.8  # Flaps per second (slow)
            wing_angle = abs(math.sin(elapsed * flap_frequency * 2 * math.pi))
            
            # Draw butterfly
            self.draw_butterfly(wing_angle)
            
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

def main():
    """Main function to run the butterfly animation."""
    try:
        animation = ButterflyAnimation()
        animation.run_animation()
    except KeyboardInterrupt:
        print("\n🦋 Animation interrupted by user")
    except Exception as e:
        print(f"❌ Error running animation: {e}")

if __name__ == "__main__":
    main()
