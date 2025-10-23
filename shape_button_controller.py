#!/usr/bin/env python3
"""
Shape Button Controller for LED Board
Cycles through different shape animations on button press
"""

import time
import threading
import subprocess
import os
import sys
from led_controller_exact import LEDControllerExact
import config

class ShapeButtonController:
    def __init__(self):
        """Initialize the shape button controller."""
        self.led = LEDControllerExact()
        self.width = 32
        self.height = 48  # 6 panels × 8 rows
        
        # Shape animations list
        self.shape_animations = [
            "growing_circle_animation.py",
            "rotating_square_animation.py", 
            "bouncing_triangle_animation.py",
            "pulsing_diamond_animation.py"
        ]
        
        self.current_shape_index = 0
        self.current_process = None
        self.is_running = False
        
        # Button simulation (for testing)
        self.button_pressed = False
        
    def stop_current_animation(self):
        """Stop the currently running animation."""
        if self.current_process and self.current_process.poll() is None:
            print("🛑 Stopping current animation...")
            self.current_process.terminate()
            self.current_process.wait()
            self.current_process = None
            print("✅ Animation stopped")
    
    def start_shape_animation(self, shape_index):
        """Start a specific shape animation."""
        if shape_index < 0 or shape_index >= len(self.shape_animations):
            print(f"❌ Invalid shape index: {shape_index}")
            return
        
        # Stop current animation
        self.stop_current_animation()
        
        # Start new animation
        shape_file = self.shape_animations[shape_index]
        print(f"🎬 Starting {shape_file}...")
        
        try:
            # Run the animation script
            self.current_process = subprocess.Popen([
                sys.executable, shape_file
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.current_shape_index = shape_index
            print(f"✅ Started {shape_file}")
            
        except Exception as e:
            print(f"❌ Error starting {shape_file}: {e}")
    
    def next_shape(self):
        """Cycle to the next shape animation."""
        self.current_shape_index = (self.current_shape_index + 1) % len(self.shape_animations)
        self.start_shape_animation(self.current_shape_index)
    
    def previous_shape(self):
        """Cycle to the previous shape animation."""
        self.current_shape_index = (self.current_shape_index - 1) % len(self.shape_animations)
        self.start_shape_animation(self.current_shape_index)
    
    def show_shape_menu(self):
        """Display the current shape menu."""
        print("\n🔷 Shape Button Controller 🔷")
        print("=" * 40)
        print("Available Shapes:")
        for i, shape in enumerate(self.shape_animations):
            status = "▶️ CURRENT" if i == self.current_shape_index else "⏸️"
            print(f"  {i+1}. {shape.replace('_animation.py', '').replace('_', ' ').title()} {status}")
        print("\nControls:")
        print("  'n' or 'next' - Next shape")
        print("  'p' or 'prev' - Previous shape")
        print("  's' or 'stop' - Stop current animation")
        print("  'q' or 'quit' - Exit")
        print("=" * 40)
    
    def run_interactive_mode(self):
        """Run the interactive shape button controller."""
        print("🎮 Starting Shape Button Controller...")
        print("Press 'n' for next shape, 'p' for previous, 's' to stop, 'q' to quit")
        
        # Start with the first shape
        self.start_shape_animation(0)
        
        try:
            while True:
                self.show_shape_menu()
                user_input = input("\nEnter command: ").strip().lower()
                
                if user_input in ['q', 'quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input in ['n', 'next']:
                    print("⏭️ Next shape...")
                    self.next_shape()
                elif user_input in ['p', 'prev', 'previous']:
                    print("⏮️ Previous shape...")
                    self.previous_shape()
                elif user_input in ['s', 'stop']:
                    print("⏹️ Stopping animation...")
                    self.stop_current_animation()
                else:
                    print("❓ Unknown command. Try 'n', 'p', 's', or 'q'")
                
                time.sleep(0.1)  # Small delay
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        finally:
            self.cleanup()
    
    def simulate_button_press(self):
        """Simulate a button press (for testing without physical button)."""
        print("🔘 Simulating button press...")
        self.next_shape()
    
    def cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up...")
        self.stop_current_animation()
        self.led.cleanup()
        print("✅ Cleanup completed")

def main():
    """Main function to run the shape button controller."""
    try:
        controller = ShapeButtonController()
        controller.run_interactive_mode()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
