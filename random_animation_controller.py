#!/usr/bin/env python3
"""
Random Animation Controller for Raspberry Pi LED Display
Runs random animations when button is pressed on GPIO 18
"""

import time
import signal
import sys
import random
import subprocess
import os
from button_controller import ButtonController
import config

class RandomAnimationController:
    def __init__(self):
        """Initialize the random animation controller."""
        self.button_controller = ButtonController()
        self.running = True
        self.current_process = None
        
        # Get list of available animation scripts from scripts folder
        self.scripts_folder = 'scripts'
        self.animation_scripts = self._get_animation_scripts()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callback for GPIO 18 (button 1)
        # Note: Button 1 is on GPIO 18 according to config.BUTTON_PINS[1]
        self.button_controller.register_callback(1, self.start_random_animation)
        
        print("Random Animation Controller Started")
        print(f"Available animations: {len(self.animation_scripts)}")
        print("Press button on GPIO 18 to start random animation")
        print("Press Ctrl+C to exit")
    
    def _get_animation_scripts(self):
        """Get list of animation scripts from the scripts folder."""
        scripts = []
        if os.path.exists(self.scripts_folder):
            for file in os.listdir(self.scripts_folder):
                if file.endswith('_animation.py'):
                    scripts.append(file)
        scripts.sort()  # Sort alphabetically for consistent ordering
        return scripts
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down...")
        self.cleanup()
        sys.exit(0)
    
    def start_random_animation(self):
        """Start a random animation."""
        # Stop current animation if running
        self.stop_current_animation()
        
        # Select random animation
        selected_script = random.choice(self.animation_scripts)
        print(f"\n🎬 Starting random animation: {selected_script}")
        
        # Run the animation script
        try:
            script_path = os.path.join(os.getcwd(), self.scripts_folder, selected_script)
            cmd = ['sudo', './venv/bin/python', script_path]
            
            print(f"Running: {' '.join(cmd)}")
            self.current_process = subprocess.Popen(cmd)
            
            # Wait for the process to complete
            self.current_process.wait()
            self.current_process = None
            
            print(f"✅ Animation completed: {selected_script}")
            
        except Exception as e:
            print(f"❌ Error running animation {selected_script}: {e}")
            self.current_process = None
    
    def stop_current_animation(self):
        """Stop the currently running animation."""
        if self.current_process:
            print("🛑 Stopping current animation...")
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Force killing animation...")
                self.current_process.kill()
            except Exception as e:
                print(f"Error stopping animation: {e}")
            finally:
                self.current_process = None
    
    def run(self):
        """Main application loop."""
        try:
            # Start button monitoring
            self.button_controller.start_monitoring()
            
            # Keep the application running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.stop_current_animation()
        self.button_controller.cleanup()
        print("Cleanup completed.")

def main():
    """Main entry point."""
    try:
        controller = RandomAnimationController()
        controller.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
