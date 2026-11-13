# Firmware: drive-control starter

**Untested on hardware; actuators disabled by default.** This is a starting implementation, not the finished follow-me robot.

Run `python3 firmware/simulate.py` from the repository root for a desktop simulation. Run `python3 -m unittest discover -s firmware/tests` for controller tests. Neither operation accesses hardware.

The portable controller implements normalized mecanum mixing, bounded commands, a 20% provisional output limit and a 400 ms command watchdog. Malformed commands disarm it. Wheel direction and sign conventions are provisional. A software watchdog cannot replace hardware isolation or battery protection.

The MicroPython runtime expects `drive_logic.py`, `pico/config.py` and `pico/main.py` copied to the controller as `/drive_logic.py`, `/config.py`, `/main.py`. Do not enable the flags until the exact board pinmap, power circuit, independent hardware stop, wheel polarity and driver truth table are reviewed. No motor output pins are initialized while the flags remain false.

Proposed USB serial protocol, one JSON object per line:
```
{"cmd":"drive","armed":true,"vx":0.1,"vy":0,"wz":0}
{"cmd":"stop"}
```
Axes must be finite numbers in -1..1. Fresh commands must arrive faster than the watchdog. There is no production host controller supplied and no approved procedure for operating the robot on the floor.

Still to implement and test: camera target selection/tracking, target-loss stop, obstacle detection and sensor-fault stop, chest UI, neck servo control and travel limits, hardware-interlock status, calibration and recovery behavior. A manually armed drive command in this starter can move without obstacle sensing; do not treat it as autonomous or safety validated.

Reference: the manufacturer's [CytronMotorDriver library](https://github.com/CytronTechnologies/CytronMotorDriver) identifies MDD3A as a two-input PWM/PWM driver, not PWM/DIR. Verify the actual board's connector labels and truth table.
