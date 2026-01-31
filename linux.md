# Connecting with mpremote on linux

I had some difficulties connecting to pico from linux. 

In order to get it working on my Arch I ended up doing the following,
I have initially done this for the Raspberry Pico, but somehow it made the ESP32 work as well:

* Considering mpremote is installed with `python -m pip install -r requirements.txt`
* Installed `pico-sdk`
* Installed `arm-none-eabi-gcc`
* Installed `arm-none-eabi-newlib`
* Added my user to uucp `sudo usermod -a -G uucp $USER`
* Installed Thonny IDE (I doubt it is actually necessary)
* Created `99-picotool.rules` in  `/etc/udev/rules.d`
* Rebooted computer

udev rules:
```
SUBSYSTEM=="usb", \
    ATTRS{idVendor}=="2e8a", \
    ATTRS{idProduct}=="0003", \
    MODE="660", \
    GROUP="plugdev"
SUBSYSTEM=="usb", \
    ATTRS{idVendor}=="2e8a", \
    ATTRS{idProduct}=="000a", \
    MODE="660", \
    GROUP="plugdev"
```

(The rules above are for Pico, Biped robot has vendor and product ids 1a86:7523)

Not sure to which extent all these steps are necessary,
I suspect udev rules and adding user to uucp may be enough.

Without doing all these I was getting `mpremote: no device found` when doing mpremote ls and 
for `mpremote connect /dev/ttyACM0` I was getting
`mpremote: failed to access /dev/ttyACM0 (it may be in use by another program)`
