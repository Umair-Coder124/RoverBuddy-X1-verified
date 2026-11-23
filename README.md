# RoverBuddy X1 🤖🚀

Hi! I'm Umair, a 15-year-old student from Riyadh, Saudi Arabia. This is my project for Hack Club's Fallen program: an autonomous, Mars-rover-inspired follow-me robot built with a Raspberry Pi 5, a Raspberry Pi Pico 2, and mecanum wheels.

---

## Why I Built This (And My Old Failures)

Before building RoverBuddy X1, I tried making a basic ESP32-CAM surveillance car controlled over Wi-Fi. It was a fun first project, but I ran into massive walls:
- The video stream lagged like crazy.
- The cheap plastic servos kept stripping gears under load.
- It had zero obstacle detection, so it crashed into walls constantly.
- The wiring was a giant spaghetti mess.

I wanted to build something way more reliable, modular, and actually capable of smart computer vision tracking without buying an overpriced pre-made chassis.

---

## What It Does (Features)

- **Smart Person Tracking:** Uses a Raspberry Pi Camera Module 3 paired with the Pi 5 to lock onto and follow a target.
- **Omnidirectional Movement:** Four mecanum wheels driven by a Pico 2, letting the robot strafe sideways, spin in place, and drive in any direction smoothly.
- **Heavy-Duty Pan-and-Tilt Head:** Powered by a ROBOTIS Dynamixel XM430 for the pan axis and a Hitec D645MW for the tilt axis.
- **Chest Status Screen:** A 3.5-inch display mounted on the front to show real-time diagnostics and system status.
- **Emergency Braking:** An HC-SR04 ultrasonic sensor that automatically cuts motor power if an obstacle gets too close.

---

## Hardware Breakdown

- **Brain (High-Level Logic & Vision):** Raspberry Pi 5 (8GB)
- **Muscle (Low-Level Motor Control & Sensors):** Raspberry Pi Pico 2
- **Vision:** Raspberry Pi Camera Module 3
- **Chassis & Movement:** Custom 3D printed PETG parts + 4x Mecanum wheels + DC gear motors with encoders
- **Steering:** ROBOTIS Dynamixel XM430-W210-T & Hitec D645MW servos
- **Power:** 3S LiPo battery pack regulated down via a 5V 5A BEC

---

## Project Structure & Quick Links

- [CAD Model (Onshape)](https://cad.onshape.com) *(Update with your exact Onshape link)*
- [`wiring/pinout_connection.md`](wiring/pinout_connection.md) – How everything is wired up
- [Bill of materials (table)](BOM.md) – Full parts list and pricing
- [`bom.csv`](bom.csv) – Downloadable CSV

---

## Current Status

- **CAD & Simulation:** Designed in Onshape and tested logic via desktop scripts.
- **Physical Build:** Waiting on Hack Club Fallen funding approval to order parts, print the PETG chassis, and assemble everything for Maker Faire Shenzhen!
