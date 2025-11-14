#!/usr/bin/env python3
"""
Test script for 4-button functionality
Tests all 4 buttons and prints pin numbers when pressed
"""

import time
import sys
from button_controller import ButtonController
import config

# Button functions mapping
BUTTON_FUNCTIONS = {
    0: "Shapes",
    1: "Nature Animations",
    2: "Animals Animation",
    3: "Objects Animations"
}

def button_pressed(button_id):
    """Called when a button is pressed."""
    pin_number = config.BUTTON_PINS[button_id]
    function = BUTTON_FUNCTIONS.get(button_id, "Unknown")
    print(f"🎉 Button {button_id + 1} pressed! Pin: {pin_number} ({function})")

def main():
    """Test all 4 buttons."""
    print("🧪 4-Button Test Started")
    print("=" * 50)
    print("Button Configuration:")
    for i, pin in enumerate(config.BUTTON_PINS):
        function = BUTTON_FUNCTIONS.get(i, "Unknown")
        print(f"  Button {i + 1}: GPIO Pin {pin} - {function}")
    print("=" * 50)
    print()
    print("🎯 Press any of the 4 buttons to test...")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        # Initialize button controller
        button_controller = ButtonController()
        
        # Register callbacks for all 4 buttons
        for i in range(4):
            button_controller.register_callback(i, lambda btn_id=i: button_pressed(btn_id))
        
        # Start monitoring
        button_controller.start_monitoring()
        
        print("✅ Ready! Press any button...")
        
        # Keep running
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Test completed")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        button_controller.cleanup()

if __name__ == "__main__":
    main()
