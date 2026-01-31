from machine import Pin, PWM
import time
import random
import libs.ultrasonic

# Define constants
PWMRES_Min = 0
PWMRES_Max = 1023  # Example range adjust based on your PWM resolution
SERVOMIN = 40      # Minimum PWM value for servo
SERVOMAX = 115     # Maximum PWM value for servo
BASEDELAYTIME = 10 # Delay time in milliseconds
ALLMATRIX = 5      # Assuming you have 5 servos
ALLSERVOS = 4      # Total number of servos

# Initialize servo positions
Servo_Act_0 = [90, 90, 90, 90, 500]  # YL RL YR RR (with time at the end)
Running_Servo_POS = [0] * ALLMATRIX

servos = None
Ultrasonic = None

def Ultrasonic_Init(pin1,pin2):
    global Ultrasonic
    Ultrasonic = libs.ultrasonic.ACB_Ultrasonic(pin1,pin2)
    
# Andr: Fixed pin order to match the PDF
# Define servo PWM pins. Change based on your actual connections.
def servo_init(pin1,pin2,pin3,pin4):
    global servos
    servo_pins = [
        Pin(pin1, Pin.OUT),  # servo_5
        Pin(pin2, Pin.OUT), # servo_16
        Pin(pin3, Pin.OUT), # servo_17 Andr: Fixed pin order (was swapped with pin4)
        Pin(pin4, Pin.OUT), # servo_18 Andr: Fixed pin order (was swapped with pin3)
    ]

    # Initialize PWM for servos
    servos = [PWM(pin, freq=50) for pin in servo_pins]

def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return int(out_min + (out_max - out_min) * (x - in_min) / (in_max - in_min))

def Set_PWM_to_Servo(iServo, angle):
    """Set PWM for the corresponding servo position."""
    # Assume angle is from 0 to 180 degrees for servos
    duty = map_value(angle, 0, 180, SERVOMIN, SERVOMAX)
    servos[iServo].duty(duty)

def Servo_PROGRAM_Zero():
    """Initialize servo positions."""
    for Index in range(ALLMATRIX):
        Running_Servo_POS[Index] = Servo_Act_0[Index]
    
    for iServo in range(ALLSERVOS):
        Set_PWM_to_Servo(iServo, Running_Servo_POS[iServo])
        time.sleep_ms(10)  # Delay to allow servo to move

def Servo_PROGRAM_Run(iMatrix, iSteps):
    """Run the servo program based on the provided matrix."""
    for MainLoopIndex in range(iSteps):
        InterTotalTime = iMatrix[MainLoopIndex][ALLMATRIX - 1]
        InterDelayCounter = InterTotalTime // BASEDELAYTIME
        
        for InterStepLoop in range(InterDelayCounter):
            for ServoIndex in range(ALLSERVOS):
                INT_TEMP_A = Running_Servo_POS[ServoIndex]
                INT_TEMP_B = iMatrix[MainLoopIndex][ServoIndex]
                
                if INT_TEMP_A != INT_TEMP_B:
                    if INT_TEMP_A > INT_TEMP_B:
                        increment = map_value(BASEDELAYTIME * InterStepLoop, 0, InterTotalTime, 0, INT_TEMP_A - INT_TEMP_B)
                        Set_PWM_to_Servo(ServoIndex, INT_TEMP_A - increment)
                    else:  # INT_TEMP_A < INT_TEMP_B
                        increment = map_value(BASEDELAYTIME * InterStepLoop, 0, InterTotalTime, 0, INT_TEMP_B - INT_TEMP_A)
                        Set_PWM_to_Servo(ServoIndex, INT_TEMP_A + increment)
            
            time.sleep_ms(BASEDELAYTIME)  # Delay in milliseconds
        
        # Backup current servo values
        for Index in range(ALLMATRIX):
            Running_Servo_POS[Index] = iMatrix[MainLoopIndex][Index]

# forward
iMatrix1 = [
    [70, 110, 70, 120, 300],
    [60, 90, 60, 90, 300],

    [110, 50, 110, 60, 300],
    [105, 90, 105, 90, 300],
]

def forward():
    try:
        Servo_PROGRAM_Run(iMatrix1, len(iMatrix1))
    except Exception as e:
        pass


# Backward
iMatrix2 = [
    [110, 110, 110, 120, 300], # Andr: Adjusted for correct backward motion (inverted Thighs from Forward)
    [120, 90, 120, 90, 300], # Andr: Adjusted for correct backward motion
    [70, 50, 70, 60, 300],   # Andr: Adjusted for correct backward motion
    [75, 90, 75, 90, 300], # Andr: Adjusted for correct backward motion
]

def backward():
    try:
        Servo_PROGRAM_Run(iMatrix2, len(iMatrix2))
    except Exception as e:
        pass
    
# leftward
iMatrix3 = [
    [90, 60, 125, 90, 300],
    [60, 60, 125, 90, 300],
    [60, 90, 125, 90, 300],

    [60, 120, 55, 120, 300],
    [60, 90, 55, 90, 300],

    [80, 90, 90, 90, 150],
]

def left():
    try:
        Servo_PROGRAM_Run(iMatrix3, len(iMatrix3))
    except Exception as e:
        pass

# rightward
iMatrix4 = [
    [50, 90, 90, 120, 300], 
    [50, 90, 130, 120, 300], 
    [50, 90, 130, 90, 300],

    [120, 50, 130, 60, 300],
    [120, 90, 130, 90, 300],

    [90, 90, 80, 90, 150],
]

def right():
    try:
        Servo_PROGRAM_Run(iMatrix4, len(iMatrix4))
    except Exception as e:
        pass

# sprint
iMatrix5 = [
    [75, 105, 68, 110, 600],
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
]

