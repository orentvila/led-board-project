#!/usr/bin/env python3
"""
Code Validation Helper
Checks for common errors before code is provided
"""

def validate_led_animation_code(code_string):
    """Validate LED animation code for common errors."""
    errors = []
    warnings = []
    
    # Check for undefined variables
    if 'self.width' in code_string and 'self.width =' not in code_string:
        errors.append("❌ 'self.width' used but not defined - use 'width = 32' instead")
    
    if 'self.height' in code_string and 'self.height =' not in code_string:
        errors.append("❌ 'self.height' used but not defined - use 'height = 48' instead")
    
    # Check for missing imports
    if 'random.' in code_string and 'import random' not in code_string:
        errors.append("❌ 'random' module used but not imported")
    
    if 'math.' in code_string and 'import math' not in code_string:
        errors.append("❌ 'math' module used but not imported")
    
    # Check for color values
    if 'RGB(' in code_string:
        warnings.append("⚠️ Check RGB color values are within 0-255 range")
    
    # Check for proper LED controller usage
    if 'self.led.set_pixel' in code_string and 'LEDControllerExact' not in code_string:
        warnings.append("⚠️ Ensure using LEDControllerExact for proper mapping")
    
    return errors, warnings

def validate_color_values(r, g, b):
    """Validate RGB color values."""
    if not (0 <= r <= 255):
        return f"❌ Red value {r} out of range (0-255)"
    if not (0 <= g <= 255):
        return f"❌ Green value {g} out of range (0-255)"
    if not (0 <= b <= 255):
        return f"❌ Blue value {b} out of range (0-255)"
    return "✅ Color values valid"

def check_common_led_errors():
    """Check for common LED animation errors."""
    common_errors = [
        "❌ Using self.width/self.height without defining them",
        "❌ Missing random or math imports",
        "❌ RGB values outside 0-255 range",
        "❌ Using old LEDController instead of LEDControllerExact",
        "❌ Not handling display boundaries properly",
        "❌ Missing error handling for edge cases"
    ]
    return common_errors

if __name__ == "__main__":
    print("🔍 Code Validation Helper")
    print("=" * 40)
    
    print("\nCommon LED Animation Errors to Avoid:")
    for error in check_common_led_errors():
        print(f"  {error}")
    
    print("\n✅ Always validate before providing code!")
