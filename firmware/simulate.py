"""Run on a desktop: python3 firmware/simulate.py"""
from drive_logic import DriveController, HeadController
controller = DriveController()
controller.receive({'cmd':'drive','armed':True,'vx':0.5,'vy':0,'wz':0.1}, 0)
print('Simulated FL/FR/RL/RR at 0 ms:', controller.output(0))
print('After command timeout at 401 ms:', controller.output(401))

head = HeadController()
target = dict(cmd='head', armed=True, pan_deg=30, tilt_deg=10)
print('\nSimulated head angles: (pan degrees, tilt degrees)')
head.receive(target, 0)
for now in (100, 200, 300):
    head.receive(target, now)  # Refresh before the 400 ms command watchdog.
    print('At {} ms: {}'.format(now, head.output(now)))
print('After lost commands at 701 ms:', head.output(701), 'armed:', head.armed)
held = head.position
print('Later at 1000 ms:', head.output(1000))
assert head.position == held and not head.armed
accepted = head.receive(dict(cmd='head', armed=True, pan_deg=181, tilt_deg=0), 1000)
print('Out-of-range pan accepted:', accepted)
assert not accepted
print('Simulation only. No motors, GPIO pins or serial devices were accessed.')

