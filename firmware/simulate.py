"""Run a basic wheel demo or optional desktop experiments."""
import argparse
import json
from pathlib import Path
from drive_logic import DriveController, mix
from desktop_experiments import (
    demo_drive, demo_head, demo_tilt, demo_follow, run_demo,
    detection_report, box_coordinates, box_iou, BoxTargetLock,
    make_people_detector, video_reports,
)


def drive_example():
    for label, axes in [('Forward', (1, 0, 0)),
                        ('Sideways', (0, 1, 0)),
                        ('Turn', (0, 0, 1))]:
        print(label, mix(*axes))

    drive = DriveController()
    command = dict(cmd='drive', armed=True, resume=True, vx=.5, vy=0, wz=0)
    drive.receive(command, 0)
    print('Drive:', drive.output(0))
    print('After timeout:', drive.output(401))
    print('Desktop only: no motors are connected.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, help='local recorded video; detection diagnostics only')
    parser.add_argument('--max-frames', type=int, default=300, help='video frame limit (default: 300)')
    parser.add_argument('--target-index', type=int, help='zero-based detection index to select explicitly')
    parser.add_argument('--select-frame', type=int, default=0,
                        help='zero-based frame on which to select (default: 0)')
    parser.add_argument('--full', action='store_true', help='run the desktop head and follow experiments')
    args = parser.parse_args(argv)
    if args.max_frames <= 0:
        parser.error('--max-frames must be positive')
    if args.video is None and (args.target_index is not None or args.select_frame != 0):
        parser.error('target selection requires --video')
    try:
        if args.video is None:
            if args.full:
                run_demo()
            else:
                drive_example()
        else:
            for report in video_reports(args.video, args.max_frames,
                                        target_index=args.target_index,
                                        select_frame=args.select_frame):
                print(json.dumps(report, allow_nan=False))
    except (ValueError, RuntimeError) as exc:
        parser.exit(2, 'error: {}\n'.format(exc))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
