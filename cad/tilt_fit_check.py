"""Screen the shell and camera against a stationary tilt-servo envelope."""
import argparse
from pathlib import Path

import cadquery as cq

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("parts", type=Path, help="Directory containing the repaired part STEP files")
parser.add_argument("servo", type=Path, help="Hitec D645MW.stp")
args = parser.parse_args()

# Original, unraised head coordinates. The axis is a trial location.
servo = cq.Compound.makeCompound(cq.importers.importStep(str(args.servo)).solids().vals())
servo = servo.rotate((0, 0, 0), (0, 0, 1), 90).translate((59, 18, 212.5))
moving = {}
for prefix in ("Hollow_Head_", "Camera_"):
    for path in sorted(args.parts.glob(f"{prefix}*.step")):
        moving[path.stem] = cq.importers.importStep(str(path)).val()
if len(moving) != 4:
    parser.error("expected one head shell and three camera STEP files")

# Rotation about X preserves every point's X coordinate.
servo_min = servo.BoundingBox().xmin
for name, part in moving.items():
    gap = servo_min - part.BoundingBox().xmax
    if gap <= 0:
        raise ValueError(f"No separating X interval for {name}")
    print(f"{name}: {gap:.3f} mm lateral clearance across the full sweep")
