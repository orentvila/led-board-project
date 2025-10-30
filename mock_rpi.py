"""
Mock Raspberry Pi modules for Windows development
This allows testing the code structure without actual hardware
"""

import time
import random

class MockGPIO:
    """Mock GPIO class for Windows development"""
    
    # GPIO modes
    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    
    # GPIO states
    HIGH = 1
    LOW = 0
    
    # GPIO pull up/down
    PUD_UP = 1
    PUD_DOWN = 0
    
    def __init__(self):
        self.pins = {}
        print("Mock GPIO initialized (Windows development mode)")
    
    def setmode(self, mode):
        print(f"GPIO mode set to: {mode}")
    
    def setwarnings(self, warnings):
        print(f"GPIO warnings set to: {warnings}")
    
    def setup(self, pin, mode, initial=0, pull_up_down=None):
        self.pins[pin] = initial
        pull_text = f" with pull-up" if pull_up_down == self.PUD_UP else f" with pull-down" if pull_up_down == self.PUD_DOWN else ""
        print(f"GPIO pin {pin} setup as {'OUTPUT' if mode == self.OUT else 'INPUT'}{pull_text}")
    
    def output(self, pin, state):
        self.pins[pin] = state
        print(f"GPIO pin {pin} set to {state}")
    
    def input(self, pin):
        # Simulate button press with random chance
        return random.choice([self.HIGH, self.LOW])
    
    def cleanup(self):
        self.pins.clear()
        print("GPIO cleanup completed")

class MockWS281x:
    """Mock WS281x class for Windows development"""
    
    def __init__(self, led_count, pin, freq_hz=800000, dma=10, invert=False, 
                 brightness=255, channel=0, strip_type=None, gamma=None):
        self.led_count = led_count
        self.pin = pin
        self.freq_hz = freq_hz
        self.brightness = brightness
        self.pixels = [(0, 0, 0)] * led_count
        print(f"Mock WS281x initialized: {led_count} LEDs on pin {pin}")
    
    def begin(self):
        print("WS281x strip begin() called")
    
    def setPixelColor(self, pixel, color):
        if 0 <= pixel < self.led_count:
            self.pixels[pixel] = color
            # Print every 100th pixel to avoid spam
            if pixel % 100 == 0:
                print(f"Pixel {pixel} set to color {color}")
    
    def setPixelColorRGB(self, pixel, red, green, blue, white=0):
        if 0 <= pixel < self.led_count:
            self.pixels[pixel] = (red, green, blue)
            # No debug prints - too noisy
    
    def show(self):
        # No debug print - too noisy
        # Simulate some delay for the display
        time.sleep(0.01)
    
    def setBrightness(self, brightness):
        self.brightness = brightness
        print(f"Brightness set to {brightness}")
    
    def numPixels(self):
        return self.led_count
    
    def getPixelColor(self, pixel):
        if 0 <= pixel < self.led_count:
            return self.pixels[pixel]
        return (0, 0, 0)
    
    def clear(self):
        self.pixels = [(0, 0, 0)] * self.led_count
        print("All pixels cleared")

# Create mock instances
GPIO = MockGPIO()
WS281x = MockWS281x

print("Mock Raspberry Pi modules loaded for Windows development") 