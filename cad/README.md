# 3D model

![Current assembly preview](Current%20assembly.png)

![Rear view](Current%20assembl%20rear.png)

![Pivot screenshot](Current%20pivot.png)

![Neck bracket screenshot](Current%20neck.png)

- [Complete assembly STEP](RoverBuddy%20X1.step)
- [Individual STEP files](current-parts/)
- [Download all individual parts](Current%20parts.zip)
- [Current parts list](Current%20parts.csv)

On November 24, the STEP export had to be restored after an update went wrong. The latest export includes the new shell, bearings, brackets and bolts. It opens again, but the ribbon cable route is missing.

The design started with the base. The chest screen and moving head came later. The cable hole was too restrictive for the planned moving head, so the opening was widened.

## Measurements to check

| Part | Design measurements |
| --- | --- |
| Pi tray | 58 × 49 mm board mounting pattern |
| Battery space | 108 × 35 × 27 mm space used in the model |
| Chest display | 121 × 89.48 mm space used in the model |
| Camera cable | 342 mm longest sampled route; 500 mm cable candidate |
| Pan mount | 43 mm deck-to-yoke gap in November 24 STEP; 42.7 mm modeled actuator height |
| Pan power board | 70 × 39 × 32 mm board to fit |

Check these dimensions against the actual parts before printing.

## November 27 fit check

A desktop CAD check reopened 24 individual STEP files for the chassis, battery, display, head, neck, pan mount, bearings and selected tilt parts. Each imported solid was valid. One tilt subpart (Tilt Servo 2) could not be retrieved, so this is a partial check.

- The top of the pan deck is at 157 mm and the bottom of the tilt yoke is at 200 mm. The old 41 mm gap came from an earlier design. The current 43 mm gap leaves 0.3 mm between the modeled pan servo and yoke at the exported pose. Check the real horn, coupling, bolts and tolerances before cutting the brackets.
- The two modeled head pivot bearings are 10 mm across and 3 mm thick, matching the chosen bearing size on the BOM. Check their bore, shaft retention and fit with actual parts.
- The 500 mm ribbon cable leaves 158 mm beyond the earlier 342 mm sampled path. The latest solid file does not contain the cable, so the full-motion route and bend clearance remain open.
- The battery model and tray show no solid overlap in the exported pose. The actual battery, connector and strap still have to fit.

Manufacturer drawings to compare: [ROBOTIS XM430](https://en.robotis.com/service/selection_guide.php), [Hitec D645MW](https://www.hiteccs.com/public/uploads/data_sheet/HCS_D645MW_Specsheetv2.2_102-1729815560.pdf), [500 mm camera cable](https://www.adafruit.com/product/5820).

## What changed and what needs checking

- The tilt mount has space modeled for two 6 × 10 × 3 mm bearings.
- The neck has two brackets and fasteners modeled.
- The cable opening was widened to 21.5 × 21.5 mm in the revised head shell. The cable route clears the shell with the head facing forward. The real cable still needs a movement test.
- Check real bearing fit, fastener engagement, head travel and mounting strength before building.

Custom metal parts need a supplier quote. Quote request: https://www.thanfa.com/en/rfq/

See the [build checklist](../docs/build-checklist.md) for the remaining fit checks.

[Revised head shell](current-parts/Head%20Shell.step)
