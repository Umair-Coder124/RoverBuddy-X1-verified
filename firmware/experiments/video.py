"""Find and track a person in a recorded video."""
from pathlib import Path
from drive_logic import finite_number


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
        if (len(box) != 4 or any(not finite_number(v) for v in box)
                or not finite_number(score)):
            raise ValueError('finite detection coordinates and score required')
        x, y, w, h = box
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            raise ValueError('detection box must be inside the frame')
        valid.append(dict(box=list(box), score=float(score)))
    if not valid:
        status = 'no_person'
    elif len(valid) == 1:
        status = 'one_person_candidate'
    else:
        status = 'multiple_candidates'
    report = dict(frame=index, width=width, height=height, status=status,
                  detections=valid, motion_enabled=False)
    if len(valid) == 1:
        x, y, w, h = valid[0]['box']
        report['center_offset'] = dict(x=2 * (x + w / 2) / width - 1,
                                       y=2 * (y + h / 2) / height - 1)
    return report


def box_coordinates(detection):
    try:
        box = tuple(detection['box'])
        if (len(box) != 4 or any(not finite_number(v) for v in box)
                or box[0] < 0 or box[1] < 0 or box[2] <= 0 or box[3] <= 0):
            raise ValueError('invalid target box')
        return box
    except (KeyError, TypeError) as exc:
        raise ValueError('target detection needs a valid box') from exc


def box_iou(a, b):
    """Intersection-over-union for finite (x, y, width, height) boxes."""
    a, b = box_coordinates(dict(box=a)), box_coordinates(dict(box=b))
    left, top = max(a[0], b[0]), max(a[1], b[1])
    right, bottom = min(a[0]+a[2], b[0]+b[2]), min(a[1]+a[3], b[1]+b[3])
    area = max(0, right-left) * max(0, bottom-top)
    return area / (a[2]*a[3] + b[2]*b[3] - area)


class BoxTargetLock:
    """Conservative box-overlap association, not person identity recognition."""
    def __init__(self, min_iou=0.3, ambiguity_margin=0.1):
        if (not finite_number(min_iou) or not 0 < min_iou <= 1
                or not finite_number(ambiguity_margin)
                or not 0 <= ambiguity_margin <= 1):
            raise ValueError('valid overlap and ambiguity thresholds required')
        self.min_iou = min_iou
        self.ambiguity_margin = ambiguity_margin
        self.state = 'unselected'
        self.reason = 'not_selected'
        self.box = None
        self.frame_size = None
        self.index = None

    def snapshot(self):
        result = dict(state=self.state, reason=self.reason,
                      box=list(self.box) if self.box is not None else None,
                      candidate_index=self.index)
        if self.state == 'locked':
            x, y, w, h = self.box
            width, height = self.frame_size
            result['center_offset'] = dict(x=2*(x+w/2)/width-1,
                                           y=2*(y+h/2)/height-1)
        return result

    def lose(self, reason):
        self.state, self.reason = 'lost', reason
        self.box, self.index = None, None
        return self.snapshot()

    def select(self, detections, index, frame_size):
        if (isinstance(index, bool) or not isinstance(index, int)
                or index < 0 or index >= len(detections)):
            raise ValueError('selection index is unavailable in this frame')
        size = tuple(frame_size)
        if (len(size) != 2 or any(isinstance(v, bool) or not isinstance(v, int)
                                 or v <= 0 for v in size)):
            raise ValueError('positive integer frame size required')
        self.box = box_coordinates(detections[index])
        self.frame_size = size
        self.index = index
        self.state, self.reason = 'locked', 'selected'
        return self.snapshot()

    def update(self, detections, frame_size):
        if self.state != 'locked':
            return self.snapshot()
        if tuple(frame_size) != self.frame_size:
            return self.lose('frame_size_changed')
        matches = []
        for index, detection in enumerate(detections):
            box = box_coordinates(detection)
            overlap = box_iou(self.box, box)
            if overlap >= self.min_iou:
                matches.append((overlap, index, box))
        matches.sort(reverse=True)
        if not matches:
            return self.lose('no_overlap')
        if len(matches) > 1 and matches[0][0] - matches[1][0] <= self.ambiguity_margin:
            return self.lose('ambiguous_overlap')
        _, self.index, self.box = matches[0]
        self.reason = 'overlap_match'
        return self.snapshot()


def make_people_detector(cv):
    """OpenCV HOG baseline; scores are SVM margins, not probabilities."""
    hog = cv.HOGDescriptor()
    hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    def detect(frame):
        height, width = frame.shape[:2]
        factor = min(1.0, 640.0 / width)
        small = frame
        if factor < 1:
            new_width = max(1, round(width * factor))
            new_height = max(1, round(height * factor))
            small = cv.resize(frame, (new_width, new_height))
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


def video_reports(video_path, max_frames=300, cv_module=None, detector=None,
                  target_index=None, select_frame=0):
    """Read only an explicitly supplied local file; yield JSON-ready diagnostics."""
    if isinstance(max_frames, bool) or not isinstance(max_frames, int) or max_frames <= 0:
        raise ValueError('max_frames must be a positive integer')
    if (isinstance(select_frame, bool) or not isinstance(select_frame, int)
            or not 0 <= select_frame < max_frames):
        raise ValueError('select_frame must be inside the processed frame range')
    if target_index is not None:
        if isinstance(target_index, bool) or not isinstance(target_index, int) or target_index < 0:
            raise ValueError('target_index must be a nonnegative integer')
    elif select_frame != 0:
        raise ValueError('select_frame requires a target_index')
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
    target = BoxTargetLock()
    try:
        if not cap.isOpened():
            raise ValueError('could not open the video file')
        detect = detector if detector is not None else make_people_detector(cv_module)
        while count < max_frames:
            ok, frame = cap.read()
            if not ok:
                if count == 0:
                    raise ValueError('video contains no decodable frames')
                if target.state == 'locked':
                    target.lose('end_of_video')
                yield dict(status='end_of_video', frames=count, motion_enabled=False,
                           target=target.snapshot())
                return
            height, width = frame.shape[:2]
            report = detection_report(count, int(width), int(height), detect(frame))
            if target_index is not None and count == select_frame:
                try:
                    target.select(report['detections'], target_index, (int(width), int(height)))
                except ValueError:
                    target.lose('selection_unavailable')
            else:
                target.update(report['detections'], (int(width), int(height)))
            report['target'] = target.snapshot()
            yield report
            count += 1
        if target.state == 'locked':
            target.lose('frame_limit')
        yield dict(status='frame_limit', frames=count, motion_enabled=False,
                   target=target.snapshot())
    finally:
        cap.release()
