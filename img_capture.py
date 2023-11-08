"""
Version: 1.0

Function: Capture images using Arducam 16MP Autofocus Quad-Camera Kit for Raspberry Pi, 

            16MP IMX519 Autofocus Synchronized Pi Camera, 

Author: suxing liu

Author-email: suxingliu@gmail.com

USAGE:

    python3 img_capture.py -n 5
    

Parameters:

    -p: path to image save folders, 
    
    -td: delay time for auto focus, time unit: ms
   
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



# generate foloder to store the output results
def mkdir(path):
    # import module
    import os
 
    # remove space at the beginning
    path=path.strip()
    # remove slash at the end
    path=path.rstrip("\\")
 
    # path exist?   # True  # False
    isExists=os.path.exists(path)
 
    # process
    if not isExists:
        # construct the path and folder
        #print path + ' folder constructed!'
        # make dir
        os.makedirs(path)
        return True
    else:
        # if exists, return 
        print('path exists!\n')
        shutil.rmtree(path)
        os.makedirs(path)
        return False
        


# execute script inside program
def execute_script(cmd_line):
    
    try:
        #print(cmd_line)
        #os.system(cmd_line)

        process = subprocess.getoutput(cmd_line)
        
        print(process)
        
        #process = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE)
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





# execute pipeline scripts in order
def single_image_capture(file_path):
    
    #record the time for capture and write images
    start_time = time.time()
    
    # initialize error sign
    error = 0
    
    #output image storage path
    print("Writing images to folder '{}'...\n".format(file_path))
    
    file_path_full = file_path + '/'

    # set the camera list by ID
    camera_IC_list = ["i2cset -y 10 0x24 0x24 0x02", "i2cset -y 10 0x24 0x24 0x12",
                        "i2cset -y 10 0x24 0x24 0x22", "i2cset -y 10 0x24 0x24 0x32"]
    
    
    # capture images in sequential order, as instructed by Arducam 16MP Autofocus Quad-Camera Kit
    for image_id, set_cam_ID in enumerate(camera_IC_list):
        
        img_name =  "{:%Y-%m-%d-%H-%M-%S}".format(datetime.now())
        
        img_file = file_path + img_name + "_{:02d}".format(image_id) + ".jpg"
        
        
        # libcamera-still -t 5000 -n -o test.jpg --width 4656 --height 3496
        #capture_cmd = set_cam_ID + " && " + "libcamera-still -t 2000 -n -o " + img_file + " --width 4656 --height 3496"
        
        capture_cmd = set_cam_ID + " && " + "libcamera-still -t " + str(time_delay) + " -n -o " + img_file + " --width 4656 --height 3496"


        print(capture_cmd)
        
        execute_script(capture_cmd)
        
    # resume camera to normal status
    resume_cmd = "i2cset -y 10 0x24 0x24 0x00"
    
    execute_script(resume_cmd)
    
    # compute the time used for captur images
    cost_time = time.time() - start_time

    #output cost time
    print("Time used for capturing images: {0:.2f} seconds\n".format(cost_time))
    
    
    # check images 
    if len(os.listdir(file_path_full)) == 0:
        print("Image output directory is empty\n")
    else:    
        print("Image capture successful..\n")
        error = 1
    
    
    return cost_time, error
        

# convert degree to steps for stepper motor to move 
def degree_step(v_degree):
    #[(960 teeth in large gear/20 teeth in small gear)*(200 motor steps/one full revolution of small gear)] = 9600 motor steps/one full revolution of large gear
    
    steps_per_degree = 9600/360
    
    steps_motor = round(v_degree*steps_per_degree)
    
    return steps_motor

   
    
if __name__ == '__main__':
    
    # construct the argument and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required = False, help = "path to image save folders")
    ap.add_argument("-td", "--time_delay", required = False, type = int, default = 2000, help = "delay time for auto focus, time unit: ms")
    ap.add_argument("-n", "--number_set_img", required = False, type = int, default = 5, help = "Number of image sets (4 images for one set)")
    ap.add_argument("-nd", "--n_degree", required = False, type = int, default = 6, help = "Moving angles of the stepper motor, 6 degree as default")
    ap.add_argument("-sf", "--speed_forward", required = False, type = float, default = 0.01, help = "stepper motor speed in clockwise direction")
    ap.add_argument("-sb", "--speed_backword", required = False, type = float, default = 0.005, help = "stepper motor speed in counterclockwise direction")
    args = vars(ap.parse_args())
    
   
    #parameter sets
    # path to individual folders
    current_path = args["path"]
    time_delay = args["time_delay"]
    
    # set of images to capture
    n_set_img = args["number_set_img"]
    
    # set the stepper movement parameters
    n_step = degree_step(args["n_degree"])
    
    print("{} steps are needed to move {} degree\n".format(n_step, args["n_degree"]))
    
    speed_forward_sec = args["speed_forward"]
    speed_backword_sec = args["speed_backword"]
    
    
    
    # setup image storage path
    if (args['path']):
        save_path = args['path']
    else:
        # save folder construction
        current_path = os.getcwd()
        
        #setup saving path for captured images
        date_today = str(date.today())
        
        mkpath = current_path + '/' + date_today
        mkdir(mkpath)
        save_path = mkpath + '/'
    
    # list device (all cameras on board) 
    list_camera_cmd = "libcamera-still --list-camera"
    
    execute_script(list_camera_cmd)
    
    
    
    
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
    ####################################################################


    

    # Assume the way it is pointing is zero degrees
    #current_angle = 0  

    
    
    # move specific numbers and capture images
    ###################################################################
    #n_set_img = 5
    
    #capture image pipeline, keep camera open and streaming  
    for index in range(n_set_img):

        print("Capturing and writing images using Arducam 16MP Autofocus Quad-Camera Kit...\n")

        (cost_time, error) = single_image_capture(save_path)
        
        #wait the motor to move to next angle
        time.sleep(move_setps(CW, n_step))
    
    
    #move_setps(CW, step_number)
    
    #change_direction(DIR,CCW)

    #move_setps(CCW, 10)
    
    ####################################################################
    # clean up Pi board GPIO pins
    print("Stepper motor finished moving, cleanup GPIO")
    
    GPIO.cleanup()
    



