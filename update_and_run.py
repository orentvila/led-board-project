#!/usr/bin/env python3
"""
Update and Run Script
Pulls latest changes from git and runs the main application
"""

import subprocess
import os
import sys
import time

def git_pull():
    """Pull latest changes from git repository."""
    try:
        print("🔄 Checking for updates...")
        
        # Get the current directory
        current_dir = os.getcwd()
        print(f"Current directory: {current_dir}")
        
        # Check if this is a git repository
        if not os.path.exists('.git'):
            print("❌ Not a git repository")
            return False
        
        # Fetch latest changes
        print("📡 Fetching latest changes...")
        result = subprocess.run(['git', 'fetch'], 
                              capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode != 0:
            print(f"❌ Git fetch failed: {result.stderr}")
            return False
        
        # Check if we're behind the remote
        result_behind = subprocess.run(['git', 'rev-list', 'HEAD..origin/main', '--count'], 
                                     capture_output=True, text=True, cwd=current_dir)
        
        if result_behind.returncode == 0 and result_behind.stdout.strip() != '0':
            commits_behind = int(result_behind.stdout.strip())
            print(f"📦 Found {commits_behind} new commits, pulling updates...")
            
            # Pull the changes
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  capture_output=True, text=True, cwd=current_dir)
            
            if result.returncode == 0:
                print("✅ Successfully updated from git repository!")
                print("📝 Changes pulled:")
                print(result.stdout)
                return True
            else:
                print(f"❌ Git pull failed: {result.stderr}")
                return False
        else:
            print("✅ Already up to date!")
            return False
            
    except Exception as e:
        print(f"❌ Error during git update: {e}")
        return False

def run_main_app():
    """Run the main application."""
    try:
        print("🚀 Starting LED Display Application...")
        result = subprocess.run(['python', 'main.py'], cwd=os.getcwd())
        return result.returncode
    except Exception as e:
        print(f"❌ Error running main application: {e}")
        return 1

def main():
    """Main function."""
    print("=" * 50)
    print("🔄 LED Display - Update and Run")
    print("=" * 50)
    
    # Pull updates
    updated = git_pull()
    
    if updated:
        print("\n🔄 Updates found! Restarting with new code...")
        time.sleep(2)
    
    # Run the main application
    print("\n" + "=" * 50)
    exit_code = run_main_app()
    
    if exit_code != 0:
        print(f"\n❌ Application exited with code {exit_code}")
    else:
        print("\n✅ Application completed successfully")

if __name__ == "__main__":
    main() 