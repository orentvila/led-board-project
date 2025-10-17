#!/usr/bin/env python3
"""
Test button system for final program
"""

import time
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from button_controller import ButtonController
import config

def main():
    """Test button detection."""
    print("🔘 Testing Button System")
    print("=" * 30)
    print("Button Configuration:")
    for i, pin in enumerate(config.BUTTON_PINS):
        print(f"  Button {i + 1}: GPIO Pin {pin}")
    print("=" * 30)
    print()
    print("🎯 Press any button to test...")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        # Initialize button controller
        button_controller = ButtonController()
        
        # Register callbacks for all 4 buttons
        for i in range(4):
            def make_callback(button_id):
                def callback():
                    pin_number = config.BUTTON_PINS[button_id]
                    print(f"🎉 Button {button_id + 1} pressed! Pin: {pin_number}")
                return callback
            
            button_controller.register_callback(i, make_callback(i))
        
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
