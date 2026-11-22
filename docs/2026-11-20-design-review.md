# Design check - November 20

This is a review of the design files, not a hardware test.

| Item | Review result |
| --- | --- |
| Camera ribbon | The cable route was checked in 65 model positions. The longest route was about 342 mm before extra cable allowance. The planned 500 mm cable still needs a real fit test. |
| Pan and tilt | The CAD and wiring documents use the XM430-W210-T pan and D645MW tilt candidates. Shaft coupling, fastener access, cable travel and actual bracket fit remain open. |
| CAD publication | The repository STEP and [CAD revision notes](../cad/README.md) are present. The README identifies the linked Onshape import as an earlier revision. Matching the live Onshape geometry to the STEP could not be verified in the browser because the workspace reported that WebGL was unavailable. |
| Wiring | The [SVG](wiring_draft.svg) and [wiring notes](WIRING.md) identify the DFR0946 candidate, U2D2 Power Hub and separate tilt supply. No electrical qualification is implied. |
| BOM | All 53 priced line totals equal quantity × unit price; subtotal is US$1,533.29. Four rows remain unpriced. Two outdated descriptions were corrected to reflect the already-priced DFR0946 candidate. Shipping, tax and protection hardware still need confirmation. |
| Fallen | Live submission status was not verified; the public portal does not show the personal submission. |

## Things still to check

- [ ] Import and inspect the latest repository STEP in the existing Onshape document without overwriting the native design prematurely.
- [ ] Record the actual ribbon fit and connector clearance at the neutral position and throughout the intended bounded range of motion.
- [ ] Verify actual actuator, adapter, horn and fastener fit before fabrication.
- [ ] Complete the power protection design and bench review with qualified adult supervision before connecting batteries or enabling actuators.
- [ ] Confirm all delivered prices and outstanding items before ordering.
- [ ] Check the existing Fallen submission status from the account dashboard.

Keep outputs disabled and the robot unpowered until the relevant hardware checks have passed. Existing digital studies and desktop checks are not physical test results.
