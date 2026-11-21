# November 21 mounting review

This dimensional review uses the documented CAD studies and supplier drawings. It is not a new solid-intersection test or a physical fit approval.

| Interface | Documented geometry / calculation | Decision |
| --- | --- | --- |
| Pan mount | 50 × 35 mm neck plate; imported actuator axis offset gives 10.25 mm overhang. Existing reference screw pattern is 22 × 40 mm. | Preserve the output-axis datum; compare the proposed frame and adapter before changing the model. |
| Pan height | Original gap 33 mm; raised study gap 41 mm; imported reference envelope 42.7 mm. Nominal shortfall is 1.7 mm even in the raised gap if the complete envelope lies between those planes. | Verify mounting-face datums and fastener stack. The separate 5.3 mm modeled rotating clearance does not establish coupling fit. |
| Tilt mount | Current Hitec v2.2 drawing lists 40.8 × 20.0 × 37.8 mm body, 53.4 mm overall tab length, 10.2 mm transverse mounting-hole spacing and 4.5 mm mounting holes. Older Hitec drawing differs in some dimensions. | Use the current drawing and actual purchased revision; do not manufacture from a generic servo footprint. The existing side-to-side screening box includes tabs but excludes horn and cable. |
| Tilt horn | 25T, nominal 6 mm spline; Hitec 55738 is a candidate only. | Compare drawing, actual horn attachment and bracket clearance. |
| Camera ribbon | 500 mm candidate minus 342 mm longest documented sampled centerline gives 158 mm gross nominal remainder. | This is not usable slack: internal run, exits, bend behavior and strain relief are not included in the sampled length. Verify actual ribbon fit. |
| Pan supply enclosure | DFR0946 candidate 70 × 39 × 32 mm; bounding footprint 2,730 mm² and envelope volume 87,360 mm³. | Reserve a separate accessible stationary location with connector and ventilation space; the current CAD does not verify placement. |

## Onshape verification sequence

- Make a separate revision before replacing imported geometry.
- Inspect the fixed neck plate, actuator reference, moving adapter and tilt support individually.
- Use the supplier drawings to verify the actual mount hole geometry and access for the chosen fasteners.
- Review the horn and plug envelopes at the intended motion limits. Record the tightest clearance and the corresponding pose.
- Check ribbon fit and regulator placement separately; retain pending status wherever the actual hardware or vendor geometry is unavailable.

The current repository STEP could not be retrieved as geometry during this review. No new assembly file has been generated and the live Onshape document was not edited. Refer to [the existing CAD study](README.md) and [wiring study](../docs/WIRING.md).

Sources: [Hitec v2.2 drawing](https://www.hiteccs.com/public/uploads/data_sheet/HCS_D645MW_Specsheetv2.2_102-1729815560.pdf), [older Hitec drawing](https://www.hiteccs.com/public/uploads/data_sheet/D645MW-DataSheet-1642815005.pdf), [ROBOTIS actuator drawings](https://emanual.robotis.com/docs/en/dxl/x/xm430-w210/#drawings), [DFRobot module](https://www.dfrobot.com/product-2539.html).
