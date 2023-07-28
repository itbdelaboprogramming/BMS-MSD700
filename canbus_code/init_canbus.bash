#!/bin/bash
#title           :init_canbus.bash
#description     :CAN/RS485 Hat module installation script
#author          :Nicholas Putra Rihandoko
#date            :2023/06/21
#version         :2.1
#usage           :CANbus programming in Python
#notes           :
#==============================================================================

# Install can-utils package for debugging CAN massages
sudo apt update
sudo apt install can-utils python3-pip -y
# Install the necessary python library
sudo pip3 install python-can
sudo pip3 install pymysql
# 'zerotier' for virtual LAN and remote access
sudo apt install curl nmap -y
curl -s https://install.zerotier.com | sudo bash
# cron for task automation
sudo apt install cron -y
sudo systemctl enable cron

# Check whether the command line is already exist in /boot/config.txt
if ! sudo grep -q "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" /boot/config.txt; then
    # Append the file into /boot/config.txt to enable RaspberryPi handling of CAN device
    sudo echo "# Enable CAN controller on Waveshare RS485/CAN Hat" >> /boot/config.txt
    sudo echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" >> /boot/config.txt
fi

# Enable SPI interface to communicate with the CAN Hat
sudo raspi-config nonint do_spi 0
# ssh and VNC for remote access
sudo systemctl enable ssh
sudo systemctl start ssh
sudo raspi-config nonint do_vnc 0

# Enable execute (run program) privilege for the python script
sudo chmod +x /home/$(logname)/canbus_code/main__canbus.py
sudo chmod 777 /home/$(logname)/canbus_code/save/canbus_log.csv

echo ""
echo "=========================================================="
echo ""
echo "Installation of CANbus system is finished"
echo ""
echo "Please reboot the RaspberryPi, just in case :)"
echo ""
echo "=========================================================="
echo ""
exit 0