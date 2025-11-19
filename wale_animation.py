#!/usr/bin/env python3
"""
Whale Animation for LED Board
Loads whale animation frames from C file format (15 seconds)
"""

import time
import re
from led_controller_exact import LEDControllerExact
import config

# Frame dimensions
FRAME_WIDTH = 36
FRAME_HEIGHT = 48
FRAME_COUNT = 12

class WhaleAnimation:
    def __init__(self, c_file_path=None):
        """Initialize the whale animation from C file."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Load frames from C file
        if c_file_path:
            self.frames = self.load_frames_from_c_file(c_file_path)
        else:
            # Use embedded data (will be loaded from embedded C data)
            self.frames = self.load_embedded_frames()
        
        print(f"Loaded {len(self.frames)} frames")
    
    def argb_to_rgb(self, argb_value):
        """Convert ARGB uint32_t value to RGB tuple."""
        # ARGB format: 0xAARRGGBB
        r = (argb_value >> 16) & 0xFF
        g = (argb_value >> 8) & 0xFF
        b = argb_value & 0xFF
        return (r, g, b)
    
    def parse_c_file(self, file_path):
        """Parse C file and extract pixel data."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the array data between { and }
        # Match pattern: 0x[0-9a-fA-F]+
        hex_values = re.findall(r'0x[0-9a-fA-F]+', content)
        
        # Convert hex strings to integers
        pixels = [int(hex_val, 16) for hex_val in hex_values]
        
        # Group into frames (each frame has FRAME_WIDTH * FRAME_HEIGHT pixels)
        frames = []
        pixels_per_frame = FRAME_WIDTH * FRAME_HEIGHT
        
        for frame_idx in range(FRAME_COUNT):
            start_idx = frame_idx * pixels_per_frame
            end_idx = start_idx + pixels_per_frame
            frame_pixels = pixels[start_idx:end_idx]
            
            # Convert to 2D array (y, x) and convert ARGB to RGB
            frame = []
            for y in range(FRAME_HEIGHT):
                row = []
                for x in range(FRAME_WIDTH):
                    pixel_idx = y * FRAME_WIDTH + x
                    argb = frame_pixels[pixel_idx]
                    rgb = self.argb_to_rgb(argb)
                    row.append(rgb)
                frame.append(row)
            
            frames.append(frame)
        
        return frames
    
    def load_frames_from_c_file(self, c_file_path):
        """Load frames from C file."""
        return self.parse_c_file(c_file_path)
    
    def load_embedded_frames(self):
        """Load frames from embedded C data."""
        # For now, return empty - will be populated if needed
        # In production, you could embed the parsed data here
        raise ValueError("Please provide C file path or use embedded data")
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def display_frame(self, frame_index):
        """Display a single frame on the LED display."""
        self.led.clear()
        
        frame = self.frames[frame_index]
        
        # Center the frame if it's wider than display (36x48 -> 32x48)
        x_offset = (FRAME_WIDTH - self.width) // 2
        
        # Display pixels
        for y in range(min(FRAME_HEIGHT, self.height)):
            for x in range(min(FRAME_WIDTH, self.width)):
                # Get pixel color from frame
                pixel_x = x + x_offset
                if pixel_x < FRAME_WIDTH:
                    r, g, b = frame[y][pixel_x]
                    self.safe_set_pixel(x, y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the whale animation for 15 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 15  # 15 seconds
        start_time = time.time()
        
        # Frame duration: 15 seconds / 12 frames = 1.25 seconds per frame
        frame_duration = duration / len(self.frames)
        
        print("Starting whale animation...")
        print(f"Animation duration: {duration} seconds")
        print(f"Frame count: {len(self.frames)}")
        print(f"Frame duration: {frame_duration:.2f} seconds")
        
        frame_index = 0
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("Whale animation stopped by user")
                break
            
            # Display current frame
            self.display_frame(frame_index)
            
            # Wait for frame duration
            time.sleep(frame_duration)
            
            # Move to next frame (loop)
            frame_index = (frame_index + 1) % len(self.frames)
        
        print("Whale animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run whale animation."""
    import sys
    import os
    
    # Default path to C file (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    c_file = os.path.join(script_dir, "wale.c")
    
    # Allow override via command line or check Downloads folder
    if len(sys.argv) > 1:
        c_file = sys.argv[1]
    elif not os.path.exists(c_file):
        # Try Downloads folder (Windows path)
        downloads_c_file = r"c:\Users\Oren\Downloads\wale.c"
        if os.path.exists(downloads_c_file):
            c_file = downloads_c_file
        else:
            print(f"Error: C file not found at {c_file}")
            print("Usage: python wale_animation.py [path_to_wale.c]")
            return
    
    try:
        animation = WhaleAnimation(c_file)
        animation.run_animation()
        animation.cleanup()
        
    except KeyboardInterrupt:
        print("\nAnimation interrupted by user")
        if 'animation' in locals():
            animation.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animation' in locals():
            animation.cleanup()

if __name__ == "__main__":
    main()
