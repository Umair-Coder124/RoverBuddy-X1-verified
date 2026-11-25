import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from drive_logic import DriveController, mix

class DriveTests(unittest.TestCase):
    def command(self, **changes):
        data=dict(cmd='drive',armed=True,resume=True,vx=.5,vy=0,wz=0)
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
        for axes, expected in [((1, 0, 0), (1, 1, 1, 1)),
                               ((0, 1, 0), (-1, 1, 1, -1)),
                               ((0, 0, 1), (-1, 1, -1, 1))]:
            with self.subTest(axes=axes):
                self.assertEqual(mix(*axes), expected)
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                for z in [-1,0,1]:
                    self.assertLessEqual(max(abs(v) for v in mix(x,y,z)),1)
                    c=DriveController();c.receive(self.command(vx=x,vy=y,wz=z),0)
                    self.assertLessEqual(max(abs(v) for v in c.output(0)),.2)

    def test_startup_and_ordinary_keepalives(self):
        c = DriveController()
        ordinary = self.command()
        del ordinary['resume']
        self.assertFalse(c.receive(ordinary, 0))
        self.assertEqual(c.output(0), (0, 0, 0, 0))
        self.assertTrue(c.receive(self.command(), 10))
        self.assertTrue(c.receive(ordinary, 100))
        self.assertTrue(c.receive(self.command(resume=False), 200))
        self.assertTrue(any(c.output(200)))

    def test_stop_latches_until_explicit_resume(self):
        c = DriveController()
        c.receive(self.command(), 0)
        self.assertTrue(c.receive({'cmd': 'stop'}, 10))
        for now in (20, 100, 500):
            self.assertFalse(c.receive(self.command(resume=False), now))
            self.assertEqual(c.output(now), (0, 0, 0, 0))
            self.assertIsNone(c.last_ms)
        self.assertTrue(c.receive(self.command(), 600))
        self.assertTrue(any(c.output(600)))

    def test_timeout_latches_even_if_late_packet_arrives_before_output(self):
        for observe_timeout in (True, False):
            with self.subTest(observe_timeout=observe_timeout):
                c = DriveController()
                c.receive(self.command(), 0)
                self.assertTrue(any(c.output(400)))
                if observe_timeout:
                    self.assertEqual(c.output(401), (0, 0, 0, 0))
                self.assertFalse(c.receive(self.command(resume=False), 401))
                self.assertEqual(c.output(500), (0, 0, 0, 0))
                self.assertTrue(c.receive(self.command(), 600))
                self.assertTrue(any(c.output(600)))

    def test_invalid_motion_requires_resume_after_correction(self):
        for bad in (None, {}, self.command(vx=2), self.command(vy=float('nan')),
                    self.command(wz=10**1000)):
            c = DriveController()
            c.receive(self.command(), 0)
            self.assertFalse(c.receive(bad, 100))
            self.assertFalse(c.receive(self.command(resume=False), 200))
            self.assertEqual(c.output(200), (0, 0, 0, 0))
            self.assertTrue(c.receive(self.command(), 300))
