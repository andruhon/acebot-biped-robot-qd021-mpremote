# Assistance Guidelines

You are helping to program STEM bipedal robot Acebot Biped QD021.

Robot is based on ESP32 and has four MG90S servos.

## Original sources

`readonly/python/` contains python files for 8 lessons.

## Lessons Overview

- Lesson 1: Basic Servo Initialization
- Lesson 2: Move Forward and Backward, Turn Left and Right, Serial Control
- Lesson 3: Ultrasonic Sensor Following Movement
- Lesson 4: Obstacle Avoidance Movement
- Lesson 5: Dance Routine 1
- Lesson 6: Dance Routine 2
- Lesson 7: Web-based Control Interface
- Lesson 8: Mobile App Control Interface

## Deploying lesson

If you were asked to deploy or upload a lesson, figure out the correct file from `fixed` directory and use `deploy_lesson` command to deploy it.

### Example 1

User: deploy lesson 5
You:
list `fixed`
list `fixed/lesson5`
deploy_lesson /dev/ttyUSB0 fixed/lesson5/Move_Dance1.py

The expected output
cp fixed/lesson5/Move_Dance1.py :main.py

### Example 2

User: upload avoid program
You:
list `fixed`
list `fixed/lesson4`
deploy_lesson /dev/ttyUSB0 fixed/lesson4/Move_Avoid.py

The expected output
cp fixed/lesson4/Move_Avoid.py :main.py

### Troubleshooting
If something goes wrong with deployment list devices if it seems like device ttyUSB0 didn't work; Check README.md, INSTALLATION.md, try guiding user to find the solution.

### Stopping the robot

If user wants to "stop the robot" RUN lesson 1, it will set all servos to neutral positions (use run_lesson).
