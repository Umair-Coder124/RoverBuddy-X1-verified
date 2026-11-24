# RoverBuddy X1

Hi, I’m Umair. I’m 15 and I live in Riyadh, Saudi Arabia. This is my Hack Club Fallen project.

RoverBuddy X1 is a follow-me robot I’m designing. It’s kind of inspired by Mars rovers. The plan is to use a Raspberry Pi 5, a Raspberry Pi Pico 2, and mecanum wheels so it can move in any direction.

## Why I’m building this

Before this, I built a small ESP32-CAM car that I controlled from my phone. It was fun, but a lot of things went wrong:

1. The camera lagged a lot
2. The cheap plastic servos kept breaking
3. It had no obstacle detection, so it hit walls
4. The wiring was a mess

I wanted to make something stronger and smarter, with better camera tracking, instead of just buying a ready-made robot kit.

## What I want it to do

1. Follow a person using the Raspberry Pi Camera Module 3
2. Move forward, sideways, and turn using 4 mecanum wheels
3. Have a moving camera head (pan + tilt)
4. Show status on a small screen on the front
5. Stop when something is too close (ultrasonic sensor)

Right now this is still mostly design and computer testing. I haven’t built the full robot yet.

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

## Current status

- **CAD & simulation:** Design files and desktop tests are ready. I updated the mounting parts in Onshape and exported STEP files. Still needs review and real fit checks when parts arrive.
- **Physical build:** Waiting on Hack Club Fallen funding so I can order parts, print the chassis, and start assembling. I want to take it to Maker Faire Shenzhen if I can finish in time.
