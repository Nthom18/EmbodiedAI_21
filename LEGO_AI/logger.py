"""
Logging passed information to csv files format.

Author: Nicoline Louise Thomsen
"""

import csv
import datetime


class Logger():

    def __init__(self):

        time = str(datetime.datetime.now())[11:19]
        dateid = time.replace(':', '')

        # file_name = 'logs/data_' + dateid + '.csv'
        file_name = 'logs/data.csv'
        log = open(file_name, 'w+', newline='')  # w+ mode truncates (clears) the file (new file for every test)   
        self.logger = csv.writer(log, dialect = 'excel')

        self.logger.writerow(['Time', 'Light_sensor_1', 'Light_sensor_2', 'last_seen'])
        # self.logger.writerow(['Time', 'Light_sensor_1', 'Light_sensor_2', 'control_input', 'base_speed'])
        # self.logger.writerow(['Time', 'left', 'right', 'error', 'control_input', 'base_speed'])



    def log_to_file(self, t, *data):

        row = [t]
        row.extend(data)

        self.logger.writerow(row)

