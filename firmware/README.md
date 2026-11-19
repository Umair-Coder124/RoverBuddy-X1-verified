# Firmware: drive control and head simulation

**Untested on hardware; actuators disabled by default.** The drive starter and desktop head model are development tools, not a finished follow-me robot.

## Desktop checks

From the repository root:

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -v
```

Neither command accesses GPIO, serial devices or actuators. The simulation prints wheel outputs, rate-limited head angles, the command-timeout stop and rejection of an out-of-range pan target.

All 17 desktop tests passed: five drive tests and twelve head-model tests. These cover mixing/output bounds, malformed input, timeout behavior, angle limits, independent axis speed limits, endpoint reversal without wrapping, explicit stop, invalid timestamps and fresh-command recovery. Hardware behavior has not been tested.

## Desktop head-motion model

`HeadController` in `drive_logic.py` models requested angles and rate-limited movement. It assumes an initial neutral pose of (0°, 0°); those numbers are not measured actuator positions.

| Setting | Simulation default |
|---|---|
| Pan interval | −180° to +180° |
| Tilt interval | −30° to +30° |
| Maximum pan rate | 30°/s |
| Maximum tilt rate | 15°/s |
| Command watchdog | 400 ms |

The limits come from the CAD study assumptions, not a verified physical sweep. Configure narrower limits and suitable rates after mechanical and cable testing. The model does not account for acceleration, load, inertia, cable forces or servo dynamics.

Desktop model command:

```json
{"cmd":"head","armed":true,"pan_deg":30,"tilt_deg":10}
```

Both targets must be finite numbers inside the configured intervals. Booleans, strings, missing axes and invalid command types are rejected and disarm the model. An explicit `{"cmd":"stop"}` freezes its current simulated angles. Send fresh commands faster than the watchdog. If an update arrives late, the model advances only as far as the watchdog deadline, then freezes and requires a fresh armed command to move again.

Pan movement stays inside the configured interval. For example, +170° → −170° travels back through 0°; it does not take a short path across the ±180° boundary and add another cable turn.

This head command is accepted only by the desktop `HeadController`. It is **not** part of the Pico drive runtime's serial protocol. No XM430 packets, D645MW PWM output, physical position feedback, homing or hardware head-stop implementation is supplied. Freezing a simulated angle is not proof that real hardware stops or removes torque.

## Pico drive starter

The portable drive controller implements normalized mecanum mixing, bounded commands, a 20% provisional output limit and a 400 ms command watchdog. Malformed commands disarm it. Wheel direction and sign conventions are provisional. A software watchdog cannot replace hardware isolation or battery protection.

The MicroPython runtime expects `drive_logic.py`, `pico/config.py` and `pico/main.py` copied to the controller as `/drive_logic.py`, `/config.py`, `/main.py`. Do not enable the flags until the exact board pinmap, power circuit, independent hardware stop, wheel polarity and driver truth table are reviewed. No motor output pins are initialized while the flags remain false.

Proposed drive USB serial protocol, one JSON object per line:

```json
{"cmd":"drive","armed":true,"vx":0.1,"vy":0,"wz":0}
{"cmd":"stop"}
```

Drive axes must be finite numbers in −1..1. Fresh commands must arrive faster than the watchdog. There is no production host controller supplied and no approved procedure for operating the robot on the floor.

Still to implement and test: camera target selection/tracking, target-loss stop, obstacle detection and sensor-fault stop, chest UI, physical pan/tilt interfaces and position recovery, hardware-interlock status, calibration and recovery behavior. A manually armed drive command in this starter can move without obstacle sensing; do not treat it as autonomous or safety validated.

Reference: the manufacturer's [CytronMotorDriver library](https://github.com/CytronTechnologies/CytronMotorDriver) identifies MDD3A as a two-input PWM/PWM driver. Verify the actual board's connector labels and truth table.

