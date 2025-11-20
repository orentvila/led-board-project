#!/usr/bin/env python3
"""
Audio Test Script
Tests audio playback to diagnose issues
"""

import os
import sys

print("=" * 60)
print("Audio System Diagnostic Test")
print("=" * 60)

# Test 1: Check if pygame is available
print("\n1. Checking pygame availability...")
try:
    import pygame
    print("✅ Pygame is installed")
    print(f"   Pygame version: {pygame.version.ver}")
except ImportError:
    print("❌ Pygame is NOT installed")
    print("   Install with: pip install pygame")
    sys.exit(1)

# Test 2: Initialize pygame mixer
print("\n2. Initializing pygame mixer...")
try:
    pygame.mixer.init()
    print("✅ Pygame mixer initialized")
    mixer_info = pygame.mixer.get_init()
    if mixer_info:
        print(f"   Frequency: {mixer_info[0]} Hz")
        print(f"   Format: {mixer_info[1]}")
        print(f"   Channels: {mixer_info[2]}")
    else:
        print("⚠️ Mixer initialized but get_init() returned None")
except Exception as e:
    print(f"❌ Failed to initialize mixer: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check audio directory
print("\n3. Checking audio directory...")
script_dir = os.path.dirname(os.path.abspath(__file__))
audio_dir = os.path.join(script_dir, 'audio')
if os.path.exists(audio_dir):
    print(f"✅ Audio directory exists: {audio_dir}")
    audio_files = os.listdir(audio_dir)
    if audio_files:
        print(f"   Found {len(audio_files)} audio file(s):")
        for f in audio_files[:10]:  # Show first 10
            print(f"     - {f}")
        if len(audio_files) > 10:
            print(f"     ... and {len(audio_files) - 10} more")
    else:
        print("⚠️ Audio directory is empty")
else:
    print(f"❌ Audio directory not found: {audio_dir}")
    print(f"   Create it with: mkdir {audio_dir}")

# Test 4: Try to play a test file
print("\n4. Testing audio playback...")
if os.path.exists(audio_dir):
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(('.wav', '.mp3', '.ogg'))]
    if audio_files:
        test_file = audio_files[0]
        test_path = os.path.join(audio_dir, test_file)
        print(f"   Trying to play: {test_file}")
        try:
            pygame.mixer.music.load(test_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            print(f"✅ Audio file loaded and play() called")
            
            import time
            time.sleep(0.2)  # Give it time to start
            
            if pygame.mixer.music.get_busy():
                print(f"✅ Audio is playing! (get_busy() = True)")
                print(f"   Playing for 2 seconds...")
                time.sleep(2)
                pygame.mixer.music.stop()
                print(f"✅ Audio playback test successful!")
            else:
                print(f"❌ Audio not playing (get_busy() = False)")
                print(f"   This usually means:")
                print(f"   - Audio output device not configured")
                print(f"   - On Raspberry Pi: Run 'sudo raspi-config' -> Advanced Options -> Audio")
                print(f"   - Or set audio output: 'export SDL_AUDIODRIVER=alsa'")
                print(f"   - Or try: 'export SDL_AUDIODRIVER=pulse'")
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ No audio files found to test")

# Test 5: Check environment variables
print("\n5. Checking environment variables...")
env_vars = ['SDL_AUDIODRIVER', 'AUDIODEV', 'PULSE_RUNTIME_PATH']
for var in env_vars:
    value = os.environ.get(var)
    if value:
        print(f"   {var} = {value}")
    else:
        print(f"   {var} = (not set)")

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print("\nIf audio is not working, try:")
print("1. On Raspberry Pi: sudo raspi-config -> Advanced Options -> Audio")
print("2. Set audio driver: export SDL_AUDIODRIVER=alsa")
print("3. Check audio output: aplay /usr/share/sounds/alsa/Front_Left.wav")
print("4. Test with pygame: python test_audio.py")

