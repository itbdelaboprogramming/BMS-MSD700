"""
#title           :main__canbus.py
#description     :CAN-BUS Communication between SCiB Battery and Raspberry Pi
#author          :Fajar Muhammad Noor Rozaqi, Nicholas Putra Rihandoko
#date            :2023/04/03
#version         :2.1
#usage           :BMS-python
#notes           :
#python_version  :3.7.3
#==============================================================================
"""

# Import library
import debug
import can # code packet for CAN-BUS communication
import datetime # RTC Real Time Clock
import time
import pymysql
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lib'))
import toshiba_SCiB as battery

# Define CAN-BUS communication parameters
bustype         = 'socketcan' # CAN-BUS interface for Waveshare RS485/CAN Hat module
channel         = 'can0' # location of channel used for CAN-BUS Communication
bitrate         = 250000 # Toshiba SCiB speed of CAN-BUS = 250000
restart         = 100 # the time it takes to restart CAN-BUS communication if it fails (in milisecond)
timeout         = 2 # the maximum time the master/client will wait for response from slave/server (in seconds)
com_delay       = 1 # the period between each subsequent communication routine/loop (in seconds)

# Define MySQL Database parameters
mysql_host      = '****'
mysql_db        = '****'
mysql_user      = '****'
mysql_password  = '****'
update_delay    = 60   # the period between each subsequent update to database (in seconds)

# Other parameters
#debug.debugging()
cpu_temp = None     # RaspberryPi temperature for hardware fault monitoring
init = [True,True]  # variable to check modbus & mysql initialization

def setup_canbus():
    global bustype, channel, bitrate
    # Configure and bring up the SocketCAN network interface
    os.system('sudo modprobe can && sudo modprobe can_raw') # load SocketCAN related kernel modules
    os.system('sudo ip link set down {}'.format(channel)) # disable can0 before config to implement changes in bitrate settings
    os.system('sudo ip link set {} type can bitrate {} restart-ms {}'.format(channel,bitrate,restart)) # configure can0 & set to 250000 bit/s
    os.system('sudo ip link set up {}'.format(channel)) # enable can0 so configuration take effects
    client = can.interface.Bus(bustype=bustype, channel=channel, bitrate=bitrate)
    bat = battery.node(name='TOSHIBA BATTERY', client=client, timeout=timeout)
    server = [bat]
    return server

# Checking the connection CAN-BUS
while init[0]:
    try:
        # Setup Raspberry Pi as CAN-BUS client/master
        server = setup_canbus()
        print("<===== Connected to CAN-BUS Communication =====>")
        print("")
        init[0] = False

    except BaseException as e:
        # Print the error message
        print("problem with CAN-BUS communication:")
        print(e)
        print("<===== ===== retrying ===== =====>")
        print("")
        time.sleep(3)

# Checking the connection MySQL
while init[1]:
    try:
        # Setup Raspberry Pi as Database client
        db = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db)
        print("<===== Connected to MySQl Server =====>")
        print("")
        init[1] = False

    except BaseException as e:
        # Print the error message
        print("problem with MySQL Server:")
        print(e)
        print("<===== ===== retrying ===== =====>")
        print("")
        time.sleep(3)

first = [True, True]
# Reading a CAN-BUS message and Upload to database sequence
while not init[0] and not init[1]:
    try:
        # First run (start-up) sequence
        if first[0]:
            first[0] = False
            # time counter
            start = datetime.datetime.now()
            # Reset accumulated values for first time measurements
            for i in range(len(server)):
                server[i].reset_read_attr()
            debug.log_in_csv(server, cpu_temp, timer, first_row=True)

        # Send the command to read the measured value
        for i in range(len(server)):
            try:
                server[i].send_command(command="receive")
            except BaseException as e:
                # Reset the value of measurement
                server[i].reset_read_attr()
                # Print the error message
                print("problem with",server._name,":")
                print(e)
                print("<===== ===== continuing ===== =====>")
                print("")

        # Save and print the data
        timer = datetime.datetime.now()
        cpu_temp = debug.get_cpu_temperature()
        debug.log_in_csv(server, cpu_temp, timer)
        debug.print_response(server, cpu_temp, timer)
        
        # Check elapsed time
        if (timer - start).total_seconds() > update_delay or first[1] == True:
            start = timer
            first[1] = False
            # Update/push data to database
            debug.update_database(server, db, cpu_temp, timer)
        
        time.sleep(com_delay)
    
    except BaseException as e:
        # Print the error message
        print("problem with -->",e)
        print("<===== ===== retrying ===== =====>")
        print("")
        time.sleep(1)
