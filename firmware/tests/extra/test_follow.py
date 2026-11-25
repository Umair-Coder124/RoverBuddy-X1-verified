import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.follow import FollowController


class FollowTests(unittest.TestCase):
    def sample(self, now=0, **changes):
        data = dict(cmd='follow', armed=True, target_visible=True, sensor_ok=True,
                    target_ms=now, obstacle_ms=now, obstacle_cm=100,
                    vx=0.5, vy=0, wz=0, pan_deg=30, tilt_deg=10)
        data.update(changes)
        return data

    def started(self):
        c = FollowController()
        self.assertTrue(c.receive(self.sample(resume=True), 0))
        return c

    def assertStopped(self, state):
        self.assertFalse(state['armed'])
        self.assertEqual(state['wheels'], (0.0,) * 4)

    def test_requires_explicit_resume_to_start(self):
        c = FollowController()
        self.assertFalse(c.receive(self.sample(), 0))
        self.assertStopped(c.output(0))
        self.assertTrue(c.receive(self.sample(resume=True), 0))
        self.assertTrue(c.output(0)['armed'])

    def test_valid_sample_coordinates_drive_and_head(self):
        c = self.started()
        state = c.output(100)
        self.assertEqual(state['head_deg'], (3.0, 1.5))
        self.assertTrue(any(state['wheels']))
        self.assertLessEqual(max(abs(x) for x in state['wheels']), 0.2)

    def test_independent_head_stop_requires_supervisor_resume(self):
        c = self.started()
        c.output(100)
        c.head.stop()
        held = c.head.position
        self.assertFalse(c.receive(self.sample(110), 110))
        self.assertStopped(c.output(110))
        self.assertFalse(c.drive.armed)
        self.assertFalse(c.receive(self.sample(120), 120))
        self.assertEqual(c.output(120)['head_deg'], held)
        self.assertTrue(c.receive(self.sample(130, resume=True), 130))
        self.assertTrue(c.head.armed)
        self.assertTrue(c.drive.armed)
        self.assertNotEqual(c.output(140)['head_deg'], held)

    def test_independent_drive_stop_requires_supervisor_resume(self):
        c = self.started()
        c.output(100)
        c.drive.stop()
        self.assertFalse(c.receive(self.sample(110), 110))
        self.assertStopped(c.output(110))
        self.assertFalse(c.head.armed)
        held = c.head.position
        self.assertFalse(c.receive(self.sample(120), 120))
        self.assertEqual(c.output(120)['head_deg'], held)
        self.assertTrue(c.receive(self.sample(130, resume=True), 130))
        self.assertTrue(c.drive.armed)
        self.assertTrue(c.head.armed)

    def test_target_loss_or_sensor_fault_stops_both(self):
        for changes, reason in [(dict(target_visible=False), 'target_lost'),
                                (dict(sensor_ok=False), 'sensor_fault')]:
            with self.subTest(reason=reason):
                c = self.started()
                self.assertFalse(c.receive(self.sample(100, **changes), 100))
                state = c.output(100)
                self.assertStopped(state)
                self.assertFalse(c.drive.armed)
                self.assertFalse(c.head.armed)
                self.assertEqual(state['reason'], reason)
                self.assertEqual(c.output(5000)['head_deg'], state['head_deg'])

    def test_obstacle_threshold_includes_boundary_and_zero(self):
        for distance in [0, 29.9, 30]:
            c = self.started()
            self.assertFalse(c.receive(self.sample(100, obstacle_cm=distance), 100))
            self.assertStopped(c.output(100))
            self.assertEqual(c.reason, 'obstacle')
        self.assertTrue(FollowController().receive(self.sample(resume=True, obstacle_cm=30.1), 0))

    def test_camera_and_range_have_independent_freshness(self):
        for changes in [dict(target_ms=0), dict(obstacle_ms=0),
                        dict(target_ms=301), dict(obstacle_ms=301)]:
            c = FollowController()
            self.assertFalse(c.receive(self.sample(300, resume=True, **changes), 300))
            self.assertStopped(c.output(300))
            self.assertEqual(c.reason, 'stale_observation')

    def test_replayed_samples_do_not_extend_freshness(self):
        c = self.started()
        for now in [50, 100, 150, 200]:
            self.assertTrue(c.receive(self.sample(), now))
        self.assertTrue(c.output(200)['armed'])
        self.assertStopped(c.output(201))
        self.assertEqual(c.reason, 'stale_observation')

    def test_late_update_integrates_head_only_until_sample_deadline(self):
        c = self.started()
        state = c.output(10000)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (6.0, 3.0))
        self.assertEqual(state['reason'], 'stale_observation')

    def test_clear_sample_does_not_resume_after_a_stop(self):
        c = self.started()
        c.receive(self.sample(100, obstacle_cm=10), 100)
        self.assertFalse(c.receive(self.sample(110), 110))
        self.assertStopped(c.output(110))
        self.assertFalse(c.receive(self.sample(120, resume=True, obstacle_cm=10), 120))
        self.assertTrue(c.receive(self.sample(130, resume=True), 130))
        self.assertTrue(c.output(130)['armed'])

    def test_invalid_observations_and_intent_disarm(self):
        for bad in [None, {}, self.sample(100, armed=1),
                    self.sample(100, target_visible=1), self.sample(100, sensor_ok=None),
                    self.sample(100, obstacle_cm=float('nan')),
                    self.sample(100, obstacle_cm=-1), self.sample(100, obstacle_cm=None),
                    self.sample(100, obstacle_ms=True), self.sample(100, resume='yes'),
                    self.sample(100, vx=2), self.sample(100, pan_deg=181)]:
            c = self.started()
            self.assertFalse(c.receive(bad, 100))
            self.assertStopped(c.output(100))
            self.assertFalse(c.head.armed)

    def test_explicit_stop_holds_until_fresh_resume(self):
        c = self.started()
        self.assertTrue(c.receive(dict(cmd='stop'), 100))
        state = c.output(1000)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (3.0, 1.5))

    def test_time_reversal_disarms_without_moving_head(self):
        c = self.started()
        held = c.output(100)['head_deg']
        self.assertFalse(c.receive(self.sample(99, resume=True), 99))
        self.assertStopped(c.output(100))
        self.assertEqual(c.head.position, held)
        self.assertEqual(c.reason, 'invalid_time')

    def test_configuration_and_controller_timeout_ceiling(self):
        for kwargs in [dict(obstacle_stop_cm=-1), dict(obstacle_stop_cm=True),
                       dict(sample_timeout_ms=0), dict(sample_timeout_ms=True)]:
            with self.assertRaises(ValueError):
                FollowController(**kwargs)
        c = FollowController(sample_timeout_ms=1000)
        c.receive(self.sample(resume=True), 0)
        state = c.output(401)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (12.0, 6.0))
