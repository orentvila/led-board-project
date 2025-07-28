#!/usr/bin/env python3
"""
Simple test script to display mushroom on LED board
"""

import sys
import signal
from mushroom_display import MushroomDisplay

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print("\nShutting down mushroom display...")
    sys.exit(0)

def main():
    """Main function to test mushroom display."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Mushroom LED Display Test")
    print("Press Ctrl+C to exit")
    print()
    
    try:
        mushroom = MushroomDisplay()
        
        print("Displaying static mushroom for 5 seconds...")
        mushroom.display_mushroom(duration=5)
        
        print("Displaying animated mushroom for 10 seconds...")
        mushroom.display_mushroom_animation(duration=10)
        
        print("Test completed!")
        mushroom.cleanup()
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        mushroom.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        if 'mushroom' in locals():
            mushroom.cleanup()

if __name__ == "__main__":
    main() 