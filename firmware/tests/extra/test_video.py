import sys
import unittest
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from experiments.video import detection_report, video_reports, make_people_detector, BoxTargetLock, box_iou


class VideoTests(unittest.TestCase):
    class Frame:
        shape = (240, 320, 3)

    class Capture:
        def __init__(self, frames, opened=True):
            self.frames = iter(frames)
            self.opened = opened
            self.released = False
        def isOpened(self):
            return self.opened
        def read(self):
            frame = next(self.frames, None)
            return frame is not None, frame
        def release(self):
            self.released = True

    class Backend:
        def __init__(self, capture):
            self.capture = capture
        def VideoCapture(self, path):
            self.path = path
            return self.capture

    def test_no_person_and_multiple_candidates_do_not_select_a_target(self):
        for boxes, status in [([], 'no_person'),
                ([dict(box=[0, 0, 50, 100], score=1),
                  dict(box=[100, 0, 50, 100], score=2)], 'multiple_candidates')]:
            report = detection_report(0, 320, 240, boxes)
            self.assertEqual(report['status'], status)
            self.assertNotIn('center_offset', report)
            self.assertFalse(report['motion_enabled'])

    def test_single_candidate_reports_normalized_center_without_motion(self):
        report = detection_report(3, 320, 240,
                                  [dict(box=[120, 60, 80, 120], score=2)])
        self.assertEqual(report['status'], 'one_person_candidate')
        self.assertEqual(report['center_offset'], dict(x=0.0, y=0.0))
        self.assertFalse(report['motion_enabled'])

    def test_bad_detection_coordinates_are_rejected(self):
        for box in [[-1, 0, 50, 100], [0, 0, 0, 100], [300, 0, 50, 100],
                    [0, 0, 50, float('nan')], [True, 0, 50, 100]]:
            with self.assertRaises(ValueError):
                detection_report(0, 320, 240, [dict(box=box, score=1)])
        with self.assertRaises(ValueError):
            detection_report(0, 320, 240, [dict(box=[0, 0, 50, 100], score=float('inf'))])

    def test_video_eof_emits_final_status_and_releases_file(self):
        cap = self.Capture([self.Frame(), self.Frame()])
        with tempfile.NamedTemporaryFile() as f:
            reports = list(video_reports(f.name, cv_module=self.Backend(cap), detector=lambda frame: []))
        self.assertEqual([r.get('frame') for r in reports[:-1]], [0, 1])
        self.assertEqual(reports[-1], dict(status='end_of_video', frames=2, motion_enabled=False,
                         target=dict(state='unselected', reason='not_selected', box=None, candidate_index=None)))
        self.assertTrue(cap.released)
        self.assertTrue(all(r['motion_enabled'] is False for r in reports))

    def test_frame_limit_and_early_close_release_capture(self):
        cap = self.Capture([self.Frame(), self.Frame()])
        with tempfile.NamedTemporaryFile() as f:
            reports = list(video_reports(f.name, 1, self.Backend(cap), lambda frame: []))
        self.assertEqual(reports[-1]['status'], 'frame_limit')
        self.assertTrue(cap.released)
        cap = self.Capture([self.Frame(), self.Frame()])
        with tempfile.NamedTemporaryFile() as f:
            stream = video_reports(f.name, cv_module=self.Backend(cap), detector=lambda frame: [])
            next(stream)
            stream.close()
        self.assertTrue(cap.released)

    def test_open_decode_and_detector_errors_release_capture(self):
        for frames, opened in [([], False), ([], True)]:
            cap = self.Capture(frames, opened)
            with tempfile.NamedTemporaryFile() as f:
                with self.assertRaises(ValueError):
                    list(video_reports(f.name, cv_module=self.Backend(cap), detector=lambda frame: []))
            self.assertTrue(cap.released)
        cap = self.Capture([self.Frame()])
        def broken(frame):
            raise RuntimeError('detector failed')
        with tempfile.NamedTemporaryFile() as f:
            with self.assertRaises(RuntimeError):
                list(video_reports(f.name, cv_module=self.Backend(cap), detector=broken))
        self.assertTrue(cap.released)

    def test_video_requires_a_local_file_and_positive_frame_limit(self):
        with self.assertRaises(ValueError):
            list(video_reports('https://example.com/video.mp4'))
        for limit in [0, -1, True, 1.5]:
            with self.assertRaises(ValueError):
                list(video_reports('missing.avi', limit))

    def test_detector_resize_maps_boxes_back_to_original_frame(self):
        class HOG:
            def setSVMDetector(self, coefficients):
                pass
            def detectMultiScale(self, frame, **kwargs):
                return [(100, 50, 100, 200)], [2.0]
        class CV:
            HOGDescriptor = HOG
            @staticmethod
            def HOGDescriptor_getDefaultPeopleDetector():
                return [1]
            @staticmethod
            def resize(frame, size):
                class Resized:
                    shape = (size[1], size[0], 3)
                return Resized()
        class Large:
            shape = (960, 1280, 3)
        detect = make_people_detector(CV)
        self.assertEqual(detect(Large()), [dict(box=[200, 100, 200, 400], score=2.0)])
        class Small:
            shape = (60, 40, 3)
        self.assertEqual(detect(Small()), [])


