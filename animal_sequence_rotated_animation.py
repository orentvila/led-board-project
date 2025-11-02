#!/usr/bin/env python3
"""
Animal Sequence Animation (Rotated 180 degrees) for LED Board
Shows cat, dog, and elephant in sequence, rotated 180 degrees
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class AnimalSequenceRotatedAnimation:
    def __init__(self):
        """Initialize the rotated animal sequence animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),     # Black background
            'cat_orange': (255, 165, 0), # Orange cat
            'cat_black': (50, 50, 50),   # Dark gray cat
            'cat_white': (200, 200, 200), # Light gray cat
            'cat_pink': (255, 192, 203), # Pink nose
            'dog_brown': (139, 69, 19),  # Brown dog
            'dog_black': (30, 30, 30),   # Black dog
            'dog_white': (220, 220, 220), # White dog
            'elephant_gray': (128, 128, 128), # Gray elephant
            'elephant_dark': (64, 64, 64),    # Dark gray elephant
            'elephant_pink': (255, 182, 193), # Pink elephant
            'eyes': (255, 255, 255),     # White eyes
            'pupils': (0, 0, 0)          # Black pupils
        }
        
    def rotate_180(self, x, y):
        """Rotate coordinates 180 degrees."""
        return (self.width - 1 - x, self.height - 1 - y)
    
    def safe_set_pixel_rotated(self, x, y, color):
        """Safely set a pixel with 180-degree rotation."""
        rot_x, rot_y = self.rotate_180(x, y)
        if 0 <= rot_x < self.width and 0 <= rot_y < self.height:
            self.led.set_pixel(rot_x, rot_y, color)
    
    def create_cat_rotated(self):
        """Create a cat pattern rotated 180 degrees."""
        print("Creating rotated cat pattern...")
        self.led.clear()
        
        # Cat position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Cat head (oval shape) - rotated
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 8
                dy = (y - center_y) / 6
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat ears (triangular) - rotated
        # Left ear
        ear_y_start = max(0, center_y - 8)
        ear_y_end = min(self.height, center_y - 2)
        ear_x_start = max(0, center_x - 6)
        ear_x_end = min(self.width, center_x - 1)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= (x - (center_x - 6)) * 0.8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Right ear
        ear_x_start = max(0, center_x + 1)
        ear_x_end = min(self.width, center_x + 6)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= ((center_x + 6) - x) * 0.8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat eyes - rotated
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['eyes'])  # Left eye
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['eyes'])  # Right eye
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['pupils'])  # Right pupil
        
        # Cat nose - rotated
        self.safe_set_pixel_rotated(center_x, center_y, self.colors['cat_pink'])
        
        # Cat mouth - rotated
        self.safe_set_pixel_rotated(center_x - 1, center_y + 2, self.colors['cat_black'])
        self.safe_set_pixel_rotated(center_x + 1, center_y + 2, self.colors['cat_black'])
        
        # Cat whiskers - rotated
        for i in range(3):
            self.safe_set_pixel_rotated(center_x - 5 - i, center_y, self.colors['cat_white'])  # Left whiskers
            self.safe_set_pixel_rotated(center_x + 5 + i, center_y, self.colors['cat_white'])  # Right whiskers
        
        # Cat body - rotated
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 12)
        body_x_start = max(0, center_x - 4)
        body_x_end = min(self.width, center_x + 5)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 8:
                    self.safe_set_pixel_rotated(x, y, self.colors['cat_orange'])
        
        # Cat tail (curved) - rotated
        tail_points = [
            (center_x + 6, center_y + 8),
            (center_x + 8, center_y + 6),
            (center_x + 10, center_y + 4),
            (center_x + 12, center_y + 2)
        ]
        for px, py in tail_points:
            self.safe_set_pixel_rotated(px, py, self.colors['cat_orange'])
    
    def create_dog_rotated(self):
        """Create a dog pattern rotated 180 degrees."""
        print("Creating rotated dog pattern...")
        self.led.clear()
        
        # Dog position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Dog head (rounder than cat) - rotated
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
        
        # Dog ears (floppy) - rotated
        ear_y_start = max(0, center_y - 10)
        ear_y_end = min(self.height, center_y - 1)
        ear_x_start = max(0, center_x - 8)
        ear_x_end = min(self.width, center_x - 2)
        
        # Left ear
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= (x - (center_x - 8)) * 0.6:
                    self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
        
        # Right ear
        ear_x_start = max(0, center_x + 2)
        ear_x_end = min(self.width, center_x + 8)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= ((center_x + 8) - x) * 0.6:
                    self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
        
        # Dog eyes (bigger than cat) - rotated
        self.safe_set_pixel_rotated(center_x - 4, center_y - 3, self.colors['eyes'])
        self.safe_set_pixel_rotated(center_x + 4, center_y - 3, self.colors['eyes'])
        self.safe_set_pixel_rotated(center_x - 4, center_y - 3, self.colors['pupils'])
        self.safe_set_pixel_rotated(center_x + 4, center_y - 3, self.colors['pupils'])
        
        # Dog nose (bigger) - rotated
        self.safe_set_pixel_rotated(center_x - 1, center_y, self.colors['dog_black'])
        self.safe_set_pixel_rotated(center_x, center_y, self.colors['dog_black'])
        self.safe_set_pixel_rotated(center_x + 1, center_y, self.colors['dog_black'])
        
        # Dog mouth (smile) - rotated
        self.safe_set_pixel_rotated(center_x - 2, center_y + 2, self.colors['dog_black'])
        self.safe_set_pixel_rotated(center_x - 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel_rotated(center_x + 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel_rotated(center_x + 2, center_y + 2, self.colors['dog_black'])
        
        # Dog body (larger than cat) - rotated
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 15)
        body_x_start = max(0, center_x - 6)
        body_x_end = min(self.width, center_x + 7)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 11:
                    self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
        
        # Dog legs - rotated
        leg_y_start = max(0, center_y + 15)
        leg_y_end = min(self.height, center_y + 20)
        
        for y in range(leg_y_start, leg_y_end):
            for x in range(max(0, center_x - 5), min(self.width, center_x - 2)):
                self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
            for x in range(max(0, center_x + 2), min(self.width, center_x + 5)):
                self.safe_set_pixel_rotated(x, y, self.colors['dog_brown'])
        
        # Dog tail (wagging) - rotated
        tail_points = [
            (center_x + 8, center_y + 10),
            (center_x + 10, center_y + 8),
            (center_x + 12, center_y + 6),
            (center_x + 14, center_y + 4)
        ]
        for px, py in tail_points:
            self.safe_set_pixel_rotated(px, py, self.colors['dog_brown'])
    
    def create_elephant_rotated(self):
        """Create an elephant pattern rotated 180 degrees."""
        print("Creating rotated elephant pattern...")
        self.led.clear()
        
        # Elephant position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Elephant head (large and round) - rotated
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 12
                dy = (y - center_y) / 10
                if dx*dx + dy*dy <= 1:
                    self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
        
        # Elephant trunk (long and curved) - rotated
        trunk_points = [
            (center_x, center_y + 2),
            (center_x, center_y + 4),
            (center_x, center_y + 6),
            (center_x, center_y + 8),
            (center_x, center_y + 10),
            (center_x, center_y + 12),
            (center_x - 1, center_y + 14),
            (center_x - 2, center_y + 16)
        ]
        for px, py in trunk_points:
            self.safe_set_pixel_rotated(px, py, self.colors['elephant_gray'])
        
        # Elephant eyes (small) - rotated
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['eyes'])
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['eyes'])
        self.safe_set_pixel_rotated(center_x - 3, center_y - 2, self.colors['pupils'])
        self.safe_set_pixel_rotated(center_x + 3, center_y - 2, self.colors['pupils'])
        
        # Elephant ears (large and floppy) - rotated
        ear_y_start = max(0, center_y - 12)
        ear_y_end = min(self.height, center_y - 2)
        ear_x_start = max(0, center_x - 10)
        ear_x_end = min(self.width, center_x - 2)
        
        # Left ear
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 12) >= (x - (center_x - 10)) * 0.5:
                    self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
        
        # Right ear
        ear_x_start = max(0, center_x + 2)
        ear_x_end = min(self.width, center_x + 10)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 12) >= ((center_x + 10) - x) * 0.5:
                    self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
        
        # Elephant body (very large) - rotated
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 20)
        body_x_start = max(0, center_x - 8)
        body_x_end = min(self.width, center_x + 9)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 16:
                    self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
        
        # Elephant legs (thick) - rotated
        leg_y_start = max(0, center_y + 20)
        leg_y_end = min(self.height, center_y + 25)
        
        for y in range(leg_y_start, leg_y_end):
            for x in range(max(0, center_x - 6), min(self.width, center_x - 3)):
                self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
            for x in range(max(0, center_x - 2), min(self.width, center_x + 1)):
                self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
            for x in range(max(0, center_x + 1), min(self.width, center_x + 4)):
                self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
            for x in range(max(0, center_x + 3), min(self.width, center_x + 6)):
                self.safe_set_pixel_rotated(x, y, self.colors['elephant_gray'])
    
    def display_animal_sequence_rotated(self, should_stop=None):
        """Display the sequence: cat -> dog -> elephant (rotated 180 degrees).
        
        Args:
            should_stop: Optional callback function that returns True if animation should stop.
        """
        print("🐱🐶🐘 Animal Sequence Animation (Rotated 180°) 🐱🐶🐘")
        print("Sequence: Cat (5s) -> Dog (5s) -> Elephant (5s)")
        
        try:
            # Display cat
            print("Displaying rotated Cat...")
            start_time = time.time()
            while time.time() - start_time < 5:
                # Check stop flag
                if should_stop and should_stop():
                    print("⚠️ Animal sequence interrupted by user")
                    return
                
                self.led.clear()
                self.create_cat_rotated()
                self.led.show()
                time.sleep(0.1)
            print("✅ Cat display completed!")
            
            # Check stop flag before continuing
            if should_stop and should_stop():
                print("⚠️ Animal sequence interrupted by user")
                return
            
            # Brief pause between animals (interruptible)
            pause_start = time.time()
            while time.time() - pause_start < 1.0:
                if should_stop and should_stop():
                    print("⚠️ Animal sequence interrupted by user")
                    return
                time.sleep(0.1)
            
            # Display dog
            print("Displaying rotated Dog...")
            start_time = time.time()
            while time.time() - start_time < 5:
                # Check stop flag
                if should_stop and should_stop():
                    print("⚠️ Animal sequence interrupted by user")
                    return
                
                self.led.clear()
                self.create_dog_rotated()
                self.led.show()
                time.sleep(0.1)
            print("✅ Dog display completed!")
            
            # Check stop flag before continuing
            if should_stop and should_stop():
                print("⚠️ Animal sequence interrupted by user")
                return
            
            # Brief pause between animals (interruptible)
            pause_start = time.time()
            while time.time() - pause_start < 1.0:
                if should_stop and should_stop():
                    print("⚠️ Animal sequence interrupted by user")
                    return
                time.sleep(0.1)
            
            # Display elephant
            print("Displaying rotated Elephant...")
            start_time = time.time()
            while time.time() - start_time < 5:
                # Check stop flag
                if should_stop and should_stop():
                    print("⚠️ Animal sequence interrupted by user")
                    return
                
                self.led.clear()
                self.create_elephant_rotated()
                self.led.show()
                time.sleep(0.1)
            print("✅ Elephant display completed!")
            
            print("🎉 Animal sequence (rotated) completed!")
            
        except KeyboardInterrupt:
            print("\n⚠️ Animal sequence interrupted by user")
        
        # Final clear
        self.led.clear()
        self.led.show()
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run rotated animal sequence animation."""
    try:
        animals = AnimalSequenceRotatedAnimation()
        animals.display_animal_sequence_rotated()
        animals.cleanup()
        
    except KeyboardInterrupt:
        print("\n⚠️ Animation interrupted by user")
        if 'animals' in locals():
            animals.cleanup()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'animals' in locals():
            animals.cleanup()

if __name__ == "__main__":
    main()

