#!/usr/bin/env python3
"""
Test imports for final program
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

print("🧪 Testing Imports")
print("=" * 20)

try:
    print("Testing button_controller import...")
    from button_controller import ButtonController
    print("✅ button_controller imported successfully")
except Exception as e:
    print(f"❌ button_controller import failed: {e}")

try:
    print("Testing led_controller import...")
    from led_controller import LEDController
    print("✅ led_controller imported successfully")
except Exception as e:
    print(f"❌ led_controller import failed: {e}")

try:
    print("Testing config import...")
    import config
    print("✅ config imported successfully")
    print(f"   Button pins: {config.BUTTON_PINS}")
    print(f"   LED pin: {config.LED_PIN}")
except Exception as e:
    print(f"❌ config import failed: {e}")

try:
    print("Testing Saturn animation import...")
    from themes.shapes.saturn_animation import SaturnAnimation
    print("✅ Saturn animation imported successfully")
except Exception as e:
    print(f"❌ Saturn animation import failed: {e}")

print("\n🎯 Import test completed!")
