# RoverBuddy X1 🤖🚀

Hi! I'm Umair, a 9th-grade student from Riyadh, Saudi Arabia. This is my project for Hack Club's Fallen program: an autonomous, Mars-rover-inspired follow-me robot I plan to build using a Raspberry Pi 5, a Raspberry Pi Pico 2, and mecanum wheels.

## Why I Built This (My Backstory)
Before starting RoverBuddy X1, I built an ESP32-CAM surveillance car controlled via phone. While it was a fun first project, I ran into major limitations:
- Poor camera quality and bad video lag.
- Plastic pan-and-tilt servos that kept wearing out.
- No obstacle detection or automatic braking.
- Power and wiring headaches.

I wanted to build something much better, more reliable, and capable of smart person-tracking.

## Planned Features
- **Camera Tracking:** Will use a Raspberry Pi Camera Module 3 to track a target.
- **Omnidirectional Movement:** Four mecanum wheels driven by a Pico 2 so the robot can move sideways, spin, and drive in any direction.
- **Pan-and-Tilt Head:** Powered by a ROBOTIS Dynamixel XM430 servo and a Hitec D645MW servo.
- **Chest Display:** Will show real-time status and information.
- **Safety:** Ultrasonic distance sensor for obstacle detection and automatic stopping.

## Hardware Components
- **Brain (High-level):** Raspberry Pi 5
- **Muscle (Low-level motor control):** Raspberry Pi Pico 2
- **Vision:** Raspberry Pi Camera Module 3
- **Movement:** 4x Mecanum wheels + DC motors with drivers
- **Steering:** Dynamixel XM430-W210-T (Pan) & Hitec D645MW (Tilt)
- **Safety:** Ultrasonic Sensor
- **Power:** Lithium battery pack + regulators

See the [parts list (BOM)](bom.csv) for estimated prices and supplier links.

## CAD Design
The design is inspired by planetary exploration rovers. Here are the CAD previews and the earlier Onshape import:

![RoverBuddy X1 assembly](cad/Assembly_Preview.png)

![Camera head](cad/Head_Camera.png)

👉 [Onshape Document](https://cad.onshape.com/documents/6810cacad94ccaed2254a4c9/w/506e2971336fa1f66d037230/e/09c7e032cc91bfb2e46e0e5d)

[Latest STEP model](cad/RoverBuddy_X1_Full_Pan_Tilt_Fit_Study.step) · [CAD notes](cad/README.md)

## Wiring

![Wiring overview](docs/wiring_overview.svg)

[Pinout guide](wiring/pinout_connection.md) · [Detailed wiring notes](docs/WIRING.md)

## Status
- **CAD & Simulation:** Design study and desktop simulation prepared. 77 software tests passed. Mounting and physical tests are still pending.
- **Physical Assembly:** Waiting for BOM approval and component delivery.
- **Software:** [Desktop test instructions](firmware/README.md). The real camera tracking and hardware controls still need integration and testing.
