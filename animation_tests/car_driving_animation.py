#!/usr/bin/env python3
"""
Car Driving Animation for LED Board
A calm 20-second animation of a car driving smoothly across the screen
"""

import time
import numpy as np
from led_controller_exact import LEDControllerExact
import config

class CarDrivingAnimation:
    def __init__(self):
        """Initialize the car driving animation."""
        self.led = LEDControllerExact()
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        print(f"Display dimensions: {self.width}x{self.height}")
        
        # Colors - peaceful and calming
        self.colors = {
            'background': (20, 40, 60),      # Dark blue sky
            'road': (60, 60, 60),            # Gray road
            'road_line': (120, 120, 120),    # Light gray road line
            'car_body': (100, 150, 200),     # Blue car body
            'car_windows': (180, 220, 255),  # Light blue windows
            'car_wheels': (30, 30, 30),      # Dark wheels
            'car_lights': (255, 255, 200),   # Soft yellow lights
            'grass': (40, 80, 40)            # Dark green grass
        }
        
        # Animation timing (20 seconds total)
        self.total_duration = 20.0
        self.car_speed = 0.5  # pixels per second - slow and steady
        
        # Car dimensions
        self.car_width = 6
        self.car_height = 4
        self.wheel_radius = 1
        
    def safe_set_pixel(self, array, x, y, color):
        """Safely set a pixel if coordinates are within bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            array[y, x] = color
        
    def create_background(self):
        """Create the background with sky, road, and grass."""
        background = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Create road (horizontal strip in middle)
        road_y = self.height // 2
        road_height = 8
        
        for y in range(road_y - road_height//2, road_y + road_height//2):
            for x in range(self.width):
                background[y, x] = self.colors['road']
        
        # Add road line
        line_y = road_y
        for x in range(0, self.width, 4):  # Dashed line
            if x + 2 < self.width:
                background[line_y, x] = self.colors['road_line']
                background[line_y, x + 1] = self.colors['road_line']
        
        # Add grass at bottom
        grass_start_y = road_y + road_height//2
        for y in range(grass_start_y, self.height):
            for x in range(self.width):
                background[y, x] = self.colors['grass']
        
        return background
    
    def create_car(self, car_x, wheel_rotation=0):
        """Create a simple car at the given position."""
        car = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Car position
        car_y = self.height // 2 - 2  # Slightly above road center
        
        # Car body (rectangle)
        for y in range(car_y, car_y + self.car_height):
            for x in range(car_x, car_x + self.car_width):
                if 0 <= x < self.width and 0 <= y < self.height:
                    car[y, x] = self.colors['car_body']
        
        # Car windows (smaller rectangle on top)
        window_y = car_y + 1
        window_width = 4
        window_x = car_x + 1
        for y in range(window_y, window_y + 2):
            for x in range(window_x, window_x + window_width):
                if 0 <= x < self.width and 0 <= y < self.height:
                    car[y, x] = self.colors['car_windows']
        
        # Car lights (front and back)
        # Front light
        if car_x + self.car_width < self.width:
            car[car_y + 1, car_x + self.car_width] = self.colors['car_lights']
        # Back light
        if car_x > 0:
            car[car_y + 1, car_x - 1] = self.colors['car_lights']
        
        # Wheels (circles)
        # Front wheel
        front_wheel_x = car_x + 1
        front_wheel_y = car_y + self.car_height
        self.draw_wheel(car, front_wheel_x, front_wheel_y, wheel_rotation)
        
        # Back wheel
        back_wheel_x = car_x + self.car_width - 2
        back_wheel_y = car_y + self.car_height
        self.draw_wheel(car, back_wheel_x, back_wheel_y, wheel_rotation)
        
        return car
    
    def draw_wheel(self, car, center_x, center_y, rotation):
        """Draw a wheel with rotation animation."""
        for y in range(center_y - self.wheel_radius, center_y + self.wheel_radius + 1):
            for x in range(center_x - self.wheel_radius, center_x + self.wheel_radius + 1):
                # Check if pixel is within wheel circle
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                if distance <= self.wheel_radius:
                    # Add rotation effect with a small dot
                    if abs(x - center_x) <= 0.5 and abs(y - center_y) <= 0.5:
                        car[y, x] = (100, 100, 100)  # Wheel hub
                    else:
                        car[y, x] = self.colors['car_wheels']
    
    def run_animation(self):
        """Run the complete car driving animation."""
        print("🚗 Car Driving Animation 🚗")
        print("Duration: 20 seconds")
        print("A peaceful car driving across the screen")
        
        start_time = time.time()
        
        try:
            while True:
                current_time = time.time() - start_time
                
                # Calculate car position
                car_x = int(current_time * self.car_speed)
                
                # Calculate wheel rotation (for visual effect)
                wheel_rotation = int(current_time * 10) % 4
                
                # Create background
                frame = self.create_background()
                
                # Add car if it's still on screen
                if car_x < self.width + self.car_width:
                    car = self.create_car(car_x, wheel_rotation)
                    
                    # Combine background and car
                    for y in range(self.height):
                        for x in range(self.width):
                            if not np.array_equal(car[y, x], self.colors['background']):
                                frame[y, x] = car[y, x]
                
                # Display the frame
                for y in range(self.height):
                    for x in range(self.width):
                        self.led.set_pixel(x, y, frame[y, x])
                
                self.led.show()
                
                # Check if animation is complete
                if current_time >= self.total_duration:
                    print("Car driving animation completed!")
                    break
                
                time.sleep(0.05)  # 20 FPS for smooth animation
                
        except KeyboardInterrupt:
            print("\nCar driving animation interrupted by user")
    
    def cleanup(self):
        """Clean up resources."""
        self.led.cleanup()

def main():
    """Main function to run car driving animation."""
    try:
        car_driving = CarDrivingAnimation()
        car_driving.run_animation()
        car_driving.cleanup()
        
    except KeyboardInterrupt:
        print("\nCar driving animation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 