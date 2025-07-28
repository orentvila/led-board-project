#!/usr/bin/env python3
"""
Script to prepare code for Raspberry Pi deployment
Reverts mock module changes and restores original imports
"""

import os
import shutil
import sys

def backup_file(filename):
    """Create a backup of the original file."""
    if os.path.exists(filename):
        backup_name = f"{filename}.backup"
        shutil.copy2(filename, backup_name)
        print(f"✓ Backed up {filename} to {backup_name}")

def restore_led_controller():
    """Restore led_controller.py to use real Raspberry Pi modules."""
    content = '''import time
import numpy as np
from rpi_ws281x import PixelStrip, Color
import config

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
            self.strip.setPixelColor(i, Color(0, 0, 0))
    
    def set_pixel(self, x, y, color):
        """Set a single pixel at position (x, y) with the given color."""
        if 0 <= x < config.TOTAL_WIDTH and 0 <= y < config.TOTAL_HEIGHT:
            self.display_matrix[y, x] = color
            led_index = self._get_led_index(x, y)
            self.strip.setPixelColor(led_index, Color(*color))
    
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
        self.display_matrix.fill(color)
        for i in range(config.TOTAL_LEDS):
            self.strip.setPixelColor(i, Color(*color))
    
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
            'E': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,0], [1,1,1,1,1]],
            'F': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,0], [1,0,0,0,0]],
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
            ' ': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]],
            '!': [[0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,0,0,0], [0,0,1,0,0]],
            '?': [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,1,0], [0,0,0,0,0], [0,0,1,0,0]],
            '.': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0]],
            ',': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,1,0,0], [0,1,0,0,0]],
            '-': [[0,0,0,0,0], [0,0,0,0,0], [1,1,1,1,1], [0,0,0,0,0], [0,0,0,0,0]],
            '_': [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [1,1,1,1,1]],
            '0': [[0,1,1,1,0], [1,0,0,0,1], [1,0,0,0,1], [1,0,0,0,1], [0,1,1,1,0]],
            '1': [[0,0,1,0,0], [0,1,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,1,1,1,0]],
            '2': [[0,1,1,1,0], [1,0,0,0,1], [0,0,0,1,0], [0,1,0,0,0], [1,1,1,1,1]],
            '3': [[1,1,1,1,0], [0,0,0,0,1], [0,1,1,1,0], [0,0,0,0,1], [1,1,1,1,0]],
            '4': [[0,0,0,1,0], [0,0,1,1,0], [0,1,0,1,0], [1,1,1,1,1], [0,0,0,1,0]],
            '5': [[1,1,1,1,1], [1,0,0,0,0], [1,1,1,1,0], [0,0,0,0,1], [1,1,1,1,0]],
            '6': [[0,1,1,1,0], [1,0,0,0,0], [1,1,1,1,0], [1,0,0,0,1], [0,1,1,1,0]],
            '7': [[1,1,1,1,1], [0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0]],
            '8': [[0,1,1,1,0], [1,0,0,0,1], [0,1,1,1,0], [1,0,0,0,1], [0,1,1,1,0]],
            '9': [[0,1,1,1,0], [1,0,0,0,1], [0,1,1,1,1], [0,0,0,0,1], [0,1,1,1,0]]
        }
        
        char_width = 6
        char_height = 7
        
        for i, char in enumerate(text.upper()):
            if char in font:
                char_x = x + i * char_width
                if char_x + 5 < config.TOTAL_WIDTH:
                    for row in range(min(char_height, config.TOTAL_HEIGHT - y)):
                        for col in range(5):
                            if font[char][row][col]:
                                self.set_pixel(char_x + col, y + row, color)
    
    def _get_led_index(self, x, y):
        """Convert (x, y) coordinates to LED strip index."""
        # Assuming serpentine pattern: left to right, then right to left
        if y % 2 == 0:
            return y * config.TOTAL_WIDTH + x
        else:
            return y * config.TOTAL_WIDTH + (config.TOTAL_WIDTH - 1 - x)
    
    def show(self):
        """Update the LED display."""
        self.strip.show()
    
    def set_brightness(self, brightness):
        """Set the brightness of all LEDs."""
        brightness_uint8 = int(brightness * 255)
        self.strip.setBrightness(brightness_uint8)
    
    def cleanup(self):
        """Clean up resources."""
        self.strip.clear()
        self.strip.show()
'''
    
    with open('led_controller.py', 'w') as f:
        f.write(content)
    print("✓ Restored led_controller.py for Raspberry Pi")

