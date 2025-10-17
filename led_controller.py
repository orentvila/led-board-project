import time
import numpy as np
import sys
import config

# Use mock modules on Windows, real modules on Raspberry Pi
if sys.platform.startswith('win'):
    from mock_rpi import WS281x
    PixelStrip = WS281x
    Color = lambda r, g, b: (r, g, b)
    print("Using mock Raspberry Pi modules for Windows development")
else:
    try:
        from rpi_ws281x import PixelStrip, Color
    except ImportError:
        print("Warning: rpi_ws281x not found, using mock modules")
        from mock_rpi import WS281x
        PixelStrip = WS281x
        Color = lambda r, g, b: (r, g, b)

class LEDController:
    def __init__(self):
        """Initialize the LED controller for the 40x32 display."""
        # Convert brightness to uint8 (0-255)
        brightness_uint8 = int(config.BRIGHTNESS * 255)
        
        self.strip = PixelStrip(
            config.TOTAL_LEDS,
            config.LED_PIN,
            config.LED_FREQ_HZ,
            config.LED_DMA,
            config.LED_INVERT,
            brightness_uint8,
            config.LED_CHANNEL
        )
        self.strip.begin()
        
        # Create display matrix (40x32)
        self.display_matrix = np.zeros((config.TOTAL_HEIGHT, config.TOTAL_WIDTH, 3), dtype=np.uint8)
        
        # Clear display on startup
        self.clear()
        self.show()
    
    def clear(self):
        """Clear the entire display."""
        self.display_matrix.fill(0)
        for i in range(config.TOTAL_LEDS):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
    
    def set_pixel(self, x, y, color):
        """Set a single pixel at position (x, y) with the given color."""
        if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
            self.display_matrix[y, x] = color
            led_index = self._get_led_index(x, y)
            # Use setPixelColorRGB method which is more reliable
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            self.strip.setPixelColorRGB(led_index, r, g, b)
    
    def set_panel_pixel(self, panel, x, y, color):
        """Set a pixel within a specific panel."""
        if 0 <= panel < config.PANELS_COUNT:
            global_x = panel * config.PANEL_WIDTH + x
            self.set_pixel(global_x, y, color)
    
    def fill_panel(self, panel, color):
        """Fill an entire panel with a color."""
        if 0 <= panel < config.PANELS_COUNT:
            start_x = panel * config.PANEL_WIDTH
            end_x = start_x + config.PANEL_WIDTH
            for y in range(config.TOTAL_HEIGHT):
                for x in range(start_x, end_x):
                    self.set_pixel(x, y, color)
    
    def fill_display(self, color):
        """Fill the entire display with a color."""
        # Fill the display matrix with the color
        for y in range(config.TOTAL_HEIGHT):
            for x in range(config.TOTAL_WIDTH):
                self.display_matrix[y, x] = color
        
        # Update the physical LEDs
        for i in range(config.TOTAL_LEDS):
            # Use setPixelColorRGB method which is more reliable
            r, g, b = int(color[0]), int(color[1]), int(color[2])
            self.strip.setPixelColorRGB(i, r, g, b)
    
    def draw_rectangle(self, x1, y1, x2, y2, color, fill=False):
        """Draw a rectangle from (x1, y1) to (x2, y2)."""
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if fill or (x == x1 or x == x2 or y == y1 or y == y2):
                    self.set_pixel(x, y, color)
    
    def draw_line(self, x1, y1, x2, y2, color):
        """Draw a line from (x1, y1) to (x2, y2) using Bresenham's algorithm."""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        n = 1 + dx + dy
        x_inc = 1 if x2 > x1 else -1
        y_inc = 1 if y2 > y1 else -1
        error = dx - dy
        dx *= 2
        dy *= 2
        
        for _ in range(n):
            self.set_pixel(x, y, color)
            if x == x2 and y == y2:
                break
            if error > 0:
                x += x_inc
                error -= dy
            else:
                y += y_inc
                error += dx
    
    def draw_text(self, text, x, y, color, font_size=1):
        """Draw text at position (x, y). Simple 5x7 font implementation."""
        # Simple 5x7 font (basic implementation)
        font = {
            'A': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1]],
            'B': [[1,1,1,1,0], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,0,1], [1,1,1,1,0]],
            'C': [[0,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [0,1,1,1,1]],
            'D': [[1,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,0]],
            'E': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,0,0], [1,0,0,0,0], [1,1,1,1,1]],
            'F': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,0,0], [1,0,0,0,0], [1,0,0,0,0]],
            'G': [[0,1,1,1,1], [1,0,0,0,0], [1,0,1,1,1], [1,0,0,0,1], [0,1,1,1,0]],
            'H': [[1,0,0,0,1], [1,0,0,0,1], [1,1,1,1,1], [1,0,0,0,1], [1,0,0,0,1]],
            'I': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [1,1,1,1,1]],
            'J': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [1,0,1,0,0], [0,1,0,0,0]],
            'K': [[1,0,0,0,1], [1,0,0,1,0], [1,1,1,0,0], [1,0,0,1,0], [1,0,0,0,1]],
            'L': [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,1,1,1,1]],
            'M': [[1,0,0,0,1], [1,1,0,1,1], [1,0,1,0,1], [1,0,0,0,1], [1,0,0,0,1]],
            'N': [[1,0,0,0,1], [1,1,0,0,1], [1,0,1,0,1], [1,0,0,1,1], [1,0,0,0,1]],
            'O': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
            'P': [[1,1,1,1,0], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0]],
            'Q': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,1,0], [0,1,1,0,1]],
            'R': [[1,1,1,1,0], [1,0,0,0,1], [1,1,1,1,0], [1,0,0,1,0], [1,0,0,0,1]],
            'S': [[0,1,1,1,1], [1,0,0,0,0], [0,1,1,1,0], [0,0,0,0,1], [1,1,1,1,0]],
            'T': [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0]],
            'U': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
            'V': [[1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0]],
            'W': [[1,0,0,0,1], [1,0,0,0,1], [1,0,1,0,1], [1,1,0,1,1], [1,0,0,0,1]],
            'X': [[1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,1,0,1,0], [1,0,0,0,1]],
            'Y': [[1,0,0,0,1], [0,1,0,1,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0]],
            'Z': [[1,1,1,1,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,1,1,1,1]],
            ' ': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
        }
        
        char_width = 6 * font_size
        for i, char in enumerate(text.upper()):
            if char in font:
                char_x = x + i * char_width
                for row in range(5):
                    for col in range(5):
                        if font[char][row][col]:
                            for dy in range(font_size):
                                for dx in range(font_size):
                                    self.set_pixel(char_x + col * font_size + dx, 
                                                 y + row * font_size + dy, color)
    
    def _get_led_index(self, x, y):
        """Convert (x, y) coordinates to LED strip index."""
        # LED mapping: Right to left, serpentine vertical within 8-row bands
        # X=0 is rightmost, X=31 is leftmost
        # Y=0 is bottom, Y=39 is top
        # Serpentine pattern: even X columns go up, odd X columns go down
        
        # Calculate which 8-row band we're in (0-4)
        band = y // 8
        
        # Calculate Y position within the current 8-row band
        y_in_band = y % 8
        
        # Calculate X position (0 = rightmost, 31 = leftmost)
        # But we need to invert X since our coordinate system has X=0 as leftmost
        x_led = config.TOTAL_WIDTH - 1 - x  # Convert our X to LED X
        
        # Calculate base index for this band
        base_index = band * (config.TOTAL_WIDTH * 8)
        
        # Calculate index within the band
        if x_led % 2 == 0:
            # Even X columns: scan upward (0→7)
            y_offset = y_in_band
        else:
            # Odd X columns: scan downward (7→0)
            y_offset = 7 - y_in_band
        
        # Calculate final index
        band_index = x_led * 8 + y_offset
        return base_index + band_index
    
    def show(self):
        """Update the physical LED display."""
        self.strip.show()
    
    def set_brightness(self, brightness):
        """Set the brightness of all LEDs (0.0 to 1.0)."""
        # Ensure brightness is within valid range and convert to uint8
        brightness = max(0.0, min(1.0, brightness))
        brightness_uint8 = int(brightness * 255)
        self.strip.setBrightness(brightness_uint8)
    
    def cleanup(self):
        """Clean up resources."""
        try:
            self.clear()
            self.show()
            time.sleep(0.1)
            # Properly cleanup the strip to prevent memory leaks
            if hasattr(self, 'strip'):
                del self.strip
        except Exception as e:
            print(f"Cleanup warning: {e}") 