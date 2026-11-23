# Robot code

The software is still being developed on a computer. The physical robot has not been tested.

| File | Purpose |
| --- | --- |
| `drive_logic.py` | Wheel speeds, stop and timeout logic, and simulated head movement. |
| `simulate.py` | Desktop examples and recorded-video detection. |
| `pico/main.py` | Motor-control starter for the Pico. |
| `pico/config.py` | Proposed pin settings and hardware enable flags. |
| `tests/` | Desktop tests. |

## Run on a computer

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -v
```

The desktop demo and 77 tests passed on November 23. They use simulated inputs and mocked hardware. Recorded-video detection is optional and uses OpenCV.

## What is left

- Real camera and sensor inputs, Pi-to-Pico integration and phone controls.
- Actual motor direction, camera head movement and stopping tests.
- Keep the Pico hardware flags off until the power, wiring and independent stop circuit are checked with qualified adult supervision.

The [full firmware reference](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/firmware/README.md) contains the command format, test details, video options and safety limits.
