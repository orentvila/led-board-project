#!/usr/bin/env python3
"""
Whale Animation for LED Board
Converts Piskel animation file to LED display animation (15 seconds)
"""

import time
import json
import base64
import io
from PIL import Image
from led_controller_exact import LEDControllerExact
import config

class WhaleAnimation:
    def __init__(self, piskel_file_path):
        """Initialize the whale animation from Piskel file."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Load and parse Piskel file
        self.frames = self.load_piskel_frames(piskel_file_path)
        print(f"Loaded {len(self.frames)} frames from Piskel file")
    
    def load_piskel_frames(self, piskel_file_path):
        """Load frames from Piskel file."""
        with open(piskel_file_path, 'r') as f:
            piskel_data = json.load(f)
        
        # Extract layer data
        layer_data = json.loads(piskel_data['piskel']['layers'][0])
        chunk = layer_data['chunks'][0]
        
        # Get sprite sheet dimensions
        frame_count = layer_data['frameCount']
        frame_width = piskel_data['piskel']['width']  # 36
        frame_height = piskel_data['piskel']['height']  # 48
        
        # Decode base64 PNG sprite sheet
        base64_data = chunk['base64PNG'].split(',')[1]  # Remove data:image/png;base64, prefix
        image_data = base64.b64decode(base64_data)
        sprite_sheet = Image.open(io.BytesIO(image_data))
        
        # Extract individual frames
        # Layout indicates frames are stacked vertically: [[0],[1],[2],...,[11]]
        frames = []
        for i in range(frame_count):
            # Each frame is at y position i * frame_height
            y_start = i * frame_height
            y_end = y_start + frame_height
            
            # Crop frame from sprite sheet
            frame = sprite_sheet.crop((0, y_start, frame_width, y_end))
            
            # Convert to RGB if needed
            if frame.mode != 'RGB':
                frame = frame.convert('RGB')
            
            frames.append(frame)
        
        return frames
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def display_frame(self, frame_index):
        """Display a single frame on the LED display."""
        self.led.clear()
        
        frame = self.frames[frame_index]
        
        # Center the frame if it's wider than display (36x48 -> 32x48)
        # Crop or center the frame
        frame_width, frame_height = frame.size
        
        # Calculate offset to center horizontally if needed
        x_offset = 0
        if frame_width > self.width:
            x_offset = (frame_width - self.width) // 2
        
        # Display pixels
        for y in range(min(frame_height, self.height)):
            for x in range(min(frame_width, self.width)):
                # Get pixel color from frame
                pixel_x = x + x_offset
                if pixel_x < frame_width:
                    r, g, b = frame.getpixel((pixel_x, y))
                    self.safe_set_pixel(x, y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the whale animation for 15 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 15  # 15 seconds
        start_time = time.time()
        
        # Original animation: 12 frames at 2 fps = 6 seconds
        # For 15 seconds, we'll loop the animation 2.5 times
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
    
    # Default path to Piskel file
    piskel_file = r"c:\Users\Oren\Downloads\wale-20251119-202446.piskel"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        piskel_file = sys.argv[1]
    
    try:
        animation = WhaleAnimation(piskel_file)
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

