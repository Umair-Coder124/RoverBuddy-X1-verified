# Robot code

The software is still being developed on a computer. The physical robot has not been tested.

| File | Purpose |
| --- | --- |
| `drive_logic.py` | Wheel speeds, stop and timeout logic. Start here. |
| `desktop_models.py` | Simulated head movement, tilt calculations and follow-mode checks. |
| `simulate.py` | Desktop examples and recorded-video detection. |
| `pico/main.py` | Motor-control starter for the Pico. |
| `pico/config.py` | Proposed pin settings and hardware enable flags. |
| `tests/` | Desktop tests. |

The Pico only needs the drive module for the current motor-control starter. The desktop model stays on the computer.

## How the code works

- Wheel mixing: `vx` is forward/backward, `vy` is sideways and `wz` is turning. The mix function calculates four wheel speeds.
- Timeout: if the drive controller gets no new command for over 400 ms, it requests zero wheel speed.
- Resume: after stopping, a valid command with an explicit resume is needed to start moving again.
- Head movement: the computer model shows how pan and tilt angles change within limits. Real servos are still to be tested.
- Follow mode: the desktop model uses simulated sensor readings to check stops when a target is lost, an obstacle is close, or readings are missing.

## Development

AI assistance was used to design, write, simplify and test the firmware, including the stop and resume logic. The next step for me is to study the code and test it independently as I build the robot.

## Run on a computer

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -v
```

The desktop demo and 77 tests passed again on November 24, 2026, after separating the drive and desktop models. They use simulated inputs and mocked hardware. Recorded-video detection is optional and uses OpenCV.

## What is left

- Real camera and sensor inputs, Pi-to-Pico integration and phone controls.
- Actual motor direction, camera head movement and stopping tests.
- Keep the Pico hardware flags off until the power, wiring and independent stop circuit are checked with qualified adult supervision.

The [full firmware reference](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/firmware/README.md) contains the command format, test details, video options and safety limits.
