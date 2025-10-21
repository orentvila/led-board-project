#!/usr/bin/env python3
"""
Final LED Program Main Controller
4-Button LED Controller with Theme Animations
"""

import time
import signal
import sys
import os
import threading
import pygame
import random

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from button_controller import ButtonController
from led_controller import LEDController
import config

# Import animations
from animations.saturn_animation import SaturnAnimation
from animations.star_animation import StarAnimation
from animations.bubbles_animation import BubblesAnimation
from animations.cube_3d_animation import Cube3DAnimation

class FinalLEDController:
    def __init__(self):
        """Initialize the final LED controller."""
        self.led = LEDController()
        self.button_controller = ButtonController()
        self.running = True
        self.current_animation = None
        
        # Initialize pygame for audio
        try:
            pygame.mixer.init()
            print("🔊 Audio system initialized")
        except Exception as e:
            print(f"⚠️ Audio system not available: {e}")
            self.audio_available = False
        else:
            self.audio_available = True
        
        # Theme configurations
        self.themes = {
            0: {  # Pin 18 - Shapes
                'name': 'Shapes',
                'animations': [
                    {'name': '3D Cube', 'class': Cube3DAnimation, 'audio': 'cube_theme.wav'},
                    {'name': 'Saturn', 'class': SaturnAnimation, 'audio': 'saturn_theme.wav'}
                ]
            },
            1: {  # Pin 17 - Nature
                'name': 'Nature',
                'animations': [
                    {'name': 'Bubbles', 'class': BubblesAnimation, 'audio': 'bubbles_theme.wav'}
                ]
            },
            2: {  # Pin 27 - Space
                'name': 'Space',
                'animations': [
                    {'name': 'Stars', 'class': StarAnimation, 'audio': 'star_theme.wav'}
                ]
            },
            3: {  # Pin 22 - Future theme
                'name': 'Theme 4',
                'animations': []
            }
        }
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Register button callbacks
        self.setup_button_callbacks()
    
    def setup_button_callbacks(self):
        """Setup button callbacks for all 4 buttons."""
        for i in range(4):
            self.button_controller.register_callback(i, self.button_pressed)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutting down final LED controller...")
        self.cleanup()
        sys.exit(0)
    
    def button_pressed(self):
        """Called when any button is pressed."""
        # Get the button ID that was pressed
        button_id = None
        for i in range(4):
            if self.button_controller.get_button_state(i):
                button_id = i
                break
        
        if button_id is not None:
            pin_number = config.BUTTON_PINS[button_id]
            theme_name = self.themes[button_id]['name']
            print(f"🎉 Button pressed! Pin: {pin_number} - {theme_name} Theme")
            
            # Start theme animation
            self.start_theme_animation(button_id)
    
    def start_theme_animation(self, theme_id):
        """Start a random animation from the specified theme."""
        theme = self.themes[theme_id]
        
        if not theme['animations']:
            print(f"⚠️ No animations available for {theme['name']} theme")
            return
        
        # Stop current animation
        self.stop_current_animation()
        
        # Select random animation from theme
        animation_info = random.choice(theme['animations'])
        animation_name = animation_info['name']
        
        print(f"🎬 Starting {theme['name']} animation: {animation_name}")
        
        # Play audio if available
        if self.audio_available and 'audio' in animation_info:
            self.play_audio(animation_info['audio'])
        
        # Start animation
        animation_class = animation_info['class']
        animation = animation_class(self.led)
        
        self.current_animation = animation
        animation.start(30)  # 30 seconds duration
    
    def play_audio(self, audio_file):
        """Play audio file if available."""
        if not self.audio_available:
            return
        
        try:
            audio_path = os.path.join('audio', audio_file)
            if os.path.exists(audio_path):
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                print(f"🔊 Playing audio: {audio_file}")
            else:
                print(f"⚠️ Audio file not found: {audio_file}")
        except Exception as e:
            print(f"⚠️ Error playing audio: {e}")
    
    def stop_current_animation(self):
        """Stop the currently running animation."""
        if self.current_animation:
            self.current_animation.stop()
            # Stop any playing audio
            if self.audio_available:
                pygame.mixer.music.stop()
    
    def run(self):
        """Main application loop."""
        print("🎮 Final LED Controller Started")
        print("=" * 50)
        print("Hardware Configuration:")
        print(f"  LED Pin: {config.LED_PIN}")
        print(f"  Button Pins: {config.BUTTON_PINS}")
        print(f"  Total LEDs: {config.TOTAL_LEDS}")
        print(f"  Display Size: {config.TOTAL_WIDTH}x{config.TOTAL_HEIGHT}")
        print("=" * 50)
        print()
        print("🎯 Theme Configuration:")
        for i, theme in self.themes.items():
            pin = config.BUTTON_PINS[i]
            anim_count = len(theme['animations'])
            print(f"  Pin {pin}: {theme['name']} ({anim_count} animations)")
        print()
        print("🎯 Instructions:")
        print("  - Press ANY of the 4 buttons to start a theme animation")
        print("  - Each animation runs for 30 seconds")
        print("  - Press Ctrl+C to exit")
        print()
        
        # Start button monitoring
        self.button_controller.start_monitoring()
        
        # Initial display
        self.led.fill_display(config.COLORS['BLUE'])
        self.led.show()
        time.sleep(1)
        self.led.clear()
        self.led.show()
        
        print("✅ Ready! Press any button to start...")
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up...")
        self.running = False
        self.stop_current_animation()
        self.button_controller.cleanup()
        self.led.cleanup()
        if self.audio_available:
            pygame.mixer.quit()
        print("✅ Cleanup completed.")

def main():
    """Main entry point."""
    try:
        print("🚀 Starting Final LED Controller...")
        app = FinalLEDController()
        app.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
