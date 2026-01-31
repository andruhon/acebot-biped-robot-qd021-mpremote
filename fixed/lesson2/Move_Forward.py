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


#Define an array of forward movements of the robot
forward = [
    # GPIO4,GPIO27,GPIO26,GPIO25,time
    [70, 110, 70, 120, 300],#Left leg up, left leg forward
    [60, 90, 60, 90, 300],#Left leg landing
    [110, 50, 110, 60, 300],#Right leg up, right leg forward
    [105, 90, 105, 90, 300],#Right leg landing
]


while True:
    Servo_PROGRAM_Run(forward, len(forward))

    
