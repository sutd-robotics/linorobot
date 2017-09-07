# RaspberryPi Installation and Configuration Guide

* [Installation](#Installtion)
* [RPi Configurations](#RPi Configurations)
* [Remote Access](#Remote Access)
* [MicroSD Image Handling](#MicroSD Image Handling)


## Installation

* Download Ubuntu Mate <br />
https://ubuntu-mate.org/raspberry-pi/ <br />
(Make sure you install Ubuntu MATE 16.04 ONLY. It's the only version compatible with ROS Kinetic) <br />
(Ubuntu is chosen it install ROS Kinetic Kame more quickly <br />
http://wiki.ros.org/kinetic/Installation/Ubuntu)

* Burn into SD card <br />
Use Etcher to burn the image of Ubuntu Mate into the SD card. <br />
https://etcher.io/ <br />
Minimum size of SD card 8GB. Recommended size of SD card is 32GB, as you will install many packages.

* Accessories <br />
Attach SD card, HDMI output, USB Mouse, USB Keybaord <br />
Then, attach power to turn on. (5V 2.5A) <br />
Configure your username and password. <br />
Connect to WiFi (iLP2 WiFi works) <br />
Reboot, as the RPi may be laggy in its first boot <br />

## RPi Configurations

* Setting up the time <br />
There is no hardware clock on RPi. Script to sync clock with Internet on every boot: <br />
sudo nano /etc/ rc.local <br />
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z" <br />
(accept changes, if there is) <br />
Control-X to exit
 
* Connecting to student WiFi <br />
Authentication: PEAP <br />
Check option (No CA certificate)

* Update and upgrade, and reboot <br />
sudo apt-get update && sudo apt-get upgrade -y && sudo reboot

* Uninstall unnecessary preloaded programs <br />
To save some around 500MB of space <br />
sudo apt-get purge scratch minecraft-pi shotwell firefox hexchat pidgin thunderbird atril fluid sonic-pi brasero cheese rhythmbox libreoffice-writer libreoffice-impress libreoffice-calc libreoffice-draw simple-scansudo synapse <br />
sudo apt-get autoremove

* Customising indicators <br />
For CPU indicator: right click top bar > add to panel > CPU <br />
For thermomter: add to panel > command > /opt/vc/bin/vcgencmd measure_temp

* Installing Chrome <br />
sudo apt-get install chromium-browser

* Installation of ROS <br />
http://wiki.ros.org/kinetic/Installation/Ubuntu  <br />
Follow the steps on the page, choose desktop-full install  <br />
(How to find the environments: system > control center > software and updates)

## Remote Access 
(copy from Timothy's docs) <br />
(remove iLP2 WiFi and use you own student WiFi)

* Enable SSH on RPi <br />
To connect and control wirelessly <br />
sudo systemctl enable ssh

* Install PuTTY on your remote computer <br />
To use SSH to remotely use RPi's terminal
https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html <br />
(refer to Timothy's docs)

* Download VNC Viewer on your remote computer https://www.realvnc.com/en/connect/download/viewer/ <br />
Install with the .exe file <br />
(What is VNC Viewer used for, and how to use it?)

## MicroSD Image Handling
Reading and writing, and resizing MicroSD image

* Reading and Writing  <br />
Win32 Disk Imager  <br /> 
https://sourceforge.net/projects/win32diskimager/files/Archive/

* Upsizing <br />
To expand disk memory to the entire of the SD card, for example after flashing 8GB image into a 32GB drive. <br />
sudo raspi-config > Advanced > Expand Filesystem <br />
After rebooting, all the memory of the SD card will be occupied.

* Downsizing <br />
How? You may need to decrease the size occupied to transfer between SD card of almost similar capacity.

