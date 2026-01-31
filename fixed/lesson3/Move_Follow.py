# This is a fixed version and that the original can be downloaded from https://acebott.com/product/acebott-qd021-bionic-biped-robot-kit-for-arduino-esp32-electronic-toy-programming/?srsltid=AfmBOoq9a9pHc1a1ynt7Tx79tU8Wh5OVMYjRRdCgY6kQDarNoWvZtNEB
from machine import Pin, PWM

#import libs.ultrasonic

from libs.ACB_Biped_Robot import *

# Define the GPIO pin numbers connected to different parts of the Biped robot
Left_thigh = 4     
Left_calf = 27   
Right_thigh = 25 # Andr: Corrected pin to 25 (was 26) as per paper documentation
Right_calf = 26  # Andr: Corrected pin to 26 (was 25) as per paper documentation

Trig_PIN = 13
Echo_PIN = 14

# Initialize the Biped robot with the specified pins
servo_init(Left_thigh, Left_calf, Right_thigh, Right_calf)

Servo_PROGRAM_Zero() # 90 90 90 90

Ultrasonic = None

def Ultrasonic_Init(pin1,pin2):
    global Ultrasonic
    Ultrasonic = libs.ultrasonic.ACB_Ultrasonic(pin1,pin2)

Ultrasonic_Init(Trig_PIN,Echo_PIN)

#Ultrasonic = libs.ultrasonic.ACB_Ultrasonic(Trig_PIN,Echo_PIN)

#Forward
forward = [
    # GPIO4,GPIO27,GPIO26,GPIO25,time
    [70, 110, 70, 120, 300],
    [60, 90, 60, 90, 300],
    [110, 50, 110, 60, 300],
    [105, 90, 105, 90, 300],
]

#Backward
# Andr: Updated backward matrix to be the inverse of Forward movement (inverting Thigh angles)
backward = [
    # GPIO4,GPIO27,GPIO26,GPIO25,time
    [110, 110, 110, 120, 300],#Andr: Adjusted values (LT 70->110, RT 70->110 for backward step) 
    [120, 90, 120, 90, 300],#Andr: Adjusted values
    [70, 50, 70, 60, 300],#Andr: Adjusted values (LT 110->70, RT 110->70)
    [75, 90, 75, 90, 300],#Andr: Adjusted values
]


while True:
    UT_distance = Ultrasonic.get_distance()
    print(UT_distance)
    
    if UT_distance <= 15:
        Servo_PROGRAM_Run(backward, len(backward))
    elif 15 <= UT_distance and UT_distance <= 20:
        Servo_PROGRAM_Zero()
    elif 20 < UT_distance and UT_distance <= 35:
        Servo_PROGRAM_Run(forward, len(forward))
    else:
        Servo_PROGRAM_Zero()