def sprint():
    try:
        Servo_PROGRAM_Run(iMatrix5, len(iMatrix5))
    except Exception as e:
        pass

# left_kick
iMatrix6 = [
    [90, 65, 90, 95, 500],
    [40, 65, 90, 95, 300],
    [150, 65, 90, 95, 300],

    [90, 90, 90, 90, 300],
]

def left_kick():
    try:
        Servo_PROGRAM_Run(iMatrix6, len(iMatrix6))
    except Exception as e:
        pass


# right_kick
iMatrix7 = [
    [90, 80, 90, 100, 500],
    [90, 80, 150, 100, 300],
    [90, 80, 40, 100, 300],

    [90, 90, 90, 90, 300],
]

def right_kick():
    try:
        Servo_PROGRAM_Run(iMatrix7, len(iMatrix7))
    except Exception as e:
        pass

# left_tilt
iMatrix8 = [
    [96, 110, 90, 90, 500],

    [100, 75, 90, 45, 500],

    [130, 60, 90, 20, 500],

    [140, 35, 90, 20, 500],

    [90, 35, 90, 90, 500],

    [90, 35, 90, 20, 500],

    [130, 60, 90, 20, 500],

    [120, 60, 90, 25, 500],

    [100, 75, 90, 45, 500],

    [96, 110, 90, 90, 500],
    
]

def left_tilt():
    try:
        Servo_PROGRAM_Run(iMatrix8, len(iMatrix8))
    except Exception as e:
        pass

# right_tilt
iMatrix9 = [
    [90, 90, 82, 70, 500],

    [90, 135, 80, 105, 500],

    [90, 163, 40, 120, 500],


    [90, 163, 40, 140, 500],

    [90, 90, 90, 140, 500],

    [90, 163, 90, 145, 500],


    [90, 163, 50, 120, 500],
    [90, 158, 60, 120, 500],

    [90, 135, 80, 105, 500],

    [90, 90, 82, 70, 500],
]

def right_tilt():
    try:
        Servo_PROGRAM_Run(iMatrix9, len(iMatrix9))
    except Exception as e:
        pass

# left_stamp
iMatrix10 = [
    [90, 100, 92, 95, 300],

    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],
    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],
    [90, 60, 92, 85, 300],
    [90, 120, 92, 95, 300],

    [90, 90, 90, 90, 300],
]

def left_stamp():
    try:
        Servo_PROGRAM_Run(iMatrix10, len(iMatrix10))
    except Exception as e:
        pass


# right_stamp
iMatrix12 = [
    [90, 80, 90, 100, 300],

    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],
    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],
    [90, 95, 90, 60, 300],
    [90, 75, 90, 120, 300],

    [90, 90, 90, 90, 300],
]

def right_stamp():
    try:
        Servo_PROGRAM_Run(iMatrix12, len(iMatrix12))
    except Exception as e:
        pass
    
# dance
iMatrix11 = [
    [75, 140, 90, 70, 500],
    [75, 55, 90, 55, 500],
    [75, 90, 90, 90, 500],
    [75, 140, 90, 70, 500],
    [75, 55, 90, 55, 500],
    [75, 90, 90, 90, 500], 

    [75, 140, 90, 70, 500],
    [75, 55, 90, 55, 500],
    [75, 90, 90, 90, 500],
    [75, 140, 90, 70, 500],
    [75, 55, 90, 55, 500],
    [75, 90, 90, 90, 500], 

    [75, 110, 90, 45, 500],
    [75, 125, 90, 105, 500],
    [75, 90, 90, 90, 500],
    [75, 110, 90, 45, 500],
    [75, 125, 90, 105, 500],
    [75, 90, 90, 90, 500],

    [75, 110, 90, 45, 500],
    [75, 125, 90, 105, 500],
    [75, 90, 90, 90, 500],
    [75, 110, 90, 45, 500],
    [75, 125, 90, 105, 500],
    [75, 90, 90, 90, 500],
]

def dance():
    try:
        Servo_PROGRAM_Run(iMatrix11, len(iMatrix11))
    except Exception as e:
        pass


# left_ankles
iMatrix13 = [
    [50,90,80,90, 300],
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
]

def left_ankles():
    try:
        Servo_PROGRAM_Run(iMatrix13, len(iMatrix13))
    except Exception as e:
        pass


# right_ankles
iMatrix14 = [
    [100,90,125,90, 300],
    [100,75,125,50, 300], 
    [100,75,100,50, 300],
    [100,75,120,50, 300], 
    [100,75,100,50, 300],

    [100,75,120,50, 300], 
    [100,75,100,50, 300],
    [100,75,120,50, 300], 
    [100,75,100,50, 300],

    [100,90,120,70, 300],
]

def right_ankles():
    try:
        Servo_PROGRAM_Run(iMatrix14, len(iMatrix14))
    except Exception as e:
        pass

def stop():
    try:
        Servo_PROGRAM_Zero()
    except Exception as e:
        pass

def avoid():
    UT_distance = Ultrasonic.get_distance()
    if UT_distance <= 15:
        stop()

        backward()
        backward()
        backward()
        backward()
        backward()
        backward()
        
        rand_number = random.randint(1, 2)
        if rand_number == 1:
            for _ in range(5):  # 重复5次
                left()
                time.sleep(0.5)
        elif rand_number == 2:
            for _ in range(5):  # 重复5次
                right()
                time.sleep(0.5)
                
    else:
        forward()
        
def follow():
    UT_distance = Ultrasonic.get_distance()
    if UT_distance <= 15:
        backward()
    elif 15 <= UT_distance and UT_distance <= 20:
        stop()
    elif 20 < UT_distance and UT_distance <= 35:
        forward()
    else:
        stop()