class TargetLockTests(unittest.TestCase):
    def detection(self, x=100, y=40, w=80, h=160, score=1):
        return dict(box=[x, y, w, h], score=score)

    def selected(self):
        target = BoxTargetLock()
        target.select([self.detection()], 0, (640, 480))
        return target

    def test_iou_identity_disjoint_and_partial_overlap(self):
        self.assertEqual(box_iou((0, 0, 10, 10), (0, 0, 10, 10)), 1)
        self.assertEqual(box_iou((0, 0, 10, 10), (20, 0, 10, 10)), 0)
        self.assertAlmostEqual(box_iou((0, 0, 10, 10), (2, 0, 10, 10)), 2/3)

    def test_target_is_never_automatically_selected(self):
        t = BoxTargetLock()
        self.assertEqual(t.update([self.detection()], (640, 480))['state'], 'unselected')

    def test_selected_box_wins_over_larger_high_scoring_bystander(self):
        t = self.selected()
        state = t.update([self.detection(x=350, w=200, h=300, score=10),
                          self.detection(x=105, score=0.6)], (640, 480))
        self.assertEqual(state['state'], 'locked')
        self.assertEqual(state['candidate_index'], 1)
        self.assertEqual(state['box'][0], 105)
        self.assertAlmostEqual(state['center_offset']['x'], 2*(105+40)/640-1)

    def test_detection_order_changes_do_not_change_the_matching_box(self):
        t = BoxTargetLock()
        person, other = self.detection(), self.detection(x=400)
        t.select([other, person], 1, (640, 480))
        state = t.update([person, other], (640, 480))
        self.assertEqual(state['candidate_index'], 0)
        self.assertEqual(state['box'], person['box'])

    def test_missing_target_latches_loss_even_if_it_reappears(self):
        t = self.selected()
        self.assertEqual(t.update([], (640, 480))['state'], 'lost')
        state = t.update([self.detection()], (640, 480))
        self.assertEqual(state['state'], 'lost')
        self.assertIsNone(state['box'])
        self.assertEqual(t.select([self.detection()], 0, (640, 480))['state'], 'locked')

    def test_nonoverlapping_bystander_does_not_replace_lost_target(self):
        state = self.selected().update([self.detection(x=400)], (640, 480))
        self.assertEqual(state['reason'], 'no_overlap')
        self.assertIsNone(state['candidate_index'])

    def test_ambiguous_overlap_latches_loss(self):
        t = self.selected()
        state = t.update([self.detection(x=99), self.detection(x=101)], (640, 480))
        self.assertEqual(state['state'], 'lost')
        self.assertEqual(state['reason'], 'ambiguous_overlap')

    def test_frame_size_change_requires_reselection(self):
        state = self.selected().update([self.detection()], (1280, 960))
        self.assertEqual(state['state'], 'lost')
        self.assertEqual(state['reason'], 'frame_size_changed')

    def test_snapshot_boxes_do_not_mutate_tracker_or_previous_reports(self):
        t = self.selected()
        first = t.snapshot()
        first['box'][0] = 500
        self.assertEqual(t.box[0], 100)
        old = t.snapshot()
        t.update([self.detection(x=105)], (640, 480))
        self.assertEqual(old['box'][0], 100)

    def test_invalid_thresholds_selection_and_boxes_are_rejected(self):
        for kwargs in [dict(min_iou=0), dict(min_iou=True), dict(min_iou=1.1),
                       dict(ambiguity_margin=-1), dict(ambiguity_margin=float('nan'))]:
            with self.assertRaises(ValueError):
                BoxTargetLock(**kwargs)
        t = BoxTargetLock()
        for index in [-1, True, 1, 0.5]:
            with self.assertRaises(ValueError):
                t.select([self.detection()], index, (640, 480))
        for box in [[0, 0, 0, 1], [0, 0, 1, float('nan')], [True, 0, 1, 1]]:
            with self.assertRaises(ValueError):
                t.select([dict(box=box)], 0, (640, 480))

    def reports(self, batches, **options):
        cap = VideoTests.Capture([VideoTests.Frame() for _ in batches])
        batches = iter(batches)
        with tempfile.NamedTemporaryFile() as f:
            reports = list(video_reports(f.name, cv_module=VideoTests.Backend(cap),
                           detector=lambda frame: next(batches), **options))
        self.assertTrue(cap.released)
        self.assertTrue(all(r['motion_enabled'] is False for r in reports))
        return reports

    def test_video_selects_only_requested_frame_then_latches_loss(self):
        person = self.detection()
        reports = self.reports([[], [person], [], [person]], target_index=0, select_frame=1)
        self.assertEqual([r['target']['state'] for r in reports],
                         ['unselected', 'locked', 'lost', 'lost', 'lost'])

    def test_unavailable_selection_is_not_retried_on_later_frames(self):
        reports = self.reports([[], [self.detection()]], target_index=0)
        self.assertTrue(all(r['target']['state'] == 'lost' for r in reports))
        self.assertEqual(reports[0]['target']['reason'], 'selection_unavailable')

    def test_eof_and_frame_limit_clear_an_active_lock(self):
        for options, reason in [({}, 'end_of_video'), (dict(max_frames=1), 'frame_limit')]:
            reports = self.reports([[self.detection()]], target_index=0, **options)
            self.assertEqual(reports[0]['target']['state'], 'locked')
            self.assertEqual(reports[-1]['target']['state'], 'lost')
            self.assertEqual(reports[-1]['target']['reason'], reason)

    def test_invalid_selection_options_fail_before_opening_file(self):
        for options in [dict(target_index=-1), dict(target_index=True),
                        dict(target_index=0, select_frame=-1),
                        dict(target_index=0, select_frame=300), dict(select_frame=2)]:
            with self.assertRaises(ValueError):
                list(video_reports('unused.avi', **options))
