#!/usr/bin/env python3
"""
Test script for Windows development environment
"""

import sys
import time

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        import config
        print("✓ config imported successfully")
    except Exception as e:
        print(f"✗ config import failed: {e}")
        return False
    
    try:
        from led_controller import LEDController
        print("✓ LEDController imported successfully")
    except Exception as e:
        print(f"✗ LEDController import failed: {e}")
        return False
    
    try:
        from button_controller import ButtonController
        print("✓ ButtonController imported successfully")
    except Exception as e:
        print(f"✗ ButtonController import failed: {e}")
        return False
    
    try:
        from display_patterns import DisplayPatterns
        print("✓ DisplayPatterns imported successfully")
    except Exception as e:
        print(f"✗ DisplayPatterns import failed: {e}")
        return False
    
    return True

def test_led_controller():
    """Test LED controller functionality."""
    print("\nTesting LED controller...")
    
    try:
        from led_controller import LEDController
        
        led = LEDController()
        print("✓ LED controller initialized")
        
        # Test basic operations
        led.set_pixel(0, 0, (255, 0, 0))  # Red pixel
        print("✓ set_pixel() works")
        
        led.fill_panel(0, (0, 255, 0))  # Green panel
        print("✓ fill_panel() works")
        
        led.clear()
        print("✓ clear() works")
        
        led.cleanup()
        print("✓ cleanup() works")
        
        return True
    except Exception as e:
        print(f"✗ LED controller test failed: {e}")
        return False

def test_button_controller():
    """Test button controller functionality."""
    print("\nTesting button controller...")
    
    try:
        from button_controller import ButtonController
        
        buttons = ButtonController()
        print("✓ Button controller initialized")
        
        # Test callback registration
        def test_callback():
            print("Button callback triggered!")
        
        buttons.register_callback(0, test_callback)
        print("✓ callback registration works")
        
        buttons.start_monitoring()
        print("✓ monitoring started")
        
        time.sleep(0.1)  # Brief pause
        
        buttons.stop_monitoring()
        print("✓ monitoring stopped")
        
        buttons.cleanup()
        print("✓ cleanup() works")
        
        return True
    except Exception as e:
        print(f"✗ Button controller test failed: {e}")
        return False

def test_display_patterns():
    """Test display patterns functionality."""
    print("\nTesting display patterns...")
    
    try:
        from led_controller import LEDController
        from display_patterns import DisplayPatterns
        
        led = LEDController()
        patterns = DisplayPatterns(led)
        print("✓ Display patterns initialized")
        
        # Test a simple pattern
        patterns.stop()  # Ensure clean state
        print("✓ stop() works")
        
        led.cleanup()
        print("✓ cleanup() works")
        
        return True
    except Exception as e:
        print(f"✗ Display patterns test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Windows Development Environment Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_led_controller,
        test_button_controller,
        test_display_patterns
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Windows development environment is ready.")
        print("\nYou can now:")
        print("- Run 'python main.py' to see the demo")
        print("- Develop and test your LED patterns")
        print("- Use the mock modules for development")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 