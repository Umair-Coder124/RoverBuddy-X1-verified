# Build checklist

## Before ordering

- [ ] Check Fallen review status and funding.
- [ ] Confirm the exact parts, stock, delivered prices, shipping and tax in the [BOM](../BOM.md).
- [ ] Check FR12-H101K pan bracket fit, R-ML25 tilt horn fit and whether extra X3P cables are needed.
- [ ] Get quotes for the remaining custom tilt bracket, neck brackets, bearing plates and pivot hardware. Confirm fastener quantities.
- [ ] Confirm D645MW input voltage limits and whether a PWM buffer is needed.

## CAD and mounting

- [ ] Independently inspect the revised tilt bearing and shaft retention, neck attachment, and bolt fit against Sophia's feedback.
- [ ] Export the reviewed assembly, individual revised STEP files and updated screenshots to GitHub.
- [x] Widen the cable opening in the draft and check the centerline at the neutral position.
- [ ] Check the real ribbon width, bending and clearance throughout head movement. Review the shell strength before printing.

- [ ] Compare the latest STEP with the Onshape import in a separate revision.
- [ ] Check the pan mount gap (41 mm in the raised study versus a 42.7 mm reference envelope), screw holes, shaft position and coupling.
- [ ] Compare actual tilt servo and horn dimensions with the supplier drawing before fabrication.
- [ ] Check all mounting holes, fasteners, wheel clearance, camera alignment, connector access and cable movement.
- [ ] Check the 500 mm camera ribbon throughout head travel. The longest sampled route was 342 mm; the remaining 158 mm also has to cover bends and connectors.
- [ ] Find room for the DFR0946 (70 × 39 × 32 mm), wiring and airflow.

## Before powering

- [ ] Have a qualified adult check the complete power circuit, battery protection, independent hardware stop, cable ratings, voltage regulation, grounding and isolation.
- [ ] Confirm GPIO, sensor level conversion, startup behavior, servo travel and wheel polarity.
- [ ] Complete the pin-to-pin schematic, power budget and supervised bench checks.
- [ ] Assemble with power off. Keep actuators disabled until checks pass.
- [ ] Record supervised real-world tests and fix any failures before a working demo.

See the [wiring notes](WIRING.md) and [CAD notes](../cad/README.md).

## Previous design notes

Earlier measurements and decisions remain available in Git history:

- [November 20 design check](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/docs/2026-11-20-design-review.md)
- [November 21 parts plan](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/docs/2026-11-21-procurement-review.md)
- [November 21 mounting check](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/cad/2026-11-21-mounting-review.md)
