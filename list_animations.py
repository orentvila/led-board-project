#!/usr/bin/env python3
"""
List all available animation scripts
"""

import os

def list_animations():
    """List all available animation scripts."""
    scripts_folder = 'scripts'
    
    if not os.path.exists(scripts_folder):
        print("❌ Scripts folder not found!")
        return
    
    print("🎬 Available Animation Scripts:")
    print("=" * 50)
    
    animation_scripts = []
    for file in os.listdir(scripts_folder):
        if file.endswith('_animation.py'):
            animation_scripts.append(file)
    
    animation_scripts.sort()
    
    for i, script in enumerate(animation_scripts, 1):
        print(f"{i:2d}. {script}")
    
    print("=" * 50)
    print(f"Total: {len(animation_scripts)} animation scripts")

if __name__ == "__main__":
    list_animations()