def restore_button_controller():
    """Restore button_controller.py to use real Raspberry Pi GPIO."""
    content = '''import RPi.GPIO as GPIO
import time
import threading
import config

class ButtonController:
    def __init__(self):
        """Initialize button controller for 4 buttons."""
        self.buttons = {}
        self.button_callbacks = {}
        self.running = False
        self.button_thread = None
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Initialize buttons
        for i, pin in enumerate(config.BUTTON_PINS):
            self.buttons[i] = {
                'pin': pin,
                'state': False,
                'last_press': 0
            }
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def register_callback(self, button_id, callback):
        """Register a callback function for a button press."""
        if 0 <= button_id < len(config.BUTTON_PINS):
            self.button_callbacks[button_id] = callback
    
    def start_monitoring(self):
        """Start monitoring button presses in a separate thread."""
        if not self.running:
            self.running = True
            self.button_thread = threading.Thread(target=self._monitor_buttons)
            self.button_thread.daemon = True
            self.button_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring button presses."""
        self.running = False
        if self.button_thread:
            self.button_thread.join()
    
    def _monitor_buttons(self):
        """Monitor button presses in a loop."""
        while self.running:
            for button_id, button_info in self.buttons.items():
                current_state = GPIO.input(button_info['pin']) == GPIO.LOW
                current_time = time.time()
                
                # Detect button press with debouncing
                if (current_state and not button_info['state'] and 
                    current_time - button_info['last_press'] > config.BUTTON_DEBOUNCE_TIME):
                    
                    button_info['last_press'] = current_time
                    
                    # Call registered callback
                    if button_id in self.button_callbacks:
                        try:
                            self.button_callbacks[button_id]()
                        except Exception as e:
                            print(f"Error in button {button_id} callback: {e}")
                
                button_info['state'] = current_state
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    
    def get_button_state(self, button_id):
        """Get the current state of a button."""
        if 0 <= button_id < len(config.BUTTON_PINS):
            return GPIO.input(self.buttons[button_id]['pin']) == GPIO.LOW
        return False
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop_monitoring()
        GPIO.cleanup()

# Example button functions
def button_1_action():
    """Action for button 1."""
    print("Button 1 pressed - Starting rainbow pattern")
    # This will be connected to the main application

def button_2_action():
    """Action for button 2."""
    print("Button 2 pressed - Starting wave pattern")
    # This will be connected to the main application

def button_3_action():
    """Action for button 3."""
    print("Button 3 pressed - Starting text scroll")
    # This will be connected to the main application

def button_4_action():
    """Action for button 4."""
    print("Button 4 pressed - Starting fire effect")
    # This will be connected to the main application
'''
    
    with open('button_controller.py', 'w') as f:
        f.write(content)
    print("✓ Restored button_controller.py for Raspberry Pi")

def create_pi_deployment_package():
    """Create a deployment package for Raspberry Pi."""
    deploy_dir = "pi-deploy"
    
    # Create deployment directory
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)
    
    # Files to include for Pi deployment
    pi_files = [
        'main.py',
        'led_controller.py',
        'button_controller.py',
        'display_patterns.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'HARDWARE_SETUP.md',
        'led-display.service',
        'start.sh',
        'test_basic.py',
        'test_display.py'
    ]
    
    # Copy files
    for file in pi_files:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print(f"✓ Copied {file}")
        else:
            print(f"⚠ Warning: {file} not found")
    
    print(f"\n✓ Deployment package created in '{deploy_dir}' directory")
    print("You can now copy this directory to your Raspberry Pi")

def main():
    """Main function to prepare code for Raspberry Pi."""
    print("Preparing code for Raspberry Pi deployment...")
    print("=" * 50)
    
    # Backup original files
    backup_file('led_controller.py')
    backup_file('button_controller.py')
    
    # Restore files for Raspberry Pi
    restore_led_controller()
    restore_button_controller()
    
    # Create deployment package
    create_pi_deployment_package()
    
    print("\n" + "=" * 50)
    print("✓ Code prepared for Raspberry Pi deployment!")
    print("\nNext steps:")
    print("1. Copy the 'pi-deploy' directory to your Raspberry Pi")
    print("2. Follow the setup instructions in pi_setup_guide.md")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the application: python3 main.py")

if __name__ == "__main__":
    main() 