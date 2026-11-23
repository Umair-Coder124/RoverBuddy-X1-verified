"""Portable drive logic and desktop head-motion model. No hardware access."""
import math


def is_integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def valid_time(now_ms, previous_ms):
    if not is_integer(now_ms) or now_ms < 0:
        return False
    return previous_ms is None or now_ms >= previous_ms


def finite_number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def mix(vx, vy, wz):
    # vx = forward, vy = sideways, wz = turn.
    # Check the actual wheel directions during hardware testing.
    front_left = vx - vy - wz
    front_right = vx + vy + wz
    rear_left = vx + vy - wz
    rear_right = vx - vy + wz
    wheels = (front_left, front_right, rear_left, rear_right)
    # Scale all wheels together so none exceeds the allowed range.
    largest_speed = max(1.0, max(abs(speed) for speed in wheels))
    return tuple(speed / largest_speed for speed in wheels)


class DriveController:
    """Limits wheel speed and stops when commands are missing."""
    def __init__(self, timeout_ms=400, max_output=0.20):
        if not is_integer(timeout_ms) or timeout_ms <= 0:
            raise ValueError('positive integer timeout required')
        if (isinstance(max_output, bool) or not isinstance(max_output, (int, float))
                or not 0 <= max_output <= 1):
            raise ValueError('finite output limit in 0..1 required')
        self.timeout_ms = timeout_ms
        self.max_output = max_output
        self.armed = False
        self.last_ms = None
        self.updated_ms = None
        self.requested = (0.0, 0.0, 0.0, 0.0)

    def _time_valid(self, now_ms):
        return valid_time(now_ms, self.updated_ms)

    def stop(self):
        self.armed = False
        self.last_ms = None
        self.requested = (0.0, 0.0, 0.0, 0.0)

    def receive(self, command, now_ms):
        if not self._time_valid(now_ms):
            self.stop()
            return False
        # Stop if the old command expired before accepting the next one.
        self.output(now_ms)
        try:
            if not isinstance(command, dict):
                raise ValueError('expected an object')
            if command.get('cmd') == 'stop':
                self.stop()
                return True
            if command.get('cmd') != 'drive' or command.get('armed') is not True:
                raise ValueError('explicit armed drive command required')
            axes = [command[k] for k in ('vx', 'vy', 'wz')]
            if any(not finite_number(axis) or abs(axis) > 1 for axis in axes):
                raise ValueError('axis outside -1..1')
            resume = command.get('resume', False)
            if not isinstance(resume, bool):
                raise ValueError('boolean resume required')
            if not self.armed and not resume:
                return False
            self.requested = tuple(speed * self.max_output for speed in mix(*axes))
            self.last_ms = now_ms
            self.armed = True
            return True
        except (KeyError, TypeError, ValueError, OverflowError):
            self.stop()
            return False

    def output(self, now_ms):
        # Runtime uses a monotonic integer accumulated from MicroPython ticks_diff.
        if not self._time_valid(now_ms):
            self.stop()
            return self.requested
        if not self.armed or self.last_ms is None or now_ms - self.last_ms > self.timeout_ms:
            self.stop()
        self.updated_ms = now_ms
        return self.requested


