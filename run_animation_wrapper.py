#!/usr/bin/env python3
"""
Wrapper script to run animation scripts with correct Python path
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the animation script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 run_animation_wrapper.py <animation_script>")
        sys.exit(1)
    
    script_name = sys.argv[1]
    script_path = os.path.join(project_root, 'scripts', script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Animation script not found: {script_path}")
        sys.exit(1)
    
    # Execute the animation script
    try:
        exec(open(script_path).read())
    except Exception as e:
        print(f"❌ Error running animation: {e}")
        sys.exit(1)
