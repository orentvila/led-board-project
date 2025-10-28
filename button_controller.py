import time
import threading
import sys
import config

# Use mock GPIO on Windows, real GPIO on Raspberry Pi
if sys.platform.startswith('win'):
    from mock_rpi import GPIO
    print("Using mock GPIO for Windows development")
else:
    import RPi.GPIO as GPIO

class ButtonController:
    def __init__(self):
        """Initialize button controller for 4 buttons."""
        self.buttons = {}
        self.button_callbacks = {}
        self.running = False
        self.button_thread = None
        
        # Setup GPIO with error handling
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
        except Exception as e:
            print(f"Error: 'GPIO busy' - {e}")
            print("Attempting to cleanup and retry...")
            try:
                GPIO.cleanup()
                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)
                print("✅ GPIO successfully reinitialized")
            except Exception as e2:
                print(f"Failed to reinitialize GPIO: {e2}")
                raise e2
        
        # Initialize buttons
        for i, pin in enumerate(config.BUTTON_PINS):
            self.buttons[i] = {
                'pin': pin,
                'state': False,
                'last_press': 0
            }
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def register_callback(self, button_id, callback):
        """Register a callback function for a button press."""
        if 0 <= button_id < len(config.BUTTON_PINS):
            self.button_callbacks[button_id] = callback
    
    def start_monitoring(self):
        """Start monitoring button presses in a separate thread."""
        if not self.running:
            self.running = True
            self.button_thread = threading.Thread(target=self._monitor_buttons)
            self.button_thread.daemon = True
            self.button_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring button presses."""
        self.running = False
        if self.button_thread:
            self.button_thread.join()
    
    def _monitor_buttons(self):
        """Monitor button presses in a loop."""
        while self.running:
            for button_id, button_info in self.buttons.items():
                current_state = GPIO.input(button_info['pin']) == GPIO.LOW
                current_time = time.time()
                
                # Detect button press with debouncing
                if (current_state and not button_info['state'] and 
                    current_time - button_info['last_press'] > config.BUTTON_DEBOUNCE_TIME):
                    
                    button_info['last_press'] = current_time
                    
                    # Call registered callback
                    if button_id in self.button_callbacks:
                        try:
                            self.button_callbacks[button_id]()
                        except Exception as e:
                            print(f"Error in button {button_id} callback: {e}")
                
                button_info['state'] = current_state
            
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    
    def get_button_state(self, button_id):
        """Get the current state of a button."""
        if 0 <= button_id < len(config.BUTTON_PINS):
            return GPIO.input(self.buttons[button_id]['pin']) == GPIO.LOW
        return False
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop_monitoring()
        GPIO.cleanup()

# Example button functions
def button_1_action():
    """Action for button 1."""
    print("Button 1 pressed - Starting rainbow pattern")
    # This will be connected to the main application

def button_2_action():
    """Action for button 2."""
    print("Button 2 pressed - Starting wave pattern")
    # This will be connected to the main application

def button_3_action():
    """Action for button 3."""
    print("Button 3 pressed - Starting text scroll")
    # This will be connected to the main application

def button_4_action():
    """Action for button 4."""
    print("Button 4 pressed - Starting fire effect")
    # This will be connected to the main application 