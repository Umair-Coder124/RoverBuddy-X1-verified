# Planned wiring

These are the planned connections. The actual wiring still needs to be built and tested. Follow the [detailed wiring notes](../docs/WIRING.md) and have a qualified adult check the electrical setup before connecting power.

## Pi 5, Pico 2 and power
- **Raspberry Pi 5:** Powered by the main 5V regulator. Runs the camera and tracking software.
- **Raspberry Pi Pico 2:** Connected to the Pi 5 via USB Serial. Gets drive commands from the Pi and sends signals to the motor drivers.
- **Battery Pack:** Powers the system through separate regulated power branches.


## Motor pins on the Pico 2
The Pico 2 sends signals to four motor channels on two MDD3A driver boards:
- **Left Front motor channel:** Connected to Pico digital pins GP2 & GP3
- **Right Front motor channel:** Connected to Pico digital pins GP4 & GP5
- **Left Rear motor channel:** Connected to Pico digital pins GP6 & GP7
- **Right Rear motor channel:** Connected to Pico digital pins GP8 & GP9


## Head, sensor and display
- **Camera Module 3:** Planned 500 mm ribbon cable to the Pi 5 camera connector.
- **Pan Servo (Dynamixel XM430):** Pi USB to U2D2, then the TTL bus through the Power Hub. The separate regulated 12 V supply still needs checking.
- **Tilt Servo (Hitec D645MW):** The planned PWM output is GP11 (physical pin 15). The signal interface still needs checking.
- **Ultrasonic Distance Sensor:**
  - `VCC` -> 5V
  - `GND` -> Ground
  - `Trig` -> GP12 (reserved)
  - `Echo` -> planned GP13 through level conversion (reserved; check the interface before connecting)
- **Interlock status:** GP14 is reserved. The independent stop circuit still needs checking.
- **Chest Display:** Uses the Raspberry Pi 5 HDMI port and USB for touch.

The current Pico starter handles the proposed motor connections only. The code for turning the head and reading distance still needs to be written.
