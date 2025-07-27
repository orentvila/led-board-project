# Hardware Setup Guide

This guide explains how to connect your 5 LED panels and 4 buttons to the Raspberry Pi 4.

## LED Panels Setup

### Components Required
- 5x WS2812B LED panels (32x8 pixels each)
- Raspberry Pi 4
- 5V power supply (adequate for WS2812B LEDs)
- Jumper wires
- Breadboard (optional, for testing)

### LED Panel Specifications
- **Type**: WS2812B
- **Panel Size**: 32x8 pixels (256 LEDs per panel)
- **Total LEDs**: 1,280 LEDs (5 panels × 256 LEDs)
- **Voltage**: 5V
- **Data Protocol**: Single-wire protocol
- **Current**: ~60mA per LED at full brightness

### Power Requirements
- **Total Current**: Up to 76.8A at full brightness (1,280 LEDs × 60mA)
- **Recommended Power Supply**: 5V, 80A or higher
- **For Testing**: Start with lower brightness (30% or less)

### Wiring Diagram

```
Raspberry Pi 4          LED Panels
┌─────────────┐        ┌─────────┬─────────┬─────────┬─────────┬─────────┐
│             │        │ Panel 1 │ Panel 2 │ Panel 3 │ Panel 4 │ Panel 5 │
│ GPIO 21 ────┼────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │         │
│ GND ────────┼────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │         │
└─────────────┘        └─────────┴─────────┴─────────┴─────────┴─────────┘
                                │         │         │         │         │
                                │         │         │         │         │
                                ▼         ▼         ▼         ▼         ▼
                           5V Power Supply (80A+)
```

### Connection Details

1. **Data Line**: Connect GPIO 21 to the DIN (Data In) of the first panel
2. **Power**: Connect 5V power supply to VCC of all panels
3. **Ground**: Connect GND from power supply and Raspberry Pi to GND of all panels
4. **Data Chain**: Connect DOUT (Data Out) of each panel to DIN of the next panel

### Important Notes
- **Power Supply**: Use a separate 5V power supply for the LEDs, not the Raspberry Pi's 5V
- **Ground Connection**: Ensure the Raspberry Pi and LED power supply share a common ground
- **Data Line**: Use a short, shielded cable for the data line to reduce interference
- **Power Distribution**: Distribute power evenly across all panels

## Button Setup (Future Implementation)

### Components Required
- 4x Push buttons
- 4x 10kΩ pull-up resistors
- Jumper wires
- Breadboard

### Button Pin Assignment
| Button | GPIO Pin | Function |
|--------|----------|----------|
| Button 1 | GPIO 17 | Rainbow pattern |
| Button 2 | GPIO 18 | Wave pattern |
| Button 3 | GPIO 27 | Text scroll |
| Button 4 | GPIO 22 | Fire effect |

### Button Wiring Diagram

```
Raspberry Pi 4          Buttons
┌─────────────┐        ┌─────────┬─────────┬─────────┬─────────┐
│             │        │ Button1 │ Button2 │ Button3 │ Button4 │
│ GPIO 17 ────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
│ GPIO 18 ────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
│ GPIO 27 ────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
│ GPIO 22 ────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
│ 3.3V ───────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
│ GND ────────┼────────┼─────────┼─────────┼─────────┼─────────┤
│             │        │         │         │         │         │
└─────────────┘        └─────────┴─────────┴─────────┴─────────┴─────────┘
```

### Button Connection Details

For each button:
1. Connect one terminal to the corresponding GPIO pin
2. Connect the other terminal to GND
3. Connect a 10kΩ resistor between the GPIO pin and 3.3V (pull-up resistor)

## Testing Setup

### Step 1: Basic LED Test
1. Connect only the first LED panel
2. Run the test script: `python test_display.py`
3. Verify the panel lights up correctly

### Step 2: Add More Panels
1. Add panels one by one
2. Test after each addition
3. Verify the total display works correctly

### Step 3: Button Test (When Connected)
1. Connect buttons according to the diagram
2. Run the main application: `python main.py`
3. Test each button function

## Troubleshooting

### Common Issues

1. **LEDs Not Lighting Up**
   - Check power supply voltage (should be 5V)
   - Verify ground connections
   - Check data line connection
   - Ensure GPIO 21 is not used by other services

2. **Intermittent LED Issues**
   - Check for loose connections
   - Verify power supply capacity
   - Check for electromagnetic interference

3. **Wrong Colors or Patterns**
   - Verify LED strip orientation
   - Check data line connections
   - Ensure proper power supply

4. **Buttons Not Responding**
   - Check GPIO pin assignments
   - Verify pull-up resistors
   - Check button connections

### Power Supply Recommendations

- **For Testing**: 5V, 10A power supply
- **For Full Display**: 5V, 80A+ power supply
- **For Production**: Multiple 5V, 20A power supplies distributed across panels

### Safety Notes

- **Never exceed 5V** on the LED data or power lines
- **Use appropriate wire gauge** for high current applications
- **Ensure proper ventilation** for power supplies
- **Test with low brightness first** to avoid overloading
- **Disconnect power** before making wiring changes 