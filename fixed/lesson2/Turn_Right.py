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

#Define an array of Right movements of the robot
right = [

    [50, 90, 90, 120, 300], #The left thigh rotates laterally, and the right calf rotates laterally
    [50, 90, 130, 120, 300],#Turn the right calf inwards
    [50, 90, 130, 90, 300],#Turn the right calf inwards
    [120, 50, 130, 60, 300],#The right calf rotates inwards, the left thigh rotates inwards, and the left calf rotates laterally
    [120, 90, 130, 90, 300],#The right calf rotates laterally and the left calf rotates inwards
    [90, 90, 80, 90, 150],#The right thigh rotates inwards and the left thigh laterally
]


while True:
    Servo_PROGRAM_Run(right, len(right))
