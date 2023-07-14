#!/bin/bash
#title           :init_canbusMSD700.bash
#description     :CAN Hat module installation script (main)
#author          :Nicholas Putra Rihandoko
#date            :2023/04/03
#version         :2.1
#usage           :BMS-Python
#notes           :take a look at README.txt for further info
#==============================================================================

# Install can-utils package for debugging CAN massages
sudo apt install can-utils
sleep 1
# Check whether the command line is already exist in /boot/config.txt
if ! sudo grep -q "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" /boot/config.txt; then
    # Append the file into /boot/config.txt to enable RaspberryPi handling of CAN device
    sudo echo "# Enable CAN controller on Waveshare RS485/CAN Hat" >> /boot/config.txt
    sudo echo "dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000" >> /boot/config.txt
fi
sleep 1
# Enable SPI interface to communicate with the CAN Hat
sudo raspi-config nonint do_spi 0
sleep 1

# Enable execute (run program) privilege for the python script
sudo chmod +x /home/$(logname)/canbus_code/main__canbus.py
sudo chmod 777 /home/$(logname)/canbus_code/save/canbus_log.csv
sleep 1
# Install pip for python library manager
sudo apt install python3-pip
sleep 1
# Install the necessary python library
sudo pip3 install python-can
sudo pip3 install pymysql
sleep 1

echo ""
echo "=========================================================="
echo "Installation of CAN-BUS system is finished"
echo ""
echo "=========================================================="
echo ""
exit 0