import time
import threading
import sqlite3
import serial

# environment variables can be set in .env file by using the following format:
# VARIABLE_NAME=VARIABLE_VALUE
# example:
# port=/tes/tport123
# baudrate=123456

# # read all environment variables from .env file
environment_variables = {}
with open('.env') as f:
    for line in f:
        if line[0] != '#':
            key, value = line.split('=')
            environment_variables[key] = value.strip()


class Reader:
    port = None
    baudrate = None
    ser = None
    value_store = {}
    translation_table = {
        '1-0:1.8.1': 'verbruik stand',
        '1-0:1.8.2': 'verbruik stand',
        '1-0:2.8.1': 'lever stand',
        '1-0:2.8.2': 'lever stand',
        '1-0:1.7.0': 'verbruik',
        '1-0:2.7.0': 'leveren',
        '0-1:24.2.1': 'aardgas'
    }
    
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
    
    # function that continuously reads data from the serial port and keeps the connection open
    def read_continuously(self):
        while True:
            line = self.ser.readline().decode().strip()

            # check if any of the keys in the translation table are in the line
            if any(key in line for key in self.translation_table.keys()):
                # check if the value is gas
                if '0-1:24.2.1' in line:
                    value = line.split('(')[2].split('*')[0]
                else:
                    # get the value from the line
                    value = line.split('(')[1].split('*')[0]
                    # translate the code to the name of the value
                code = line.split('(')[0].strip()
                self.value_store[self.translation_table[code]] = value

class collector:
    instance = None
    database = "data.db" # TODO: use the existing database instead of creating a new one
    reader = Reader(environment_variables['port'], environment_variables['baudrate'])

    def __init__(self):
        # create the database if it doesn't exist
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Data (type INTEGER, time INTEGER, data INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS DataTypes (type INTEGER, name TEXT, unit TEXT)")
        conn.commit()
        conn.close()

        # make sure only one instance of the collector is running
        if collector.instance is not None:
            raise Exception("Only one instance of the collector can be running at a time")
        collector.instance = self

    def start(self):
        # create a thread that will run in the background and collect data
        thread = threading.Thread(target=self.collect)
        thread.daemon = True
        thread.start()

    def collect(self):
        # start reading data from the serial port
        self.reader.read_continuously()
        
    def store_data(self):
        pass

    def fill_data_types(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("INSERT INTO DataTypes VALUES (0, 'verbruik stand', 'kWh')")
        c.execute("INSERT INTO DataTypes VALUES (1, 'lever stand', 'kWh')")

        c.execute("INSERT INTO DataTypes VALUES (2, 'verbruik', 'kW')")
        c.execute("INSERT INTO DataTypes VALUES (3, 'leveren', 'kW')")

        c.execute("INSERT INTO DataTypes VALUES (4, 'aardgas', 'm3')")
        conn.commit()
        conn.close()
            