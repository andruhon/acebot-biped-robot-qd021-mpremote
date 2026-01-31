# Acebott Biped Controller

Acebott QD021 Bionic Biped Robot Kit for Arduino ESP32 Electronic Toy Programming
https://acebott.com/product/acebott-qd021-bionic-biped-robot-kit-for-arduino-esp32-electronic-toy-programming/

This project contains the code for controlling a biped robot using MicroPython.

Original code provided with robot has some pin allocation and motion matrix issues,
causing robot not to move properly and to limp badly.
Fixed files are provided in the [fixed](fixed) directory.

## Using mpremote

`mpremote` is a command-line tool that provides utilities to interact with MicroPython devices over a serial connection. It allows you to manage the filesystem, run scripts, and access the REPL.

See [INSTALLATION.md](INSTALLATION.md) for installation instructions.

### Connecting to a Device

To list available devices, use:

```bash
mpremote connect list
```

This will show output similar to:

```
/dev/ttyS0 None 0000:0000 None None
...
/dev/ttyUSB0 None 1a86:7523 None USB Serial
```

If the robot is connected to the computer, one of ttyUSB is most likely the robot.

To connect to a specific device, you can use the device path directly:

```bash
mpremote connect /dev/ttyUSB0
```

### Listing Files

Once connected to a device, you can list files on the MicroPython filesystem:

```bash
mpremote connect /dev/ttyUSB0 fs ls
```

This will show output similar to:

```
ls :
         362 acecode.py
         139 boot.py
```

You can also combine commands in a single line:

```bash
mpremote connect /dev/ttyUSB0 fs ls
```

### Other Useful Commands

- **Enter REPL**: `mpremote` (without arguments) or `mpremote connect /dev/ttyUSB0`
- **Run a script**: `mpremote connect /dev/ttyUSB0 run <local_script.py>`
- **Copy file to device**: `mpremote connect /dev/ttyUSB0 fs cp <local_file> :`
- **Copy file from device**: `mpremote connect /dev/ttyUSB0 fs cp :<device_file> .`

For more information about mpremote commands, refer to the [MicroPython documentation](https://docs.micropython.org/en/latest/reference/mpremote.html).

## Deploying Fixed Code

A `fixed` directory has been created containing corrected versions of the robot control code and lessons. These files fix pin wiring discrepancies and movement logic issues.

### 1. Update the Library

First, you must update the robot library on the device.

```bash
# Copy the fixed library to the device's lib folder
mpremote connect /dev/ttyUSB0 fs cp fixed/ACB_Biped_Robot.py :libs/ACB_Biped_Robot.py
```

_Note: Ensure the destination path `:libs/` exists. If not, create it first using `fs mkdir :libs`._

### 2. Run/Deploy Lessons

You can run the fixed lesson files directly from your computer:

```bash
# Run Forward Movement
mpremote connect /dev/ttyUSB0 run fixed/lesson2/Move_Forward.py

# Run Backward Movement (Fixed gait)
mpremote connect /dev/ttyUSB0 run fixed/lesson2/Move_Backward.py
```

Or copy them to the device for autonomous execution:

```bash
mpremote connect /dev/ttyUSB0 fs cp fixed/lesson2/Move_Forward.py :main.py
```
