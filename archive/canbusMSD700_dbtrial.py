#!/usr/bin/env python

# Import library
import os
import can # code packet for canbus communication
import pymysql
import datetime # RTC Real Time Clock
import time

os.system('sudo modprobe can')
os.system('sudo modprobe can_raw')
os.system('sudo ip link set can0 type can bitrate 500000 restart-ms 100')
os.system('sudo ifconfig can0 up')

# Specifications of Socket CAN (Check first the type)
bustype = 'socketcan' # Types of socket
channel = 'can0' # location of channel used for CAN BUS Communication

# CAN-ID
# Temperature
TEMPERATURE_ID_1 = 0x055
TEMPERATURE_ID_2 = 0x075

# Voltage cell
VOLTAGE_ID_1_1 = 0x057
VOLTAGE_ID_1_2 = 0x058
VOLTAGE_ID_1_3 = 0x059
VOLTAGE_ID_1_4 = 0x05A

VOLTAGE_ID_2_1 = 0x077
VOLTAGE_ID_2_2 = 0x078
VOLTAGE_ID_2_3 = 0x079
VOLTAGE_ID_2_4 = 0x07A

# Voltage & Current module
MODULE_ID_1 = 0x056  
MODULE_ID_2 = 0x076

# State of Charge
SOC_ID = 0x053

# Checking the connection "CAN-BUS"
try:
    # Default speed of CANBUS = 500000
    canbus0 = can.interface.Bus(bustype=bustype, channel=channel, bitrate= 500000)
    # canbus0.connect()
    print("Conected to CANBUS Communication")
except:
    print("Cannot find CANBUS Communication")
    canbus0.close()

i = True
# Reading a CANBUS Message
while i:
    try:
        # time counter
        timer = datetime.datetime.now()
        # recv() method for reading or receiving from the bus (in here we are using a SCiB Battery)
        canbus_message = canbus0.recv(1.0)
        # scib_battery_data = canbus_message.arbitration_id

        # Converting HEX Data from CAN BUS into demical, first it need manual book communication SCiB Battery
        if canbus_message is None:
            print("Failed to detect bus activity")
        # elif canbus_message.arbitration_id == TEMPERATURE_ID_1:
        #     # Temperature Battery 1
        #     t_battery_1 = round((canbus_message.data[3])+(canbus_message.data[4])) 
        # elif canbus_message.arbitration_id == TEMPERATURE_ID_2:
        #     # Temperature Battery 2
        #     t_battery_2 = round((canbus_message.data[3])+(canbus_message.data[4]))
        # elif canbus_message.arbitration_id == MODULE_ID_1:
        #     # Voltage Battery module 1
        #     v_battery_1_m = round((canbus_message.data[3])+(canbus_message.data[4]))
        # elif canbus_message.arbitration_id == MODULE_ID_1:
        #     # Current Battery module 1
        #     i_battery_1_m = round((canbus_message.data[1])+(canbus_message.data[2]))
        # elif canbus_message.arbitration_id == MODULE_ID_2:
        #     # Voltage Battery module 2
        #     v_battery_2_m = round((canbus_message.data[3])+(canbus_message.data[4]))
        # elif canbus_message.arbitration_id == MODULE_ID_2:
        #     # Current Battery module 1
        #     i_battery_2_m = round((canbus_message.data[1])+(canbus_message.data[2]))
        # elif canbus_message.arbitration_id == SOC_ID:
        #     # SoC Battery module
        #     soc_battery = ((canbus_message.data[3]))

        # # Print the data
        print("Time                 :", timer.strftime("%Y-%m-%d %H:%M:%S")) # Time
        # print("Battery data         :", canbus_message.arbitration_id)
        # print("Temperature Module 1 :", t_battery_1, "Celcius")
        # print("Temperature Module 2 :", t_battery_2, "Celcius")
        # print("Voltage Module 1 (V) :", v_battery_1_m, "Volt")
        # print("Voltage Module 2 (V) :", v_battery_2_m, "Volt")
        # print("Current Module 1 (I) :", i_battery_1_m, "Ampere")
        # print("Current Module 2 (I) :", i_battery_2_m, "Ampere")
        # print("State of Charge (SoC):", soc_battery, "%")
        # print("============")

        # # Delay
        time.sleep(1)

        # # Database Connection 
        db = pymysql.connect(host='localhost',
                            user='root',
                            password='root',
                            db='test')
        
        cur = db.cursor()

        add_c0 = "INSERT INTO `monitoring_scib`(Timestamp) VALUES(%s)"
        # Temperature_Module_1,Temperature_Module_2, Voltage_Module_1, Voltage_Module_2, Current_Module_1, Current_Module_2, SoC) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        
        cur.execute(add_c0, timer.strftime("%Y-%m-%d %H:%M"))
        #                     t_battery_1,
        #                     t_battery_2,
        #                     v_battery_1_m,
        #                     v_battery_2_m,
        #                     i_battery_1_m,
        #                     i_battery_2_m,
        #                     soc_battery)))
        print("============")
        db.commit()
        print("Data is sent to database")
    
    except:
        # print("============")
        print("Disconnected")
        # print("============")
        # time.sleep(0)
        # pass
        i = False