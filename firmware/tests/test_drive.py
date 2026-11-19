import unittest, sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from drive_logic import DriveController, HeadController, FollowController, mix
from simulate import detection_report, video_reports, make_people_detector, BoxTargetLock, box_iou

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


class FollowTests(unittest.TestCase):
    def sample(self, now=0, **changes):
        data = dict(cmd='follow', armed=True, target_visible=True, sensor_ok=True,
                    target_ms=now, obstacle_ms=now, obstacle_cm=100,
                    vx=0.5, vy=0, wz=0, pan_deg=30, tilt_deg=10)
        data.update(changes)
        return data

    def started(self):
        c = FollowController()
        self.assertTrue(c.receive(self.sample(resume=True), 0))
        return c

    def assertStopped(self, state):
        self.assertFalse(state['armed'])
        self.assertEqual(state['wheels'], (0.0,) * 4)

    def test_requires_explicit_resume_to_start(self):
        c = FollowController()
        self.assertFalse(c.receive(self.sample(), 0))
        self.assertStopped(c.output(0))
        self.assertTrue(c.receive(self.sample(resume=True), 0))
        self.assertTrue(c.output(0)['armed'])

    def test_valid_sample_coordinates_drive_and_head(self):
        c = self.started()
        state = c.output(100)
        self.assertEqual(state['head_deg'], (3.0, 1.5))
        self.assertTrue(any(state['wheels']))
        self.assertLessEqual(max(abs(x) for x in state['wheels']), 0.2)

    def test_target_loss_stops_drive_and_freezes_head(self):
        c = self.started()
        self.assertFalse(c.receive(self.sample(100, target_visible=False), 100))
        state = c.output(100)
        self.assertStopped(state)
        self.assertEqual(state['reason'], 'target_lost')
        self.assertEqual(c.output(5000)['head_deg'], state['head_deg'])

    def test_obstacle_threshold_includes_boundary_and_zero(self):
        for distance in [0, 29.9, 30]:
            c = self.started()
            self.assertFalse(c.receive(self.sample(100, obstacle_cm=distance), 100))
            self.assertStopped(c.output(100))
            self.assertEqual(c.reason, 'obstacle')
        self.assertTrue(FollowController().receive(self.sample(resume=True, obstacle_cm=30.1), 0))

    def test_sensor_fault_stops_both_controllers(self):
        c = self.started()
        self.assertFalse(c.receive(self.sample(100, sensor_ok=False), 100))
        self.assertStopped(c.output(100))
        self.assertFalse(c.drive.armed)
        self.assertFalse(c.head.armed)
        self.assertEqual(c.reason, 'sensor_fault')

    def test_camera_and_range_have_independent_freshness(self):
        for changes in [dict(target_ms=0), dict(obstacle_ms=0),
                        dict(target_ms=301), dict(obstacle_ms=301)]:
            c = FollowController()
            self.assertFalse(c.receive(self.sample(300, resume=True, **changes), 300))
            self.assertStopped(c.output(300))
            self.assertEqual(c.reason, 'stale_observation')

    def test_replayed_samples_do_not_extend_freshness(self):
        c = self.started()
        for now in [50, 100, 150, 200]:
            self.assertTrue(c.receive(self.sample(), now))
        self.assertTrue(c.output(200)['armed'])
        self.assertStopped(c.output(201))
        self.assertEqual(c.reason, 'stale_observation')

    def test_late_update_integrates_head_only_until_sample_deadline(self):
        c = self.started()
        state = c.output(10000)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (6.0, 3.0))
        self.assertEqual(state['reason'], 'stale_observation')

    def test_clear_sample_does_not_resume_after_a_stop(self):
        c = self.started()
        c.receive(self.sample(100, obstacle_cm=10), 100)
        self.assertFalse(c.receive(self.sample(110), 110))
        self.assertStopped(c.output(110))
        self.assertFalse(c.receive(self.sample(120, resume=True, obstacle_cm=10), 120))
        self.assertTrue(c.receive(self.sample(130, resume=True), 130))
        self.assertTrue(c.output(130)['armed'])

    def test_invalid_observations_and_intent_disarm(self):
        for bad in [None, {}, self.sample(100, armed=1),
                    self.sample(100, target_visible=1), self.sample(100, sensor_ok=None),
                    self.sample(100, obstacle_cm=float('nan')),
                    self.sample(100, obstacle_cm=-1), self.sample(100, obstacle_cm=None),
                    self.sample(100, obstacle_ms=True), self.sample(100, resume='yes'),
                    self.sample(100, vx=2), self.sample(100, pan_deg=181)]:
            c = self.started()
            self.assertFalse(c.receive(bad, 100))
            self.assertStopped(c.output(100))
            self.assertFalse(c.head.armed)

    def test_explicit_stop_holds_until_fresh_resume(self):
        c = self.started()
        self.assertTrue(c.receive(dict(cmd='stop'), 100))
        state = c.output(1000)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (3.0, 1.5))

    def test_time_reversal_disarms_without_moving_head(self):
        c = self.started()
        held = c.output(100)['head_deg']
        self.assertFalse(c.receive(self.sample(99, resume=True), 99))
        self.assertStopped(c.output(100))
        self.assertEqual(c.head.position, held)
        self.assertEqual(c.reason, 'invalid_time')

    def test_configuration_and_controller_timeout_ceiling(self):
        for kwargs in [dict(obstacle_stop_cm=-1), dict(obstacle_stop_cm=True),
                       dict(sample_timeout_ms=0), dict(sample_timeout_ms=True)]:
            with self.assertRaises(ValueError):
                FollowController(**kwargs)
        c = FollowController(sample_timeout_ms=1000)
        c.receive(self.sample(resume=True), 0)
        state = c.output(401)
        self.assertStopped(state)
        self.assertEqual(state['head_deg'], (12.0, 6.0))


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


if __name__=='__main__':unittest.main()




