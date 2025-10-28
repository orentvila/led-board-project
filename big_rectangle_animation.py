#!/usr/bin/env python3
"""
Big Rectangle Animation
Creates a large rectangle that slowly turns on with soft blue color #34ABE4
Duration: 20 seconds
"""

import time
import math
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from led_controller_exact import LEDControllerExact
import config

class BigRectangleAnimation:
    def __init__(self):
        """Initialize the rectangle animation."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48
        
        # Starting color #73C0E0 and ending color #157BB8
        self.start_color = (115, 192, 224)  # RGB values for #73C0E0
        self.end_color = (21, 123, 184)     # RGB values for #157BB8
        
        # Animation parameters
        self.duration = 20  # 20 seconds
        self.fade_steps = 200  # Number of fade steps for smooth transition
        
    def run_animation(self):
        """Run the big rectangle animation."""
        print("🔷 Starting Big Rectangle Animation...")
        print(f"Starting Color: #{self.start_color[0]:02X}{self.start_color[1]:02X}{self.start_color[2]:02X}")
        print(f"Ending Color: #{self.end_color[0]:02X}{self.end_color[1]:02X}{self.end_color[2]:02X}")
        print(f"Duration: {self.duration} seconds")
        
        start_time = time.time()
        
        # Calculate rectangle dimensions (big rectangle)
        # Leave some margin from edges
        margin_x = 2
        margin_y = 4
        rect_width = self.width - (2 * margin_x)  # 28 pixels wide
        rect_height = self.height - (2 * margin_y)  # 40 pixels tall
        
        # Rectangle position (centered)
        rect_x = margin_x
        rect_y = margin_y
        
        print(f"Rectangle size: {rect_width}x{rect_height}")
        print(f"Rectangle position: ({rect_x}, {rect_y})")
        
        while time.time() - start_time < self.duration:
            # Calculate progress (0 to 1)
            elapsed = time.time() - start_time
            progress = elapsed / self.duration
            
            # Calculate fade intensity using smooth easing function (ease-out cubic)
            # This provides a much smoother fade-in without flickering
            fade_intensity = 1.0 - (1.0 - progress) ** 3
            
            # Calculate color transition from start to end color
            current_color = (
                int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * progress),
                int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * progress),
                int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * progress)
            )
            
            # Clear display
            self.led.clear()
            
            # Draw the rectangle with current color and fade intensity
            for y in range(rect_height):
                for x in range(rect_width):
                    # Calculate final color with fade intensity
                    final_color = (
                        int(current_color[0] * fade_intensity),
                        int(current_color[1] * fade_intensity),
                        int(current_color[2] * fade_intensity)
                    )
                    
                    # Set pixel
                    pixel_x = rect_x + x
                    pixel_y = rect_y + y
                    
                    if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                        self.led.set_pixel(pixel_x, pixel_y, final_color)
            
            # Show the frame
            self.led.show()
            
            # Higher frame rate for smoother animation
            time.sleep(0.03)  # ~33 FPS for much smoother animation
        
        # Keep the rectangle fully lit for a moment at the end
        print("🔷 Rectangle fully lit, keeping for 2 seconds...")
        time.sleep(2)
        
        # Fade out slowly
        print("🔷 Fading out...")
        fade_out_duration = 3  # 3 seconds fade out
        fade_start = time.time()
        
        while time.time() - fade_start < fade_out_duration:
            elapsed_fade = time.time() - fade_start
            fade_progress = elapsed_fade / fade_out_duration
            
            # Calculate fade out intensity (1 to 0)
            fade_out_intensity = 1.0 - fade_progress
            
            # Use the final color for fade out
            final_color_for_fade = self.end_color
            
            # Clear display
            self.led.clear()
            
            # Draw the rectangle with fade out intensity
            for y in range(rect_height):
                for x in range(rect_width):
                    # Calculate final color with fade out intensity
                    final_color = (
                        int(final_color_for_fade[0] * fade_out_intensity),
                        int(final_color_for_fade[1] * fade_out_intensity),
                        int(final_color_for_fade[2] * fade_out_intensity)
                    )
                    
                    # Set pixel
                    pixel_x = rect_x + x
                    pixel_y = rect_y + y
                    
                    if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                        self.led.set_pixel(pixel_x, pixel_y, final_color)
            
            # Show the frame
            self.led.show()
            
            # Higher frame rate for smoother animation
            time.sleep(0.03)
        
        # Clear display completely
        self.led.clear()
        self.led.show()
        
        print("🔷 Big Rectangle Animation completed!")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main entry point for standalone execution."""
    try:
        animation = BigRectangleAnimation()
        animation.run_animation()
        animation.cleanup()
    except KeyboardInterrupt:
        print("\n🛑 Animation interrupted by user")
    except Exception as e:
        print(f"❌ Error running animation: {e}")
    finally:
        print("🔷 Animation finished")

if __name__ == "__main__":
    main()
