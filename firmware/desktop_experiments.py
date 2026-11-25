"""Optional desktop experiments for movement and recorded video. The Pico does not load this file."""
from experiments.video import (
    detection_report, box_coordinates, box_iou, BoxTargetLock,
    make_people_detector, video_reports,
)
from drive_logic import DriveController
from desktop_models import HeadController, FollowController, TiltPulsePlanner


def demo_drive():
    controller = DriveController()
    drive = dict(cmd='drive', armed=True, vx=0.5, vy=0, wz=0.1)
    assert controller.receive(dict(drive, resume=True), 0)
    print('Simulated FL/FR/RL/RR at 0 ms:', controller.output(0))
    print('After command timeout at 401 ms:', controller.output(401))
    accepted = controller.receive(drive, 500)
    print('Ordinary drive command after timeout accepted:', accepted)
    assert not accepted and not any(controller.output(500))
    assert controller.receive(dict(drive, resume=True), 600)
    print('Explicit drive resume at 600 ms:', controller.output(600))
    assert any(controller.output(600))
    controller.stop()



def demo_head():
    head = HeadController()
    target = dict(cmd='head', armed=True, pan_deg=30, tilt_deg=10)
    print('\nSimulated head angles: (pan degrees, tilt degrees)')
    assert head.receive(dict(target, resume=True), 0)
    for now in (100, 200, 300):
        head.receive(target, now)  # Refresh before the 400 ms command watchdog.
        print('At {} ms: {}'.format(now, head.output(now)))
    print('After lost commands at 701 ms:', head.output(701), 'armed:', head.armed)
    held = head.position
    print('Later at 1000 ms:', head.output(1000))
    assert head.position == held and not head.armed
    accepted = head.receive(target, 1000)
    print('Ordinary head command after timeout accepted:', accepted)
    assert not accepted and head.output(1100) == held
    assert head.receive(dict(target, resume=True), 1100)
    print('After explicit head resume at 1200 ms:', head.output(1200))
    assert head.armed and head.position != held
    accepted = head.receive(dict(cmd='head', armed=True, pan_deg=181, tilt_deg=0), 1200)
    print('Out-of-range pan accepted:', accepted)
    assert not accepted



def demo_tilt():
    tilt = TiltPulsePlanner()
    print('\nPlanned tilt pulse widths (desktop calculation; no PWM output):')
    for angle in (-30, 0, 30):
        print('{} degrees -> {} us'.format(angle, tilt.pulse_us(angle)))
    try:
        tilt.pulse_us(31)
    except ValueError:
        print('31-degree tilt rejected by the planning limit')
    else:
        raise AssertionError('out-of-range tilt accepted')



def demo_follow():
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


def run_demo():
    demo_drive()
    demo_head()
    demo_tilt()
    demo_follow()
    print('Simulation only. No camera, sensors, motors, GPIO pins or serial devices were accessed.')
