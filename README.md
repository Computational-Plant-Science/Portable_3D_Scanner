# Portable_3D_Scanner


Parts:
2 Raspberry Pi 4 Model B
1 crossover ethernet cable
Arducam 16MP Autofocus Quad-Camera Kit for Raspberry Pi, 16MP IMX519 Autofocus Synchronized Pi Camera
Stepper motor plus hat

Step 1: Connect one Raspberry Pi (master/controller) to cameras and the stepper motor.

Step 2: Connect the second Raspberry Pi to cameras and the first Raspberry Pi via crossover cable.

Configure each Pi to have a unique static IP within the same network.
sudo geany /etc/network/interfaces

For example, setup PiController (IP address: 192.168.1.5) (PiController)
                      setup Pi 01 (IP address: 192.168.1.6)
on PiController
auto eth0
iface eth0 inet static
address 192.168.1.5
netmask 255.255.255.0
gateway 192.168.1.6

on Pi 01
auto eth0
iface eth0 inet static
address 192.168.1.6
netmask 255.255.255.0
gateway 192.168.1.5
