import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from drive_logic import DriveController, HeadController, mix

class DriveTests(unittest.TestCase):
    def command(self, **changes):
        data=dict(cmd='drive',armed=True,vx=.5,vy=0,wz=0)
        data.update(changes)
        return data

    def test_starts_stopped(self):
        self.assertEqual(DriveController().output(0),(0,0,0,0))

    def test_timeout_disarms_and_does_not_resume(self):
        c=DriveController();self.assertTrue(c.receive(self.command(),10))
        self.assertTrue(any(c.output(410)))
        self.assertEqual(c.output(411),(0,0,0,0));self.assertFalse(c.armed)
        self.assertEqual(c.output(412),(0,0,0,0))

    def test_invalid_commands_disarm(self):
        for bad in [None,{},self.command(vx=float('nan')),self.command(vy=2),
                    self.command(armed=1),self.command(wz=True),self.command(vx='1')]:
            c=DriveController();c.receive(self.command(),0)
            self.assertFalse(c.receive(bad,1));self.assertEqual(c.output(1),(0,0,0,0))

    def test_stop_and_new_command(self):
        c=DriveController();c.receive(self.command(),0)
        c.receive({'cmd':'stop'},1);self.assertEqual(c.output(1),(0,0,0,0))
        c.receive(self.command(),2);self.assertTrue(any(c.output(2)))

    def test_combined_motion_stays_bounded(self):
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                for z in [-1,0,1]:
                    self.assertLessEqual(max(abs(v) for v in mix(x,y,z)),1)
                    c=DriveController();c.receive(self.command(vx=x,vy=y,wz=z),0)
                    self.assertLessEqual(max(abs(v) for v in c.output(0)),.2)

class HeadTests(unittest.TestCase):
    def command(self, **changes):
        data = dict(cmd='head', armed=True, pan_deg=90.0, tilt_deg=20.0)
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

    def test_stop_holds_current_angle_until_new_command(self):
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


if __name__=='__main__':unittest.main()

