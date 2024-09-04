"""
Version: 1.0

Function: Transfer images from cluster pis to PiContrller

Author: suxing liu

Author-email: suxingliu@gmail.com

USAGE

    python3 img_transfer.py -p /home/pi/code/image_data/ -a 1

"""

import subprocess, os
import sys
import argparse


from os.path import relpath




def move_img(host_address):
    
    #cmd_line = "ssh pi@" + ''.join(host_adr) + ' exit'
    
    #cmd_line = "ls && ls -la"
    
    cmd_line = "scp " + host_address + folder_path + "*.jpg " + folder_path
    
    #cmd_line = "scp " + host_address + folder_path + "transfer.zip " + folder_path
    
    #scp 192.168.1.110:/home/pi/code/cam/*.jpg .
    
    print(cmd_line)

    
    
    try:
        #subprocess.call(cmd_line + [str(img_name)])
        os.system(cmd_line)
        print("Captured images were moved to PiController...\n")
    except OSError:
        print("Failed moving image!\n")
    







def delete_img(host_address):
    
    host_add = host_address.replace(":", "")
    
    #delete_cmd = " sudo rm -rf " + folder_path + "*.jpg "
    
    delete_cmd = " sudo rm -rf " + folder_path
    
    cmd_line = "ssh " + ''.join(host_add) + delete_cmd + " exit"

    print(cmd_line)

    
    try:
        #subprocess.call(cmd_line + [str(img_name)])
        os.system(cmd_line)
        print( "Images on Pi01 were deleted...\n")
        
    except OSError:
        print("Failed moving image!\n")
    




def main(args):
    
    #pasre paramters 
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--path', required = False, type = str, default = '/home/pi/code/image_data/', help = "image files path")
    ap.add_argument('-a', '--action', required = True, type = int, help = '"1" is move files' + '"2" is delete files')
    args = vars(ap.parse_args())
    
    global folder_path
    
    folder_path = args['path']
    

    
    host_list = "pi@192.168.1.6:"

    
    #move file to PiController

    
    if args['action'] == 1:
        
        move_img(host_list)
    
    elif args['action'] == 2:

        delete_img(host_list)
            
        delete_local = "sudo rm -rf " + folder_path

        
    else:
        print("Invalid action choice!\n")
        
        
        

if __name__ == '__main__':
    
    sys.exit(main(sys.argv))
    