class HeadController:
    """Simulates head angles on a computer.

    Starts at an assumed zero pose, keeps pan within its limits,
    and requires resume after every stop. No hardware output.
    """
    def __init__(self, timeout_ms=400, pan_speed_dps=30.0,
                 tilt_speed_dps=15.0, pan_limits=(-180.0, 180.0),
                 tilt_limits=(-30.0, 30.0)):
        if not is_integer(timeout_ms) or timeout_ms <= 0:
            raise ValueError('positive integer timeout required')
        speeds = (pan_speed_dps, tilt_speed_dps)
        limits = (tuple(pan_limits), tuple(tilt_limits))
        # Both axes need valid speeds and limits that include zero.
        if any(not finite_number(v) or v <= 0 for v in speeds):
            raise ValueError('positive finite axis speeds required')
        if any(len(pair) != 2 or any(not finite_number(v) for v in pair)
               or not pair[0] <= 0 <= pair[1] or pair[0] >= pair[1]
               for pair in limits):
            raise ValueError('finite ordered limits containing neutral required')
        self.timeout_ms = timeout_ms
        self.speeds = speeds
        self.limits = limits
        self.position = (0.0, 0.0)
        self.target = self.position
        self.armed = False
        self.last_ms = None
        self.updated_ms = None

    _number = staticmethod(finite_number)

    def _time_valid(self, now_ms):
        return valid_time(now_ms, self.updated_ms)

    def stop(self):
        # Hold the current simulated angle. No physical torque command.
        self.armed = False
        self.last_ms = None
        self.target = self.position

    def receive(self, command, now_ms):
        if not self._time_valid(now_ms):
            self.stop()
            return False
        self.output(now_ms)
        try:
            if not isinstance(command, dict):
                raise ValueError('expected an object')
            if command.get('cmd') == 'stop':
                self.stop()
                return True
            if command.get('cmd') != 'head' or command.get('armed') is not True:
                raise ValueError('explicit armed head command required')
            target = tuple(command[k] for k in ('pan_deg', 'tilt_deg'))
            if any(not finite_number(v) or not lo <= v <= hi
                   for v, (lo, hi) in zip(target, self.limits)):
                raise ValueError('angle outside configured limits')
            resume = command.get('resume', False)
            if not isinstance(resume, bool):
                raise ValueError('boolean resume required')
            if not self.armed and not resume:
                # A new angle alone cannot restart a stopped head.
                return False
            self.target = target
            self.last_ms = now_ms
            self.armed = True
            return True
        except (KeyError, TypeError, ValueError, OverflowError):
            self.stop()
            return False

    def output(self, now_ms):
        if not self._time_valid(now_ms):
            self.stop()
            return self.position
        if self.armed and self.last_ms is not None and self.updated_ms is not None:
            deadline = self.last_ms + self.timeout_ms
            # Only count movement time before the command expires.
            motion_end = min(now_ms, deadline)
            seconds = max(0, motion_end - self.updated_ms) / 1000.0
            new_angles = []
            for current, target, speed in zip(self.position, self.target, self.speeds):
                distance = target - current
                step = min(abs(distance), speed * seconds)
                new_angles.append(current + (step if distance >= 0 else -step))
            self.position = tuple(new_angles)
            if now_ms > deadline:
                self.stop()
        self.updated_ms = now_ms
        return self.position


class TiltPulsePlanner:
    """Calculates example tilt pulse widths without hardware output.

    The assumed 10 us per degree and angle limits need real calibration.
    """
    def __init__(self, center_us=1500, us_per_degree=10.0,
                 angle_limits=(-30.0, 30.0), pulse_limits=(1200, 1800),
                 reverse=False):
        try:
            angles, pulses = tuple(angle_limits), tuple(pulse_limits)
        except TypeError as exc:
            raise ValueError('angle and pulse limit pairs required') from exc
        if (not is_integer(center_us)
                or not finite_number(us_per_degree) or us_per_degree <= 0
                or not isinstance(reverse, bool)):
            raise ValueError('integer center, positive finite scale and boolean reverse required')
        if (len(angles) != 2 or any(not finite_number(v) for v in angles)
                or not angles[0] <= 0 <= angles[1] or angles[0] >= angles[1]):
            raise ValueError('ordered finite angle limits containing neutral required')
        if (len(pulses) != 2
                or any(not is_integer(v) for v in pulses)
                or not 900 <= pulses[0] <= center_us <= pulses[1] <= 2100
                or pulses[0] >= pulses[1]):
            raise ValueError('ordered integer pulse limits inside 900..2100 us required')
        self.center_us = center_us
        self.us_per_degree = us_per_degree
        self.angle_limits = angles
        self.pulse_limits = pulses
        self.reverse = reverse
        try:
            for angle in angles:
                self.pulse_us(angle)
        except (ValueError, OverflowError) as exc:
            raise ValueError('angle endpoints exceed the configured pulse window') from exc

    def pulse_us(self, angle_deg):
        if (not finite_number(angle_deg)
                or not self.angle_limits[0] <= angle_deg <= self.angle_limits[1]):
            raise ValueError('tilt angle outside configured limits')
        try:
            offset = angle_deg * self.us_per_degree
            if self.reverse:
                offset = -offset
            pulse = self.center_us + offset
            if (not finite_number(pulse)
                    or not self.pulse_limits[0] <= pulse <= self.pulse_limits[1]):
                raise ValueError('tilt pulse outside configured limits')
            return int(round(pulse))
        except OverflowError as exc:
            raise ValueError('tilt pulse overflow') from exc


