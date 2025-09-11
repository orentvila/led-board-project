#!/usr/bin/env python3
"""
Test script for main animation controller
Simulates button presses to test animation switching
"""

import time
import threading
from main_animation_controller import MainAnimationController

def simulate_button_presses(controller, num_presses=3, interval=10):
    """Simulate button presses for testing."""
    print(f"🧪 Simulating {num_presses} button presses every {interval} seconds...")
    
    for i in range(num_presses):
        time.sleep(interval)
        if controller.running:
            print(f"\n🔘 Simulating button press #{i+1}")
            controller.switch_animation()

def main():
    """Test the main animation controller."""
    print("🧪 Testing Main Animation Controller")
    print("=" * 40)
    
    try:
        # Create controller
        controller = MainAnimationController()
        
        # Start controller in a separate thread
        controller_thread = threading.Thread(target=controller.run)
        controller_thread.daemon = True
        controller_thread.start()
        
        # Wait a moment for initialization
        time.sleep(2)
        
        # Simulate button presses
        simulate_button_presses(controller, num_presses=3, interval=15)
        
        # Stop controller
        print("\n🛑 Stopping test...")
        controller.running = False
        controller.stop_current_animation()
        controller.cleanup()
        
        print("✅ Test completed")
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()
