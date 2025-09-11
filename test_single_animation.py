#!/usr/bin/env python3
"""
Test a single animation script directly
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_animation(script_name):
    """Test a specific animation script."""
    print(f"🧪 Testing animation: {script_name}")
    
    try:
        script_path = os.path.join(project_root, 'scripts', script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ Script not found: {script_path}")
            return False
        
        print(f"📁 Script path: {script_path}")
        print("▶️  Running animation...")
        
        # Execute the script
        exec(open(script_path).read())
        
        print("✅ Animation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_single_animation.py <animation_script>")
        print("Example: python3 test_single_animation.py squares_animation.py")
        sys.exit(1)
    
    script_name = sys.argv[1]
    success = test_animation(script_name)
    sys.exit(0 if success else 1)
