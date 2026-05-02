# Custom program for Acebott QD021 Biped Robot

This is an adaptation of [Lesson 7 Web Control](../fixed/lesson7/Biped_Robot_Web.py),
which removes all the HTML and changes the API to be more like a REST API, which is easier for AI to digest.

To make it work with AI from a cloud provider (e.g. Claude), you'd need to either have a second network interface allowing you to connect to the robot (a WiFi dongle would do), or you could follow the instructions in [wifi_config.example.py](wifi_config.example.py) and upload your WiFi credentials to the robot.

## Files included

- [Biped_Robot_Web.py](Biped_Robot_Web.py) - the main program
- [wifi_config.example.py](wifi_config.example.py) - example WiFi config for the case where you don't have a second network interface.

## Installation

- Upload the standard Acebott firmware to the robot following their installation guide and upload Lesson 7. You may still need the fixed version of the libs; in this case follow the instructions in [../INSTALLATION.md](../INSTALLATION.md)
- Download [Biped_Robot_Web.py](Biped_Robot_Web.py)
- Use mpremote (Thonny IDE would also do) to upload Biped_Robot_Web.py as main.py to the robot: `mpremote connect /dev/ttyUSB0 fs cp for-agents/Biped_Robot_Web.py :main.py`

## Controlling the robot

- Connect to the robot's WiFi, or configure the robot to connect to your WiFi
- Send the following commands to your robot to control it:
```bash
curl 'http://192.168.4.1/forward'             # one step forward
curl 'http://192.168.4.1/forward?steps=4'     # four steps forward
curl 'http://192.168.4.1/backward?steps=2'
curl 'http://192.168.4.1/turn_left?steps=6'   # ~90° left
curl 'http://192.168.4.1/turn_right?steps=3'  # ~45° right
curl 'http://192.168.4.1/stop'                # freeze
```

(When using the setup where the robot connects to your WiFi, you will need to figure out the IP issued to the robot; this is likely to be different from 192.168.4.1.)
