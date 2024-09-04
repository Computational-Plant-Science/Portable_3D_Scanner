#!/bin/bash

#login in to pi01
#ssh pi@192.168.1.6

# change to the directory containing the Python script
cd /home/pi/code

# run the script
python3 img_capture.py -n 1
#hostname -I

# exit
exit


