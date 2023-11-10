"""
Version: 1.0

Function: Capture images using Arducam 16MP Autofocus Quad-Camera Kit for Raspberry Pi, 

            16MP IMX519 Autofocus Synchronized Pi Camera, 

Author: suxing liu

Author-email: suxingliu@gmail.com

USAGE:

     python3 pipeline.py -n 5
     

Parameters:

   
    -n: Number of image sets (4 images for one set)
   
    -nd: Moving steps of the stepper motor

    -sf: stepper motor speed in clockwise direction

    -sb, stepper motor speed in counterclockwise direction


Note: all the paramters have default values, can be adjusted.

"""


import subprocess, os
import sys
import argparse
import numpy as np 
import pathlib
import os
import glob

import shutil

import time
from time import sleep
from datetime import date, datetime

import RPi.GPIO as GPIO
from time import sleep

from multiprocessing import Pool



# execute script inside program
def execute_script(cmd_line):
    

    
    print(cmd_line)
    
    
    try:
        #print(cmd_line)
        #os.system(cmd_line)

        process = subprocess.getoutput(cmd_line)
        
        print(process)
        
        error_id = 0
        
        #process = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE)
        
        #process = subprocess.Popen(f"ssh pi@192.168.1.6 {cmd_line}", shell = True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
        
        #process.wait()
        #print (process.communicate())
        
    except OSError:
        
        print("Failed ...!\n")





# make the stepper motor move specific numbers
def move_setps(direction_sign, step_number):
    
    # get the direction to move stepper motor
    if direction_sign == 0:
        print("Moving {} steps in clockwise direction...\n".format(step_number))
    else:
        print("Moving {} steps in counterclockwise direction...\n".format(step_number))
    
    #record the start time
    start_time = time.time()

    # move specific steps
    for x in range(step_number):
        # Set one coil winding to high
        GPIO.output(STEP,GPIO.HIGH)
        # Allow it to get there.
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run
        # Set coil winding to low
        GPIO.output(STEP,GPIO.LOW)
        sleep(speed_forward_sec) # Dictates how fast stepper motor will run
    
    
    # compute the time used for captur images
    cost_time = time.time() - start_time

    #output cost time
    print("Time used for stepper motor movement: {0:.2f} seconds\n".format(cost_time))
    
    # return the time used for moving specific steps
    return cost_time
    


# change the moving direction of the stepper motor 
def change_direction(DIR,CCW):
    
    print("Change direction...\n".format(step_number))
    
    sleep(1.0)
    
    # change the GPIO output voltage
    GPIO.output(DIR,CCW)





# capture images using Pi with ID_PI
def Pi_img_capture(ID_PI):
    
    
    #record the time for capture and write images
    start_time = time.time()
    
    # initialize error sign
    error = 0
    
    # capture images using ID_PI
    if ID_PI == 5:
        
        print("Capture images using PiController...\n")
        # PiController with IP address 192.168.1.5, current local Pi, no need ssh
        cmd_line = "./img_cap_remote.sh"
    
    elif ID_PI == 6:
        
        print("Capture images using Pi01...\n")
        # Pi01 with IP address 192.168.1.6, remote access from PiController to Pi01 using ssh and bash command to capture images
        cmd_line = "ssh -t pi@192.168.1.6 < img_cap_remote.sh"
    
    else:
        
        print("Pi ID was not ccorect!\n")
        error = 1
        
        cmd_line = "ls"
        
    
    # run the bash file inside python script
    execute_script(cmd_line)
    
    # compute the time used for captur images
    cost_time = time.time() - start_time

    #output cost time
    print("Time used for capturing images: {0:.2f} seconds\n".format(cost_time))
    
    
    return cost_time, error
        



def parallel_capture(n_set_img, ID_PI):
    
    
    # capture image pipeline, keep camera open and streaming  
    for index in range(n_set_img):

        print("Capturing and writing {} set of images using Arducam 16MP Autofocus Quad-Camera Kit...\n".format(index+1))
        
        #image capture for both PiController and Pi01 
        (cost_time, error) = Pi_img_capture(ID_PI)
        
        if ID_PI == 5:
            
            #wait the motor to move to next angle
            time.sleep(move_setps(CW, n_step))
        else:
            print("Waiting for Pi01 to finish the task!\n")
        
 

# convert degree to steps for stepper motor to move 
def degree_step(v_degree):
    #[(960 teeth in large gear/20 teeth in small gear)*(200 motor steps/one full revolution of small gear)] = 9600 motor steps/one full revolution of large gear
    
    steps_per_degree = 9600/360
    
    steps_motor = round(v_degree*steps_per_degree)
    
    return steps_motor




    
if __name__ == '__main__':
    
    # construct the argument and parse the arguments
    ap = argparse.ArgumentParser()
    #ap.add_argument("-p", "--path", required = False, help = "path to image save folders")
    #ap.add_argument("-td", "--time_delay", required = False, type = int, default = 2000, help = "delay time for auto focus, time unit: ms")
    ap.add_argument("-n", "--number_set_img", required = False, type = int, default = 5, help = "Number of image sets (4 images for one set)")
    ap.add_argument("-nd", "--n_degree", required = False, type = int, default = 6, help = "Moving angles of the stepper motor, 6 degree as default")
    ap.add_argument("-sf", "--speed_forward", required = False, type = float, default = 0.01, help = "stepper motor speed in clockwise direction")
    ap.add_argument("-sb", "--speed_backword", required = False, type = float, default = 0.005, help = "stepper motor speed in counterclockwise direction")
    args = vars(ap.parse_args())
    
   
    #parameter sets
    # path to individual folders
    #current_path = args["path"]
    #time_delay = args["time_delay"]
    
    # set of images to capture
    n_set_img = args["number_set_img"]
    
    # set the stepper movement parameters
    n_step = degree_step(args["n_degree"])
    
    print("{} steps are needed to move {} degree\n".format(n_step, args["n_degree"]))
    
    speed_forward_sec = args["speed_forward"]
    speed_backword_sec = args["speed_backword"]
    

    # list device (all cameras on board) 
    #list_camera_cmd = "libcamera-still --list-camera"
    
    #execute_script(list_camera_cmd)
    
    
    
    #Initialize Pi borad pins for motor 
    ####################################################################
    # Direction pin from controller
    DIR = 10
    
    # Step pin from controller
    STEP = 11
    
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1

    # Steps per Revolution (360 / 7.5)
    #SPR = 48   


    GPIO.setwarnings(False)
    
    # Setup pin layout on PI
    GPIO.setmode(GPIO.BOARD)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR, CW)
    

    # move specific numbers and capture images
    ###################################################################
    #n_set_img = 5
    # Assume the way it is pointing is zero degrees
    #current_angle = 0  
    
    ID_PI = 6

    #parallel_capture(n_set_img, ID_PI)
    
    
    # capture image pipeline, keep camera open and streaming  
    for index in range(n_set_img):

        print("Capturing and writing {} set of images using Arducam 16MP Autofocus Quad-Camera Kit...\n".format(index+1))
        
        with Pool(processes = 2) as pool:
            
            result = pool.map(Pi_img_capture, [5,6])

        #wait the motor to move to next angle
        time.sleep(move_setps(CW, n_step))

    
    #move_setps(CW, step_number)
    
    #change_direction(DIR,CCW)

    #move_setps(CCW, 10)
    
    ####################################################################
    # clean up Pi board GPIO pins
    print("Stepper motor finished moving, cleanup GPIO")
    
    GPIO.cleanup()
    



