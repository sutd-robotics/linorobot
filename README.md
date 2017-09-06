# linorobot
UBUNTU INSTALLATION on RPi

* [Installation](#Installtion)
* [Examples](#examples)
* [Matching Routes](#matching-routes)
* [Static Files](#static-files)
* [Registered URLs](#registered-urls)
* [Walking Routes](#walking-routes)
* [Full Example](#full-example)


## Installation

* Download Ubuntu Mate
https://ubuntu-mate.org/raspberry-pi/ (!!! Make sure you install Ubuntu MATE 16.04 ONLY. It's the only version compatible with ROS Kinetic)
(Ubuntu is chosen it install ROS Kinetic Kame more quickly
http://wiki.ros.org/kinetic/Installation/Ubuntu)

* Burn into SD card
Use Etcher to burn the image of Ubuntu Mate into the SD card. 
https://etcher.io/
Minimum size of SD card 8GB. Recommended size of SD card is 32GB, as you will install many packages.

* Accessories <br />
Attach SD card, HDMI output, USB Mouse, USB Keybaord <br />
Then, attach power to turn on. (5V 2.5A) <br />
Configure your username and password. <br />
Connect to WiFi (iLP2 WiFi works) <br />
Reboot, as the RPi may be laggy in its first boot <br />

* Update and upgrade, and reboot <br />
sudo apt-get update && sudo apt-get upgrade -y && sudo reboot

* Uninstall unnecessary preloaded programs (to save space) <br />
sudo apt-get autoremove

* Installing Chrome <br />
sudo apt-get install chromium-browser

* Setting up the time <br />
There is no hardware clock on RPi. Script to sync clock with Internet on every boot: <br />
sudo nano /etc/ rc.local
sudo date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
(accept changes, if there is)
Control-X to exit

ENABLE SSH (To connect and control wirelessly)
sudo systemctl enable ssh

SETTING UP VNC (Virtual desktop viewing on computer)
https://www.raspberrypi.org/documentation/remote-access/vnc/

Installation of ROS
http://wiki.ros.org/kinetic/Installation/Ubuntu
Follow the steps on the page, choose desktop-full install

