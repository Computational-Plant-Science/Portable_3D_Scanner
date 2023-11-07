"""
Version: 1.0
Function: Control step motor using Raspberry Pi 4 Model B and general step motor 
Author: suxing liu
Authoremail: suxingliu@gmail.com

USAGE

    python3 motor_test.py

"""


import RPi.GPIO as GPIO
from time import sleep




def move_to(STEP, current_angle, angle):
    """Take the shortest route to a particular angle (degrees)."""
    # Make sure there is a 1:1 mapping between angle and stepper angle
    
    #deg_per_step = 1.8 / 200
    
    deg_per_step = 360 / 9600
    
    steps_per_rev = int(360 / deg_per_step)  # 40,000
    
    
    #target_step_angle = 1 * (int(angle / deg_per_step) / 1)
    
    #steps = target_step_angle - current_angle
    
    #steps = int(steps % steps_per_rev)
    
    steps = int(angle/deg_per_step)
    
    steps = int(steps % steps_per_rev)
    

    print("Moving angle = {}, related steps = {}\n".format(angle, steps))
    
    for x in range(steps):

        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run

    #current_angle = target_step_angle


# make the stepper motor move specific numbers
def move_setps(direction_sign, step_number):
    
    if direction_sign == 0:
        print("Moving {} steps in clockwise direction...\n".format(step_number))
    else:
        print("Moving {} steps in counterclockwise direction...\n".format(step_number))
    
    for x in range(step_number):

        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run
    
    


# change the moving direction of the stepper motor 
def change_direction(DIR,CCW):
    
    print("Change direction...\n".format(step_number))
    
    sleep(1.0)
    GPIO.output(DIR,CCW)


if __name__ == "__main__":
    
    
    # Direction pin from controller
    DIR = 10
    
    # Step pin from controller
    STEP = 11
    
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1

    # Steps per Revolution (360 / 7.5)
    SPR = 48   


    GPIO.setwarnings(False)
    
    # Setup pin layout on PI
    GPIO.setmode(GPIO.BOARD)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR, CW)



    # set the stepper movement parameters
    speed_forward_sec = .1

    speed_backword_sec = .005

    step_number = 20
    
    current_angle = 0  # Assume the way it is pointing is zero degrees
    
    
    #move_to(STEP, current_angle, 10)
    
    
    # move specific numbers 
    move_setps(CW, step_number)
    
    
    change_direction(DIR,CCW)
    
    
    move_setps(CCW, 10)
    
    
    print("Stepper motor finished moving, cleanup GPIO")
    GPIO.cleanup()
    
    '''
    try:
        # Run forever.
        while True:

            """Change Direction: Changing direction requires time to switch. The
            time is dictated by the stepper motor and controller. """
            sleep(1.0)
            # Esablish the direction you want to go
            GPIO.output(DIR,CW)

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(step_number):

                # Set one coil winding to high
                GPIO.output(STEP,GPIO.HIGH)
                # Allow it to get there.
                sleep(speed_forward_sec) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP,GPIO.LOW)
                sleep(speed_forward_sec) # Dictates how fast stepper motor will run

            """Change Direction: Changing direction requires time to switch. The
            time is dictated by the stepper motor and controller. """
            sleep(1.0)
            GPIO.output(DIR,CCW)
            for x in range(step_number):
                GPIO.output(STEP,GPIO.HIGH)
                sleep(speed_backword_sec)
                GPIO.output(STEP,GPIO.LOW)
                sleep(speed_backword_sec)

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
    '''
