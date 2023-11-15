"""
Version: 1.0

Function: Transfer images from cluster pis to PiContrller

Author: suxing liu

Author-email: suxingliu@gmail.com

USAGE

    python3 bluetooth_startup.py 

"""

import subprocess, os

# execute script inside program
def execute_script(cmd_line):
    

    
    print(cmd_line)
    
    
    try:
        #print(cmd_line)
        #os.system(cmd_line)

        process = subprocess.getoutput(cmd_line)
        
        print(process)
        
        error_id = 0
        
        print("bluetooth serial terminal connection successful!\n")
        
    except OSError:
        
        print("bluetooth serial terminal connection...!\n")





if __name__ == "__main__":
    
    
        # enable a bluetooth serial terminal connection at startup of Pi, auto login in as pi.
        bluetooth_cmd = "sudo rfcomm watch hci0 1 getty rfcomm0 115200 vt100 -a pi"

        execute_script(bluetooth_cmd)
