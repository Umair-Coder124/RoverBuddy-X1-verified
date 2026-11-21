# November 21 component and build-readiness review

## Outstanding components

These public manufacturer references are for comparison, not authorization to purchase or proof of CAD fit.

| Item | Candidate/reference | Open decision |
| --- | --- | --- |
| Pan mounting hardware | [ROBOTIS FR12-H101K, 903-0239-000](https://en.robotis.com/shop_en/item.php?it_id=903-0239-000) | Manufacturer lists XM430 compatibility and included idler bearing; compare against the current raised adapter and confirm whether this particular hinge geometry is useful. |
| Tilt horn | [Hitec R-ML25, 55738](https://hitecrcd.com/25t-aluminum-servo-horn/) | Standard 25T aluminum horn candidate; compare actual hole pattern, offset and engagement against the tilt assembly. |
| Additional pan cable | [ROBOTIS cable selection guide](https://robotis.us/blogs/robotis-ir-pr-blog/tech-tips-picking-the-right-cables-for-your-dynamixel) | X3P is the relevant connector family for the TTL actuator. Determine length and whether included leads suffice first. |
| Tilt signal interface | [D645MW specification](https://www.hiteccs.com/public/uploads/data_sheet/HCS_D645MW_Specsheetv2.2_102-1729815560.pdf) | Obtain manufacturer confirmation of input thresholds before selecting any additional interface. |

Do not order the hinge assembly or horn until actual suitability is confirmed. The existing BOM remains unchanged.

## Build sequence and acceptance gates

1. Procurement: confirm the approved revision, delivery dates and actual supplier quotes.
2. Mechanical review: compare delivered part drawings with CAD, check mount and connector clearances, and obtain fabrication quotes.
3. Unpowered assembly: inspect fasteners, retention, wheel clearance, ribbon routing and access for maintenance.
4. Electrical review: have a qualified adult review battery protection, wiring and isolation before any energized tests. Keep actuators disabled until qualified.
5. Supervised integration: record results from each subsystem using the existing acceptance checklist; only proceed after unresolved issues are addressed.
6. Demo readiness: document actual results and limitations; do not label simulations as physical tests.

The live Onshape revision and actual component fit have not been verified in this review. See [CAD notes](../cad/README.md), [wiring notes](WIRING.md), and the [November 20 checklist](2026-11-20-design-review.md).
