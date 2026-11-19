# Firmware: motion simulation and video detection

**Untested on hardware; actuators disabled by default.** The drive starter and desktop head/follow models are development tools, not a finished follow-me robot.

## Desktop checks

From the repository root:

```sh
python3 firmware/simulate.py
python3 -m unittest discover -s firmware/tests -v
```

Neither command accesses GPIO, serial devices or actuators. The simulation prints wheel outputs, rate-limited head angles, the command-timeout stop and rejection of an out-of-range pan target.

All 52 desktop tests passed: five drive tests, twelve head-model tests, thirteen follow-supervisor tests, eight video/reporting tests and fourteen target-lock tests. They cover motion bounds, command and observation validation, independent sample freshness, coordinated stops, explicit resume, timeout deadlines and pan reversal without wrapping. Hardware behavior has not been tested.

## Recorded-video detection dry run

The existing simulator can read a local recorded clip and report baseline person detections:

```sh
python3 -m pip install opencv-python-headless==4.11.0.86
python3 firmware/simulate.py --video /path/to/clip.mp4 --max-frames 300
```

OpenCV is optional. The ordinary simulation and unit tests still run without it. Video mode accepts an existing local file and prints one JSON report per processed frame, followed by `end_of_video` or `frame_limit`. It opens no live camera, GPIO or actuator interface.

| Report status | Meaning |
|---|---|
| `no_person` | No person box returned by the baseline detector |
| `one_person_candidate` | One box; report includes its normalized center offset |
| `multiple_candidates` | Multiple boxes; an existing explicit lock can match one by overlap, otherwise none is selected |
| `end_of_video` | Decoder reached the end after at least one frame |
| `frame_limit` | Requested frame limit was reached |

Every report sets `motion_enabled: false`. One candidate does not establish target identity or a clear path. Video reports are not passed into the motion supervisor, and the program does not invent obstacle readings or send motion commands.

The baseline uses OpenCV's bundled HOG people detector. Wide frames are reduced to at most 640 pixels for analysis; boxes are mapped back to original frame coordinates. Frames smaller than the 64 × 128 detection window return no candidates. HOG scores are classifier margins, not probability estimates. The detector can miss people, return false positives, or lose a person between frames. Persistent identity, camera calibration, distance estimation, steering intent and real-time performance remain open.

Verification used OpenCV 4.11.0 and a temporary three-frame MJPEG clip: blank frame, [OpenCV's basketball sample image](https://github.com/opencv/opencv/blob/4.x/samples/data/basketball1.png), blank frame. It produced `no_person → one_person_candidate → no_person → end_of_video`, with motion disabled throughout. This checks decoding and reporting; it does not measure detection accuracy. The eight unit tests also cover ambiguity, invalid boxes, coordinate scaling, file-open/decode errors, frame limits and capture cleanup.

Sources: [OpenCV HOG descriptor and people detector](https://docs.opencv.org/4.11.0/d5/d33/structcv_1_1HOGDescriptor.html) · [VideoCapture](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html)

## Explicit target locking in recorded video

First inspect the ordinary video reports to choose a detection on a particular frame. Then rerun the clip with explicit zero-based frame and detection indices:

```sh
python3 firmware/simulate.py --video /path/to/clip.mp4 --max-frames 300 --select-frame 10 --target-index 0
```

This selects the first detection in frame 10's `detections` array. There is no automatic initial selection. If that index is unavailable on the selected frame, the attempt is reported as `selection_unavailable` and is not retried on a later frame.

Each frame now includes a separate `target` object:

| Target state | Meaning |
|---|---|
| `unselected` | No explicit selection has been made |
| `locked` | The selected box, or a sufficiently overlapping continuation, is available |
| `lost` | Selection failed, association became unreliable, frame size changed, or processing ended |

A locked target includes its box, current detection index and normalized center offset. The detection index can change when the detector changes output order; it is not a person ID. A top-level single-candidate center describes a detection only; use the separate `target` state to inspect the explicit lock.

The baseline compares intersection-over-union with the previous target box. The default minimum overlap is 0.3. If the two best qualifying matches differ by no more than 0.1, the match is treated as ambiguous and the lock is lost. A nonoverlapping bystander, a higher detection score or a larger box does not trigger automatic replacement.

Loss remains latched even if a similar detection reappears. The CLI makes one selection attempt per run; choose again by rerunning the clip with the desired frame and index. An active lock is cleared at end-of-video or the frame limit. Every report still has `motion_enabled: false`.

Verification used a temporary four-frame clip: blank, OpenCV sample image, a slightly shifted copy, blank. The target states were `unselected → locked (selected) → locked (overlap_match) → lost (no_overlap)`. Tests additionally cover changed detection order, bystanders, ambiguous overlap, missing targets, frame-size changes, failed selection and latched loss.

Box overlap is not identity recognition. Nearby or crossing people can still cause incorrect associations, and fast motion or missed detections can lose the target. Appearance-based identity checks, practical tracking accuracy and hardware integration remain open.

## Desktop follow-mode supervisor

`FollowController` combines the existing drive and head models. It gates supplied motion intent using synthetic target status and obstacle readings. It does not detect people, measure distance or generate motion intent from camera images.

Run the same `simulate.py` command for examples of target loss, a nearby obstacle, sensor failure, stale samples and deliberate recovery. No extra packages or hardware are needed.

| Input / behavior | Desktop rule |
|---|---|
| Target visibility | `target_visible` must be the boolean `true` |
| Sensor health | `sensor_ok` must be the boolean `true` |
| Obstacle distance | A finite, nonnegative number; at or below 30 cm stops motion by default |
| Sample freshness | Separate target and obstacle timestamps must each be no more than 200 ms old by default |
| Stop | Zero simulated wheel outputs and freeze the simulated head pose |
| Recovery | A fresh valid observation with explicit `resume: true` is required |

The 30 cm threshold and 200 ms age limit are simulation settings, not verified real-world stopping parameters. Timestamps are nonnegative integer milliseconds from the same monotonic clock as `receive(..., now_ms)`. Future timestamps are rejected. Repeating an old observation cannot extend its freshness deadline. Configured sample age also cannot extend the underlying drive/head command watchdogs.

Example input to the **desktop supervisor** at `now_ms=0`:

```json
{
  "cmd": "follow",
  "armed": true,
  "resume": true,
  "target_visible": true,
  "sensor_ok": true,
  "target_ms": 0,
  "obstacle_ms": 0,
  "obstacle_cm": 100,
  "vx": 0.5,
  "vy": 0,
  "wz": 0,
  "pan_deg": 30,
  "tilt_deg": 10
}
```

Subsequent valid observations can omit `resume` while already armed. After any stop, returning to clear readings alone does not restart motion. A `{"cmd":"stop"}` also stops both models. Invalid motion intent, missing data, reversed time or a stale sample disarms the supervisor.

The scenarios use invented fixture values. Real target identity, target switching, camera latency, ultrasonic failures, physical braking and head-stop behavior still require implementation and validation. The follow input is **not** accepted by the Pico drive USB runtime, and an ordinary cleared observation must not be translated into an automatic operator resume.

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

Hardware and camera integration still to implement and test: target selection/tracking, real target-loss and obstacle/sensor-fault inputs, chest UI, physical pan/tilt interfaces and position recovery, hardware-interlock status, calibration and recovery behavior. A manually armed drive command in this starter can move without obstacle sensing; do not treat it as autonomous or safety validated.

Reference: the manufacturer's [CytronMotorDriver library](https://github.com/CytronTechnologies/CytronMotorDriver) identifies MDD3A as a two-input PWM/PWM driver. Verify the actual board's connector labels and truth table.




