# Wiring draft — engineering review required

This diagram shows the intended architecture. It is not a validated electrical schematic. Do not wire or energize the robot from this diagram alone.

## Power architecture

The selected assembled 3S battery reaches 12.6 V fully charged. A suitably rated fuse, disconnect, automatic low-voltage protection and hardware drive isolation must be specified before the power distribution is finalized. The current emergency-stop candidate is not approved to interrupt battery current directly.

Separate branches feed the Pi power module, 6 V servo regulator and 6 V motor regulator. All signal interfaces require a common reference ground; separate positive rails must not be joined. Regulator mounting, current limits, cooling and transient suppression are unverified. Four selected motors can draw approximately 6 A combined at stall, above the selected motor regulator's nominal 5.5 A rating. Resolve that mismatch.

The Pi supplies HDMI to the display, USB for touch/audio, CSI for the camera and USB data to the Pico. Confirm total USB power demand. Avoid backfeeding power through USB during external-power development. The Pico power arrangement must follow the exact board documentation; the selected third-party board pinout has not been verified.

## Proposed logical GPIO allocation

These are logical GP identifiers, not physical header positions. Check the purchased board and driver labels before connecting anything.

| Function | Input A | Input B |
|---|---|---|
| Front-left motor, driver 1 channel 1 | GP2 | GP3 |
| Front-right motor, driver 1 channel 2 | GP4 | GP5 |
| Rear-left motor, driver 2 channel 1 | GP6 | GP7 |
| Rear-right motor, driver 2 channel 2 | GP8 | GP9 |

The MDD3A uses two control inputs per motor. This starter uses one PWM input at a time for forward/reverse; it does not assume a PWM/DIR interface. Actual wheel polarity and correct left/right wheel placement must be calibrated with the robot lifted.

GP10/GP11 are reserved for future pan/tilt signals, and GP12/GP13 for future ultrasonic trigger/echo. No servo or ultrasonic implementation is included in this drive starter. Do not feed a 5 V echo directly into 3.3 V GPIO: the exact level-conversion circuit remains to be designed and verified. GP14 is reserved for a future hardware-interlock status input; reading that input in software would not itself provide a hardware stop.

## Motor driver 1 — front wheels

| Controller or motor connection | Cytron MDD3A driver 1 |
|---|---|
| Controller GP2 | M1A signal input |
| Controller GP3 | M1B signal input |
| Controller GP4 | M2A signal input |
| Controller GP5 | M2B signal input |
| Controller signal ground | GND on the signal header |
| Front-left motor, two leads | Motor 1 output terminal pair |
| Front-right motor, two leads | Motor 2 output terminal pair |
| No connection | 5VO |
| Motor supply positive and return | VB+ and VB− respectively, pending power design |

Match the GP labels against the exact controller board before assigning physical header pin numbers. Keep the hardware unpowered until the power design and protection are verified.

[Cytron MDD3A datasheet, board layout and functions](https://www.electrokit.com/upload/product/41018/41018266/MDD3A%20Datasheet.pdf)

## Unresolved before operation

- Battery cutoff thresholds and circuit, hardware stop, fuse and switch ratings at 12.6 V.
- Motor regulator sizing, cable ratings, connectors, grounding and power sequencing.
- Actual board pinout, safe startup levels, wheel polarity and mecanum orientation.
- Ultrasonic level conversion, sensor failure behavior, servo rail and mechanical travel limits.
- Complete pin-to-pin schematic, connector numbering and power budget.

References: [Cytron manufacturer library](https://github.com/CytronTechnologies/CytronMotorDriver) documents the MDD3A-compatible PWM/PWM mode; [Raspberry Pi microcontroller documentation](https://www.raspberrypi.com/documentation/microcontrollers/) covers supported official boards. Neither reference establishes compatibility of an unverified third-party controller.
