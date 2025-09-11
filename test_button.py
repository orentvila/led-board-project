#!/usr/bin/env python3
"""
Simple button test script
Tests if the button on GPIO 18 is working
"""

import time
from button_controller import ButtonController

def button_pressed():
    """Called when button is pressed."""
    print("🎉 BUTTON PRESSED! GPIO 18 is working correctly!")

def main():
    """Test button functionality."""
    print("Button Test Started")
    print("Press the button connected to GPIO 18...")
    print("Press Ctrl+C to exit")
    
    try:
        # Initialize button controller
        button_controller = ButtonController()
        
        # Register callback for button 1 (GPIO 18)
        button_controller.register_callback(1, button_pressed)
        
        # Start monitoring
        button_controller.start_monitoring()
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest completed")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        button_controller.cleanup()

if __name__ == "__main__":
    main()
