# How to Add Audio Files to Animations

This guide shows you how to add audio files to animations in the LED board project.

## Quick Steps

1. **Place audio file** in the `audio/` folder
2. **Add mapping** in `main.py` → `animation_audio` dictionary
3. **Add playback call** in the animation function

---

## Detailed Instructions

### Step 1: Place Your Audio File

1. Create an `audio` folder in your project root (if it doesn't exist):
   ```bash
   mkdir audio
   ```

2. Place your audio file in the `audio/` folder:
   - Supported formats: **WAV** (recommended), **MP3**, or **OGG**
   - Example: `audio/elephant.wav` or `audio/balloon.mp3`

### Step 2: Add Audio Mapping

Open `main.py` and find the `animation_audio` dictionary (around line 100):

```python
self.animation_audio = {
    'big_rectangle': 'big_rectangle.wav',
    'floating_clouds': 'floating_clouds.wav',
    'rain': 'rain.wav',
    # ... existing mappings ...
    'truck': 'truck.wav',
}
```

Add your new mapping:
```python
self.animation_audio = {
    # ... existing mappings ...
    'truck': 'truck.wav',
    'elephant': 'elephant.wav',        # NEW: Add this line
    'balloon': 'balloon.mp3',           # NEW: Add this line (MP3 example)
    'saturn': 'saturn.wav',             # NEW: Add this line
}
```

**Important:** The key (e.g., `'elephant'`) is what you'll use in Step 3.

### Step 3: Add Playback Call

Find where your animation is called and add `self.play_animation_audio('animation_name')` right before starting the animation.

#### Example 1: Adding Audio to Balloon Animation

**Current code** (around line 2395):
```python
elif self.current_object_index == 2:
    # Balloon animation
    self.animation_stop_flag = False
    self.objects_animation_running = True
    
    def should_stop():
        # ... stop callback ...
    
    from balloon_animation import BalloonAnimation
    animation = BalloonAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

**Updated code** (add the audio call):
```python
elif self.current_object_index == 2:
    # Balloon animation
    self.animation_stop_flag = False
    self.objects_animation_running = True
    
    # Play audio for this animation
    self.play_animation_audio('balloon')  # ADD THIS LINE
    
    def should_stop():
        # ... stop callback ...
    
    from balloon_animation import BalloonAnimation
    animation = BalloonAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

#### Example 2: Adding Audio to Elephant Animation

**Current code** (around line 1464):
```python
if animation_name == "elephant_bitmap":
    from elephant_bitmap_animation import ElephantBitmapAnimation
    animation = ElephantBitmapAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

**Updated code**:
```python
if animation_name == "elephant_bitmap":
    # Play audio for this animation
    self.play_animation_audio('elephant')  # ADD THIS LINE
    
    from elephant_bitmap_animation import ElephantBitmapAnimation
    animation = ElephantBitmapAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

#### Example 3: Adding Audio to Saturn Animation

**Current code** (around line 2414):
```python
elif self.current_object_index == 3:
    # Saturn animation
    self.animation_stop_flag = False
    self.objects_animation_running = True
    
    def should_stop():
        # ... stop callback ...
    
    from saturn_animation import SaturnAnimation
    animation = SaturnAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

**Updated code**:
```python
elif self.current_object_index == 3:
    # Saturn animation
    self.animation_stop_flag = False
    self.objects_animation_running = True
    
    # Play audio for this animation
    self.play_animation_audio('saturn')  # ADD THIS LINE
    
    def should_stop():
        # ... stop callback ...
    
    from saturn_animation import SaturnAnimation
    animation = SaturnAnimation()
    animation.run_animation(should_stop)
    animation.cleanup()
```

---

## Complete Example: Adding Audio to Horse Animation

Let's say you want to add `horse.wav` to the horse animation:

### 1. Place the file:
```
audio/horse.wav
```

### 2. Add to `animation_audio` dictionary (line ~100):
```python
self.animation_audio = {
    # ... existing ...
    'truck': 'truck.wav',
    'horse': 'horse.wav',  # ADD THIS
}
```

### 3. Add playback call (around line 1469):
```python
elif animation_name == "horse_bitmap":
    # Play audio for this animation
    self.play_animation_audio('horse')  # ADD THIS
    
    from horse_static_animation_bitmap import HorseStaticAnimationBitmap
    animation = HorseStaticAnimationBitmap()
    animation.run_animation(should_stop)
    animation.cleanup()
```

---

## Where to Find Animation Functions

- **Shapes animations**: `run_squares_animation()`, `run_triangles_animation()`, etc. (around line 1690)
- **Nature animations**: `run_floating_clouds()`, `run_rain_animation()`, etc. (around line 294)
- **Animals animations**: `run_animals_animation()` (around line 1453)
- **Objects animations**: `run_objects_animation()` (around line 2359)

---

## Testing

After adding audio:

1. Run your animation
2. Check console output:
   - ✅ Success: `🔊 Playing audio for [animation_name]: [filename.wav]`
   - ⚠️ File not found: `⚠️ Audio file not found: [path]`
   - ⚠️ No mapping: `⚠️ No audio mapped for animation: [animation_name]`

---

## Notes

- Audio files **loop automatically** while the animation plays
- Audio **stops automatically** when animation ends or is interrupted
- If the audio file doesn't exist, the animation will still work (you'll just see a warning)
- You can use **WAV, MP3, or OGG** formats - just make sure the extension matches in the dictionary

---

## Current Animations Without Audio

These animations currently don't have audio (you can add it!):

**Animals:**
- Elephant
- Horse
- Snail
- Deer
- Cat
- Jellyfish
- Birds

**Objects:**
- Balloon
- Saturn

