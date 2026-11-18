# RoverBuddy X1 CAD studies

The [November 17 integrated CAD study](RoverBuddy_X1_Full_Pan_Tilt_Fit_Study.step) combines the lower camera cable route and corrected Pi tray. Import with appearances enabled. The [assembly preview](Assembly_Preview.png) and [rear preview](Integrated_Rear_Preview.png) show this STEP.

## November 17 study

- The neutral cable centerline exits through the head-floor opening before turning. The lower pan loop is modeled at Z = 193 mm with a 45 mm planning radius.
- The Pi mounting pattern is 58 × 49 mm. The board and cooler move 3 mm toward negative X, and the ribbon endpoint reference follows the board.
- Reopening the integrated STEP retained 155 named components. Checks involving the updated tray, spacers, board, cooler and neutral cable reference found no positive-volume overlaps.
- The earlier route sampling covered 65 poses at 30° pan and 15° tilt increments. Connector markers identify approximate areas. Actual connector positions and the physical ribbon remain open.
- The rendered cable uses a 1.3 mm diameter centerline marker for visibility. Check the real ribbon width, thickness, bending and twisting behavior on the build.
- Keep the 500 mm Standard-Mini camera ribbon as the physical-test candidate. The priced BOM still lists the earlier 300 mm cable pending product selection and delivered cost.

## Base assembly notes

The existing full-assembly STEP and Assembly_Preview.png paths now carry the integrated study. Earlier revisions remain accessible through Git history.

The notes below document the earlier detailed assembly based on the colored RoverBuddy STEP. Import
RoverBuddy_X1_Detailed_Assembly.step with **Import appearances** enabled.
The full assembly includes purchased component envelopes for fit review.
Parts_Manifest.csv identifies individual parts and reference models.
Interference_Check.csv records positive-volume intersections in this CAD
revision.

## How the parts attach

| Area | Modeled in this revision | Verify before printing or ordering |
|---|---|---|
| Four wheel corners | A shaft and supplied-coupling reference join each motor to its hub. Each 60 mm wheel has nine angled rollers. | Confirm the exact wheel and motor SKU from the kit or BOM, shaft cross section, usable engagement, retaining hardware, roller handedness, and clearance through full rotation. |
| Motor cradles | Four separate saddle brackets sit on the chassis. The chassis and cradles have matching nominal 3.1 mm holes and M3 screw envelopes. Each saddle has a removable cap. | Compare with the kit bracket if supplied. Confirm gearbox retention, real shaft position, cap hardware and loads. The hole pattern is for the concept cradle, not a vendor bracket. |
| Battery | A lengthwise 108 × 35 × 27 mm envelope sits in an open-end tray with strap slots. A raised Pi platform clears the pack in CAD. | Verify plug, strap, cable exit, withdrawal clearance, mounting hardware and protection components on the actual pack. |
| Pi and electronics | Four bridge supports, raised Pi plate, board spacers, and space claims for controllers and drivers. | Confirm exact PCB hole patterns, connector clearance, cooler envelope, wiring and regulators. Electronics footprint blocks are provisional. |
| Chest display | The chest shifted 14 mm toward the Pi to clear the front motors. Revised bezel, 121 × 89.48 mm display envelope, two side retainers and two chassis-to-chest brackets. | Verify active-area location, mounting pattern, connector clearance and clamp contact. The rectangular envelope is not a supplier STEP. |
| Camera and head | Lens opening, ribbon exit, internal camera carrier with edge retainers, lens and board references. | Confirm the board layout, hole positions, lens alignment and ribbon routing against the exact camera. Check cable movement throughout pan and tilt. |
| Neck | Pan shaft reference, head adapter, pan and tilt servo envelopes and support references. | Confirm real metal bracket, bearing and horn interfaces and servo sweep. The motion assembly is still a concept. |
| Obstacle sensor | Retained sensor envelope plus two supports. | Check actual board fasteners and clear sight lines for both transducers. |

## Hardware sources

The existing BOM read for this revision lists Adafruit 3777 and DFRobot
FIT0765/FIT0766 separately. If you are ordering a different matched kit,
substitute its product drawings before finalizing the mounts. The shaft
and bore in the CAD are explanatory references, with assumed shape and
placement. The manufacturer lists 70 × 22 × 18 mm for the motor body and
60 × 30.62 mm for the wheel.

- [Adafruit 3777 motor](https://www.adafruit.com/product/3777)
- [DFRobot FIT0765 left wheel](https://www.dfrobot.com/product-2268.html)
- [DFRobot FIT0766 right wheel](https://www.dfrobot.com/product-2269.html)
- [Raspberry Pi Camera Module 3 product brief](https://pip-assets.raspberrypi.com/categories/786-raspberry-pi-camera-module-3/documents/RP-008151-DS-1-camera-module-3-product-brief.pdf)
- [Waveshare display documentation](https://www.waveshare.com/wiki/5inch_HDMI_LCD_%28H%29_V4)

## Before submission

Review the colored STEP in Onshape as a separate revision. Once the exact kit
and connector dimensions are confirmed, revise the affected parts, finish
the pin-to-pin wiring diagram, and synchronize the CAD and BOM. Sophia said a
wiring diagram is acceptable for this module-based project. This package
addresses mechanical detail and component placement. Electrical validation,
hardware fit and a physical build are still pending.

