#!/usr/bin/env python3
"""
Base Animation Class for LED Board
All animations should inherit from this class
"""

import time
import threading
from abc import ABC, abstractmethod

class BaseAnimation(ABC):
    """Base class for all LED animations."""
    
    def __init__(self, led_controller):
        """Initialize the animation with LED controller."""
        self.led = led_controller
        self.running = False
        self.thread = None
        
    @abstractmethod
    def run(self, duration=30):
        """Run the animation for specified duration in seconds."""
        pass
    
    def start(self, duration=30):
        """Start the animation in a separate thread."""
        if self.running:
            self.stop()
        
        self.running = True
        self.thread = threading.Thread(target=self.run, args=(duration,))
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """Stop the animation."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
    
    def cleanup(self):
        """Clean up resources."""
        self.stop()
        if hasattr(self.led, 'cleanup'):
            self.led.cleanup()
