import time

from machine import Pin

pin2 = Pin(2, Pin.OUT)
while True:
    pin2.value(1)
    time.sleep(1)
    pin2.value(0)
    time.sleep(1)
