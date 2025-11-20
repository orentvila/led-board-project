# Configuration file for Raspberry Pi LED Display Project

# Hardware Configuration
LED_PIN = 21  # GPIO pin for WS2812B LEDs
LED_FREQ_HZ = 800000  # LED signal frequency
LED_DMA = 10  # DMA channel
LED_INVERT = False  # Signal inversion
LED_CHANNEL = 0  # PWM channel

# Display Configuration
PANELS_COUNT = 6  # Number of LED panels (increased from 5 to 6)
PANEL_WIDTH = 32  # Width of each panel
PANEL_HEIGHT = 8  # Height of each panel
TOTAL_WIDTH = PANEL_WIDTH  # 32 pixels (width of each panel)
TOTAL_HEIGHT = PANELS_COUNT * PANEL_HEIGHT  # 48 pixels (6 panels stacked)
TOTAL_LEDS = TOTAL_WIDTH * TOTAL_HEIGHT  # 1536 LEDs

# Display Settings
BRIGHTNESS = 0.2  # Brightness level (0.0 to 1.0)
DEFAULT_COLOR = (0, 0, 0)  # Default color (black)

# Animation Settings
DEFAULT_FPS = 30  # Default frames per second
ANIMATION_SPEED = 0.1  # Animation speed multiplier

# Button Configuration (Future Implementation)
BUTTON_PINS = [18, 17, 27, 22]  # GPIO pins for 4 buttons
BUTTON_DEBOUNCE_TIME = 0.2  # Button debounce time in seconds

# Color Definitions
COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'YELLOW': (255, 255, 0),
    'CYAN': (0, 255, 255),
    'MAGENTA': (255, 0, 255),
    'ORANGE': (255, 165, 0),
    'PURPLE': (128, 0, 128),
    'PINK': (255, 192, 203)
}

# Pattern Settings
RAINBOW_SPEED = 0.01
WAVE_SPEED = 0.05
SCROLL_SPEED = 0.1 