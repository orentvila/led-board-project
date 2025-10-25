#!/usr/bin/env python3
"""
Script to fix import statements in animation test files.
"""

import os
import glob

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace the import statement
        if 'from led_controller_fixed import LEDControllerFixed' in content:
            content = content.replace(
                'from led_controller_fixed import LEDControllerFixed',
                'from led_controller_exact import LEDControllerExact'
            )
            content = content.replace(
                'LEDControllerFixed()',
                'LEDControllerExact()'
            )
            
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all animation test files."""
    print("🔧 Fixing animation test imports...")
    
    # Find all Python files in animation_tests directory
    animation_files = glob.glob("animation_tests/*.py")
    
    fixed_count = 0
    for file_path in animation_files:
        if fix_imports_in_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")
    print("🎉 All animation test files should now work!")

if __name__ == "__main__":
    main()
