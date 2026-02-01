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


Dance1 = [
    # GPIO4,GPIO27,GPIO26,GPIO25,time
    [50,90,80,90, 300],  #Left thigh to the lateral rotation
    [50,130,80,100, 300],#Left calf to the inward rotation
    [80,130,80,100, 300],#Left thigh to the inward rotation
    [60,130,80,100, 300],#Left thigh to the lateral rotation
    [80,130,80,100, 300],#Left thigh to the inward rotation

    [60,130,80,100, 300],#Left thigh to the lateral rotation
    [80,130,80,100, 300],#Left thigh to the inward rotation
    [60,130,80,100, 300],#Left thigh to the lateral rotation
    [80,130,80,100, 300],#Left thigh to the inward rotation
    [60,110,80,105, 300],#Left thigh to the lateral rotation，Left calf to the inward rotation

    [90,90,90,90, 300],  #Action initialization of biped robot
    [100,90,125,90, 300],#Right thigh to the lateral rotation
    [100,75,125,50, 300],#Right calf to the inward rotation
    [100,75,100,50, 300],#Right thigh to the inward rotation
    [100,75,120,50, 300],#Right thigh to the lateral rotation
    [100,75,100,50, 300],#Right thigh to the inward rotation

    [100,75,120,50, 300],#Right thigh to the lateral rotation
    [100,75,100,50, 300],#Right thigh to the inward rotation
    [100,75,120,50, 300],#Right thigh to the lateral rotation
    [100,75,100,50, 300],#Right thigh to the inward rotation

    [100,90,120,70, 300],#Right thigh to the lateral rotation，Right calf to the lateral rotation
    [90,90,90,90, 300],  #Action initialization of biped robot
]


while True:  
    Servo_PROGRAM_Run(Dance1, len(Dance1))
