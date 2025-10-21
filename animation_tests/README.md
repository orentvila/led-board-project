# Animation Scripts

This folder contains all the LED display animation scripts for the Raspberry Pi project.

## Available Animations

- `animal_sequence_animation.py` - Animal sequence animation
- `big_shapes_animation.py` - Big shapes animation
- `black_hole_animation.py` - Black hole animation
- `bubbles_animation.py` - Bubbles animation
- `calming_ambient_animation.py` - Calming ambient animation
- `car_driving_animation.py` - Car driving animation
- `dudi_paddleboarding_animation.py` - Dudi paddleboarding animation
- `gravity_bend_animation.py` - Gravity bend animation
- `music_instruments_animation.py` - Music instruments animation
- `saturn_animation.py` - Saturn animation
- `shapes_animation.py` - Shapes animation
- `shark_animation.py` - Shark animation
- `ship_sailing_animation.py` - Ship sailing animation
- `squares_animation.py` - 24 squares animation (6 rows × 4 columns)
- `star_animation.py` - Star animation
- `tree_growing_animation.py` - Tree growing animation
- `tree_growth_animation.py` - Tree growth animation

## Usage

### Run Random Animation
```bash
sudo ./venv/bin/python random_animation_controller.py
```

### Run Specific Animation
```bash
sudo ./venv/bin/python scripts/<animation_name>.py
```

### List All Animations
```bash
python3 list_animations.py
```

## Button Control

- **GPIO 18**: Press to start random animation
- **Ctrl+C**: Stop current animation and exit

## Adding New Animations

1. Create your animation script with `_animation.py` suffix
2. Place it in this `scripts/` folder
3. The random controller will automatically detect it
4. Make sure your script has a `main()` function for standalone execution
