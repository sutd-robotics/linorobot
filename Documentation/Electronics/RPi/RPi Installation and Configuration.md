# RaspberryPi Installation and Configuration Guide

* [Installation](#Installation)
* [RPi Configurations](#RPi Configurations)
* [Remote Access](#Remote Access)
* [MicroSD Image Handling](#MicroSD Image Handling)
* [Testing the XV-11 Lidar](#Testing the XV-11 Lidar)
* [Using RViz to visualise XV-11 Lidar input](#Using RViz to visualise XV-11 Lidar input)


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
Reading and writing, and resizing MicroSD image, as per: <br /> 
https://computers.tutsplus.com/articles/how-to-clone-your-raspberry-pi-sd-cards-with-windows--mac-59294

* Reading and Writing  <br />
Win32 Disk Imager  <br /> 
https://sourceforge.net/projects/win32diskimager/files/Archive/ <br /> 
Install with the exe file <br /> 
Choose location, and write your file name e.g. C:\Users\tong\Documents\UbuntuROS_040917.img <br /> 
Press "Read" to save image of SD card. Takes some time.
Replace SD card, press "Write" to write the selected image into the SD card.

* Upsizing <br />
To expand disk memory to the entire of the SD card, for example after flashing 8GB image into a 32GB drive. <br />
sudo raspi-config > Advanced > Expand Filesystem <br />
After rebooting, all the memory of the SD card will be occupied.

* Downsizing <br />
You could only transfer to and from SD cards with a higher capacity. 
Not any lower - two different brands of 32GB SD card may not work. <br />
(to be explored, since we may need to decrease the size occupied to transfer between SD card of almost similar capacity)

## Testing the XV-11 Lidar

* Checking LIDAR port <br />
Download arduino to check which port is the LIDAR <br />
https://www.arduino.cc/en/Main/Software > Linux ARM <br />
Extract folder <br />
Set permission on the install script: chmod +x *.sh <br />
Run command line sudo ./install.sh <br />
Check which port is the LIDAR (example ttyACM0) <br />
Alternatively, unplug and plug in the lidar, open new terminal, enter dmesg

* Visualising XV-11 Lidar information <br />
The RPi reads the LIDAR through serial. A python script is used to visualize the information. <br />
Allow permissions sudo chmod 777 /dev/(portname: e.g.ttyACM0) <br />
Download and unzip folder: <br />
https://github.com/simondlevy/xvlidar <br />
Go to XVLidar folder, open in terminal (downloaded from where) python lidarplot.py

## Using RViz to visualise XV-11 Lidar input
Modified instructions from: <br />
http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment <br />
http://wiki.ros.org/xv_11_laser_driver/Tutorials/Running%20the%20XV-11%20Node
 
* Create catkin workspace with XV-11lidardriver <br />
sudo apt-get install git <br />
source /opt/ros/kinetic/setup.bash <br />
printenv | grep ROS (should show up some ROS packages including) <br />
mkdir -p ~/catkin_ws/src <br />
cd ~/catkin_ws/src/ <br />
git clone https://github.com/rohbotics/xv_11_laser_driver.git <br />
cd .. <br />
catkin_make <br />
source devel/setup.bash

* Starting roscore
On another terminal <br />
cd catkin_ws <br />
roscore

* Starting publisher
New terminal: <br />
cd catkin_ws <br />
source devel/setup.bash <br />
rosrun xv_11_laser_driver neato_laser_publisher _port:=/dev/ttyACM0 (or another port name) <br />
Should see the publisher running

* Starting the RViz
New terminal: <br />
cd catkin_ws <br />
source devel/setup.bash <br />
rosrun rviz rviz

* Configuring RViz <br />
Set fixed frame and change frame rate <br />
Edit "Fixed Frame" value (top-left in rviz window). <br />
Click where it says, "map" and enter "/neato_laser" (without quotes) <br />
Click on the right of "Frame Rate" and change to 10 <br />
Add laser scan <br />
Click on the "Add" button (bottom-left in rviz window) and select "LaserScan" from the list. <br />
Add scan topic <br />
Expand LaserScan (in left pane of rviz window) and click to the right of "Topic" and select "/scan" from the drop-down list. <br />
You should see a lidar map. Change LaserScan>"size" to bolden the outline.
