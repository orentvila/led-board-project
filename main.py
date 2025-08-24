#!/usr/bin/env python3
"""
Main application for Raspberry Pi LED Display Project
Controls 6 LED panels (32x8 each) to create a 48x32 display
"""

import time
import signal
import sys
import threading
from led_controller import LEDController
from display_patterns import DisplayPatterns
from button_controller import ButtonController
import config

class LEDDisplayApp:
    def __init__(self):
        """Initialize the LED display application."""
        self.led = LEDController()
        self.patterns = DisplayPatterns(self.led)
        self.button_controller = ButtonController()
        self.current_pattern = None
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for the 4 buttons."""
        self.button_controller.register_callback(0, self.start_rainbow_pattern)
        self.button_controller.register_callback(1, self.start_wave_pattern)
        self.button_controller.register_callback(2, self.start_text_scroll)
        self.button_controller.register_callback(3, self.start_fire_effect)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down LED display...")
        self.cleanup()
        sys.exit(0)
    
    def start_rainbow_pattern(self):
        """Start rainbow wave pattern."""
        print("Starting rainbow pattern")
        self.stop_current_pattern()
        self.current_pattern = threading.Thread(target=self.patterns.rainbow_wave)
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def start_wave_pattern(self):
        """Start color wave pattern."""
        print("Starting wave pattern")
        self.stop_current_pattern()
        self.current_pattern = threading.Thread(
            target=self.patterns.color_wave, 
            args=(config.COLORS['BLUE'],)
        )
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def start_text_scroll(self):
        """Start text scrolling pattern."""
        print("Starting text scroll")
        self.stop_current_pattern()
        self.current_pattern = threading.Thread(
            target=self.patterns.scrolling_text,
            args=("HELLO RASPBERRY PI!", config.COLORS['GREEN'])
        )
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def start_fire_effect(self):
        """Start fire effect pattern."""
        print("Starting fire effect")
        self.stop_current_pattern()
        self.current_pattern = threading.Thread(target=self.patterns.fire_effect)
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def stop_current_pattern(self):
        """Stop the currently running pattern."""
        if self.current_pattern and self.current_pattern.is_alive():
            self.patterns.stop()
            self.current_pattern.join(timeout=1.0)
    
    def demo_sequence(self):
        """Run a demo sequence of various patterns."""
        print("Starting demo sequence...")
        
        # Demo 1: Mushroom display
        print("Demo 1: Mushroom display")
        from mushroom_display import MushroomDisplay
        mushroom = MushroomDisplay()
        mushroom.display_mushroom(duration=5)
        mushroom.display_mushroom_animation(duration=5)
        mushroom.cleanup()
        
        # Demo 2: Panel sequence
        print("Demo 2: Panel sequence")
        colors = [config.COLORS['RED'], config.COLORS['GREEN'], config.COLORS['BLUE'], 
                 config.COLORS['YELLOW'], config.COLORS['MAGENTA']]
        self.patterns.panel_sequence(colors, duration=3)
        
        # Demo 3: Rainbow wave
        print("Demo 3: Rainbow wave")
        self.patterns.rainbow_wave(duration=3)
        
        # Demo 4: Text scroll
        print("Demo 4: Text scroll")
        self.patterns.scrolling_text("MUSHROOM LED DISPLAY", config.COLORS['WHITE'], duration=3)
        
        print("Demo sequence completed!")
    
    def run(self):
        """Main application loop."""
        print("LED Display Application Started")
        print("Display Configuration:")
        print(f"  Total LEDs: {config.TOTAL_LEDS}")
        print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print(f"  Panels: {config.PANELS_COUNT} ({config.PANEL_WIDTH}x{config.PANEL_HEIGHT} each)")
        print(f"  LED Pin: {config.LED_PIN}")
        print(f"  Brightness: {config.BRIGHTNESS}")
        print()
        
        # Start button monitoring
        self.button_controller.start_monitoring()
        
        # Run demo sequence
        self.demo_sequence()
        
        # Keep the application running
        print("Application running. Press Ctrl+C to exit.")
        print("Button controls (when connected):")
        print("  Button 1: Rainbow pattern")
        print("  Button 2: Wave pattern")
        print("  Button 3: Text scroll")
        print("  Button 4: Fire effect")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.stop_current_pattern()
        self.button_controller.cleanup()
        self.led.cleanup()
        print("Cleanup completed.")

def git_pull_update():
    """Pull latest changes from git repository."""
    import subprocess
    import os
    
    try:
        print("Checking for updates...")
        
        # Get the current directory
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        
        # Check if this is a git repository
        if not os.path.exists('.git'):
            print("Not a git repository, skipping update check")
            return False
        
        # Fetch latest changes
        print("Fetching latest changes...")
        result = subprocess.run(['git', 'fetch'], 
                              capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode != 0:
            print(f"Git fetch failed: {result.stderr}")
            return False
        
        # Check if there are any changes to pull
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=current_dir)
        
        # Check if we're behind the remote
        result_behind = subprocess.run(['git', 'rev-list', 'HEAD..origin/main', '--count'], 
                                     capture_output=True, text=True, cwd=current_dir)
        
        if result_behind.returncode == 0 and result_behind.stdout.strip() != '0':
            commits_behind = int(result_behind.stdout.strip())
            print(f"Found {commits_behind} new commits, pulling updates...")
            
            # Pull the changes
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  capture_output=True, text=True, cwd=current_dir)
            
            if result.returncode == 0:
                print("✅ Successfully updated from git repository!")
                print("Changes pulled:")
                print(result.stdout)
                return True
            else:
                print(f"❌ Git pull failed: {result.stderr}")
                return False
        else:
            print("✅ Already up to date!")
            return False
            
    except Exception as e:
        print(f"❌ Error during git update: {e}")
        return False

def main():
    """Main entry point."""
    try:
        # Check for git updates first
        updated = git_pull_update()
        
        if updated:
            print("🔄 Restarting application with updated code...")
            # Restart the application to load new code
            import os
            import sys
            os.execv(sys.executable, ['python'] + sys.argv)
        
        # Start the application
        app = LEDDisplayApp()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 