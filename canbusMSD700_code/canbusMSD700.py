"""
#!/usr/bin/env python
#title           :canbusMSD700.py
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
import os # used to run terminal command through Python script
import can # code packet for canbus communication
import datetime # RTC Real Time Clock
import time
import pymysql

time.sleep(10) # wait for RaspberryPi to complete its boot-up sequence

# Configure and brung up the SocketCAN network interface
os.system('sudo modprobe can && sudo modprobe can_raw') # load SocketCAN related kernel modules
#os.system('sudo ip link set down can0') # disable can0 before config to implement changes in bitrate settings
os.system('sudo ip link set can0 type can bitrate 250000 restart-ms 100') # configure can0
os.system('sudo ip link set up can0') # enable can0 so configuration take effects

# Specifications of Socket CAN (Check first the type)
bustype = 'socketcan' # CAN bus interface for Waveshare RS485/CAN Hat module
channel = 'can0' # location of channel used for CAN BUS Communication
bitrate = 250000 # Toshiba SCiB speed of CANBUS = 250000

# Initialize variable
t_battery_1   = None
t_battery_2   = None
v_battery_1_m = None
v_battery_2_m = None
i_battery_1_m = None
i_battery_2_m = None
soc_battery   = None

# CAN-ID
# Temperature
TEMPERATURE_ID_1 = 0x055
TEMPERATURE_ID_2 = 0x075
TEMPERATURE_BIAS = 0x8000
TEMPERATURE_SCALE = 0.1 # in Celcius

# Voltage cell
VOLTAGE_ID_1_1 = 0x057
VOLTAGE_ID_1_2 = 0x058
VOLTAGE_ID_1_3 = 0x059
VOLTAGE_ID_1_4 = 0x05A

VOLTAGE_ID_2_1 = 0x077
VOLTAGE_ID_2_2 = 0x078
VOLTAGE_ID_2_3 = 0x079
VOLTAGE_ID_2_4 = 0x07A

VOLTAGE_SCALE = 0.3052 # in mV

# Voltage & Current module
MODULE_ID_1 = 0x056
MODULE_ID_2 = 0x076
MODULE_I_BIAS = 0x8000
MODULE_I_SCALE = 0.01119 # in Ampere
MODULE_V_SCALE = 4.8832/1000 # in Volts

# State of Charge
SOC_ID = 0x053

# Checking the connection "CAN-BUS"
try:
    canbus0 = can.interface.Bus(bustype=bustype, channel=channel, bitrate=bitrate)
    print("Connected to CANBUS Communication")
except:
    print("Cannot find CANBUS Communication")

# Reading a CANBUS Message
while True:
    try:
        # time counter
        timer = datetime.datetime.now()
        # recv() method for reading or receiving from the bus (in here we are using a SCiB Battery)
        canbus_message = canbus0.recv(1) # waiting timeout for bus data (default = None)
        # scib_battery_data = canbus_message.arbitration_id

        # Converting HEX Data from CAN BUS into demical, first it need manual book communication SCiB Battery
        if canbus_message is None:
            print("Failed to detect bus activity")
        elif canbus_message.arbitration_id == TEMPERATURE_ID_1:
            # Temperature Battery 1
            t_battery_1 = round((((canbus_message.data[3] << 8) | canbus_message.data[4]) - TEMPERATURE_BIAS) * TEMPERATURE_SCALE , 1)
            #print("data T1")
        elif canbus_message.arbitration_id == TEMPERATURE_ID_2:
            # Temperature Battery 2
            t_battery_2 = round((((canbus_message.data[3] << 8) | canbus_message.data[4]) - TEMPERATURE_BIAS) * TEMPERATURE_SCALE , 1)
            #print("data T2")
        elif canbus_message.arbitration_id == MODULE_ID_1:
            # Voltage Battery module 1
            v_battery_1_m = round(((canbus_message.data[3] << 8) | canbus_message.data[4]) * MODULE_V_SCALE , 2)
            #print("data V1")
        elif canbus_message.arbitration_id == MODULE_ID_1:
            # Current Battery module 1
            i_battery_1_m = round((((canbus_message.data[3] << 8) | canbus_message.data[4]) - MODULE_I_BIAS) * MODULE_I_SCALE , 2)
            #print("data I1")
        elif canbus_message.arbitration_id == MODULE_ID_2:
            # Voltage Battery module 2
            v_battery_2_m = round(((canbus_message.data[3] << 8) | canbus_message.data[4]) * MODULE_V_SCALE , 2)
            #print("data V2")
        elif canbus_message.arbitration_id == MODULE_ID_2:
            # Current Battery module 1
            i_battery_2_m = round((((canbus_message.data[3] << 8) | canbus_message.data[4]) - MODULE_I_BIAS) * MODULE_I_SCALE , 2)
            #print("data I2")
        elif canbus_message.arbitration_id == SOC_ID:
            # SoC Battery module
            soc_battery = round(canbus_message.data[3])
            #print("data SoC")
        #else:
            #print("others")

        # Print the data
        print("Time                 :", timer.strftime("%Y-%m-%d %H:%M:%S")) # Time
        print("Battery data         :", canbus_message.arbitration_id)
        print("Temperature Module 1 :", t_battery_1, "Celcius")
        print("Temperature Module 2 :", t_battery_2, "Celcius")
        print("Voltage Module 1 (V) :", v_battery_1_m, "Volt")
        print("Voltage Module 2 (V) :", v_battery_2_m, "Volt")
        print("Current Module 1 (I) :", i_battery_1_m, "Ampere")
        print("Current Module 2 (I) :", i_battery_2_m, "Ampere")
        print("State of Charge (SoC):", soc_battery, "%")
        print("")

        # Delay
        time.sleep(1)

        # Database Connection
        db = pymysql.connect(host='nicholas-dell-mysql.at.remote.it',   # Remote.it
                             port=33001,                                # Remote.it
                             user='pi',                                 # MySQL
                             password='raspberrypi',                    # MySQL
                             db='scib')                                 # MySQL

        cur = db.cursor()

        add_c0 = "INSERT INTO `monitoring_scib`(Timestamp, Temperature_Module_1,Temperature_Module_2, Voltage_Module_1, Voltage_Module_2, Current_Module_1, Current_Module_2, SoC) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(add_c0,((timer.strftime("%Y-%m-%d %H:%M"),
                             t_battery_1,
                             t_battery_2,
                             v_battery_1_m,
                             v_battery_2_m,
                             i_battery_1_m,
                             i_battery_2_m,
                             soc_battery)))
        db.commit()
        print("Data is sent to database")
    
    except BaseException as e:
        print("============")
        # Prind the error message
        print("problem with -->",e)
        print("============")
        # time.sleep(0)
        pass
