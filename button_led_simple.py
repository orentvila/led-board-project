#!/usr/bin/env python3
"""
Simple 4-button LED controller
Handles random plan changes when any button is clicked
"""

import time
import signal
import sys
import random
from button_controller import ButtonController
from led_controller import LEDController
from display_patterns import DisplayPatterns
import config

class SimpleButtonLEDController:
    def __init__(self):
        """Initialize the simple button LED controller."""
        self.led = LEDController()
        self.patterns = DisplayPatterns(self.led)
        self.button_controller = ButtonController()
        self.running = True
        
        # Available animation plans
        self.animation_plans = [
            self.start_rainbow_pattern,
            self.start_wave_pattern,
            self.start_text_scroll,
            self.start_color_cycle,
            self.start_panel_sequence
        ]
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks for all 4 buttons
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for all 4 buttons."""
        for i in range(4):  # 4 buttons (pins 18, 17, 27, 22)
            self.button_controller.register_callback(i, self.button_pressed)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down LED controller...")
        self.cleanup()
        sys.exit(0)
    
    def button_pressed(self):
        """Called when any button is pressed."""
        # Get the button ID that was pressed
        button_id = None
        for i in range(4):
            if self.button_controller.get_button_state(i):
                button_id = i
                break
        
        if button_id is not None:
            pin_number = config.BUTTON_PINS[button_id]
            print(f"🎉 Button pressed! Pin: {pin_number} (Button {button_id + 1})")
            
            # Randomly select and start a new animation plan
            self.start_random_plan()
    
    def start_random_plan(self):
        """Start a randomly selected animation plan."""
        # Stop current pattern
        self.patterns.stop()
        
        # Select random animation plan
        random_plan = random.choice(self.animation_plans)
        plan_name = random_plan.__name__.replace('start_', '').replace('_', ' ').title()
        
        print(f"🎲 Starting random plan: {plan_name}")
        
        # Start the new pattern (no threading to avoid issues)
        try:
            random_plan()
        except Exception as e:
            print(f"❌ Error in animation: {e}")
            # Fallback to simple color cycle
            self.start_color_cycle()
    
    def start_rainbow_pattern(self):
        """Start rainbow wave pattern."""
        print("🌈 Running rainbow pattern...")
        self.patterns.rainbow_wave(duration=5)  # Run for 5 seconds
    
    def start_wave_pattern(self):
        """Start color wave pattern."""
        print("🌊 Running wave pattern...")
        colors = [config.COLORS['BLUE'], config.COLORS['GREEN'], config.COLORS['RED']]
        color = random.choice(colors)
        self.patterns.color_wave(color, duration=5)
    
    def start_text_scroll(self):
        """Start text scrolling pattern."""
        print("📝 Running text scroll...")
        messages = [
            "HELLO WORLD!",
            "BUTTON FUN!",
            "LED DISPLAY",
            "RANDOM PLAN",
            "MUSHROOM LED"
        ]
        message = random.choice(messages)
        color = random.choice(list(config.COLORS.values()))
        self.patterns.scrolling_text(message, color, duration=5)
    
    def start_panel_sequence(self):
        """Start panel sequence animation."""
        print("🎨 Running panel sequence...")
        colors = list(config.COLORS.values())
        random.shuffle(colors)
        self.patterns.panel_sequence(colors[:4], duration=3)
    
    def start_color_cycle(self):
        """Start color cycling animation."""
        print("🎨 Running color cycle...")
        colors = [config.COLORS['RED'], config.COLORS['GREEN'], config.COLORS['BLUE'], 
                 config.COLORS['YELLOW'], config.COLORS['MAGENTA'], config.COLORS['CYAN']]
        
        for color in colors:
            if not self.running:
                break
            print(f"  Setting color: {color}")
            self.led.fill_display(color)
            self.led.show()
            time.sleep(1)
            self.led.clear()
            self.led.show()
            time.sleep(0.2)
    
    def run(self):
        """Main application loop."""
        print("🎮 Simple Button LED Controller Started")
        print("=" * 50)
        print("Hardware Configuration:")
        print(f"  LED Pin: {config.LED_PIN}")
        print(f"  Button Pins: {config.BUTTON_PINS}")
        print(f"  Total LEDs: {config.TOTAL_LEDS}")
        print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print("=" * 50)
        print()
        print("🎯 Instructions:")
        print("  - Press ANY of the 4 buttons to start a random animation")
        print("  - Each button press will print the pin number")
        print("  - Press Ctrl+C to exit")
        print()
        
        # Start button monitoring
        self.button_controller.start_monitoring()
        
        # Initial display
        print("  Setting initial blue color...")
        self.led.fill_display(config.COLORS['BLUE'])
        self.led.show()
        time.sleep(2)
        self.led.clear()
        self.led.show()
        
        print("✅ Ready! Press any button to start...")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up...")
        self.running = False
        self.patterns.stop()
        self.button_controller.cleanup()
        self.led.cleanup()
        print("✅ Cleanup completed.")

def main():
    """Main entry point."""
    try:
        print("🚀 Starting Simple Button LED Controller...")
        app = SimpleButtonLEDController()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
