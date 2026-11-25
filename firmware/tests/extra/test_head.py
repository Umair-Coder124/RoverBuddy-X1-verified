import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.head import HeadController, TiltPulsePlanner


class HeadTests(unittest.TestCase):
    def command(self, **changes):
        data = dict(cmd='head', armed=True, resume=True, pan_deg=90.0, tilt_deg=20.0)
        data.update(changes)
        return data

    def test_idle_stays_at_assumed_neutral(self):
        c = HeadController()
        self.assertEqual(c.output(10000), (0.0, 0.0))
        self.assertFalse(c.armed)

    def test_axes_have_independent_speed_limits(self):
        c = HeadController()
        self.assertTrue(c.receive(self.command(), 0))
        self.assertEqual(c.output(100), (3.0, 1.5))
        self.assertEqual(c.output(200), (6.0, 3.0))

    def test_small_target_does_not_overshoot(self):
        c = HeadController()
        c.receive(self.command(pan_deg=-1, tilt_deg=0.5), 0)
        self.assertEqual(c.output(200), (-1.0, 0.5))
        self.assertEqual(c.output(300), (-1.0, 0.5))

    def test_boundary_commands_and_out_of_range_rejection(self):
        for pan, tilt in [(-180, -30), (180, 30)]:
            self.assertTrue(HeadController().receive(self.command(pan_deg=pan, tilt_deg=tilt), 0))
        for values in [dict(pan_deg=180.01), dict(pan_deg=-180.01),
                       dict(tilt_deg=30.01), dict(tilt_deg=-30.01)]:
            c = HeadController()
            self.assertFalse(c.receive(self.command(**values), 0))
            self.assertFalse(c.armed)

    def test_malformed_commands_disarm_and_freeze(self):
        bad = [None, {}, self.command(armed=1), self.command(pan_deg=True),
               self.command(tilt_deg='10'), self.command(pan_deg=float('nan')),
               self.command(tilt_deg=float('inf')), self.command(pan_deg=10**1000),
               dict(cmd='head', armed=True, pan_deg=10), self.command(cmd='drive')]
        for command in bad:
            c = HeadController()
            c.receive(self.command(), 0)
            self.assertFalse(c.receive(command, 100))
            held = c.position
            self.assertFalse(c.armed)
            self.assertEqual(c.output(10000), held)

    def test_long_update_stops_at_watchdog_deadline(self):
        c = HeadController()
        c.receive(self.command(), 0)
        self.assertEqual(c.output(10000), (12.0, 6.0))
        self.assertFalse(c.armed)
        self.assertEqual(c.output(20000), (12.0, 6.0))

    def test_watchdog_boundary_and_fresh_rearm(self):
        c = HeadController()
        c.receive(self.command(), 0)
        self.assertEqual(c.output(400), (12.0, 6.0))
        self.assertTrue(c.armed)
        self.assertEqual(c.output(401), (12.0, 6.0))
        self.assertFalse(c.armed)
        self.assertTrue(c.receive(self.command(pan_deg=0, tilt_deg=0), 500))
        self.assertEqual(c.output(600), (9.0, 4.5))

    def test_stop_holds_current_angle(self):
        c = HeadController()
        c.receive(self.command(), 0)
        self.assertTrue(c.receive({'cmd': 'stop'}, 100))
        self.assertEqual(c.output(5000), (3.0, 1.5))
        self.assertFalse(c.armed)

    def test_keepalive_reaches_endpoint_without_crossing_limits(self):
        c = HeadController()
        command = self.command(pan_deg=180, tilt_deg=-30)
        for now in range(0, 7001, 100):
            self.assertTrue(c.receive(command, now))
            pan, tilt = c.output(now)
            self.assertTrue(0 <= pan <= 180)
            self.assertTrue(-30 <= tilt <= 0)
        self.assertEqual(c.position, (180.0, -30.0))

    def test_pan_reversal_does_not_wrap_across_cable_boundary(self):
        c = HeadController(timeout_ms=1000, pan_speed_dps=1000)
        c.receive(self.command(pan_deg=170, tilt_deg=0), 0)
        self.assertEqual(c.output(170), (170.0, 0.0))
        c.receive(self.command(pan_deg=-170, tilt_deg=0), 170)
        self.assertEqual(c.output(180), (160.0, 0.0))
        self.assertEqual(c.output(340), (0.0, 0.0))
        self.assertEqual(c.output(510), (-170.0, 0.0))

    def test_invalid_or_reversed_time_disarms_without_a_jump(self):
        for bad in [True, -1, 1.5, float('nan'), 99]:
            c = HeadController()
            c.receive(self.command(), 0)
            held = c.output(100)
            self.assertFalse(c.receive(self.command(), bad))
            self.assertEqual(c.position, held)
            self.assertEqual(c.output(10000), held)
        c = HeadController()
        c.receive(self.command(), 100)
        self.assertEqual(c.output(99), (0.0, 0.0))
        self.assertFalse(c.armed)

    def test_invalid_configuration_is_rejected(self):
        for kwargs in [dict(timeout_ms=0), dict(timeout_ms=True),
                       dict(pan_speed_dps=0), dict(tilt_speed_dps=float('inf')),
                       dict(pan_limits=(10, 20)), dict(tilt_limits=(1, -1))]:
            with self.assertRaises(ValueError):
                HeadController(**kwargs)

    def test_startup_requires_resume_but_normal_keepalives_do_not(self):
        c = HeadController()
        ordinary = self.command()
        del ordinary['resume']
        self.assertFalse(c.receive(ordinary, 0))
        self.assertEqual(c.output(100), (0.0, 0.0))
        self.assertTrue(c.receive(self.command(), 100))
        self.assertTrue(c.receive(ordinary, 200))
        self.assertTrue(c.receive(self.command(resume=False), 300))
        self.assertEqual(c.output(300), (6.0, 3.0))

    def test_stop_cannot_be_cleared_by_ordinary_commands(self):
        c = HeadController()
        c.receive(self.command(), 0)
        c.receive({'cmd': 'stop'}, 100)
        held = c.position
        for now in (110, 200, 1000):
            self.assertFalse(c.receive(self.command(resume=False), now))
            self.assertEqual(c.output(now), held)
            self.assertIsNone(c.last_ms)
        self.assertTrue(c.receive(self.command(), 1100))
        self.assertEqual(c.output(1200), (6.0, 3.0))

    def test_timeout_cannot_be_cleared_by_keepalive(self):
        c = HeadController()
        c.receive(self.command(), 0)
        held = c.output(401)
        self.assertFalse(c.receive(self.command(resume=False), 500))
        self.assertEqual(c.output(600), held)
        self.assertTrue(c.receive(self.command(), 700))
        self.assertEqual(c.output(800), (15.0, 7.5))

    def test_late_command_detects_timeout_before_rearming(self):
        c = HeadController()
        c.receive(self.command(), 0)
        ordinary = self.command()
        del ordinary['resume']
        self.assertFalse(c.receive(ordinary, 401))
        self.assertFalse(c.armed)
        self.assertEqual(c.output(1000), (12.0, 6.0))
        self.assertTrue(c.receive(self.command(), 1000))
        self.assertEqual(c.output(1100), (15.0, 7.5))

    def test_invalid_input_and_time_latch_head_stop(self):
        for bad, now in [(self.command(pan_deg=181), 100),
                         (None, 100), (self.command(), 99)]:
            with self.subTest(bad=bad, now=now):
                c = HeadController()
                c.receive(self.command(), 0)
                c.output(100)
                self.assertFalse(c.receive(bad, now))
                held = c.position
                self.assertFalse(c.receive(self.command(resume=False), 200))
                self.assertEqual(c.output(300), held)
                self.assertTrue(c.receive(self.command(), 400))
                self.assertNotEqual(c.output(500), held)

    def test_resume_requires_a_boolean_and_valid_target(self):
        for resume in (None, 1, 0, 'true', [], {}):
            with self.subTest(resume=resume):
                c = HeadController()
                c.receive(self.command(), 0)
                self.assertFalse(c.receive(self.command(resume=resume), 100))
                held = c.position
                self.assertFalse(c.receive(self.command(resume=False), 200))
                self.assertEqual(c.output(300), held)
        c = HeadController()
        self.assertFalse(c.receive(self.command(pan_deg=181), 0))
        self.assertFalse(c.armed)


