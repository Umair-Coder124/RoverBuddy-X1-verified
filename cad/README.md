# 3D model

![Revised assembly draft](Assembly%20review.png)

![Pivot](Pivot%20review.png)

![Neck brackets](Neck%20review.png)

[Earlier GitHub STEP model](RoverBuddy_X1_Full_Pan_Tilt_Fit_Study.step) · [Head preview](Head_Camera.png) · [Rear preview](Integrated_Rear_Preview.png)

The GitHub exports and previews are from the earlier assembly. A revised mounting draft was prepared on November 24 and reported imported to Onshape. All 182 parts reopened successfully in the revised STEP. The pictures above show the draft, not the older GitHub STEP. The current draft still needs independent review, fit checks and upload of the matching exports.

## Main parts

- Base with four wheels, motor brackets and battery tray.
- Raspberry Pi tray, electronics space and chest display.
- Moving head with a camera and pan-and-tilt servo mounts.

## Measurements to check

| Part | Design measurements |
| --- | --- |
| Pi tray | 58 × 49 mm board mounting pattern |
| Battery space | 108 × 35 × 27 mm reference envelope |
| Chest display | 121 × 89.48 mm reference envelope |
| Camera cable | 342 mm longest sampled route; 500 mm cable candidate |
| Pan mount | 41 mm raised gap; 42.7 mm actuator reference envelope |
| Pan power board | 70 × 39 × 32 mm candidate enclosure |

These are model measurements. Check actual parts and clearances before printing or assembly.

[Parts manifest](Parts_Manifest.csv) · [Interference check](Interference_Check.csv) · [Earlier detailed STEP](RoverBuddy_X1_Detailed_Assembly.step)

See the [build checklist](../docs/build-checklist.md) for remaining checks and the [full CAD reference](https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/d836ea650516e329bdd500ddd6cfbd0f682dbf04/cad/README.md) for measurements, supplier drawings and earlier model details.

## Fit check

- Two 6 × 10 × 3 mm bearing envelopes are in the tilt mount.
- The neck has two brackets and fasteners modeled.
- The cable opening was widened to 21.5 × 21.5 mm in the revised head shell. The modeled cable path clears the shell at its neutral position. The real cable still needs a movement test.
- Check real bearing fit, fastener engagement, head travel and mounting strength before building.

Custom metal parts need a supplier quote. Quote request: https://www.thanfa.com/en/rfq/

## Checking the real parts

Once the parts arrive, compare the bearings, servos, brackets and bolts with the 3D model. Check that the screws fit and the head can move without squeezing the camera cable. If anything does not fit, adjust the design before assembly.

Cable opening draft: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/cad/Head%20Shell%20review.step
