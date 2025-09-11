#!/usr/bin/env python3
"""
Fix import paths in all animation scripts
"""

import os
import re

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common import issues
        # Add project root to sys.path
        if 'import sys' not in content and ('led_controller' in content or 'config' in content):
            # Add sys.path modification after the shebang and docstring
            lines = content.split('\n')
            insert_index = 0
            
            # Find where to insert (after shebang and docstring)
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    insert_index = i
                    break
            
            # Insert sys.path modification
            lines.insert(insert_index, 'import sys')
            lines.insert(insert_index + 1, 'import os')
            lines.insert(insert_index + 2, 'sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))')
            lines.insert(insert_index + 3, '')
            
            content = '\n'.join(lines)
        
        # Fix led_controller_fixed imports
        content = content.replace('from led_controller_fixed import LEDControllerFixed', 'from led_controller_fixed import LEDControllerFixed')
        content = content.replace('LEDControllerFixed', 'LEDControllerFixed')
        
        # Fix led_controller imports
        content = content.replace('from led_controller import LEDController', 'from led_controller import LEDController')
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Fixed imports in {file_path}")
            return True
        else:
            print(f"ℹ️  No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix imports in all animation scripts."""
    scripts_folder = 'scripts'
    
    if not os.path.exists(scripts_folder):
        print("❌ Scripts folder not found!")
        return
    
    print("🔧 Fixing imports in animation scripts...")
    print("=" * 50)
    
    fixed_count = 0
    total_count = 0
    
    for file in os.listdir(scripts_folder):
        if file.endswith('_animation.py'):
            total_count += 1
            file_path = os.path.join(scripts_folder, file)
            if fix_imports_in_file(file_path):
                fixed_count += 1
    
    print("=" * 50)
    print(f"✅ Fixed {fixed_count} out of {total_count} animation scripts")

if __name__ == "__main__":
    main()
