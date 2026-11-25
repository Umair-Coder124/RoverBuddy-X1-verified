# Planned wiring

These are the planned connections. The actual wiring still needs to be built and tested. Follow the [detailed wiring notes](../docs/WIRING.md) and have a qualified adult check the electrical setup before connecting power.

## Pi 5, Pico 2 and power
- **Raspberry Pi 5:** Powered by the main 5V regulator. Runs the camera and tracking software.
- **Raspberry Pi Pico 2:** Connected to the Pi 5 via USB Serial. Gets drive commands from the Pi and sends signals to the motor drivers.
- **Battery Pack:** Powers the system through separate regulated power branches.


## Motor pins on the Pico 2
The Pico 2 controls four DC motors attached to mecanum wheels via motor drivers:
- **Left Front Motor Driver:** Connected to Pico digital pins GP2 & GP3
- **Right Front Motor Driver:** Connected to Pico digital pins GP4 & GP5
- **Left Rear Motor Driver:** Connected to Pico digital pins GP6 & GP7
- **Right Rear Motor Driver:** Connected to Pico digital pins GP8 & GP9


## Head, sensor and display
- **Pan Servo (Dynamixel XM430):** Connected to serial/TTL bus with a separate regulated power line.
- **Tilt Servo (Hitec D645MW):** The planned PWM output is GP11 (physical pin 15). The signal interface still needs checking.
- **Ultrasonic Distance Sensor:**
  - `VCC` -> 5V
  - `GND` -> Ground
  - `Trig` -> GP12 (reserved)
  - `Echo` -> GP13 (reserved; level conversion still needs verification)
- **Chest Display:** Uses the Raspberry Pi 5 HDMI port and USB for touch.

The current Pico starter handles the proposed motor connections only. The code for turning the head and reading distance still needs to be written.
