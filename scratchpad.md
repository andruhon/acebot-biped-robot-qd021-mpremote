
```
[parents@kondr-oc acebot-biped]$ mpremote connect list
/dev/ttyS0 None 0000:0000 None None
/dev/ttyS1 None 0000:0000 None None
/dev/ttyS2 None 0000:0000 None None
/dev/ttyS30 None 0000:0000 None None
/dev/ttyS31 None 0000:0000 None None
/dev/ttyUSB0 None 1a86:7523 None USB Serial
[parents@kondr-oc acebot-biped]$ mpremote connect id:/dev/ttyUSB0 fs ls
mpremote: no device with serial number /dev/ttyUSB0
[parents@kondr-oc acebot-biped]$ mpremote connect id:1a86:7523 fs ls
mpremote: no device with serial number 1a86:7523
[parents@kondr-oc acebot-biped]$ mpremote connect /dev/ttyUSB0 fs ls
ls :
         362 acecode.py
         139 boot.py
          31 main.py
           0 oled/
```