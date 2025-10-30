# Audio Setup Guide

The LED display application now supports audio for all animations! Here's how to set it up.

## Setup Instructions

### 1. Create Audio Directory

Create an `audio` folder in your project root directory:

```bash
mkdir audio
```

### 2. Add Audio Files

Place your audio files (`.wav` format recommended) in the `audio` folder with these exact names:

- `big_rectangle.wav` - Sound for the big rectangle animation
- `floating_clouds.wav` - Sound for floating clouds animation
- `rain.wav` - Sound for rain animation
- `growing_flowers.wav` - Sound for growing flowers animation
- `bubbles.wav` - Sound for bubbles animation
- `apple_tree.wav` - Sound for apple tree animation
- `house.wav` - Sound for house animation
- `clock.wav` - Sound for clock animation

### 3. Audio File Requirements

- **Format**: WAV format is recommended (pygame supports WAV, OGG, MP3, and others)
- **Sample Rate**: 22050 Hz (or standard rates like 44100 Hz)
- **Channels**: Mono or Stereo
- **Looping**: Audio files will loop automatically while the animation plays

### 4. Testing Audio

When you run an animation:
- If audio is available and the file exists, you'll see: `🔊 Playing audio for [animation_name]: [filename.wav]`
- If audio is disabled or file not found, you'll see a warning message but the animation will still work

### 5. Disabling Audio

Audio will automatically be disabled if:
- Pygame is not installed
- Audio initialization fails (e.g., no audio hardware)
- Audio files are missing (animation will still run)

The application will continue to work normally even if audio is unavailable.

## Adding New Animation Audio

To add audio for a new animation:

1. Add the audio file mapping in `main.py` in the `__init__` method:
   ```python
   self.animation_audio = {
       # ... existing mappings ...
       'new_animation': 'new_animation.wav',
   }
   ```

2. Add the audio playback call in the animation method:
   ```python
   def run_new_animation(self):
       self.play_animation_audio('new_animation')
       # ... rest of animation code ...
   ```

3. Place the audio file in the `audio` folder with the specified name.

## Troubleshooting

**Audio not playing:**
- Check that pygame is installed: `pip install pygame`
- Verify audio files exist in the `audio` folder
- Check file permissions on Raspberry Pi
- Ensure audio hardware is available (HDMI audio, 3.5mm jack, etc.)

**Audio format issues:**
- Convert files to WAV format using ffmpeg: `ffmpeg -i input.mp3 output.wav`
- Or use online converters to convert to WAV format

**Raspberry Pi audio:**
- Enable audio in `raspi-config`: `sudo raspi-config` → Advanced Options → Audio
- For HDMI audio, set `hdmi_drive=2` in `/boot/config.txt`
- For 3.5mm jack, ensure it's not muted: `alsamixer`

