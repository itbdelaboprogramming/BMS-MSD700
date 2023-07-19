"""
#title           :query.py
#description     :custom functions for PyMySQL ant others
#author          :Nicholas Putra Rihandoko
#date            :2023/07/19
#version         :0.1
#usage           :Python programming
#notes           :
#python_version  :3.7.3
#==============================================================================
"""

import logging
import pymysql
import signal
import datetime
import time
import csv
import os

# Define the directory of the backup file and the data to be logged
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'save')
log_limit = 31

#################################################################################################################

def limit_db_rows(mysql_server,row_limit,timeout=2):
    mysql_query = ("DELETE FROM {} WHERE id NOT IN ( SELECT id FROM ( "
                       "SELECT id FROM {} ORDER BY id DESC LIMIT %s ) AS limited_rows )".format(
                           mysql_server["table"],mysql_server["table"]))
    connect_mysql(mysql_server,mysql_query,[row_limit],timeout)

def dgps_correction(mysql_server,rtc,raw_gps,timeout=2):
    try:
        if rtc: mysql_query = ("SELECT diff_lat, diff_lon, num_sats, hdop, lat, lon FROM {} WHERE RTC = '{}' ORDER BY id DESC LIMIT 1".format(mysql_server["table"],rtc))
        else: mysql_query = ("SELECT diff_lat, diff_lon, num_sats, hdop, lat, lon FROM {} ORDER BY id DESC LIMIT 1".format(mysql_server["table"]))
        # Read the previous timestamps from database
        i = 1
        while True:
            base_station = connect_mysql(mysql_server,mysql_query,timeout=timeout)
            if base_station:
                # Change the format into suitable timedate objects
                for data in base_station:
                    new_latitude = round(raw_gps.Latitude + data[0],7)
                    new_longitude = round(raw_gps.Longitude + data[1],7)
                    diff_sats = raw_gps.Count_Satellites - data[2]
                    diff_hdop = round(raw_gps.HDOP - data[3],2)
                    ref_raw_lat = round(data[4],7)
                    ref_raw_lon = round(data[5],7)
                break
            else:
                print(" -- no RTC data, retrying -- ")
                if i == 3: break
                else:
                    time.sleep(1)
                    i+=1
        if base_station: return [new_latitude, new_longitude, diff_sats, diff_hdop, ref_raw_lat, ref_raw_lon]
        else:
            print(" << skipping RTC data >> ")
            print("")
            return ["","","","","",""]
    except: return ["","","","","",""]

#################################################################################################################

def strval(array):
    # Change an array into a string (used to upload array value into MySQL database)
    string = " ".join(map(str, array))
    return string

def mtemp(array):
    # Simplify a nested array into normal array (only picking the necessary values)
    var = [array[0][0], array[2][0], array[4][0], array[6][0],
            array[8][0], array[10][0], array[12][0], array[14][0]]
    return var

def get_updown_time(mysql_server,timer,bootup_time,timeout=2):
    # Read the previous timestamps from database
    datetime_query = ("SELECT startup_date, startup_time, total_uptime, shutdown_date, shutdown_time, total_downtime, downtime FROM `{}` ORDER BY id DESC LIMIT 1".format(mysql_server["table"]))
    data_datetime = connect_mysql(mysql_server,datetime_query,timeout=timeout)
    if data_datetime:
        # Change the format into suitable timedate objects
        for data in data_datetime:
            prev_startup = datetime.datetime.combine(data[0], datetime.datetime.min.time()) + data[1]
            total_uptime = data[2]
            prev_update = datetime.datetime.combine(data[3], datetime.datetime.min.time()) + data[4]
            total_downtime = data[5]
            downtime = data[6]
    else:
        # In case of no previous data, initiate the values
        prev_startup = bootup_time
        total_uptime = datetime.timedelta(seconds=0)
        prev_update = timer
        total_downtime = datetime.timedelta(seconds=0)
        downtime = datetime.timedelta(seconds=0)
    # calculate the time difference and culmulative period from the timestamps
    uptime = (timer - bootup_time)
    if abs(bootup_time - prev_startup) < datetime.timedelta(seconds=60):
        total_uptime = total_uptime + abs(timer - prev_update)
    else:
        downtime = abs(bootup_time - prev_update)
        total_downtime = total_downtime + downtime
    return [uptime, total_uptime, downtime, total_downtime]

#################################################################################################################

def handle_timeout(signum, frame):
    raise TimeoutError("Query execution timed out")
signal.signal(signal.SIGALRM, handle_timeout)

