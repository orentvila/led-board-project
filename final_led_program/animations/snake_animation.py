#!/usr/bin/env python3
"""
Snake Animation for LED Board
Features a snake that starts from the frame and moves inward step by step
"""

import time
import numpy as np
import random
from .base_animation import BaseAnimation
import config

class SnakeAnimation(BaseAnimation):
    def __init__(self, led_controller):
        """Initialize the snake animation."""
        super().__init__(led_controller)
        self.width = config.TOTAL_WIDTH  # 32
        self.height = config.TOTAL_HEIGHT  # 48
        
        # Colors
        self.colors = {
            'background': (0, 0, 0),        # Black background
            'snake_head': (255, 255, 0),     # Yellow head
            'snake_body': (0, 255, 0),       # Green body
            'snake_tail': (0, 200, 0),       # Darker green tail
            'food': (255, 0, 0),             # Red food
            'border': (100, 100, 100),        # Gray border
        }
        
        # Snake properties
        self.snake = []
        self.direction = (1, 0)  # Moving right initially
        self.food = None
        self.score = 0
        self.game_over = False
        
        # Animation parameters
        self.move_timer = 0
        self.move_delay = 0.3  # seconds between moves
        self.last_move_time = 0
        
        # Initialize snake starting from the border
        self.init_snake()
        self.spawn_food()
    
    def init_snake(self):
        """Initialize snake starting from the top border."""
        # Start from top-left corner, moving right
        start_x = 1
        start_y = 1
        
        # Create initial snake body (3 segments)
        self.snake = [
            (start_x, start_y),      # Head
            (start_x - 1, start_y),  # Body
            (start_x - 2, start_y),  # Tail
        ]
        
        self.direction = (1, 0)  # Moving right
        self.game_over = False
        self.score = 0
    
    def spawn_food(self):
        """Spawn food at a random location not occupied by snake."""
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def change_direction(self):
        """Change snake direction based on position and available moves."""
        head_x, head_y = self.snake[0]
        
        # Define possible directions
        directions = [
            (1, 0),   # Right
            (-1, 0),  # Left
            (0, 1),   # Down
            (0, -1),  # Up
        ]
        
        # Filter out directions that would cause immediate collision
        valid_directions = []
        for dx, dy in directions:
            new_x = head_x + dx
            new_y = head_y + dy
            
            # Check bounds
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                # Check if not hitting snake body (except tail)
                if (new_x, new_y) not in self.snake[:-1]:
                    valid_directions.append((dx, dy))
        
        # If no valid directions, try to avoid walls
        if not valid_directions:
            # Try to move towards center
            center_x = self.width // 2
            center_y = self.height // 2
            
            if head_x < center_x:
                self.direction = (1, 0)  # Move right
            elif head_x > center_x:
                self.direction = (-1, 0)  # Move left
            elif head_y < center_y:
                self.direction = (0, 1)  # Move down
            else:
                self.direction = (0, -1)  # Move up
        else:
            # Choose a random valid direction
            self.direction = random.choice(valid_directions)
    
    def move_snake(self):
        """Move the snake one step."""
        if self.game_over:
            return
        
        # Change direction occasionally
        if random.random() < 0.3:  # 30% chance to change direction
            self.change_direction()
        
        # Get new head position
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check for collisions
        new_x, new_y = new_head
        
        # Check bounds
        if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
            self.game_over = True
            return
        
        # Check if hitting snake body
        if new_head in self.snake[:-1]:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw_border(self, frame):
        """Draw the game border."""
        # Top and bottom borders
        for x in range(self.width):
            frame[0, x] = self.colors['border']
            frame[self.height - 1, x] = self.colors['border']
        
        # Left and right borders
        for y in range(self.height):
            frame[y, 0] = self.colors['border']
            frame[y, self.width - 1] = self.colors['border']
    
    def draw_snake(self, frame):
        """Draw the snake."""
        for i, (x, y) in enumerate(self.snake):
            if 0 <= x < self.width and 0 <= y < self.height:
                if i == 0:
                    # Head
                    frame[y, x] = self.colors['snake_head']
                elif i == len(self.snake) - 1:
                    # Tail
                    frame[y, x] = self.colors['snake_tail']
                else:
                    # Body
                    frame[y, x] = self.colors['snake_body']
    
    def draw_food(self, frame):
        """Draw the food."""
        if self.food:
            x, y = self.food
            if 0 <= x < self.width and 0 <= y < self.height:
                frame[y, x] = self.colors['food']
    
    def create_snake_frame(self):
        """Create a single frame of the snake animation."""
        frame = np.full((self.height, self.width, 3), self.colors['background'], dtype=np.uint8)
        
        # Draw border
        self.draw_border(frame)
        
        # Draw snake
        self.draw_snake(frame)
        
        # Draw food
        self.draw_food(frame)
        
        return frame
    
    def run(self, duration=30):
        """Run the snake animation."""
        print(f"🐍 Starting Snake animation for {duration} seconds...")
        
        start_time = time.time()
        frame_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            current_time = time.time()
            
            # Move snake at regular intervals
            if current_time - self.last_move_time >= self.move_delay:
                self.move_snake()
                self.last_move_time = current_time
                
                # Reset if game over
                if self.game_over:
                    print(f"🐍 Game Over! Score: {self.score}. Restarting...")
                    self.init_snake()
                    self.spawn_food()
            
            # Create frame
            frame = self.create_snake_frame()
            
            # Update LED display
            for y in range(self.height):
                for x in range(self.width):
                    color = frame[y, x]
                    self.led.set_pixel(x, y, color)
            
            self.led.show()
            
            frame_count += 1
            time.sleep(0.05)  # 20 FPS
        
        print(f"🐍 Snake animation completed ({frame_count} frames)")
        self.cleanup()
