"""Portable drive-control draft. No hardware access in this module."""
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
