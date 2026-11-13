# Wiring draft — engineering review required

This diagram shows the intended architecture. It is not a validated electrical schematic. Do not wire or energize the robot from this diagram alone.

## Power architecture

The selected assembled 3S battery reaches 12.6 V fully charged. A suitably rated fuse, disconnect, automatic low-voltage protection and hardware drive isolation must be specified before the power distribution is finalized. The current emergency-stop candidate is not approved to interrupt battery current directly.

The revised power design budgets two independent 6 V motor rails, one per MDD3A, plus separate supplies for the servos and Raspberry Pi. Each motor rail uses one Pololu D36V50F6 and serves two Adafruit 3777 motors. At the vendor's measured 1.5 A stall per motor at 6 V, that is 3 A per rail compared with the regulator's typical 5.5 A rating. Treat this as a sizing estimate. Verify the regulator's available current across pack voltage and operating temperature, plus startup transients and supply faults. Keep the two 6 V positives separate. Use a common signal-ground reference. Battery protection, hardware drive isolation, wiring ratings, and hardware testing remain open.

- Front regulator output → driver 1 VB+ and VB− via its own positive and return.
- Rear regulator output → driver 2 VB+ and VB− via its own positive and return.
- The raw battery supply stays upstream of both regulators and their pending protection. Keep the drive unpowered until protection and wiring have been reviewed.

[Adafruit motor measurements](https://www.adafruit.com/product/3777) · [Pololu regulator specs and current curves](https://www.pololu.com/product/4092)

The Pi supplies HDMI to the display, USB for touch/audio, CSI for the camera and USB data to the Pico. Confirm total USB power demand. Avoid backfeeding power through USB during external-power development. The design now specifies the official Raspberry Pi Pico 2 with Headers (SC1632), using a USB-A to Micro-B data cable for the Pi-to-controller link.

## Proposed logical GPIO allocation

These physical pin numbers are for the official Raspberry Pi Pico 2 with Headers (SC1632). Identify the board orientation using the [official pinout](https://pip-assets.raspberrypi.com/categories/1005-raspberry-pi-pico-2/documents/RP-008301-DS-1-Pico-2-Pinout.pdf?disposition=inline) and confirm the labels on the purchased hardware.

| Function | Input A | Input B |
|---|---|---|
| Front-left motor, driver 1 channel 1 | GP2 (pin 4) | GP3 (pin 5) |
| Front-right motor, driver 1 channel 2 | GP4 (pin 6) | GP5 (pin 7) |
| Rear-left motor, driver 2 channel 1 | GP6 (pin 9) | GP7 (pin 10) |
| Rear-right motor, driver 2 channel 2 | GP8 (pin 11) | GP9 (pin 12) |

The MDD3A uses two control inputs per motor. This starter uses one PWM input at a time for forward/reverse; it does not assume a PWM/DIR interface. Actual wheel polarity and correct left/right wheel placement must be calibrated with the robot lifted.

GP10/GP11 are reserved for future pan/tilt signals, and GP12/GP13 for future ultrasonic trigger/echo. No servo or ultrasonic implementation is included in this drive starter. Do not feed a 5 V echo directly into 3.3 V GPIO: the exact level-conversion circuit remains to be designed and verified. GP14 is reserved for a future hardware-interlock status input; reading that input in software would not itself provide a hardware stop.

## Motor driver 1 — front wheels

| Controller or motor connection | Cytron MDD3A driver 1 |
|---|---|
| Controller GP2 (pin 4) | M1A signal input |
| Controller GP3 (pin 5) | M1B signal input |
| Controller GP4 (pin 6) | M2A signal input |
| Controller GP5 (pin 7) | M2B signal input |
| Controller signal ground (Pico 2 pin 8) | GND on the signal header |
| Front-left motor, two leads | Motor 1 output terminal pair |
| Front-right motor, two leads | Motor 2 output terminal pair |
| No connection | 5VO |
| Motor supply positive and return | VB+ and VB− respectively, proposed separate 6 V rail, pending protection and bench verification |

Confirm the hardware matches the selected SC1632 and the pin numbers above. Keep the hardware unpowered until the power design and protection are verified.

[Cytron MDD3A datasheet, board layout and functions](https://www.electrokit.com/upload/product/41018/41018266/MDD3A%20Datasheet.pdf)

## Motor driver 2 — rear wheels

| Controller or motor connection | Cytron MDD3A driver 2 |
|---|---|
| Controller GP6 (pin 9) | M1A signal input |
| Controller GP7 (pin 10) | M1B signal input |
| Controller GP8 (pin 11) | M2A signal input |
| Controller GP9 (pin 12) | M2B signal input |
| Controller signal ground (Pico 2 pin 8) | GND on the signal header |
| Rear-left motor, two leads | Motor 1 output terminal pair |
| Rear-right motor, two leads | Motor 2 output terminal pair |
| No connection | 5VO |
| Motor supply positive and return | VB+ and VB− respectively, proposed separate 6 V rail, pending protection and bench verification |

Use the same controller pinout and power checks listed for driver 1 before connecting or powering the hardware.

## Unresolved before operation

- Battery cutoff thresholds and circuit, hardware stop, fuse and switch ratings at 12.6 V.
- Motor regulator bench validation, cable ratings, connectors, grounding and power sequencing.
- Physical board identity, safe startup levels, wheel polarity and mecanum orientation.
- Ultrasonic level conversion, sensor failure behavior, servo rail and mechanical travel limits.
- Complete pin-to-pin schematic, connector numbering and power budget.

References: [Cytron manufacturer library](https://github.com/CytronTechnologies/CytronMotorDriver) documents the MDD3A-compatible PWM/PWM mode; [Raspberry Pi microcontroller documentation](https://www.raspberrypi.com/documentation/microcontrollers/) covers supported official boards. The pin assignments above apply to the official Pico 2.
