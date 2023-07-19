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
import query
import can # code packet for CAN-BUS communication
import datetime # RTC Real Time Clock
import time
import os
from lib import toshiba_SCiB as battery

# Define CAN-BUS communication parameters
bustype         = 'socketcan' # CAN-BUS interface for Waveshare RS485/CAN Hat module
channel         = 'can0' # location of channel used for CAN-BUS Communication
bitrate         = 250000 # Toshiba SCiB speed of CAN-BUS = 250000
restart         = 100 # the time it takes to restart CAN-BUS communication if it fails (in milisecond)
timeout         = 2 # the maximum time the master/client will wait for response from slave/server (in seconds)
interval       = 1 # the period between each subsequent communication routine/loop (in seconds)

# Define MySQL Database parameters
mysql_server    = {"host":"10.4.171.204",
                    "user":"pi",
                    "password":"raspberrypi",
                    "db":"test",
                    "table":"test",
                    "port":3306}
mysql_timeout   = 3 # the maximum time this device will wait for completing MySQl query (in seconds)
mysql_interval  = 60 # the period between each subsequent update to database (in seconds)

#query.debugging()  # Monitor Modbus communication for debugging
init = True  # variable to check Modbus initialization
bootup_time = datetime.datetime.now()   # Used to gat the startup timestamp of the script
timer = bootup_time

def setup_canbus():
    global bustype, channel, bitrate
    # Configure and bring up the SocketCAN network interface
    os.system('sudo modprobe can && sudo modprobe can_raw') # load SocketCAN related kernel modules
    os.system('sudo ip link set down {}'.format(channel)) # disable can0 before config to implement changes in bitrate settings
    os.system('sudo ip link set {} type can bitrate {} restart-ms {}'.format(channel,bitrate,restart)) # configure can0 & set to 250000 bit/s
    os.system('sudo ip link set up {}'.format(channel)) # enable can0 so configuration take effects
    client = can.interface.Bus(bustype=bustype, channel=channel, bitrate=bitrate)
    bat = battery.node(name='TOSHIBA BATTERY', client=client, timeout=timeout)
    server = bat
    return server

def read_canbus(server):
    #return
    try:
        pass
        server.send_command(command="receive")
    except Exception as e:
        # Print the error message
        print("problem with",server._name,":")
        print(e)
        print("<===== ===== continuing ===== =====>")
        print("")

def update_database(server):
    global mysql_server, timer, bootup_time
    # Define MySQL queries and data which will be used in the program
    cpu_temp = query.get_cpu_temperature()
    [uptime, total_uptime, downtime, total_downtime] = query.get_updown_time(mysql_server, timer, bootup_time, mysql_timeout)
    title = ["startup_date","startup_time","uptime","total_uptime",
                "shutdown_date","shutdown_time","downtime","total_downtime",
                "battery_percentage","battery_voltage",
                "rpi_temp","volt_1","volt_2",
                "current_1","current_2","current_total",
                "temp_1","temp_2","temp_avg"]
    mysql_query = ("INSERT INTO `{}` ({}) VALUES ({})".format(mysql_server["table"],
                                                                ",".join(title),
                                                                ",".join(['%s' for _ in range(len(title))])))
    data = [bootup_time.strftime("%Y-%m-%d"), bootup_time.strftime("%H:%M:%S"), uptime, total_uptime,
                timer.strftime("%Y-%m-%d"), timer.strftime("%H:%M:%S"), downtime, total_downtime,
                server.SOC, round((server.Module_Voltage_1 + server.Module_Voltage_2)/2,2),
                cpu_temp, server.Module_Voltage_1, server[0].Module_Voltage_2,
                server.Module_Current_1, server.Module_Current_2, (server.Module_Current_1 + server.Module_Current_2),
                server.Temperature_1, server.Temperature_2, round((server.Temperature_1 + server.Temperature_2)/2,1)]
    filename = 'canbus_log.csv'

    query.log_in_csv(title ,data, timer, filename)
    query.retry_mysql(mysql_server, mysql_query, filename, mysql_timeout)

#################################################################################################################

# Checking the connection CAN-BUS
while init:
    try:
        # Setup Raspberry Pi as Modbus client/master
        server = setup_canbus()
        print("<===== Connected to CAN-BUS Communication =====>")
        print("")
        init = False

    except Exception as e:
        # Print the error message
        print("problem with CAN-BUS communication:")
        print(e)
        print("<===== ===== retrying ===== =====>")
        print("")
        time.sleep(3)

first = [True, True]
# Reading a CAN-BUS message and Upload to database sequence
while not init:
    try:
        # First run (start-up) sequence
        if first[0]:
            first[0] = False
            start = datetime.datetime.now() # time counter
            
        # Send the command to read the measured value and do all other things
        read_canbus(server)
        timer = datetime.datetime.now()
        query.print_response(server, timer)

        # Check elapsed time
        if (timer - start).total_seconds() > mysql_interval or first[1] == True:
            start = timer
            first[1] = False
            # Update/push data to database
            update_database(server)
        
        time.sleep(interval)
    
    except Exception as e:
        # Print the error message
        print(e)
        print("<===== ===== retrying ===== =====>")
        print("")
        time.sleep(3)
