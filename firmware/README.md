# Robot code

The code is being tested on a computer. The robot still needs to be built and tested with real parts.

## Start here

- `drive_logic.py` works out the four wheel speeds and handles stop commands.
- `simulate.py` prints examples of forward, sideways and turning movement.
- `pico/main.py` is the motor starter for the Pico 2. Its hardware flags are off until the wiring and power checks are complete.

`desktop_models.py` and `desktop_experiments.py` are desktop experiments for the moving head, follow mode and recorded video. They are not needed on the Pico.

## Try it on a computer

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -p test_drive.py -v
```

The drive tests check mixing, timeout, resume, bad commands. If a command stops arriving for over 400 ms, wheel output goes to zero. The next movement needs `armed=true` and `resume=true`.

## Optional desktop experiments

Run `python3 firmware/simulate.py --full` to see what happens when a target disappears or a sensor stops sending readings. The extra tests in `firmware/tests/extra/` also check the Pico loop with pretend motors. Run all tests with `python3 -m unittest discover -s firmware/tests -v`.

## Still to do

- Finish the camera, sensor, phone controls and Pi-to-Pico connection.
- Test motor directions, stopping and the moving head with real parts.
- Keep hardware outputs disabled until the power, wiring and independent stop circuit have been checked with qualified adult supervision.
