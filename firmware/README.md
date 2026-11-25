# Robot code

The main code is the drive logic and a Pico 2 starter. The real robot is still at the design stage.

## Try the drive demo

From the project folder, run:

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -p test_drive.py -v
```

`drive_logic.py` turns forward, sideways and turn commands into four wheel speeds. In the demo, the speeds drop to zero when the last command is more than 400 ms old. To move again, the next drive command needs both `armed=true` and `resume=true`.

`pico/main.py` is the motor starter. Its outputs stay disabled until the wiring, power, wheel directions and independent stop have been checked with a qualified adult.

Anything under `experiments/` is optional computer practice. One example limits the head angles. The other uses pretend readings to decide when to follow or stop. The real camera, sensors and motors still need testing together.
