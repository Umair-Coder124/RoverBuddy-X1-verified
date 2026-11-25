# Robot code

The planned setup uses the Pi 5 for the camera and the Pico 2 for the motors. So far the drive code runs on a computer. The robot has yet to be assembled.

## Try the drive demo

From the project folder, run:

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -p test_drive.py -v
```

`drive_logic.py` turns forward, sideways and turn commands into four wheel speeds. In the demo, the speeds drop to zero when the last command is more than 400 ms old. To move again, the next drive command needs both `armed=true` and `resume=true`.

`pico/main.py` is the motor starter. Its outputs stay disabled until the wiring, power, wheel directions and independent stop have been checked with a qualified adult.

Anything under `experiments/` is optional computer practice. One example limits the head angles. The other uses pretend readings to decide when to follow or stop. The nine basic drive tests passed on a computer. The camera, sensors and motors still need real testing.
