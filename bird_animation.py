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
        
        # Load frames
        self.frames = self.load_frames(piskel_file_path)
        
        if not self.frames:
            print("Warning: No frames loaded. Please provide animation data.")
            print(f"Tried to load from: {piskel_file_path or os.path.join(os.path.expanduser('~'), 'Downloads', 'bird.piskel')}")
        
        print(f"Loaded {len(self.frames)} frames")
    
    def load_frames(self, piskel_file_path=None):
        """Load frames from Piskel file or embedded data.
        
        Args:
            piskel_file_path: Path to Piskel file (optional)
            
        Returns:
            List of PIL Image frames
        """
        # Try default path if not provided
        if not piskel_file_path:
            default_path = os.path.join(os.path.expanduser("~"), "Downloads", "bird.piskel")
            if os.path.exists(default_path):
                piskel_file_path = default_path
        
        # If file path provided, try to load it
        if piskel_file_path and os.path.exists(piskel_file_path):
            return self.load_piskel_frames(piskel_file_path)
        
        # Otherwise, return empty - user needs to provide data
        return []
    
    def load_piskel_frames(self, piskel_file_path):
        """Load frames from Piskel file format (supports multiple layers)."""
        with open(piskel_file_path, 'r') as f:
            piskel_data = json.load(f)
        
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

