"""Wheel speed calculations and drive command checks."""
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


def is_stop_command(command, expected):
    if not isinstance(command, dict):
        raise ValueError('expected an object')
    if command.get('cmd') == 'stop':
        return True
    if command.get('cmd') != expected or command.get('armed') is not True:
        raise ValueError('explicit armed ' + expected + ' command required')
    return False


def resume_requested(command):
    resume = command.get('resume', False)
    if not isinstance(resume, bool):
        raise ValueError('boolean resume required')
    return resume


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
        if not finite_number(max_output) or not 0 <= max_output <= 1:
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
            if is_stop_command(command, 'drive'):
                self.stop()
                return True
            axes = [command[k] for k in ('vx', 'vy', 'wz')]
            if any(not finite_number(axis) or abs(axis) > 1 for axis in axes):
                raise ValueError('axis outside -1..1')
            resume = resume_requested(command)
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

def __getattr__(name):
    # Keep older desktop imports working without loading simulations on the Pico.
    if name in ('HeadController', 'TiltPulsePlanner', 'FollowController'):
        import desktop_models
        return getattr(desktop_models, name)
    raise AttributeError(name)
