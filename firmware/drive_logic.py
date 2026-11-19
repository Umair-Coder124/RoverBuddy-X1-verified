"""Portable drive logic and desktop head-motion model. No hardware access."""
import math

def mix(vx, vy, wz):
    # Provisional FL, FR, RL, RR convention. Physical direction requires calibration.
    values = (vx - vy - wz, vx + vy + wz, vx + vy - wz, vx - vy + wz)
    scale = max(1.0, *[abs(v) for v in values])
    return tuple(v / scale for v in values)

class DriveController:
    def __init__(self, timeout_ms=400, max_output=0.20):
        self.timeout_ms = timeout_ms
        self.max_output = max_output
        self.armed = False
        self.last_ms = None
        self.requested = (0.0, 0.0, 0.0, 0.0)

    def stop(self):
        self.armed = False
        self.last_ms = None
        self.requested = (0.0, 0.0, 0.0, 0.0)

    def receive(self, command, now_ms):
        try:
            if not isinstance(command, dict):
                raise ValueError('expected an object')
            if command.get('cmd') == 'stop':
                self.stop()
                return True
            if command.get('cmd') != 'drive' or command.get('armed') is not True:
                raise ValueError('explicit armed drive command required')
            values = [command[k] for k in ('vx', 'vy', 'wz')]
            if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in values):
                raise ValueError('numeric axes required')
            if any(not math.isfinite(v) or abs(v) > 1 for v in values):
                raise ValueError('axis outside -1..1')
            self.requested = tuple(v * self.max_output for v in mix(*values))
            self.last_ms = now_ms
            self.armed = True
            return True
        except (KeyError, TypeError, ValueError, OverflowError):
            self.stop()
            return False

    def output(self, now_ms):
        # Runtime uses a monotonic integer accumulated from MicroPython ticks_diff.
        if not self.armed or self.last_ms is None or now_ms-self.last_ms > self.timeout_ms:
            self.stop()
        return self.requested


class HeadController:
    """Desktop angle simulation; no servo pulses, bus packets or real feedback.

    Zero is an assumed simulation pose, not a hardware startup position.
    Pan follows the bounded interval without wrapping across its endpoints.
    """
    def __init__(self, timeout_ms=400, pan_speed_dps=30.0,
                 tilt_speed_dps=15.0, pan_limits=(-180.0, 180.0),
                 tilt_limits=(-30.0, 30.0)):
        if isinstance(timeout_ms, bool) or not isinstance(timeout_ms, int) or timeout_ms <= 0:
            raise ValueError('positive integer timeout required')
        speeds = (pan_speed_dps, tilt_speed_dps)
        limits = (tuple(pan_limits), tuple(tilt_limits))
        if any(not self._number(v) or v <= 0 for v in speeds):
            raise ValueError('positive finite axis speeds required')
        if any(len(pair) != 2 or any(not self._number(v) for v in pair)
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

    @staticmethod
    def _number(value):
        try:
            return (not isinstance(value, bool)
                    and isinstance(value, (int, float)) and math.isfinite(value))
        except OverflowError:
            return False

    def _time_valid(self, now_ms):
        return (not isinstance(now_ms, bool) and isinstance(now_ms, int)
                and now_ms >= 0
                and (self.updated_ms is None or now_ms >= self.updated_ms))

    def stop(self):
        # Freeze the simulated position; this is not a physical torque-off command.
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
            if any(not self._number(v) or not lo <= v <= hi
                   for v, (lo, hi) in zip(target, self.limits)):
                raise ValueError('angle outside configured limits')
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
            # A delayed simulator update must not integrate beyond the deadline.
            seconds = max(0, min(now_ms, deadline) - self.updated_ms) / 1000.0
            result = []
            for current, target, speed in zip(self.position, self.target, self.speeds):
                distance = target - current
                step = min(abs(distance), speed * seconds)
                result.append(current + (step if distance >= 0 else -step))
            self.position = tuple(result)
            if now_ms > deadline:
                self.stop()
        self.updated_ms = now_ms
        return self.position


class FollowController:
    """Desktop motion supervisor fed by synthetic observations and motion intent.

    This does not detect a person, measure distance or control hardware.
    A stop latches until a valid observation explicitly requests resume.
    """
    def __init__(self, obstacle_stop_cm=30.0, sample_timeout_ms=200):
        if not HeadController._number(obstacle_stop_cm) or obstacle_stop_cm < 0:
            raise ValueError('finite nonnegative obstacle threshold required')
        if (isinstance(sample_timeout_ms, bool)
                or not isinstance(sample_timeout_ms, int) or sample_timeout_ms <= 0):
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
        return (not isinstance(now_ms, bool) and isinstance(now_ms, int)
                and now_ms >= 0
                and (self.updated_ms is None or now_ms >= self.updated_ms))

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
            if any(isinstance(v, bool) or not isinstance(v, int)
                   or v < 0 or not 0 <= now_ms - v <= self.sample_timeout_ms
                   for v in samples):
                self.stop('stale_observation')
                return False
            distance = observation['obstacle_cm']
            if not HeadController._number(distance) or distance < 0:
                raise ValueError('finite nonnegative range required')
            if distance <= self.obstacle_stop_cm:
                self.stop('obstacle')
                return False
            resume = observation.get('resume', False)
            if not isinstance(resume, bool):
                raise ValueError('boolean resume required')
            if not self.armed and not resume:
                # A clear observation alone must not restart after a stop.
                return False
            drive = dict(cmd='drive', armed=True,
                         **{k: observation[k] for k in ('vx', 'vy', 'wz')})
            head = dict(cmd='head', armed=True,
                        **{k: observation[k] for k in ('pan_deg', 'tilt_deg')})
            if not self.drive.receive(drive, now_ms) or not self.head.receive(head, now_ms):
                raise ValueError('invalid motion intent')
            # Refreshing a command must not refresh the underlying sensor samples.
            self.deadline_ms = min([v + self.sample_timeout_ms for v in samples]
                                   + [now_ms + self.drive.timeout_ms,
                                      now_ms + self.head.timeout_ms])
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


