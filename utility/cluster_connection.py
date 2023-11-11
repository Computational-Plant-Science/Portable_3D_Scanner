"""
Version: 1.0
Test raspberry pi cluster connection with master
Author: suxing liu
Author-email: suxingliu@gmail.com

USAGE

    python3 cluster_connection.py

"""

import subprocess, os
import sys
from datetime import date


def test_connection(host_adr):
    
    cmd_line = "ssh pi@" + ''.join(host_adr) + ' exit'
    
    print(cmd_line)   
    
    returned_value = subprocess.call(cmd_line, shell=True)
    
    if returned_value == 0:
        print("Rapberry Pi host @{0} was connected...\n".format(''.join(host_adr)))
    else:
        print("SSH connection failed ...!\n")





def synchonize_date(host_adr, v_date):
    
    
    set_date_cmd = " sudo date -s " + v_date
    
    cmd_line = "ssh " + ''.join(host_adr) + set_date_cmd + ' & exit'
    
    print(cmd_line)   
    
    returned_value = subprocess.call(cmd_line, shell=True)
    
    if returned_value == 0:
        print("Rapberry Pi data @ was synchonized...\n".format(''.join(host_adr)))
    else:
        print("SSH connection failed ...!\n")
    


def main(args):
    '''
    
    PiController = "192.168.1.5"
    
    pi01 = "192.168.1.6"

    '''
    
    host_adr = "192.168.1.6"
    
    
    
    v_date = "{:%Y-%m-%d}".format(date.today())
    
    test_connection(host_adr)
    
    
    #synchonize_date(host_adr, v_date)
    
    
    




    
if __name__ == '__main__':
    
    sys.exit(main(sys.argv))
    