def connect_mysql(mysql_server,mysql_query,data=None,timeout=2):
    #return
    # Set the signal handler for the timeout
    signal.alarm(timeout)  # Start the timeout countdown
    try:
        # Setup Raspberry Pi as MySQl Database client
        with pymysql.connect(host=mysql_server["host"], user=mysql_server["user"], password=mysql_server["password"], db=mysql_server["db"], port=mysql_server["port"]) as db:
            # Write data in database
            if data:
                db.cursor().execute(mysql_query,data)
                db.commit()
                val = True
                print("<===== Data is sent to database =====>")
                print("")
            else:
                with db.cursor() as read:
                    read.execute(mysql_query)
                    val = read.fetchall()
        # Reset the alarm as the query completed successfully
        signal.alarm(0)
        return val
    except TimeoutError as e:
        # Handle the timeout error
        print("problem with MySQL Server:")
        print(e)
        print("<===== ===== continuing ===== =====>")
        print("")
        return False
    except Exception as e:
        # Print the error message
        print("problem with MySQL Server:")
        print(e)
        print("<===== ===== continuing ===== =====>")
        print("")
        return False

def retry_mysql(mysql_server,mysql_query,filename,timeout=2):
    global log_directory
    #return
    file_directory = os.path.join(log_directory,filename)
    rows_to_delete = []
    # Check if the file already exist or not
    try:
        with open(file_directory, 'r') as file:
            csv_log = list(csv.reader(file))
        # Read the line in the CSV file
        for row, row_data in enumerate(csv_log):
            if row > 0:
                # Retry uploading the data to mysql
                upload_succeed = connect_mysql(mysql_server,mysql_query,row_data,timeout)
                if upload_succeed: rows_to_delete.append(row)
                else: break
    except FileNotFoundError: pass
    # Write the updated contents to a new CSV file
    if rows_to_delete:
        csv_log = [row_data for row, row_data in enumerate(csv_log) if row not in rows_to_delete]
        with open(file_directory, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_log)

#################################################################################################################

def is_valid_date(date_string):
    # Check if a string is in correct format date
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def log_in_csv(title,data,timer,filename):
    global log_directory, log_limit
    #return
    file_directory = os.path.join(log_directory,filename)
    file_exists = True
    file_empty = True
    expired_rows_to_delete = None
    # Check if the file already exist or not
    try:
        with open(file_directory, 'r') as file:
            file_empty = not file.read(1)
            csv_log = list(csv.reader(file))
        # Read the line in the CSV file
        for row, row_data in enumerate(csv_log):
            if row > 0:
                csv_date = row_data[0]
                if is_valid_date(csv_date):
                    # Calculate the difference in days
                    log_date = datetime.datetime.strptime(csv_date, '%Y-%m-%d %H:%M:%S')
                    # Calculate how long has the data been logged
                    timediff = (timer - log_date).days
                    if timediff > log_limit: expired_rows_to_delete.append(row)
                    else: break
    except FileNotFoundError: file_exists = False
    # Remove the expired row then write the updated contents to a new CSV file
    if expired_rows_to_delete:
        csv_log = [row_data for row, row_data in enumerate(csv_log) if row not in expired_rows_to_delete]
        with open(file_directory, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(csv_log)
    # Add new data into csv file ()
    with open(file_directory, mode='a' if file_exists else 'w', newline='') as file:
        line = csv.writer(file, delimiter =',')
        if file_empty: line.writerow(title)
        line.writerow(data)

#################################################################################################################

def debugging():
    # Print the python library's process log for troubleshooting
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

def get_cpu_temperature():
    # Read CPU temperature from file
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = round(float(f.read().strip())/1000,1)
    return temp

def print_response(server,timer):
    cpu_temp = get_cpu_temperature()
    #return
    # Print the object's attribute, uncomment as needed
    for i in range(len(server)):
        print(server[i]._name, "MEASUREMENTS")
        print("Time             :", timer.strftime("%d/%m/%Y-%H:%M:%S"))
        print("CPU Temperature  :", cpu_temp, "degC")
        for attr_name, attr_value in vars(server[i]).items():
            if not attr_name.startswith("_"):
                if not isinstance(attr_value, list):
                    print(attr_name, "=", attr_value)
                else:
                    #continue
                    if not isinstance(attr_value[0], list):
                        print(attr_name, "=", attr_value)
                    else:
                        for i in range(len(attr_value)):
                            print(attr_name, i+1, "=", attr_value[i])
        print("")