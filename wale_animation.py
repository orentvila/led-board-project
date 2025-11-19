#!/usr/bin/env python3
"""
Whale Animation for LED Board
Loads whale animation frames from Piskel file format (12 seconds, 24 frames total)
"""

import time
import json
import base64
import io
import os
from PIL import Image
from led_controller_exact import LEDControllerExact
import config

# Embedded Piskel data
PISKEL_DATA = {
    "modelVersion": 2,
    "piskel": {
        "name": "wale",
        "description": "",
        "fps": 2,
        "height": 48,
        "width": 36,
        "layers": [
            "{\"name\":\"Layer 1\",\"opacity\":1,\"frameCount\":12,\"chunks\":[{\"layout\":[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11]],\"base64PNG\":\"data:image/png;base64,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\"}]}"
        ],
        "hiddenFrames": [""]
    }
}

class WhaleAnimation:
    def __init__(self, piskel_file_path=None):
        """Initialize the whale animation from Piskel file or embedded data."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Load frames from Piskel file or use embedded data
        if piskel_file_path and os.path.exists(piskel_file_path):
            self.frames = self.load_piskel_frames(piskel_file_path)
        else:
            # Use embedded data
            self.frames = self.load_piskel_frames(None)
        
        print(f"Loaded {len(self.frames)} frames from Piskel data")
    
    def load_piskel_frames(self, piskel_file_path=None):
        """Load frames from Piskel file or embedded data."""
        if piskel_file_path:
            # Load from file if provided and exists
            with open(piskel_file_path, 'r') as f:
                piskel_data = json.load(f)
        else:
            # Use embedded data
            piskel_data = PISKEL_DATA
        
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
        # Frames are arranged horizontally in the sprite sheet
        frames = []
        sprite_width, sprite_height = sprite_sheet.size
        
        for i in range(frame_count):
            # Each frame is at x position i * frame_width
            x_start = i * frame_width
            x_end = x_start + frame_width
            
            # Crop frame from sprite sheet (horizontal layout)
            frame = sprite_sheet.crop((x_start, 0, x_end, frame_height))
            
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
        """Run the whale animation for 12 seconds (24 frames total - each frame shown twice).
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        duration = 12  # 12 seconds
        start_time = time.time()
        
        # Display each frame twice to get 24 frames total
        # Frame duration: 12 seconds / 24 frames = 0.5 seconds per frame
        total_frames = len(self.frames) * 2
        frame_duration = duration / total_frames
        
        print("Starting whale animation...")
        print(f"Animation duration: {duration} seconds")
        print(f"Original frame count: {len(self.frames)}")
        print(f"Total frames (each shown twice): {total_frames}")
        print(f"Frame duration: {frame_duration:.2f} seconds")
        
        # Create a sequence where each frame appears twice
        frame_sequence = []
        for i in range(len(self.frames)):
            frame_sequence.append(i)
            frame_sequence.append(i)  # Add each frame twice
        
        frame_sequence_index = 0
        
        while time.time() - start_time < duration:
            # Check stop flag
            if should_stop and should_stop():
                print("Whale animation stopped by user")
                break
            
            # Get the frame index from sequence
            frame_index = frame_sequence[frame_sequence_index]
            
            # Display current frame
            self.display_frame(frame_index)
            
            # Debug output every few frames
            if frame_sequence_index % 6 == 0:
                print(f"Displaying frame {frame_index} (sequence index {frame_sequence_index})")
            
            # Wait for frame duration
            time.sleep(frame_duration)
            
            # Move to next frame in sequence (loop)
            frame_sequence_index = (frame_sequence_index + 1) % len(frame_sequence)
        
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
    
    # Default path to Piskel file (optional - uses embedded data if not found)
    piskel_file = None
    
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
