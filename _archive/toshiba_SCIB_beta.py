"""
#title           :toshiba_SCiB.py
#description     :canbus library for Battery: Toshiba SCiB
#author          :Nicholas Putra Rihandoko
#date            :2023/05/08
#version         :0.1
#usage           :BMS-python
#notes           :
#python_version  :3.7.3
#==============================================================================
"""
import time

class node:
    def __init__(self,name,client,timeout=1):
        self._name      = name
        self._client    = client
        self._timeout   = timeout
        # Library of CAN-BUS Arbitration ID
        self._can_id = {
            "Power_On_Time_1"   :{"id":0x050, "start":1, "end":4, "scale":0.1, "bias":0, "round":1}, # in seconds
            "Power_On_Time_2"   :{"id":0x070, "start":1, "end":4, "scale":0.1, "bias":0, "round":1}, # in seconds
            "IO_Signal_Status_1":{"id":0x050, "start":5, "end":5, "scale":0.1, "bias":0, "round":1}, # per bit value
            "IO_Signal_Status_2":{"id":0x070, "start":5, "end":5, "scale":0.1, "bias":0, "round":1}, # per bit value
            "Module_Address_1"  :{"id":0x050, "start":5, "end":5, "scale":0.1, "bias":0, "round":1},
            "Module_Address_2"  :{"id":0x070, "start":5, "end":5, "scale":0.1, "bias":0, "round":1},

            "Capacity_mAh"      :{"id":0x053, "start":1, "end":2, "scale":1, "bias":0, "round":2}, # in mAh
            "SOC"               :{"id":0x053, "start":3, "end":3, "scale":1, "bias":0, "round":0}, # in %

            "Max_Temperature_1" :{"id":0x055, "start":1, "end":2, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius
            "Max_Temperature_2" :{"id":0x075, "start":1, "end":2, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius
            "Temperature_1"     :{"id":0x055, "start":3, "end":4, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius
            "Temperature_2"     :{"id":0x075, "start":3, "end":4, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius
            "Min_Temperature_1" :{"id":0x055, "start":5, "end":6, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius
            "Min_Temperature_2" :{"id":0x075, "start":5, "end":6, "scale":0.1, "bias":0x8000, "round":1}, # in Celcius

            "Cell_Voltage_1_1"  :{"id":0x057, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_2"  :{"id":0x057, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_3"  :{"id":0x057, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_4"  :{"id":0x058, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_5"  :{"id":0x058, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_6"  :{"id":0x058, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_7"  :{"id":0x059, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_8"  :{"id":0x059, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_9"  :{"id":0x059, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_10" :{"id":0x05A, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_1_11" :{"id":0x05A, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_1"  :{"id":0x077, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_2"  :{"id":0x077, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_3"  :{"id":0x077, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_4"  :{"id":0x078, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_5"  :{"id":0x078, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_6"  :{"id":0x078, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_7"  :{"id":0x079, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_8"  :{"id":0x079, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_9"  :{"id":0x079, "start":5, "end":6, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_10" :{"id":0x07A, "start":1, "end":2, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts
            "Cell_Voltage_2_11" :{"id":0x07A, "start":3, "end":4, "scale":0.3052/1000, "bias":0, "round":2}, # in Volts

            "Module_Current_1"  :{"id":0x056, "start":1, "end":2, "scale":0.01119, "bias":0x8000, "round":2}, # in Ampere
            "Module_Current_2"  :{"id":0x076, "start":1, "end":2, "scale":0.01119, "bias":0x8000, "round":2}, # in Ampere
            "Module_Voltage_1"  :{"id":0x056, "start":3, "end":4, "scale":4.8832/1000, "bias":0, "round":2}, # in Volts
            "Module_Voltage_2"  :{"id":0x076, "start":3, "end":4, "scale":4.8832/1000, "bias":0, "round":2} # in Volts
            }

    def reset_read_attr(self):
        # Reset (and/or initiate) object's attributes
        for attr_name, attr_value in vars(self).items():
            if not attr_name.startswith("_"):
                setattr(self, attr_name, 0)

    def save_read(self,message):
        # Save responses to object's attributes
        for key, value in self._can_id.items():
            if value["id"] == message.arbitration_id:
                # Converting HEX Data from CAN-BUS into decimal
                i = 0
                n = value["end"] - value["start"]
                sorted_data = []
                for b in range(value["start"],value["end"]+1):
                    sorted_data[i] = (message.data[b] << 8*n)
                    i=i+1
                    n=n-1
                raw_data = 0x0
                for x in sorted_data: raw_data = raw_data | x
                val = round((raw_data - value["bias"]) * value["scale"], value["round"])
                setattr(self, key, val)

    def dump_sequence(self,param):
        pass

    def receive_sequence(self):
        message = self._client.recv(self._timeout)
        if message is not None:
            self.save_read(message)
            #print("Battery data: ", message.arbitration_id)
        else:
            print("-- failed to detect bus activity --")   
        return message

    def send_command(self,command,param=None):
        # Send the command and read response with function_code 0x03 (3)
        if command == "receive":
            self.receive_sequence()
            #print("-- read is a success --")
        elif command == "dump":
            self.dump_sequence(param)
            #print("-- talk is a success --")
        else:
            print("-- unrecognized command --")
            return