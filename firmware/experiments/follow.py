"""Stop or resume the simulated rover using camera and distance readings."""
from drive_logic import (
    DriveController, finite_number, is_integer, valid_time,
    is_stop_command, resume_requested,
)
from .head import HeadController


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
        self.updated_ms = None
        self.stop('disarmed')

    def stop(self, reason='stopped'):
        self.drive.stop()
        self.head.stop()
        self.armed = False
        self.deadline_ms = None
        self.reason = reason

    def receive(self, observation, now_ms):
        if not valid_time(now_ms, self.updated_ms):
            self.stop('invalid_time')
            return False
        self.output(now_ms)
        try:
            if is_stop_command(observation, 'follow'):
                self.stop()
                return True
            target_visible = observation['target_visible']
            sensor_ok = observation['sensor_ok']
            if not isinstance(target_visible, bool) or not isinstance(sensor_ok, bool):
                raise ValueError('sensor flags must be true or false')
            if not sensor_ok:
                self.stop('sensor_fault')
                return False
            if not target_visible:
                self.stop('target_lost')
                return False
            samples = (observation['target_ms'], observation['obstacle_ms'])
            for sample in samples:
                if not is_integer(sample) or sample < 0 or not 0 <= now_ms - sample <= self.sample_timeout_ms:
                    self.stop('stale_observation')
                    return False
            distance = observation['obstacle_cm']
            if not finite_number(distance) or distance < 0:
                raise ValueError('finite nonnegative range required')
            if distance <= self.obstacle_stop_cm:
                self.stop('obstacle')
                return False
            resume = resume_requested(observation)
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
        if not valid_time(now_ms, self.updated_ms):
            self.stop('invalid_time')
        else:
            if self.armed:
                self.head.output(min(now_ms, self.deadline_ms))
                if now_ms > self.deadline_ms:
                    self.stop('stale_observation')
            self.updated_ms = now_ms
        return dict(wheels=self.drive.output(now_ms) if self.armed else (0.0,) * 4,
                    head_deg=self.head.position, armed=self.armed, reason=self.reason)
