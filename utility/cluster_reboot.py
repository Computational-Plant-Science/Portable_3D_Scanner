"""
Version: 1.0
Reboot all cluster pi except PiController
Author: suxing liu
Author-email: suxingliu@gmail.com

USAGE

    python3 cluster_reboot.py

"""


import subprocess, os
import sys

def reboot_connection(host_adr):
    
    cmd_line = "ssh pi@" + ''.join(host_adr) + ' sudo reboot'
    
    print(cmd_line)   
    
    returned_value = subprocess.call(cmd_line, shell=True)
    
    if returned_value == 255:
        print("Rapberry Pi host @{0} was rebooting...\n".format(''.join(host_adr)))
    else:
        print("SSH reboot failed ...!\n")
    

def main(args):
    '''
    
    PiController = "192.168.1.5"
    
    pi01 = "192.168.1.6"

    '''
    
    host_adr = "192.168.1.6"
    
    reboot_connection(host_adr)
    
    
    
if __name__ == '__main__':
    
    sys.exit(main(sys.argv))
    

