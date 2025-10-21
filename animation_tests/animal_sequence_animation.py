#!/usr/bin/env python3
"""
Animal Sequence Animation for LED Board
Shows cat, dog, and elephant in sequence
"""

import time
import numpy as np
from led_controller_fixed import LEDControllerFixed
import config

class AnimalSequenceAnimation:
    def __init__(self):
        """Initialize the animal sequence animation."""
        self.led = LEDControllerFixed()
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
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        else:
            print(f"Warning: Pixel out of bounds ({x}, {y}) - bounds: 0-{self.width-1}, 0-{self.height-1}")
        
    def create_cat(self):
        """Create a cat pattern."""
        print("Creating cat pattern...")
        cat = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Cat position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        print(f"Cat center: ({center_x}, {center_y})")
        
        # Cat head (oval shape)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 8
                dy = (y - center_y) / 6
                if dx*dx + dy*dy <= 1:
                    cat[y, x] = self.colors['cat_orange']
        
        # Cat ears (triangular) - with strict bounds checking
        # Left ear
        ear_y_start = max(0, center_y - 8)
        ear_y_end = min(self.height, center_y - 2)
        ear_x_start = max(0, center_x - 6)
        ear_x_end = min(self.width, center_x - 1)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= (x - (center_x - 6)) * 0.8:
                    cat[y, x] = self.colors['cat_orange']
        
        # Right ear
        ear_x_start = max(0, center_x + 1)
        ear_x_end = min(self.width, center_x + 6)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 8) >= ((center_x + 6) - x) * 0.8:
                    cat[y, x] = self.colors['cat_orange']
        
        # Cat eyes
        self.safe_set_pixel(cat, center_x - 3, center_y - 2, self.colors['eyes'])  # Left eye
        self.safe_set_pixel(cat, center_x + 3, center_y - 2, self.colors['eyes'])  # Right eye
        self.safe_set_pixel(cat, center_x - 3, center_y - 2, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel(cat, center_x + 3, center_y - 2, self.colors['pupils'])  # Right pupil
        
        # Cat nose
        self.safe_set_pixel(cat, center_x, center_y, self.colors['cat_pink'])
        
        # Cat mouth
        self.safe_set_pixel(cat, center_x - 1, center_y + 2, self.colors['cat_black'])
        self.safe_set_pixel(cat, center_x + 1, center_y + 2, self.colors['cat_black'])
        
        # Cat whiskers
        for i in range(3):
            self.safe_set_pixel(cat, center_x - 5 - i, center_y, self.colors['cat_white'])  # Left whiskers
            self.safe_set_pixel(cat, center_x + 5 + i, center_y, self.colors['cat_white'])  # Right whiskers
        
        # Cat body - with strict bounds checking
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 12)
        body_x_start = max(0, center_x - 4)
        body_x_end = min(self.width, center_x + 5)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 8:
                    cat[y, x] = self.colors['cat_orange']
        
        # Cat tail (curved)
        tail_points = [
            (center_x + 6, center_y + 8),
            (center_x + 8, center_y + 6),
            (center_x + 10, center_y + 4),
            (center_x + 12, center_y + 2)
        ]
        for px, py in tail_points:
            self.safe_set_pixel(cat, px, py, self.colors['cat_orange'])
        
        print("Cat pattern created successfully")
        return cat
    
    def create_dog(self):
        """Create a dog pattern."""
        print("Creating dog pattern...")
        dog = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Dog position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Dog head (rounder than cat)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 10
                dy = (y - center_y) / 8
                if dx*dx + dy*dy <= 1:
                    dog[y, x] = self.colors['dog_brown']
        
        # Dog ears (floppy) - with strict bounds checking
        ear_y_start = max(0, center_y - 10)
        ear_y_end = min(self.height, center_y - 1)
        ear_x_start = max(0, center_x - 8)
        ear_x_end = min(self.width, center_x - 2)
        
        # Left ear
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= (x - (center_x - 8)) * 0.6:
                    dog[y, x] = self.colors['dog_brown']
        
        # Right ear
        ear_x_start = max(0, center_x + 2)
        ear_x_end = min(self.width, center_x + 8)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 10) >= ((center_x + 8) - x) * 0.6:
                    dog[y, x] = self.colors['dog_brown']
        
        # Dog eyes (bigger than cat)
        self.safe_set_pixel(dog, center_x - 4, center_y - 3, self.colors['eyes'])  # Left eye
        self.safe_set_pixel(dog, center_x + 4, center_y - 3, self.colors['eyes'])  # Right eye
        self.safe_set_pixel(dog, center_x - 4, center_y - 3, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel(dog, center_x + 4, center_y - 3, self.colors['pupils'])  # Right pupil
        
        # Dog nose (bigger)
        self.safe_set_pixel(dog, center_x - 1, center_y, self.colors['dog_black'])
        self.safe_set_pixel(dog, center_x, center_y, self.colors['dog_black'])
        self.safe_set_pixel(dog, center_x + 1, center_y, self.colors['dog_black'])
        
        # Dog mouth (smile)
        self.safe_set_pixel(dog, center_x - 2, center_y + 2, self.colors['dog_black'])
        self.safe_set_pixel(dog, center_x - 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel(dog, center_x + 1, center_y + 3, self.colors['dog_black'])
        self.safe_set_pixel(dog, center_x + 2, center_y + 2, self.colors['dog_black'])
        
        # Dog body (larger than cat) - with strict bounds checking
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 15)
        body_x_start = max(0, center_x - 6)
        body_x_end = min(self.width, center_x + 7)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 11:
                    dog[y, x] = self.colors['dog_brown']
        
        # Dog legs - with strict bounds checking
        leg_y_start = max(0, center_y + 15)
        leg_y_end = min(self.height, center_y + 20)
        
        for y in range(leg_y_start, leg_y_end):
            for x in range(max(0, center_x - 5), min(self.width, center_x - 2)):  # Front left
                dog[y, x] = self.colors['dog_brown']
            for x in range(max(0, center_x + 2), min(self.width, center_x + 5)):  # Front right
                dog[y, x] = self.colors['dog_brown']
        
        # Dog tail (wagging)
        tail_points = [
            (center_x + 8, center_y + 10),
            (center_x + 10, center_y + 8),
            (center_x + 12, center_y + 6),
            (center_x + 14, center_y + 4)
        ]
        for px, py in tail_points:
            self.safe_set_pixel(dog, px, py, self.colors['dog_brown'])
        
        print("Dog pattern created successfully")
        return dog
    
    def create_elephant(self):
        """Create an elephant pattern."""
        print("Creating elephant pattern...")
        elephant = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Elephant position (centered)
        center_x = self.width // 2
        center_y = self.height // 2
        
        # Elephant head (large and round)
        for y in range(self.height):
            for x in range(self.width):
                dx = (x - center_x) / 12
                dy = (y - center_y) / 10
                if dx*dx + dy*dy <= 1:
                    elephant[y, x] = self.colors['elephant_gray']
        
        # Elephant trunk (long and curved)
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
            self.safe_set_pixel(elephant, px, py, self.colors['elephant_gray'])
        
        # Elephant eyes (small)
        self.safe_set_pixel(elephant, center_x - 3, center_y - 2, self.colors['eyes'])  # Left eye
        self.safe_set_pixel(elephant, center_x + 3, center_y - 2, self.colors['eyes'])  # Right eye
        self.safe_set_pixel(elephant, center_x - 3, center_y - 2, self.colors['pupils'])  # Left pupil
        self.safe_set_pixel(elephant, center_x + 3, center_y - 2, self.colors['pupils'])  # Right pupil
        
        # Elephant ears (large and floppy) - with strict bounds checking
        ear_y_start = max(0, center_y - 12)
        ear_y_end = min(self.height, center_y - 2)
        ear_x_start = max(0, center_x - 10)
        ear_x_end = min(self.width, center_x - 2)
        
        # Left ear
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 12) >= (x - (center_x - 10)) * 0.5:
                    elephant[y, x] = self.colors['elephant_gray']
        
        # Right ear
        ear_x_start = max(0, center_x + 2)
        ear_x_end = min(self.width, center_x + 10)
        
        for y in range(ear_y_start, ear_y_end):
            for x in range(ear_x_start, ear_x_end):
                if y - (center_y - 12) >= ((center_x + 10) - x) * 0.5:
                    elephant[y, x] = self.colors['elephant_gray']
        
        # Elephant body (very large) - with strict bounds checking
        body_y_start = max(0, center_y + 4)
        body_y_end = min(self.height, center_y + 20)
        body_x_start = max(0, center_x - 8)
        body_x_end = min(self.width, center_x + 9)
        
        for y in range(body_y_start, body_y_end):
            for x in range(body_x_start, body_x_end):
                if (y - center_y - 4) <= 16:
                    elephant[y, x] = self.colors['elephant_gray']
        
        # Elephant legs (thick) - with strict bounds checking
        leg_y_start = max(0, center_y + 20)
        leg_y_end = min(self.height, center_y + 25)
        
        for y in range(leg_y_start, leg_y_end):
            for x in range(max(0, center_x - 6), min(self.width, center_x - 3)):  # Front left
                elephant[y, x] = self.colors['elephant_gray']
            for x in range(max(0, center_x - 2), min(self.width, center_x + 1)):  # Front right
                elephant[y, x] = self.colors['elephant_gray']
            for x in range(max(0, center_x + 1), min(self.width, center_x + 4)):  # Back left
                elephant[y, x] = self.colors['elephant_gray']
            for x in range(max(0, center_x + 3), min(self.width, center_x + 6)):  # Back right
                elephant[y, x] = self.colors['elephant_gray']
        
        print("Elephant pattern created successfully")
        return elephant
    
    def display_animal(self, animal_pattern, animal_name, duration=5):
        """Display an animal for a specified duration."""
        print(f"Displaying {animal_name} for {duration} seconds...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Display the animal pattern
            for y in range(self.height):
                for x in range(self.width):
                    color = animal_pattern[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            time.sleep(0.1)  # 10 FPS
        
        print(f"{animal_name} display completed!")
    
    def display_animal_sequence(self):
        """Display the sequence: cat -> dog -> elephant."""
        print("🐱🐶🐘 Animal Sequence Animation 🐱🐶🐘")
        print("Sequence: Cat (5s) -> Dog (5s) -> Elephant (5s)")
        
        try:
            # Create animal patterns
            cat = self.create_cat()
            dog = self.create_dog()
            elephant = self.create_elephant()
            
            # Display cat
            self.display_animal(cat, "Cat", 5)
            
            # Brief pause between animals
            print("Transitioning to dog...")
            time.sleep(1)
            
            # Display dog
            self.display_animal(dog, "Dog", 5)
            
            # Brief pause between animals
            print("Transitioning to elephant...")
            time.sleep(1)
            
            # Display elephant
            self.display_animal(elephant, "Elephant", 5)
            
            print("Animal sequence completed!")
            
        except KeyboardInterrupt:
            print("\nAnimal sequence interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run animal sequence animation."""
    try:
        animals = AnimalSequenceAnimation()
        animals.display_animal_sequence()
        animals.cleanup()
        
    except KeyboardInterrupt:
        print("\nAnimal sequence interrupted by user")
        animals.cleanup()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        animals.cleanup()

if __name__ == "__main__":
    main() 