# Parts and build plan - November 21

## Parts still to check

These are possible parts. Check their fit before ordering.

| Item | Candidate/reference | Open decision |
| --- | --- | --- |
| Pan mounting hardware | [ROBOTIS FR12-H101K, 903-0239-000](https://en.robotis.com/shop_en/item.php?it_id=903-0239-000) | Manufacturer lists XM430 compatibility and included idler bearing; compare against the current raised adapter and confirm whether this particular hinge geometry is useful. |
| Tilt horn | [Hitec R-ML25, 55738](https://hitecrcd.com/25t-aluminum-servo-horn/) | Standard 25T aluminum horn candidate; compare actual hole pattern, offset and engagement against the tilt assembly. |
| Additional pan cable | [ROBOTIS cable selection guide](https://robotis.us/blogs/robotis-ir-pr-blog/tech-tips-picking-the-right-cables-for-your-dynamixel) | X3P is the relevant connector family for the TTL actuator. Determine length and whether included leads suffice first. |
| Tilt signal interface | [D645MW specification](https://www.hiteccs.com/public/uploads/data_sheet/HCS_D645MW_Specsheetv2.2_102-1729815560.pdf) | Obtain manufacturer confirmation of input thresholds before selecting any additional interface. |

Do not order the hinge assembly or horn until actual suitability is confirmed. The existing BOM remains unchanged.

## Build steps

1. Check the correct parts, prices and delivery dates.
2. Compare the parts with the 3D design and check the mounting holes and cable space. Get printing or fabrication quotes.
3. Assemble with power off. Check screws, wheel clearance and cable routing.
4. Electrical review: have a qualified adult review battery protection, wiring and isolation before any energized tests. Keep actuators disabled until qualified.
5. Test each part with supervision and record the results. Fix problems before moving on.
6. Record a demo only after real testing. Keep simulations separate from hardware results.

The live Onshape revision and actual component fit have not been verified in this review. See [CAD notes](../cad/README.md), [wiring notes](WIRING.md), and the [November 20 checklist](2026-11-20-design-review.md).
