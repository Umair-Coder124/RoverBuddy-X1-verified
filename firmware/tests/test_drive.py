import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from drive_logic import DriveController, mix

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

if __name__=='__main__':unittest.main()