class TiltPulseTests(unittest.TestCase):
    def test_planned_endpoints_and_neutral(self):
        p = TiltPulsePlanner()
        self.assertEqual([p.pulse_us(v) for v in (-30, 0, 30)], [1200, 1500, 1800])

    def test_reverse_changes_direction_without_moving_neutral(self):
        p = TiltPulsePlanner(reverse=True)
        self.assertEqual([p.pulse_us(v) for v in (-30, 0, 30)], [1800, 1500, 1200])

    def test_custom_center_and_scale(self):
        p = TiltPulsePlanner(center_us=1520, us_per_degree=8,
                             pulse_limits=(1250, 1800))
        self.assertEqual([p.pulse_us(v) for v in (-30, 0, 30)], [1280, 1520, 1760])

    def test_fractional_angles_round_to_integer_microseconds(self):
        p = TiltPulsePlanner()
        self.assertEqual(p.pulse_us(1.24), 1512)
        self.assertEqual(p.pulse_us(-1.24), 1488)
        self.assertIsInstance(p.pulse_us(1.24), int)

    def test_invalid_and_outside_angles_are_rejected(self):
        p = TiltPulsePlanner()
        for angle in (True, '0', None, float('nan'), float('inf'),
                      -30.001, 30.001, 10**1000):
            with self.subTest(angle=angle), self.assertRaises(ValueError):
                p.pulse_us(angle)

    def test_invalid_configuration_is_rejected(self):
        cases = (dict(center_us=True), dict(center_us=1500.5), dict(center_us=2200),
                 dict(us_per_degree=0), dict(us_per_degree=-1),
                 dict(us_per_degree=float('inf')), dict(us_per_degree=True),
                 dict(reverse=1), dict(angle_limits=None), dict(angle_limits=(0,)),
                 dict(angle_limits=(30, -30)), dict(angle_limits=(1, 2)),
                 dict(angle_limits=(float('nan'), 30)), dict(pulse_limits=None),
                 dict(pulse_limits=(800, 2200)), dict(pulse_limits=(1800, 1200)),
                 dict(pulse_limits=(1200.0, 1800)), dict(pulse_limits=(True, 1800)))
        for options in cases:
            with self.subTest(options=options), self.assertRaises(ValueError):
                TiltPulsePlanner(**options)

    def test_full_angle_window_must_fit_even_before_rounding(self):
        for options in (dict(center_us=1700), dict(us_per_degree=10.001),
                        dict(us_per_degree=10**1000), dict(us_per_degree=1e308),
                        dict(pulse_limits=(1400, 1600)),
                        dict(angle_limits=(-31, 30)), dict(reverse=True, center_us=1700)):
            with self.subTest(options=options), self.assertRaises(ValueError):
                TiltPulsePlanner(**options)
