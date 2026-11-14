# D645MW tilt fit review

The official [Hitec D645MW STEP download](https://www.hitecrcd.co.kr/products/d645mw/) was used with the repaired head and camera STEP files. The internal static box study did not establish usable tilt travel. Its trial sweep hit the carrier at ±20°. The official STEP in a trial internal shaft-aligned placement intersected the shell even at neutral.

The side mount places the servo beside the shell, with the physical output axis pointing along X through Y=28 mm and Z=212.5 mm in the original head coordinates. Rotate the vendor STEP 90° about Z, then translate by (59, 18, 212.5) mm. The closest servo point is at X=42.5 mm and the head ends at X=40 mm. Rotation about X preserves this separation throughout tilt. The carrier, lens, and PCB respectively have 24.5, 37.5 and 30.0 mm of lateral separation from the vendor servo geometry. Translate the complete layout up 20 mm for the raised pan concept.

Review proposal: retain the existing chassis and use a pan-mounted yoke, with the D645MW supported on one side and a coaxial support bearing on the other. The horn and mating plate must bridge the lateral gap. Set the yoke footprint and verify the stiffness, horn fasteners, bearing support, camera ribbon service loop, and pan clearance with the added side-mounted weight and width. Neither the yoke nor the ribbon is represented in this check. The external position is a packaging candidate and does not establish a final operating range.

Run `python cad/tilt_fit_check.py cad/parts /path/to/D645MW.stp` with CadQuery installed.
