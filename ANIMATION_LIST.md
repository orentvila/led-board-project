# LED Board Animation List

Complete list of all animations, their buttons, sequences, and durations.

## Button Mapping
- **Button 18 (Index 0)**: Shapes Animations
- **Button 17 (Index 1)**: Nature Animations  
- **Button 27 (Index 2)**: Animals Animations
- **Button 22 (Index 3)**: Objects Animations

---

## 🔷 Shapes Animations (Button 18)

**Sequence:** Cycles through 4 animations
1. **Squares** - 36 seconds total (33s main + 3s fade-out) | **Audio:** `squares.wav`
2. **Triangles** - 40 seconds total (37s main + 3s fade-out) | **Audio:** `triangles.wav`
3. **Bubbles** - 30 seconds | **Audio:** `bubbles.wav`
4. **Stars** - 40 seconds | **Audio:** `stars.wav`

**Details:**
- **Squares**: 16 squares appear randomly (one every 2 seconds), fade in over 1 second each, then fade out over 3 seconds
- **Triangles**: 12 triangles appear one by one (one every 3 seconds), fade in over 1 second each, then fade out over 3 seconds
- **Bubbles**: Bubbles rise from bottom with various sizes and colors
- **Stars**: 10 stars appear one by one (one every 4 seconds)

---

## 🌿 Nature Animations (Button 17)

**Sequence:** Cycles through 4 animations
1. **Floating Clouds** - 30 seconds | **Audio:** `floating_clouds.wav`
2. **Rain** - 30 seconds | **Audio:** `rain.wav`
3. **Growing Flowers** - 39 seconds (flowers grow sequentially + 5 seconds after last flower) | **Audio:** `growing_flowers.wav`
4. **Apple Tree** - Variable duration (apples grow sequentially, then fall) | **Audio:** `apple_tree.wav`

**Details:**
- **Floating Clouds**: Clouds drift across sky with gentle movement
- **Rain**: Raindrops fall from top to bottom
- **Growing Flowers**: Multiple flowers grow from ground sequentially
- **Apple Tree**: Tree grows, apples appear, then fall one by one

---

## 🐾 Animals Animations (Button 27)

**Sequence:** Cycles through 8 animations
1. **Elephant** - 20 seconds (moves from left to center in 8s, then stays) | **Audio:** `elephant.wav`
2. **Whale** - 12 seconds (12 frames shown twice) | **Audio:** `whale.wav`
3. **Horse** - 30 seconds | **Audio:** None
4. **Snail** - 30 seconds | **Audio:** None
5. **Deer** - 30 seconds | **Audio:** None
6. **Cat** - 20 seconds | **Audio:** None
7. **Jellyfish** - 5 seconds | **Audio:** None
8. **Birds** - 5 seconds | **Audio:** None

**Details:**
- **Elephant**: Moves horizontally from left side to center, stops at center with dimmed sky, sun, and clouds
- **Whale**: Whale animation with 12 frames, each shown twice, white background dimmed 40%
- **Horse**: Moves across screen with leg animation
- **Snail**: Moves slowly across ground
- **Deer**: Static bitmap animation
- **Cat**: Cat animation
- **Jellyfish**: Short jellyfish animation
- **Birds**: Short birds animation

---

## 🎯 Objects Animations (Button 22)

**Sequence:** Cycles through 4 animations
1. **Truck** - 20 seconds (moves from left to right across screen) | **Audio:** `truck.wav`
2. **House** - 20 seconds (house with smoke rising from chimney) | **Audio:** `house.wav`
3. **Balloon** - 20 seconds (rises from bottom to top) | **Audio:** None
4. **Saturn** - 30 seconds (rotating planet with rings and stars) | **Audio:** `saturn.wav`

**Details:**
- **Truck**: Red truck (#E74D49) moves across gray ground (#7B7B7B) with dimmed blue sky and sun
- **House**: Orange house with red roof, blue windows, and white smoke rising
- **Balloon**: Hot air balloon rises from bottom of screen to top
- **Saturn**: Planet with rotating rings, stars in background

---

## Summary by Duration

### 5 seconds
- Jellyfish (Animals)
- Birds (Animals)

### 20 seconds
- Elephant (Animals)
- Cat (Animals)
- Truck (Objects)
- House (Objects)
- Balloon (Objects)

### 36 seconds
- Squares (Shapes) - includes fade-out

### 40 seconds
- Triangles (Shapes) - includes fade-out
- Stars (Shapes)

### 30 seconds
- Horse (Animals)
- Snail (Animals)
- Deer (Animals)
- Bubbles (Shapes)
- Floating Clouds (Nature)
- Rain (Nature)
- Saturn (Objects)

### 36 seconds
- Squares (Shapes) - includes fade-out

### 39 seconds
- Growing Flowers (Nature)

### Variable Duration
- Apple Tree (Nature) - depends on number of apples

---

## Notes

- Each button press cycles to the next animation in the sequence
- Animations can be stopped by pressing another button
- Audio files are located in the `audio/` folder in the project directory
- **Audio formats supported**: WAV (recommended), MP3, and OGG files all work
- Audio files loop continuously while their animation is playing
- Audio stops automatically when animation ends or is interrupted
- All animations use `should_stop` callback for graceful termination
- Ground height is typically 4 pixels for ground-based animations

## Audio Files Summary

**Animations with Audio:**
- Shapes: Squares, Triangles, Bubbles, Stars
- Nature: Floating Clouds, Rain, Growing Flowers, Apple Tree
- Objects: Truck, House, Saturn
- Animals: Elephant

**Animations without Audio:**
- Animals: Horse, Snail, Deer, Cat, Jellyfish, Birds
- Objects: Balloon

