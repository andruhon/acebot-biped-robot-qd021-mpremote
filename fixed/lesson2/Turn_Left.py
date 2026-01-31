# This is a fixed version and that the original can be downloaded from https://acebott.com/product/acebott-qd021-bionic-biped-robot-kit-for-arduino-esp32-electronic-toy-programming/?srsltid=AfmBOoq9a9pHc1a1ynt7Tx79tU8Wh5OVMYjRRdCgY6kQDarNoWvZtNEB
from libs.ACB_Biped_Robot import *
# Define the GPIO pin numbers connected to different parts of the Biped robot
Left_thigh = 4     
Left_calf = 27   
Right_thigh = 25 # Andr: Corrected pin to 25 (was 26) as per paper documentation
Right_calf = 26  # Andr: Corrected pin to 26 (was 25) as per paper documentation

# Initialize the Biped robot with the specified pins
servo_init(Left_thigh, Left_calf, Right_thigh, Right_calf)

Servo_PROGRAM_Zero() # 90 90 90 90

#Define an array of Left movements of the robot
left = [
    # GPIO4,GPIO27,GPIO26,GPIO25,time
    [90, 60, 125, 90, 300],#The right thigh rotates laterally, and the left calf rotates laterally
    [60, 60, 125, 90, 300],#Turn the left thigh inwards
    [60, 90, 125, 90, 300],#Turn the left calf inwards
    [60, 120, 55, 120, 300],#The left calf rotates inwards, the right thigh rotates inwards, and the right calf rotates laterally
    [60, 90, 55, 90, 300],#The left calf rotates laterally and the right calf rotates inwards
    [80, 90, 90, 90, 150],#The left thigh rotates inwards and the right thigh laterally
]

while True:
    
    Servo_PROGRAM_Run(left, len(left))
