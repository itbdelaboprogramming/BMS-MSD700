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
import can

class node:
    def __init__(self,name,client,timeout=1):
        self._name      = name
        self._client    = client
        self._timeout   = timeout       # maximum time to wait for CANbus message (in seconds)
        # Library of CANbus Arbitration ID
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

    def reset_rec_attr(self):
        # Reset (and/or initiate) object's attributes
        for attr_name, attr_value in vars(self).items():
            if not attr_name.startswith("_"): setattr(self, attr_name, 0)

    def map_rec_attr(self,raw_address):
        # get the attribute data using its CANbus memory address
        mapped_addr = []
        for key, value in self._can_id.items():
            for a in raw_address:
                if value["id"] == a:
                    try: mapped_addr.append([key, getattr(self, key)])
                    except: print(" -- one or more mapped address has not been read from server --")
                    break
        return mapped_addr

    def save_read(self,message,address,save):
        # Save responses to object's attributes
        index_to_remove = []
        for s, a in enumerate(address):
            if a == message.arbitration_id:
                if save[s].startswith('Hx'):
                    val=message.data
                else:
                    # Converting HEX Data from CANbus into decimal
                    sorted_data, raw_data, i, n = [], 0x0, 0, (self._can_id[save[s]]["end"] - self._can_id[save[s]]["start"])
                    for b in range(self._can_id[save[s]]["start"],self._can_id[save[s]]["end"]+1):
                        sorted_data[i] = (message.data[b] << 8*n); i+=1; n-=1
                    for x in sorted_data: raw_data = raw_data | x
                    val = round((raw_data - self._can_id[save[s]]["bias"]) * self._can_id[save[s]]["scale"], self._can_id[save[s]]["round"])
                setattr(self, save[s], val)
                index_to_remove.append(s)
        
        # Remove read address (id) that has been read
        for r in reversed(index_to_remove): address.pop(r); save.pop(r)
        return address, save

    def count_address(self,raw_address):
        # Configure the message id (addr) and the attribute name where the value is saved (save)
        addr, save, raw = [], [], [True]*len(raw_address)

        # Match the address with the information in self._can_id library
        for key, value in self._can_id.items():
            for i, a in enumerate(raw_address):
                if isinstance(a,list):
                    if (a[0] == value["id"] and a[1] == value["start"]) and key not in save:
                        addr.append(value["id"]); save.append(key)
                        raw[i] = False; break
                else:
                    if (a == key.lower() or a == value["id"]) and key not in save:
                        addr.append(value["id"]); save.append(key)
                        raw[i] = False; break

        # If the address is not available in the library, then use it as is
        for i, r in enumerate(raw):
            if r and (raw_address[i] not in addr) and (raw_address[i] not in [s.lower() for s in save]):
                if isinstance((raw_address[i]),str):
                    print(" -- unrecognized arbitration ID for '{}' --".format(raw_address[i]))
                else:
                    addr.append(raw_address[i]); save.append('Hx'+hex(raw_address[i])[2:].zfill(3).upper())
                    print(" -- address '{}' may gives raw data, use with discretion --".format(save[-1]))
        addr, save = zip(*sorted(zip(addr, save)))
        return list(addr), list(save)

    def receive_sequence(self,address):
        addr, save = self.count_address(address)
        # read messages in CANbus port
        while True:
            if addr:
                message = self._client.recv(self._timeout)
                if message:
                    # Decode message if it is in the read address list until all is read
                    if message.arbitration_id in addr:
                        addr, save = self.save_read(message,addr,save)
                else: print("-- failed to detect bus activity --"); break
            else: print("-- read completed --"); break

    def dump_sequence(self,param):
        pass
        ### Example dumping message using CAN ODB2 arbitration ID
        #obd2_message = can.Message(arbitration_id=0x7E0, data=[0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False)
        #self._client.send(obd2_message)
        ### Example dumping message using CAN J1939 arbitration ID
        #j1939_message = can.Message(arbitration_id=0x18DAF110, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08], is_extended_id=True)
        #self._client.send(j1939_message)

    def send_command(self,command,address,param=None):
        # Send the command and read response with function_code 0x03 (3)
        if command == "receive":
            address = [a.lower() if isinstance(a,str) else a for a in address]
            self.receive_sequence(address)
            #print("-- read is a success --")
        elif command == "dump":
            self.dump_sequence(param)
            #print("-- talk is a success --")
        else: print("-- unrecognized command --")