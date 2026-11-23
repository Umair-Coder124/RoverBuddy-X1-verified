# RoverBuddy X1 - Wiring & Pinout Guide 🔌

Here is how all the electronics on my rover are wired up and connected together.

## 1. Main Controllers & Power
- **Raspberry Pi 5 (The Brain):** Powered by the main 5V regulator. Handles camera input and high-level tracking logic.
- **Raspberry Pi Pico 2 (The Muscle):** Connected to the Pi 5 via USB Serial. Takes movement commands and controls the motor drivers directly.
- **Battery Pack:** Powers the system through step-down voltage regulators so the motors don't cause voltage drops on the Raspberry Pi.

---

## 2. Motor & Movement Connections (Pico 2)
The Pico 2 controls four DC motors attached to mecanum wheels via motor drivers:
- **Left Front Motor Driver:** Connected to Pico digital pins GP2 & GP3
- **Left Rear Motor Driver:** Connected to Pico digital pins GP4 & GP5
- **Right Front Motor Driver:** Connected to Pico digital pins GP6 & GP7
- **Right Rear Motor Driver:** Connected to Pico digital pins GP8 & GP9

---

## 3. Pan-and-Tilt Head & Sensors
- **Pan Servo (Dynamixel XM430):** Connected to serial/TTL bus with a separate regulated power line.
- **Tilt Servo (Hitec D645MW):** Connected to standard PWM pin on the Pico.
- **Ultrasonic Distance Sensor:**
  - `VCC` -> 5V
  - `GND` -> Ground
  - `Trig` -> Pico Pin 14
  - `Echo` -> Pico Pin 15 (with a voltage divider to protect the 3.3V pin!)
- **Chest Display:** Plugs directly into the Raspberry Pi 5 HDMI port.
