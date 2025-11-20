#!/usr/bin/env python3
"""
Bird Animation for LED Board
Loads bird animation frames (20 seconds duration)
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
        "name": "image",
        "description": "",
        "fps": 12,
        "height": 44,
        "width": 32,
        "layers": [
            "{\"name\":\"Layer 1\",\"opacity\":1,\"frameCount\":24,\"chunks\":[{\"layout\":[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]],\"base64PNG\":\"data:image/png;base64,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\"}]}",
            "{\"name\":\"Layer 2\",\"opacity\":1,\"frameCount\":24,\"chunks\":[{\"layout\":[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]],\"base64PNG\":\"data:image/png;base64,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\"}]}"
        ],
        "hiddenFrames": [""]
    }
}

class BirdAnimation:
    def __init__(self, piskel_file_path=None):
        """Initialize the bird animation from Piskel file or embedded data."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors specified by user
        self.blue_color = (66, 141, 213)  # #428DD5
        self.sun_color = (255, 202, 40)  # #ffca28
        self.cloud_color = (178, 178, 178)  # #b2b2b2
        self.bird_color = (1, 1, 1)  # #010101 (black)
        
        # Load frames from Piskel file or use embedded data
        if piskel_file_path and os.path.exists(piskel_file_path):
            self.frames = self.load_piskel_frames(piskel_file_path)
        else:
            # Use embedded data
            self.frames = self.load_piskel_frames(None)
        
        print(f"Loaded {len(self.frames)} frames")
    
    def load_piskel_frames(self, piskel_file_path=None):
        """Load frames from Piskel file format (supports multiple layers)."""
        if piskel_file_path:
            with open(piskel_file_path, 'r') as f:
                piskel_data = json.load(f)
        else:
            # Use embedded data
            piskel_data = PISKEL_DATA
        
        # Get sprite sheet dimensions
        frame_width = piskel_data['piskel']['width']
        frame_height = piskel_data['piskel']['height']
        
        # Process all layers
        all_frames = []
        num_layers = len(piskel_data['piskel']['layers'])
        
        for layer_idx in range(num_layers):
            # Extract layer data
            layer_data = json.loads(piskel_data['piskel']['layers'][layer_idx])
            chunk = layer_data['chunks'][0]
            
            # Get sprite sheet dimensions
            frame_count = layer_data['frameCount']
            
            # Decode base64 PNG sprite sheet
            base64_data = chunk['base64PNG'].split(',')[1]
            image_data = base64.b64decode(base64_data)
            sprite_sheet = Image.open(io.BytesIO(image_data))
            
            # Extract individual frames (assuming horizontal layout)
            sprite_width, sprite_height = sprite_sheet.size
            
            layer_frames = []
            for i in range(frame_count):
                x_start = i * frame_width
                x_end = x_start + frame_width
                
                frame = sprite_sheet.crop((x_start, 0, x_end, frame_height))
                
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                
                layer_frames.append(frame)
            
            all_frames.append(layer_frames)
        
        # Combine layers (if multiple layers exist)
        if len(all_frames) == 1:
            # Single layer - just convert to RGB
            frames = []
            for frame in all_frames[0]:
                if frame.mode != 'RGB':
                    frame = frame.convert('RGB')
                frames.append(frame)
            return frames
        else:
            # Multiple layers - composite them
            frames = []
            for i in range(len(all_frames[0])):
                # Start with first layer
                composite = all_frames[0][i].copy()
                
                # Composite remaining layers on top
                for layer_idx in range(1, len(all_frames)):
                    if i < len(all_frames[layer_idx]):
                        layer_frame = all_frames[layer_idx][i]
                        composite = Image.alpha_composite(composite, layer_frame)
                
                # Convert to RGB
                if composite.mode != 'RGB':
                    composite = composite.convert('RGB')
                
                frames.append(composite)
            
            return frames
    
    def load_c_array_frames(self, c_array_data):
        """Load frames from C array format (similar to whale animation).
        
        Args:
            c_array_data: List of lists, where each inner list is a frame's pixel data
                          Format: [[uint32_t ARGB values for frame 0], [frame 1], ...]
        """
        frames = []
        
        for frame_data in c_array_data:
            # Create image from pixel data
            img = Image.new('RGB', (32, 48))
            pixels = []
            
            for pixel_value in frame_data:
                # Convert ARGB to RGB
                a = (pixel_value >> 24) & 0xFF
                r = (pixel_value >> 16) & 0xFF
                g = (pixel_value >> 8) & 0xFF
                b = pixel_value & 0xFF
                
                # Apply alpha if needed
                if a < 255:
                    r = int(r * (a / 255))
                    g = int(g * (a / 255))
                    b = int(b * (a / 255))
                
                pixels.append((r, g, b))
            
            img.putdata(pixels)
            frames.append(img)
        
        return frames
    
    def replace_colors(self, r, g, b):
        """Replace colors based on the specified palette.
        
        Args:
            r, g, b: Original RGB values
            
        Returns:
            Tuple of (r, g, b) with replaced colors
        """
        # Bird black: #010101 (check first, as it's most specific)
        if r <= 20 and g <= 20 and b <= 20:
            return self.bird_color
        
        # Blue: #428DD5 (RGB: 66, 141, 213)
        # Check for blue colors (high blue component)
        if b > r and b > g and b > 100:
            return self.blue_color
        
        # Sun yellow: #ffca28 (RGB: 255, 202, 40)
        # Check for yellow colors (high red and green, low blue)
        if r > 200 and g > 150 and g < 250 and b < 100:
            return self.sun_color
        
        # Clouds grey: #b2b2b2 (RGB: 178, 178, 178)
        # Check for grey colors (similar RGB values, medium brightness)
        if abs(r - g) < 30 and abs(g - b) < 30 and 120 < r < 220:
            return self.cloud_color
        
        # Default: return original
        return (r, g, b)
    
    def safe_set_pixel(self, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.led.set_pixel(x, y, color)
    
    def display_frame(self, frame_index):
        """Display a single frame from the animation."""
        if frame_index >= len(self.frames):
            return
        
        self.led.clear()
        frame = self.frames[frame_index]
        frame_width, frame_height = frame.size
        
        # Center the frame on the display
        x_offset = (self.width - frame_width) // 2
        y_offset = (self.height - frame_height) // 2
        
        for y in range(min(frame_height, self.height)):
            for x in range(min(frame_width, self.width)):
                pixel_x = x + x_offset
                pixel_y = y + y_offset
                
                if 0 <= pixel_x < self.width and 0 <= pixel_y < self.height:
                    r, g, b = frame.getpixel((x, y))
                    r, g, b = self.replace_colors(r, g, b)
                    self.safe_set_pixel(pixel_x, pixel_y, (r, g, b))
        
        self.led.show()
    
    def run_animation(self, should_stop=None):
        """Run the bird animation for 20 seconds.
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        if not self.frames:
            print("Error: No frames loaded. Please provide animation data.")
            return
        
        duration = 20  # 20 seconds
        start_time = time.time()
        
        print("Starting bird animation...")
        print(f"Animation duration: {duration} seconds")
        print(f"Number of frames: {len(self.frames)}")
        
        # Calculate frame duration
        frame_duration = duration / len(self.frames)
        
        frame_index = 0
        while time.time() - start_time < duration:
            if should_stop and should_stop():
                print("Bird animation stopped by user")
                break
            
            # Display current frame
            self.display_frame(frame_index)
            
            # Wait for frame duration
            time.sleep(frame_duration)
            
            # Move to next frame
            frame_index = (frame_index + 1) % len(self.frames)
        
        print("Bird animation completed!")
        
        # Clear display
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run bird animation."""
    import os
    
    try:
        # Try to load from file if provided
        piskel_file = None
        if len(os.sys.argv) > 1:
            piskel_file = os.sys.argv[1]
        
        animation = BirdAnimation(piskel_file)
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

