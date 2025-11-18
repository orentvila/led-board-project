# Audio Setup Guide

The LED display application now supports audio for all animations! Here's how to set it up.

## Setup Instructions

### 1. Create Audio Directory

Create an `audio` folder in your project root directory:

```bash
mkdir audio
```

### 2. Add Audio Files

Place your audio files in the `audio` folder. You can use **WAV, MP3, or OGG** formats. The file names should match exactly:

- `big_rectangle.wav` (or `.mp3`, `.ogg`) - Sound for the big rectangle animation
- `floating_clouds.wav` (or `.mp3`, `.ogg`) - Sound for floating clouds animation
- `rain.wav` (or `.mp3`, `.ogg`) - Sound for rain animation
- `growing_flowers.wav` (or `.mp3`, `.ogg`) - Sound for growing flowers animation
- `bubbles.wav` (or `.mp3`, `.ogg`) - Sound for bubbles animation
- `apple_tree.wav` (or `.mp3`, `.ogg`) - Sound for apple tree animation
- `house.wav` (or `.mp3`, `.ogg`) - Sound for house animation
- `clock.wav` (or `.mp3`, `.ogg`) - Sound for clock animation
- `truck.wav` (or `.mp3`, `.ogg`) - Sound for truck animation

**Format Options:**
- **WAV**: Recommended - Always supported, no codecs needed, best compatibility
- **MP3**: Supported - Smaller file size, may require codecs on some systems
- **OGG**: Supported - Good compression, open format

**Note:** You can use any of these formats. WAV files are recommended for best compatibility, but MP3 and OGG work great too. Just update the file extension in `main.py` if you use a different format.

### 3. Audio File Requirements

- **Format**: **WAV (recommended), MP3, or OGG** - All formats are supported by pygame
  - **WAV**: Recommended - Always supported, no codecs needed, best compatibility
  - **MP3**: Supported - Smaller file size, may require codecs on some systems
  - **OGG**: Supported - Good compression, open format
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
       'new_animation': 'new_animation.wav',  # or .mp3, .ogg
   }
   ```
   
   **Note:** You can use `.mp3` or `.ogg` extensions directly:
   ```python
       'new_animation': 'new_animation.mp3',  # MP3 format
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
- **MP3 support**: MP3 files should work directly. If MP3 doesn't work on Raspberry Pi, install MP3 support:
  ```bash
  sudo apt-get install mpg123
  ```
- **Converting formats**: Convert files using ffmpeg:
  - MP3 to WAV: `ffmpeg -i input.mp3 output.wav`
  - WAV to MP3: `ffmpeg -i input.wav -acodec libmp3lame output.mp3`
- Or use online converters to convert between formats

**Raspberry Pi audio:**
- Enable audio in `raspi-config`: `sudo raspi-config` → Advanced Options → Audio
- For HDMI audio, set `hdmi_drive=2` in `/boot/config.txt`
- For 3.5mm jack, ensure it's not muted: `alsamixer`

