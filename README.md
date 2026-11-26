# RoverBuddy X1

Hi, I’m Umair. I’m 15 and I live in Riyadh, Saudi Arabia. This is my Hack Club Fallen project.

RoverBuddy X1 is a follow-me robot I’m designing. It’s kind of inspired by Mars rovers. The plan is to use a Raspberry Pi 5, a Raspberry Pi Pico 2, and mecanum wheels so it can move in any direction.

## How it started

My old ESP32-CAM car had a laggy camera, broken plastic servos and messy wiring. It also hit walls. I wanted to try a different design.

I started with a four-wheel base, then added a screen on the chest and a camera head that can turn and tilt. Learning Onshape was difficult at first, especially getting the thickness of parts right.

## What I want to make

- A rover that can follow a person.
- Four mecanum wheels so it can move sideways without turning first.
- A camera head that moves up, down, left and right.
- A screen that shows what the rover is doing.
- A distance sensor to help it stop near obstacles.

## Main parts

1. Raspberry Pi 5 – camera and main software
2. Raspberry Pi Pico 2 – motor control
3. Camera Module 3
4. 4 mecanum wheels + motors
5. Dynamixel XM430 for pan and Hitec D645MW for tilt
6. 3S LiPo battery with separate power for different parts
7. 3D printed PETG chassis (planned)

## Project links

1. CAD Design - https://cad.onshape.com/documents/6810cacad94ccaed2254a4c9/w/506e2971336fa1f66d037230/e/09c7e032cc91bfb2e46e0e5d
2. Wiring / pinout - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/wiring/pinout_connection.md
3. BOM.csv - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/bom.csv
   BOM table - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/BOM.md
4. Code - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/firmware/README.md
5. 3D model notes - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/cad/README.md
6. Build checklist - https://github.com/Umair-Coder124/RoverBuddy-X1-verified/blob/main/docs/build-checklist.md

![Current assembly preview](cad/Current%20assembly.png)

![Rear view](cad/Current%20assembl%20rear.png)

![Wiring overview](docs/wiring_overview.svg)

## Where I am now

The CAD has been exported and the basic drive demo runs on a computer. The head mounts and camera cable still need fit checks. I am waiting for Fallen funding to order parts and start the real build. My goal is to bring RoverBuddy to Shenzhen.

Next, I plan to draw the wiring diagram on paper so I can go through the connections one by one.
