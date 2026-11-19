"""Run on a desktop: python3 firmware/simulate.py"""
from drive_logic import DriveController, HeadController, FollowController
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

def observation(now, **changes):
    # Synthetic fixture: these values are not camera detections or sensor readings.
    data = dict(cmd='follow', armed=True, target_visible=True, sensor_ok=True,
                target_ms=now, obstacle_ms=now, obstacle_cm=100,
                vx=0.5, vy=0, wz=0, pan_deg=30, tilt_deg=10)
    data.update(changes)
    return data

print('\nFollow-mode supervisor with synthetic observations:')
for label, changes in [('Target lost', dict(target_visible=False)),
                       ('Obstacle close', dict(obstacle_cm=20)),
                       ('Sensor fault', dict(sensor_ok=False))]:
    follow = FollowController()
    assert follow.receive(observation(0, resume=True), 0)
    follow.receive(observation(100, **changes), 100)
    state = follow.output(100)
    print(label + ':', state)
    assert not state['armed'] and not any(state['wheels'])
    held = state['head_deg']
    assert follow.output(1000)['head_deg'] == held

follow = FollowController()
follow.receive(observation(0, resume=True), 0)
print('Fresh observation:', follow.output(100))
stale = follow.output(201)
print('No new sensor samples:', stale)
assert not stale['armed'] and not any(stale['wheels'])
assert not follow.receive(observation(210), 210)  # Clearing a fault does not resume.
print('Clear sample without resume:', follow.output(210))
assert follow.receive(observation(220, resume=True), 220)
print('Explicit fresh resume:', follow.output(220))
print('Simulation only. No camera, sensors, motors, GPIO pins or serial devices were accessed.')


