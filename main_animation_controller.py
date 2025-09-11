#!/usr/bin/env python3
"""
Main Animation Controller for Raspberry Pi LED Display
Single script that runs continuously and switches animations on button press
"""

import time
import signal
import sys
import random
import subprocess
import os
import threading
from button_controller import ButtonController
import config

class MainAnimationController:
    def __init__(self):
        """Initialize the main animation controller."""
        self.button_controller = ButtonController()
        self.running = True
        self.current_process = None
        self.animation_thread = None
        
        # Get list of available animation scripts from scripts folder
        self.scripts_folder = 'scripts'
        self.animation_scripts = self._get_animation_scripts()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callback for GPIO 18 (button 1)
        self.button_controller.register_callback(1, self.switch_animation)
        
        print("🎬 Main Animation Controller Started")
        print("=" * 50)
        print(f"📁 Found {len(self.animation_scripts)} animation scripts")
        print("🔘 Press button on GPIO 18 to switch animations")
        print("⏹️  Press Ctrl+C to exit")
        print("=" * 50)
    
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
        print("\n🛑 Shutting down...")
        self.running = False
        self.stop_current_animation()
        self.cleanup()
        sys.exit(0)
    
    def switch_animation(self):
        """Switch to a new random animation (called by button press)."""
        print("\n🔘 Button pressed! Switching animation...")
        
        # Stop current animation
        self.stop_current_animation()
        
        # Select random animation
        selected_script = random.choice(self.animation_scripts)
        print(f"🎬 Starting: {selected_script}")
        
        # Start new animation in a separate thread
        self.animation_thread = threading.Thread(
            target=self._run_animation, 
            args=(selected_script,)
        )
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def _run_animation(self, script_name):
        """Run a specific animation script."""
        try:
            # Use the wrapper script to handle imports correctly
            wrapper_path = os.path.join(os.getcwd(), 'run_animation_wrapper.py')
            cmd = ['sudo', './venv/bin/python', wrapper_path, script_name]
            
            print(f"▶️  Running: {' '.join(cmd)}")
            
            # Run the wrapper script
            self.current_process = subprocess.Popen(
                cmd,
                cwd=os.getcwd()  # Run from project root
            )
            
            # Wait for the process to complete
            self.current_process.wait()
            self.current_process = None
            
            print(f"✅ Completed: {script_name}")
            
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            self.current_process = None
    
    def stop_current_animation(self):
        """Stop the currently running animation."""
        if self.current_process:
            print("⏹️  Stopping current animation...")
            try:
                self.current_process.terminate()
                # Give it a moment to terminate gracefully
                try:
                    self.current_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    print("🔨 Force killing animation...")
                    self.current_process.kill()
                    self.current_process.wait()
            except Exception as e:
                print(f"⚠️  Error stopping animation: {e}")
            finally:
                self.current_process = None
        
        # Wait for animation thread to finish
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=3)
    
    def run(self):
        """Main application loop."""
        try:
            # Start button monitoring
            self.button_controller.start_monitoring()
            
            # Start with a random animation
            print("🎲 Starting with random animation...")
            self.switch_animation()
            
            # Keep the application running
            while self.running:
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.running = False
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up...")
        self.stop_current_animation()
        self.button_controller.cleanup()
        print("✅ Cleanup completed")

def main():
    """Main entry point."""
    try:
        controller = MainAnimationController()
        controller.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
