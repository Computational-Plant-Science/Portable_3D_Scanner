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
        #shutil.rmtree(path)
        #os.makedirs(path)
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
        


    
if __name__ == '__main__':
    
    # construct the argument and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required = False, help = "path to image save folders")
    ap.add_argument("-td", "--time_delay", required = False, type = int, default = 2000, help = "delay time for auto focus, time unit: ms")
    ap.add_argument("-n", "--number_set_img", required = False, type = int, default = 1, help = "Number of image sets (4 images for one set)")
    ap.add_argument("-nd", "--n_degree", required = False, type = int, default = 6, help = "Moving angles of the stepper motor, 6 degree as default")
    args = vars(ap.parse_args())
    
   
    #parameter sets
    # path to individual folders
    current_path = args["path"]
    time_delay = args["time_delay"]
    
    # set of images to capture
    n_set_img = args["number_set_img"]

    
    
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
    
    
    # move specific numbers and capture images
    ###################################################################
    #n_set_img = 5
    
    #capture image pipeline, keep camera open and streaming  
    for index in range(n_set_img):

        #print("Capturing and writing images using Arducam 16MP Autofocus Quad-Camera Kit...\n")

        (cost_time, error) = single_image_capture(save_path)

    
    

    



