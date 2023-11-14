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

Step 3: Setup Bluetooth connection between a PC/laptop (Windows OS) and the Raspberry Pi (PiController) to enable wireless access to the Pi.

Login into PiController:
sudo nano /etc/systemd/system/dbus-org.bluez.service

Add a ' -C' compatibility flag at the end of the ExecStart= line, and add a new line to add the SP profile. The two lines should look like this:
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP


Save the file and reboot. Now enter this line in a terminal:

sudo rfcomm watch hci0 1 getty rfcomm0 115200 vt100 -a pi

(Remember to type in above command!)


Paring the Raspberry Pi to your laptop/PC.
On your Raspberry Pi:
1.	Click Bluetooth ‣ Turn On Bluetooth (if it’s off)
2.	Click Bluetooth ‣ Make Discoverable
3.	Click Bluetooth ‣ Add Device
4.	Your phone will appear in the list, select it and click Pair


Login into your PC/laptop with Windows OS:


Download PuTTY terminal program and install it to your PC.
To associate a COM port with a Rasperry Pi/ Windows 10 Bluetooth pairing, we proceed as follows:
On your Windows 10 Desktop/ Laptop first enable the Bluetooth transceiver. Select Start, Settings, then Devices. At this point resist the intuitive temptation to Add bluetooth or other device. Instead, scroll down to 'Related settings', and select Devices and printers. Find your Desktop/ Laptop under 'Devices', right click it, then select Bluetooth settings from the pop up menu. This brings up the 'Bluetooth settings dialogue:
Select the COM ports tab, then select Add... to bring up the 'Add COM port' dialogue. Here we select the 'Outgoing' radio button, and then click on Browse... This will yield the 'Select Bluetooth Device' dialogue. All going well, you should see your Raspberry Pi listed as a discovered device. Select the Raspberry Pi device listed, and click OK twice. This should take you back to the COM ports tabbed dialogue, and list a COM port that is now associated with the Windows 10/ Raspberry Pi pairing. Take note of which COM port has been assigned.
       
Login to Your Pi's Bluetooth Shell.

 

You should now be able to initiate a login session from your Windows 10 PC, using the numbered COM port previously noted, at a speed of 115200 bps.
 
Good Luck!

Reference: https://forums.raspberrypi.com//viewtopic.php?p=955425#p956581
https://www.instructables.com/Raspberry-Pi-Bluetooth-to-PuTTY-on-Windows-10/
