#!/bin/sh

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
sudo chmod +x /home/$(logname)/canbusMSD700_code/canbusMSD700.py
sleep 1
# Install pip for python library manager
sudo apt install python3-pip
sleep 1
# Install the necessary python library
sudo pip3 install python-can
sudo pip3 install pymysql
sleep 1

# install and enable Cron to automate task
sudo apt install cron
sudo systemctl enable cron
# Check whether the command line is already exist in /etc/crontab
if ! sudo grep -q "@reboot root sleep 5 && sudo sh /home/$(logname)/canbusMSD700_code/canbusMSD700.py &" /etc/crontab; then
    # Append the file into /etc/crontab to enable automatic run after reboot
    sudo su -c "echo \"@reboot root sleep 5 && sudo sh /home/$(logname)/canbusMSD700_code/canbusMSD700.py &\" >> /etc/crontab"
fi
sleep 1
# Enable execute (run program) privilege /etc/rc.local
sudo chmod +x /etc/rc.local
sleep 1
echo "Installation of canbusMSD700 system is finished"
echo "Please reboot the RaspberryPi"
exit