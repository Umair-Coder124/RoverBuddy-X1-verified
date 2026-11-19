"""Desktop motion simulation and optional local-video detection; no hardware output."""
import argparse
import json
from pathlib import Path
from drive_logic import DriveController, HeadController, FollowController


def run_demo():
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


def detection_report(index, width, height, candidates):
    """Describe detections without selecting identity or enabling any motion."""
    if (isinstance(width, bool) or isinstance(height, bool)
            or not isinstance(width, int) or not isinstance(height, int)
            or width <= 0 or height <= 0):
        raise ValueError('positive integer frame dimensions required')
    valid = []
    for candidate in candidates:
        box = tuple(candidate['box'])
        score = candidate['score']
        if (len(box) != 4 or any(not HeadController._number(v) for v in box)
                or not HeadController._number(score)):
            raise ValueError('finite detection coordinates and score required')
        x, y, w, h = box
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            raise ValueError('detection box must be inside the frame')
        valid.append(dict(box=list(box), score=float(score)))
    status = ('no_person' if not valid else
              'one_person_candidate' if len(valid) == 1 else 'multiple_candidates')
    report = dict(frame=index, width=width, height=height, status=status,
                  detections=valid, motion_enabled=False)
    if len(valid) == 1:
        x, y, w, h = valid[0]['box']
        report['center_offset'] = dict(x=2 * (x + w / 2) / width - 1,
                                       y=2 * (y + h / 2) / height - 1)
    return report


def make_people_detector(cv):
    """OpenCV HOG baseline; scores are SVM margins, not probabilities."""
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    def detect(frame):
        height, width = frame.shape[:2]
        factor = min(1.0, 640.0 / width)
        small = (cv.resize(frame, (max(1, round(width * factor)),
                                   max(1, round(height * factor))))
                 if factor < 1 else frame)
        sh, sw = small.shape[:2]
        if sw < 64 or sh < 128:
            return []
        boxes, scores = hog.detectMultiScale(small, hitThreshold=0.5,
                                            winStride=(8, 8), padding=(8, 8),
                                            scale=1.05)
        result = []
        for (x, y, w, h), score in zip(boxes, scores):
            # Map back to the original frame and clip to its actual boundaries.
            left = max(0, round(float(x) * width / sw))
            top = max(0, round(float(y) * height / sh))
            right = min(width, round(float(x + w) * width / sw))
            bottom = min(height, round(float(y + h) * height / sh))
            if right > left and bottom > top:
                result.append(dict(box=[left, top, right-left, bottom-top],
                                   score=float(score)))
        return result
    return detect


def video_reports(video_path, max_frames=300, cv_module=None, detector=None):
    """Read only an explicitly supplied local file; yield JSON-ready diagnostics."""
    if isinstance(max_frames, bool) or not isinstance(max_frames, int) or max_frames <= 0:
        raise ValueError('max_frames must be a positive integer')
    path = Path(video_path)
    if not path.is_file():
        raise ValueError('video must be an existing local file')
    if cv_module is None:
        try:
            import cv2 as cv_module
        except ImportError as exc:
            raise RuntimeError('Video mode needs opencv-python-headless; see firmware/README.md') from exc
    cap = cv_module.VideoCapture(str(path.resolve()))
    count = 0
    try:
        if not cap.isOpened():
            raise ValueError('could not open the video file')
        detect = detector if detector is not None else make_people_detector(cv_module)
        while count < max_frames:
            ok, frame = cap.read()
            if not ok:
                if count == 0:
                    raise ValueError('video contains no decodable frames')
                yield dict(status='end_of_video', frames=count, motion_enabled=False)
                return
            height, width = frame.shape[:2]
            yield detection_report(count, int(width), int(height), detect(frame))
            count += 1
        yield dict(status='frame_limit', frames=count, motion_enabled=False)
    finally:
        cap.release()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, help='local recorded video; detection diagnostics only')
    parser.add_argument('--max-frames', type=int, default=300, help='video frame limit (default: 300)')
    args = parser.parse_args(argv)
    if args.max_frames <= 0:
        parser.error('--max-frames must be positive')
    try:
        if args.video is None:
            run_demo()
        else:
            for report in video_reports(args.video, args.max_frames):
                print(json.dumps(report, allow_nan=False))
    except (ValueError, RuntimeError) as exc:
        parser.exit(2, 'error: {}\n'.format(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())



