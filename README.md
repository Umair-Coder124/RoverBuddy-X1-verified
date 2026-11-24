# RoverBuddy X1 🤖🚀

Hi! I'm Umair, a 15-year-old student from Riyadh, Saudi Arabia. This is my project for Hack Club's Fallen program: an autonomous, Mars-rover-inspired follow-me robot planned around a Raspberry Pi 5, a Raspberry Pi Pico 2, and mecanum wheels.

---

## Why I Built This (And My Old Failures)

Before building RoverBuddy X1, I tried making a basic ESP32-CAM surveillance car controlled over Wi-Fi. It was a fun first project, but I ran into massive walls:
- The video stream lagged like crazy.
- The cheap plastic servos kept stripping gears under load.
- It had zero obstacle detection, so it crashed into walls constantly.
- The wiring was a giant spaghetti mess.

I wanted to build something way more reliable, modular, and actually capable of smart computer vision tracking without buying an overpriced pre-made chassis.

---

## Planned features

- **Smart Person Tracking:** Uses a Raspberry Pi Camera Module 3 paired with the Pi 5 to lock onto and follow a target.
- **Omnidirectional Movement:** Four mecanum wheels driven by a Pico 2, letting the robot strafe sideways, spin in place, and drive in any direction smoothly.
- **Heavy-Duty Pan-and-Tilt Head:** Powered by a ROBOTIS Dynamixel XM430 for the pan axis and a Hitec D645MW for the tilt axis.
- **Chest Status Screen:** A 5-inch HDMI display mounted on the front to show real-time diagnostics and system status.
- **Emergency Braking:** An HC-SR04 ultrasonic sensor is planned to provide distance readings for stopping. Independent motor cutoff and real sensor integration still need testing.

---

## Hardware Breakdown

- **Brain (High-Level Logic & Vision):** Raspberry Pi 5 (4GB)
- **Muscle (Low-Level Motor Control & Sensors):** Raspberry Pi Pico 2
- **Vision:** Raspberry Pi Camera Module 3
- **Chassis & Movement:** Custom 3D printed PETG parts + 4x Mecanum wheels + TT DC gear motors
- **Steering:** ROBOTIS Dynamixel XM430-W210-T & Hitec D645MW servos
- **Power:** 3S LiPo battery pack with separate regulated power branches

---

## Project links

- Onshape: https://cad.onshape.com/documents/6810cacad94ccaed2254a4c9/w/506e2971336fa1f66d037230/e/09c7e032cc91bfb2e46e0e5d
- Wiring: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/wiring/pinout_connection.md
- BOM table: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/BOM.md
- BOM CSV: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/bom.csv
- Code and simulation: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/firmware/README.md
- 3D model: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/cad/README.md
- Build checklist: https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/docs/build-checklist.md

---

![Revised CAD draft](cad/Assembly%20review.png)

![Wiring overview](docs/wiring_overview.svg)

## Current Status


- **CAD & Simulation:** Design files and desktop simulations are available. The revised mounting design needs independent review and the repository CAD exports still need synchronization.
- **Physical Build:** Waiting on Hack Club Fallen funding approval to order parts, print the PETG chassis, and assemble everything for Maker Faire Shenzhen!