class FollowController:
    """Tests stop and resume behavior using simulated sensor readings.

    No live sensors, detection or hardware output.
    """
    def __init__(self, obstacle_stop_cm=30.0, sample_timeout_ms=200):
        if not finite_number(obstacle_stop_cm) or obstacle_stop_cm < 0:
            raise ValueError('finite nonnegative obstacle threshold required')
        if (not is_integer(sample_timeout_ms) or sample_timeout_ms <= 0):
            raise ValueError('positive integer sample timeout required')
        self.drive = DriveController()
        self.head = HeadController()
        self.obstacle_stop_cm = obstacle_stop_cm
        self.sample_timeout_ms = sample_timeout_ms
        self.armed = False
        self.reason = 'disarmed'
        self.deadline_ms = None
        self.updated_ms = None

    def _time_valid(self, now_ms):
        return valid_time(now_ms, self.updated_ms)

    def stop(self, reason='stopped'):
        self.drive.stop()
        self.head.stop()
        self.armed = False
        self.deadline_ms = None
        self.reason = reason

    def receive(self, observation, now_ms):
        if not self._time_valid(now_ms):
            self.stop('invalid_time')
            return False
        self.output(now_ms)
        try:
            if not isinstance(observation, dict):
                raise ValueError('expected an object')
            if observation.get('cmd') == 'stop':
                self.stop()
                return True
            if observation.get('cmd') != 'follow' or observation.get('armed') is not True:
                raise ValueError('explicit armed follow command required')
            if any(not isinstance(observation[k], bool)
                   for k in ('target_visible', 'sensor_ok')):
                raise ValueError('boolean observation status required')
            if not observation['sensor_ok']:
                self.stop('sensor_fault')
                return False
            if not observation['target_visible']:
                self.stop('target_lost')
                return False
            samples = [observation[k] for k in ('target_ms', 'obstacle_ms')]
            if any(not is_integer(v) or v < 0 or not 0 <= now_ms - v <= self.sample_timeout_ms
                   for v in samples):
                self.stop('stale_observation')
                return False
            distance = observation['obstacle_cm']
            if not finite_number(distance) or distance < 0:
                raise ValueError('finite nonnegative range required')
            if distance <= self.obstacle_stop_cm:
                self.stop('obstacle')
                return False
            resume = observation.get('resume', False)
            if not isinstance(resume, bool):
                raise ValueError('boolean resume required')
            if not self.armed and not resume:
                # Wait for an explicit restart after a stop.
                return False
            drive = dict(cmd='drive', armed=True, resume=resume,
                         **{k: observation[k] for k in ('vx', 'vy', 'wz')})
            head = dict(cmd='head', armed=True, resume=resume,
                        **{k: observation[k] for k in ('pan_deg', 'tilt_deg')})
            if not self.drive.receive(drive, now_ms) or not self.head.receive(head, now_ms):
                raise ValueError('invalid motion intent')
            # A new command cannot make old sensor readings fresh.
            sensor_deadline = min(samples) + self.sample_timeout_ms
            drive_deadline = now_ms + self.drive.timeout_ms
            head_deadline = now_ms + self.head.timeout_ms
            self.deadline_ms = min(sensor_deadline, drive_deadline, head_deadline)
            self.armed = True
            self.reason = 'following'
            return True
        except (KeyError, TypeError, ValueError, OverflowError):
            self.stop('invalid_observation')
            return False

    def output(self, now_ms):
        if not self._time_valid(now_ms):
            self.stop('invalid_time')
        else:
            if self.armed:
                self.head.output(min(now_ms, self.deadline_ms))
                if now_ms > self.deadline_ms:
                    self.stop('stale_observation')
            self.updated_ms = now_ms
        return dict(wheels=self.drive.output(now_ms) if self.armed else (0.0,) * 4,
                    head_deg=self.head.position, armed=self.armed, reason=self.reason)


