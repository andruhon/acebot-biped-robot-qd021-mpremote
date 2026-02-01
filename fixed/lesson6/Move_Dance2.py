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



Dance2 = [
    [75, 105, 68, 110, 600],#First
    [75, 90, 60, 90, 600],
    [75, 68, 110, 68, 600],
    [100, 90, 110, 90, 600],
    [60, 120, 60, 120, 200],
    [60, 90, 60, 90, 200],
    [110, 60, 110, 60, 200],
    [110, 90, 110, 90, 200],
    [60, 110, 60, 110, 200],
    [60, 90, 60, 90, 200],
    [110, 60, 110, 60, 200],
    [110, 90, 110, 90, 200],

    [50,90,80,90, 300],#Second
    [50,130,80,100, 300], 
    [80,130,80,100, 300],
    [60,130,80,100, 300], 
    [80,130,80,100, 300],
    [60,130,80,100, 300], 
    [80,130,80,100, 300],
    [60,130,80,100, 300], 
    [80,130,80,100, 300],
    [60,110,80,105, 300],
    [90,90,90,90, 300], 

    [100,90,125,90, 300],#Third
    [100,75,125,50, 300], 
    [100,75,100,50, 300],
    [100,75,120,50, 300], 
    [100,75,100,50, 300],
    [100,75,120,50, 300], 
    [100,75,100,50, 300],
    [100,75,120,50, 300], 
    [100,75,100,50, 300],
    [100,90,120,70, 300],


    [90, 100, 92, 95, 300],#Fourth
    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],
    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],
    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],
    [90, 90, 90, 90, 300],


    [90, 80, 90, 100, 300],#Fifth
    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],
    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],
    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],
    [90, 90, 90, 90, 300],
]


while True:   
    Servo_PROGRAM_Run(Dance2, len(Dance2))
    
    
