# Installation

## mpremote

`mpremote` is a command-line tool that provides utilities to interact with MicroPython devices over a serial connection. It allows you to manage the filesystem, run scripts, and access the REPL.

### Installation

To install mpremote, use pip:

```bash
pip install --user mpremote
```

Or via pipx:

```bash
pipx install mpremote
```

## Esptool

### Install esptool to flash the robot

Pip:
```bash
pip install esptool
```


Arch:
```bash
yay -S esptool
```

### Flash the robot with ESP firmware

Note, esptool may be available either as `esptool` or `esptool.py`

Please refer to https://micropython.org/download/ESP32_GENERIC/ for more details.

First erase the flash entirely:

```bash
esptool erase_flash
```

Download latest Micropython firmware from https://micropython.org/download/ESP32_GENERIC/
and copy the bin file to `./readonly/` directory of this project.


Flash the ESP32 with the following command
```bash
esptool --baud 460800 write_flash 0x1000 readonly/ESP32_GENERIC-???.bin
```
, where `ESP32_GENERIC-???.bin` should be actual downloaded bin file name, for example `ESP32_GENERIC-20251209-v1.27.0.bin`


Run test `01-led.py` to confirm that it all works, see [tests](tests/README.md)


## Prepare lessons and libs

- Download product tutorial from https://acebott.com/product/acebott-qd021-bionic-biped-robot-kit-for-arduino-esp32-electronic-toy-programming/
- unpack the archive 
- copy `English/Tutorial V2/Python(Experienced  Learner)/Python(Experienced  Learner)/6.Program/*` from the archive contents to `./readonly/python` of this project.
- copy `English/Tutorial V2/Python(Experienced  Learner)/2.Install library files/libs` from the archive contents to `./readonly/libs/` of this project.

## Upload libs to the robot

After flashing the MicroPython firmware, you need to upload the library files to the robot's filesystem.

The library files are located in `./readonly/libs/`:
- `ACB_Biped_Robot.py` - Main robot control library
- `ultrasonic.py` - Ultrasonic sensor library

## Install Gaunt Sloth (optional)

[Gaunt Sloth](https://gaunt-sloth-assistant.github.io/) can help with deploying lessons to the robot.

*Prerequesites:*
- Gaunt Sloth needs [Node JS](https://nodejs.org/) to be installed.
- Gaunt Sloth needs OpenRouter API key as `OPEN_ROUTER_API_KEY` environment variable.

*Gaunt Sloth Installation*
`npm install gaunt-sloth-assistant -g`

### Connect to the robot

First, find the serial port of your robot:

```bash
mpremote connect list
```

Connect to the robot (replace `/dev/ttyUSB0` with your actual port):

```bash
mpremote connect /dev/ttyUSB0
```

### Upload the library files

First, create a `libs` directory on the robot:

```bash
mpremote mkdir libs
```

Upload library files to the `libs` folder:

```bash
mpremote cp ./readonly/libs/ACB_Biped_Robot.py :libs/
mpremote cp ./readonly/libs/ultrasonic.py :libs/
```

Or upload all library files at once:

```bash
mpremote cp ./readonly/libs/*.py :libs/
```

If `mpremote` is not using the correct port by default, specify it explicitly:

```bash
mpremote connect /dev/ttyUSB0 mkdir libs
mpremote connect /dev/ttyUSB0 cp ./readonly/libs/*.py :libs/
```

### Verify the upload

List files in the `libs` directory on the robot to confirm the libraries are in place:

```bash
mpremote ls libs/
```

You should see `ACB_Biped_Robot.py` and `ultrasonic.py` in the output.

### Upload lesson files (optional)

If you want to run specific lessons directly on the robot, upload them to the lessons directory:

```bash
# Create lessons directory on the robot
mpremote mkdir lessons

# Upload a specific lesson (e.g., lesson 1)
mpremote cp ./readonly/python/lesson1/servo_90.py :lessons/

# Or upload all lessons
for d in ./readonly/python/lesson*/; do mpremote cp "${d}"*.py :lessons/; done
```
