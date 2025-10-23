#!/usr/bin/env python3
"""
Main application for Raspberry Pi LED Display Project
Controls 6 LED panels (32x8 each) to create a 48x32 display
"""

import time
import signal
import sys
import threading
import subprocess
import os
from led_controller import LEDController
from display_patterns import DisplayPatterns
from button_controller import ButtonController
from animation_tests.squares_animation import SquaresAnimation
from led_controller_exact import LEDControllerExact
import config

class LEDDisplayApp:
    def __init__(self):
        """Initialize the LED display application."""
        self.led = LEDController()
        self.patterns = DisplayPatterns(self.led)
        self.squares_animation = SquaresAnimation(self.led)
        self.button_controller = ButtonController()
        self.current_pattern = None
        self.running = True
        
        # Shape animation system
        self.shape_animations = [
            "growing_circle_animation.py",
            "rotating_square_animation.py", 
            "bouncing_triangle_animation.py",
            "pulsing_diamond_animation.py"
        ]
        self.current_shape_index = 0
        self.current_shape_process = None
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for the 4 buttons."""
        # Button 18 (index 0) - Shapes
        self.button_controller.register_callback(0, self.start_shapes_animation)
        # Button 17 (index 1) - Wave pattern
        self.button_controller.register_callback(1, self.start_wave_pattern)
        # Button 27 (index 2) - Text scroll
        self.button_controller.register_callback(2, self.start_text_scroll)
        # Button 22 (index 3) - Squares animation
        self.button_controller.register_callback(3, self.start_squares_animation)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down LED display...")
        self.cleanup()
        sys.exit(0)
    
    def stop_current_shape_animation(self):
        """Stop the currently running shape animation."""
        if self.current_shape_process and self.current_shape_process.poll() is None:
            print("🛑 Stopping current shape animation...")
            self.current_shape_process.terminate()
            self.current_shape_process.wait()
            self.current_shape_process = None
            print("✅ Shape animation stopped")
    
    def start_shapes_animation(self):
        """Start shapes animation - cycles through different shapes."""
        print("🔷 Starting shapes animation...")
        self.stop_current_pattern()
        self.stop_current_shape_animation()
        
        # Cycle to next shape
        self.current_shape_index = (self.current_shape_index + 1) % len(self.shape_animations)
        shape_names = ["Growing Circle", "Rotating Square", "Bouncing Triangle", "Pulsing Diamond"]
        shape_name = shape_names[self.current_shape_index]
        
        print(f"🎬 Starting {shape_name}...")
        
        # Start the shape animation as a thread
        self.current_pattern = threading.Thread(target=self.run_shape_animation)
        self.current_pattern.daemon = True
        self.current_pattern.start()
        
        print(f"✅ Started {shape_name}")
    
    def run_shape_animation(self):
        """Run the current shape animation."""
        if self.current_shape_index == 0:
            self.run_growing_circle()
        elif self.current_shape_index == 1:
            self.run_rotating_square()
        elif self.current_shape_index == 2:
            self.run_bouncing_triangle()
        elif self.current_shape_index == 3:
            self.run_pulsing_diamond()
    
    def run_growing_circle(self):
        """Run growing circle animation."""
        import math
        duration = 15
        start_time = time.time()
        
        while time.time() - start_time < duration:
            center_x, center_y = 16, 24
            progress = (time.time() - start_time) / duration
            max_radius = min(16, 24) - 2
            current_radius = int(progress * max_radius)
            
            # Clear display
            self.led.clear()
            
            # Draw circle
            for y in range(48):
                for x in range(32):
                    distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    if distance <= current_radius:
                        self.led.set_pixel(x, y, (255, 0, 0))  # Red
            
            self.led.show()
            time.sleep(0.05)
    
    def run_rotating_square(self):
        """Run rotating square animation."""
        import math
        duration = 15
        start_time = time.time()
        
        while time.time() - start_time < duration:
            center_x, center_y = 16, 24
            size = 12
            rotation_angle = (time.time() - start_time) * 0.5
            
            # Clear display
            self.led.clear()
            
            # Draw rotated square
            for y in range(48):
                for x in range(32):
                    # Rotate point around center
                    dx = x - center_x
                    dy = y - center_y
                    cos_a = math.cos(rotation_angle)
                    sin_a = math.sin(rotation_angle)
                    rx = dx * cos_a - dy * sin_a
                    ry = dx * sin_a + dy * cos_a
                    
                    # Check if point is inside square
                    if abs(rx) <= size//2 and abs(ry) <= size//2:
                        self.led.set_pixel(x, y, (0, 0, 255))  # Blue
            
            self.led.show()
            time.sleep(0.05)
    
    def run_bouncing_triangle(self):
        """Run bouncing triangle animation."""
        duration = 15
        start_time = time.time()
        
        # Triangle position and movement
        triangle_x = 16
        triangle_y = 24
        triangle_dx = 2
        triangle_dy = 1
        
        while time.time() - start_time < duration:
            # Update position
            triangle_x += triangle_dx
            triangle_y += triangle_dy
            
            # Bounce off edges
            if triangle_x <= 5 or triangle_x >= 27:
                triangle_dx = -triangle_dx
            if triangle_y <= 5 or triangle_y >= 43:
                triangle_dy = -triangle_dy
            
            # Keep in bounds
            triangle_x = max(5, min(27, triangle_x))
            triangle_y = max(5, min(43, triangle_y))
            
            # Clear display
            self.led.clear()
            
            # Draw triangle
            triangle_size = 8
            for y in range(48):
                for x in range(32):
                    # Check if point is inside triangle
                    if (y <= triangle_y - triangle_size and 
                        x >= triangle_x - triangle_size and 
                        x <= triangle_x + triangle_size and
                        y >= triangle_y - triangle_size + (abs(x - triangle_x) * 2)):
                        self.led.set_pixel(x, y, (0, 255, 0))  # Green
            
            self.led.show()
            time.sleep(0.05)
    
    def run_pulsing_diamond(self):
        """Run pulsing diamond animation."""
        import math
        duration = 15
        start_time = time.time()
        
        while time.time() - start_time < duration:
            center_x, center_y = 16, 24
            pulse_phase = (time.time() - start_time) * 2
            pulse_size = int(8 + 4 * math.sin(pulse_phase))
            
            # Clear display
            self.led.clear()
            
            # Draw diamond
            for y in range(48):
                for x in range(32):
                    dx = abs(x - center_x)
                    dy = abs(y - center_y)
                    if dx + dy <= pulse_size:
                        self.led.set_pixel(x, y, (255, 255, 0))  # Yellow
            
            self.led.show()
            time.sleep(0.05)
    
    def start_rainbow_pattern(self):
        """Start rainbow wave pattern."""
        print("Starting rainbow pattern")
        self.stop_current_pattern()
        self.stop_current_shape_animation()
        self.current_pattern = threading.Thread(target=self.patterns.rainbow_wave)
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def start_wave_pattern(self):
        """Start color wave pattern."""
        print("Starting wave pattern")
        self.stop_current_pattern()
        self.stop_current_shape_animation()
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
        self.stop_current_shape_animation()
        self.current_pattern = threading.Thread(
            target=self.patterns.scrolling_text,
            args=("HELLO RASPBERRY PI!", config.COLORS['GREEN'])
        )
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def start_squares_animation(self):
        """Start squares animation pattern."""
        print("Starting squares animation")
        self.stop_current_pattern()
        self.stop_current_shape_animation()
        self.current_pattern = threading.Thread(target=self.squares_animation.run_animation)
        self.current_pattern.daemon = True
        self.current_pattern.start()
    
    def stop_current_pattern(self):
        """Stop the currently running pattern."""
        if self.current_pattern and hasattr(self.current_pattern, 'is_alive') and self.current_pattern.is_alive():
            self.patterns.stop()
            self.squares_animation.stop()
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
        
        # Demo 5: Squares animation
        print("Demo 5: Squares animation")
        self.squares_animation.run_animation()
        
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
        print("  Button 4: Squares animation")
        
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
        self.stop_current_shape_animation()
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
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main() 