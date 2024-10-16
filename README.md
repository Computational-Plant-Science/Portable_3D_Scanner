# Portable 3D_Scanner

Author: Suxing Liu, Ruben Pena




![Prototype](../main/media/Picture4.jpg)

![Portable 3D_Scanner working in the lab](../main/media/Picture7.jpg)

![Portable 3D_Scanner working in the field](../main/media/Picture3.jpg)



Function: Capture images around one root sample

Illumination environment:  LED light intensity can be adjusted from weak to strong, suggest to adjust the lighting of LED lights via capture sample images and visually check the quality. The lights in the basement room can be turned off. 

![Led lights](../main/media/Picture2.jpg)

Main parts: Two raspberry pi 4 model b+ with USB 3.0 interface (Controller pi and Pi01), connected via cross over ethernet cable (Not traditional ethernet cable), 

Each raspberry pi equipped with a Arducam 16MP Autofocus Quad-Camera Kit, 16MP IMX519 Autofocus Synchronized Pi Camera. A step motor and driver control the movement of the whole frame. 

![Cameras](../main/media/Picture6.jpg)

![Setpper motor and driver](../main/media/Picture5.jpg)

![3D model reconstrcution results](../main/media/Picture8.jpg)



Operation

1. Turn on the power of the surge protector, which connects to all the power of the scanner.

2. Check the display directly connects to “pi controller”, Make sure wireless mouse/keyboard was turned on.

3. Open command window from “pi controller” terminal, type command lines:
```bash
    cd code/cam                  #enter working path

    python3 cluster_connection.py          # check the raspberry pi unit’s connection to each other

    python3 pipeline.py -n 5                # scan root, image data will be stored in the folder named as current  
                                                                       year-date format such as /2024-10-16/
```
    Parameters:
    -n: Number of image sets (4 images for one set)
    -nd: Moving steps of the stepper motor
    -sf: stepper motor speed in clockwise direction
    -sb, stepper motor speed in counterclockwise direction
    Note: all the parameters have default values, can be adjusted.


If error. Reboot the whole system: 
```bash
python3 cluster_reboot.py  
```

Rotate the camera arm to its original position and restart the scan process.

4. Transfer files to your local computer.
Connect your mobile drive to the controller pi, rename the folder /2024-10-16/ as /genotype-samplenumber/ and download the folder from “pi controller” to your mobile drive.

6. Delete files from “pi controller” and raspberry pi units.

7. Shutdown system

```bash
    Python3 cluster_shutdown.py
```
8. Turn off the power of surge protector
    
